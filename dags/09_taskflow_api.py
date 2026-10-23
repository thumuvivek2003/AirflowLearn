"""
TASK 09 — The TaskFlow API (the modern, Pythonic way)
=====================================================
Everything you did with PythonOperator + XCom can be written much more cleanly
with decorators. This is the style most new Airflow code uses today.

  @dag    turns a function into a DAG
  @task   turns a function into a task
  - calling one @task function and passing its result to another AUTOMATICALLY
    wires the dependency AND moves the data via XCom. No xcom_pull boilerplate.

Compare this to task 03 + task 05 — same idea, far less code. As a Django dev
you'll appreciate how this reads like normal Python.
"""
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="09_taskflow_api",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
)
def pipeline():

    @task
    def extract():
        return [1, 2, 3, 4, 5]

    @task
    def transform(numbers):
        return [n * 10 for n in numbers]

    @task
    def load(numbers):
        print(f"Loading final values: {numbers}  (sum={sum(numbers)})")

    # Just call them. The data flow defines the dependencies automatically:
    raw = extract()
    cleaned = transform(raw)
    load(cleaned)


pipeline()  # don't forget to instantiate the @dag function
