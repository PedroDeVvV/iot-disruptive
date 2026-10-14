import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_COLUMNS = {"id", "room_id/id", "noted_date", "temp", "out/in"}
VIEW_NAMES = [
    "avg_temp_por_ambiente",
    "leituras_por_hora",
    "temp_max_min_por_dia",
]


def load_and_clean_csv(csv_path: Path) -> pd.DataFrame:
    dataframe = pd.read_csv(csv_path)

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas ausentes no CSV: {missing}")

    dataframe = dataframe.rename(
        columns={
            "id": "reading_id",
            "room_id/id": "room_id",
            "noted_date": "recorded_at",
            "temp": "temperature",
            "out/in": "location",
        }
    )

    dataframe["recorded_at"] = pd.to_datetime(
        dataframe["recorded_at"], dayfirst=True, errors="coerce"
    )
    dataframe["temperature"] = pd.to_numeric(
        dataframe["temperature"], errors="coerce"
    )
    dataframe["location"] = dataframe["location"].replace(
        {"In": "Interno", "Out": "Externo"}
    )

    dataframe = dataframe.dropna(
        subset=["reading_id", "recorded_at", "temperature", "location"]
    )
    dataframe = dataframe.drop_duplicates(subset=["reading_id"])
    dataframe = dataframe[
        ["reading_id", "room_id", "recorded_at", "temperature", "location"]
    ]

    return dataframe.sort_values("recorded_at").reset_index(drop=True)


def create_views(engine) -> None:
    from sqlalchemy import text

    sql_path = PROJECT_ROOT / "sql" / "views.sql"
    commands = [command.strip() for command in sql_path.read_text().split(";")]

    with engine.begin() as connection:
        for command in commands:
            if command:
                connection.execute(text(command))


def drop_views(engine) -> None:
    """Remove as views antes de recriar a tabela de leituras."""
    from sqlalchemy import text

    with engine.begin() as connection:
        for view_name in VIEW_NAMES:
            connection.execute(text(f"DROP VIEW IF EXISTS {view_name}"))


def save_to_database(dataframe: pd.DataFrame) -> None:
    from database import get_engine

    engine = get_engine()
    drop_views(engine)
    dataframe.to_sql(
        "temperature_readings",
        engine,
        if_exists="replace",
        index=False,
        chunksize=5_000,
        method="multi",
    )
    create_views(engine)


def main() -> None:
    parser = argparse.ArgumentParser(description="Carrega dados IoT no PostgreSQL")
    parser.add_argument(
        "--csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "IOT-temp.csv",
        help="Caminho do arquivo CSV",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {args.csv}")

    dataframe = load_and_clean_csv(args.csv)
    save_to_database(dataframe)
    print(f"Pipeline concluído: {len(dataframe)} leituras inseridas.")


if __name__ == "__main__":
    main()

