# Pipeline de Dados com IoT e Docker

Projeto acadêmico que processa leituras de temperatura de dispositivos IoT,
armazena os dados no PostgreSQL e apresenta três análises em um dashboard
Streamlit.

## Tecnologias

- Python e Pandas
- PostgreSQL
- Docker Compose
- SQLAlchemy e Psycopg2
- Streamlit e Plotly

## Estrutura

```text
projeto-iot/
├── data/                 # CSV do Kaggle e exemplo pequeno
├── docs/                 # Prints e roteiro do vídeo
├── sql/views.sql         # Três views SQL
├── src/database.py       # Conexão com o banco
├── src/process_data.py   # Limpeza e inserção do CSV
├── src/dashboard.py      # Dashboard Streamlit
├── docker-compose.yml
└── requirements.txt
```

## Base de dados

Baixe o conjunto [Temperature Readings: IoT Devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
e coloque o arquivo como `data/IOT-temp.csv`.

O conjunto possui leituras de sensores instalados dentro e fora de um cômodo.
As colunas originais são `id`, `room_id/id`, `noted_date`, `temp` e `out/in`.

## Como executar

### 1. Criar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Iniciar o PostgreSQL

Com o Docker Desktop aberto:

```powershell
docker compose up -d
```

### 3. Processar os dados

Com o CSV completo:

```powershell
python src/process_data.py
```

Para fazer um teste rápido com os oito registros de exemplo:

```powershell
python src/process_data.py --csv data/exemplo.csv
```

### 4. Abrir o dashboard

```powershell
streamlit run src/dashboard.py
```

O navegador abrirá normalmente em `http://localhost:8501`.

### 5. Encerrar o banco

```powershell
docker compose down
```

## Views SQL

### `avg_temp_por_ambiente`

Calcula a temperatura média e a quantidade de leituras nos ambientes interno e
externo. Ajuda a comparar a influência do clima externo no cômodo monitorado.

### `leituras_por_hora`

Agrupa os registros por hora do dia e calcula a quantidade de leituras e sua
temperatura média. Permite identificar horários com maior atividade do sensor.

### `temp_max_min_por_dia`

Apresenta as temperaturas máxima, mínima e média de cada dia. É útil para
encontrar variações e dias fora do comportamento esperado.

## Possíveis insights e aplicações

- Comparar a estabilidade da temperatura dentro e fora do ambiente.
- Identificar dias e horários com temperaturas extremas.
- Detectar falhas ou períodos sem registros do sensor.
- Aplicar o monitoramento em salas de servidores, estoques, estufas e indústrias.
- Criar alertas automáticos quando uma temperatura ultrapassar um limite seguro.

## Comandos Git utilizados

```powershell
git init
git add .
git commit -m "Projeto inicial: Pipeline de Dados IoT"
git branch -M main
git remote add origin URL_DO_SEU_REPOSITORIO
git push -u origin main
```

## Capturas de tela

### Dashboard completo

![Dashboard de Temperaturas IoT](docs/screenshots/dashboard-completo.png)

### Visualizações

![Média de temperatura por ambiente](docs/screenshots/media-por-ambiente.png)

![Quantidade de leituras por hora](docs/screenshots/leituras-por-hora.png)

![Temperaturas máximas e mínimas por dia](docs/screenshots/temperaturas-por-dia.png)

## Relatório escrito

O relatório completo está disponível em
[`output/pdf/relatorio-pipeline-iot.pdf`](output/pdf/relatorio-pipeline-iot.pdf).

