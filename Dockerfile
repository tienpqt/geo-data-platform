FROM apache/airflow:3.0.2-python3.11

COPY ./geo-dags/ /opt/airflow/dags/

COPY ./requirements.txt .

RUN  pip install --no-cache-dir -r requirements.txt