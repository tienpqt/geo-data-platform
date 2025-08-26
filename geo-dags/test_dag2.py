import time
import datetime
from airflow.sdk import DAG, task

with DAG(
    dag_id="test_dag2",
    start_date=datetime.datetime(2021, 1, 1),
    schedule="@daily"
):
    
    @task
    def hello_world():
        time.sleep(5)
        print("Hello world, from Airflow!")
    
    @task
    def modify_dag():
        time.sleep(5)
        print("Add new dags for testing Git Sync")
    
    hello_world() >> modify_dag()