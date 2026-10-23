"""
TASK 02 — Same thing, but with PythonOperator
==============================================
Now the task runs a Python FUNCTION instead of a shell command.
This is what you'll use 90% of the time, because your logic is Python.

Concepts:
  - PythonOperator    : runs a python callable as a task
  - python_callable   : the function to run
  - **context / **kwargs : Airflow passes runtime info (dates, params) into your function
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def greet(**context):
    # context holds everything about THIS run. ds = the run's date string.
    run_date = context["ds"]
    print(f"Hello from Python! This run represents the date: {run_date}")
    return "done"  # whatever you return is stored as an XCom (see task 05)


with DAG(
    dag_id="02_hello_python",
    description="First PythonOperator task",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    greet_task = PythonOperator(
        task_id="greet",
        python_callable=greet,
    )
