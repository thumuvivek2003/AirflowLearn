"""
TASK 01 — Hello World with BashOperator
========================================
The simplest possible DAG: one task that runs a shell command.

Concepts you meet here:
  - DAG            : the workflow (this whole file defines ONE dag)
  - dag_id         : its unique name (shown in the UI). Convention: match the filename.
  - schedule       : when it runs. None = only when YOU click "Trigger" in the UI.
  - start_date     : the earliest date this DAG is allowed to run for.
  - catchup        : if True, Airflow runs every missed date since start_date. Keep False while learning.
  - BashOperator   : a task that runs a bash command. Like a cron line, but tracked.

Run it: open the UI (localhost:8080), find "01_hello_bash", unpause it, click ▶ Trigger.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="01_hello_bash",
    description="My first DAG — prints hello from bash",
    start_date=datetime(2024, 1, 1),
    schedule=None,          # manual trigger only
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    say_hello = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello Airflow, buddy! The date for this run is {{ ds }}'",
        # {{ ds }} is a Jinja template — Airflow fills in the run's date (YYYY-MM-DD).
    )
