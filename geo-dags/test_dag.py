import time
import datetime
from airflow.sdk import DAG, task

with DAG(
    dag_id="test_dag",
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
        print("Modified DAG for test Git Sync")
    
    hello_world() >> modify_dag()