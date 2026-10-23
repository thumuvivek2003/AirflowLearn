"""
TASK 08 — Scheduling and catchup (the part everyone gets confused by)
=====================================================================
So far every DAG used schedule=None (manual). Now we make one run AUTOMATICALLY.

  schedule="@daily"           -> run once a day (also: @hourly, @weekly, @monthly)
  schedule="0 6 * * *"        -> cron syntax: every day at 06:00
  schedule=timedelta(hours=2) -> every 2 hours

THE BIG GOTCHA — logical date vs run time:
  Airflow runs a period AFTER that period ends. The @daily run "for" 2024-01-01
  actually executes at the START of 2024-01-02. The date the run REPRESENTS is
  the "logical date" ({{ ds }}), NOT the wall-clock time it ran. This is because
  Airflow was built for data pipelines: "process yesterday's data."

CATCHUP:
  If start_date is in the past and catchup=True, Airflow will immediately run
  EVERY missed interval (could be hundreds!). We set catchup=False so it only
  runs from now on. This DAG is paused by default — unpause to see it schedule.
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="08_scheduling_and_catchup",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",      # <-- now it runs on a schedule, no manual trigger needed
    catchup=False,          # <-- try flipping to True (and a recent start_date) to SEE backfilling
    tags=["phase2", "basics"],
) as dag:

    BashOperator(
        task_id="daily_job",
        bash_command="echo 'Daily run. Logical date (the day this represents) = {{ ds }}'",
    )
