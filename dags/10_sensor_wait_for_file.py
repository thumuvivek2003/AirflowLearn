"""
TASK 10 — Sensors (waiting for something to happen)
====================================================
A SENSOR is a special task that WAITS until a condition is true, then lets the
pipeline continue. Common uses: wait for a file to land, wait for another DAG,
wait for an API to be ready.

This DAG:
  1. wait_for_file  -> a FileSensor that blocks until /opt/airflow/data/trigger.txt exists
  2. process_file   -> runs once the file appears

To test it:
  - Unpause + trigger the DAG. wait_for_file goes pink ("running") and waits.
  - On your host, create the file:   touch data/trigger.txt
    (it maps into the container at /opt/airflow/data — see docker-compose volumes)
  - Within a few seconds the sensor succeeds and process_file runs.

Key sensor args:
  poke_interval : how often (seconds) to check the condition
  timeout       : give up after this many seconds (else it waits forever)
  mode          : "poke" holds a worker slot; "reschedule" frees it between checks
                  (use reschedule for long waits in real life)
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

with DAG(
    dag_id="10_sensor_wait_for_file",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    # FileSensor uses a Connection for its base path. The built-in "fs_default"
    # connection points at the filesystem; we give an absolute filepath here.
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/opt/airflow/data/trigger.txt",
        fs_conn_id="fs_default",
        poke_interval=5,
        timeout=120,
        mode="poke",
    )

    process_file = BashOperator(
        task_id="process_file",
        bash_command="echo 'File found! Processing now.' && cat /opt/airflow/data/trigger.txt",
    )

    wait_for_file >> process_file
