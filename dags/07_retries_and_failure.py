"""
TASK 07 — Retries and handling failure
=======================================
The #1 reason teams use Airflow instead of cron: when something fails, Airflow
RETRIES it and shows you exactly what happened.

This DAG has a task that fails ~50% of the time on purpose. Watch it in the UI:
the task turns yellow ("up_for_retry"), waits, tries again, and only turns red
("failed") after exhausting its retries.

  - default_args   : settings applied to EVERY task in the DAG
  - retries        : how many extra attempts after the first failure
  - retry_delay    : how long to wait between attempts

NOTE: this uses the run's second-of-minute to decide success, so it's
deterministic per-run but varies across runs — no randomness needed.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
}


def flaky(**context):
    # ts_nodash looks like 20240101T133057 — grab the seconds digit.
    second = int(context["ts_nodash"][-1])
    print(f"Attempt running... (derived digit = {second})")
    if second % 2 == 0:
        raise ValueError("Boom! Simulated failure — Airflow will retry me.")
    print("Success this time!")


with DAG(
    dag_id="07_retries_and_failure",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["phase2", "basics"],
) as dag:

    PythonOperator(task_id="might_fail", python_callable=flaky)
