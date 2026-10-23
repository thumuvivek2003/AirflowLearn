"""
TASK 04 — Fan-out and fan-in (parallel tasks)
=============================================
Real pipelines aren't always a straight line. Here:

                 ┌─> process_a ─┐
    start ──────>├─> process_b ─┤──────> combine
                 └─> process_c ─┘

start runs first. Then a, b, c run IN PARALLEL (LocalExecutor runs them at the
same time). Only when ALL three finish does `combine` run.

This is "fan-out" (1 -> many) then "fan-in" (many -> 1).
A python LIST on either side of >> means "all of these".
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def make_task(name):
    def _run():
        print(f"Running {name}")
    return _run


with DAG(
    dag_id="04_fan_out_fan_in",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    start = PythonOperator(task_id="start", python_callable=make_task("start"))
    a = PythonOperator(task_id="process_a", python_callable=make_task("a"))
    b = PythonOperator(task_id="process_b", python_callable=make_task("b"))
    c = PythonOperator(task_id="process_c", python_callable=make_task("c"))
    combine = PythonOperator(task_id="combine", python_callable=make_task("combine"))

    start >> [a, b, c] >> combine
