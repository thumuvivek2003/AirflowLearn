"""
TASK 03 — Chaining tasks with dependencies (the >> operator)
============================================================
A DAG is about ORDER. Here three tasks run one after another:
    extract  >>  transform  >>  load
This is the classic "ETL" shape you'll build for real in Phase 3.

The `>>` operator means "then". `a >> b` = "run a, then b".
(`<<` is the reverse. You can also write a.set_downstream(b).)

Open the "Graph" view in the UI to SEE the arrows between tasks.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract():
    print("1) Extracting raw data...")


def transform():
    print("2) Transforming data...")


def load():
    print("3) Loading data into destination...")


with DAG(
    dag_id="03_dependencies_chain",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    e = PythonOperator(task_id="extract", python_callable=extract)
    t = PythonOperator(task_id="transform", python_callable=transform)
    l = PythonOperator(task_id="load", python_callable=load)

    # This single line defines the whole pipeline order:
    e >> t >> l
