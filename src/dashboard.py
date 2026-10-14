import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database import get_engine


st.set_page_config(page_title="Temperaturas IoT", page_icon="🌡️", layout="wide")


@st.cache_data(ttl=60)
def load_data(view_name: str) -> pd.DataFrame:
    allowed_views = {
        "avg_temp_por_ambiente",
        "leituras_por_hora",
        "temp_max_min_por_dia",
    }
    if view_name not in allowed_views:
        raise ValueError("View não permitida")

    with get_engine().connect() as connection:
        return pd.read_sql(text(f"SELECT * FROM {view_name}"), connection)


st.title("🌡️ Dashboard de Temperaturas IoT")
st.write(
    "Análise das leituras registradas por sensores instalados dentro e fora "
    "de um ambiente."
)

try:
    average = load_data("avg_temp_por_ambiente")
    hourly = load_data("leituras_por_hora")
    daily = load_data("temp_max_min_por_dia")

    first_column, second_column, third_column = st.columns(3)
    first_column.metric("Total de leituras", f"{int(average['total_leituras'].sum()):,}")
    second_column.metric("Maior temperatura", f"{daily['temp_max'].max():.1f} °C")
    third_column.metric("Menor temperatura", f"{daily['temp_min'].min():.1f} °C")

    st.subheader("1. Média de temperatura por ambiente")
    average_chart = px.bar(
        average,
        x="location",
        y="avg_temp",
        color="location",
        labels={"location": "Ambiente", "avg_temp": "Temperatura média (°C)"},
        text_auto=".2f",
    )
    st.plotly_chart(average_chart, width="stretch")

    st.subheader("2. Quantidade de leituras por hora")
    hourly_chart = px.line(
        hourly,
        x="hora",
        y="contagem",
        markers=True,
        labels={"hora": "Hora do dia", "contagem": "Quantidade de leituras"},
    )
    st.plotly_chart(hourly_chart, width="stretch")

    st.subheader("3. Temperaturas máximas e mínimas por dia")
    daily_chart = px.line(
        daily,
        x="data",
        y=["temp_max", "temp_min"],
        labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Série"},
    )
    daily_chart.update_layout(legend_title_text="Temperatura")
    st.plotly_chart(daily_chart, width="stretch")

except (SQLAlchemyError, ValueError) as error:
    st.error("Não foi possível carregar os dados do PostgreSQL.")
    st.info("Inicie o Docker e execute primeiro: python src/process_data.py")
    st.code(str(error))

