"""
TASK 05 — Passing data between tasks with XCom
==============================================
Tasks are isolated — task B can't see task A's variables. To pass SMALL bits of
data (a number, a filename, a short string) between tasks, you use XCom
("cross-communication"). It's stored in the metadata DB.

  - return a value from a task        -> it's "pushed" to XCom automatically
  - ti.xcom_pull(task_ids="...")      -> "pull" another task's value

⚠️  XCom is for SMALL data only (ids, counts, paths). Never push big dataframes
    through it — for big data, write to a file/DB and pass the PATH via XCom.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def produce(**context):
    value = 42
    print(f"Producing value: {value}")
    return value  # auto-pushed to XCom under key "return_value"


def consume(**context):
    ti = context["ti"]  # ti = "task instance", your handle to XCom
    received = ti.xcom_pull(task_ids="produce")
    print(f"Consumed value from upstream task: {received}")
    print(f"Doubled it: {received * 2}")


with DAG(
    dag_id="05_xcom_passing_data",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    p = PythonOperator(task_id="produce", python_callable=produce)
    c = PythonOperator(task_id="consume", python_callable=consume)

    p >> c
