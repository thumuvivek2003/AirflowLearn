"""
TASK 06 — Variables and Connections
====================================
Don't hardcode config (API keys, paths, DB hosts) in your DAG. Airflow has two
official places to store them, both editable in the UI under Admin:

  VARIABLE   = a key/value setting.  Admin -> Variables.
               Like Django settings, but editable at runtime without redeploy.

  CONNECTION = credentials for an external system (a DB, an API, SFTP...).
               Admin -> Connections. Hooks/Operators read these by conn_id.
               Like Django's DATABASES dict, but managed by Airflow.

BEFORE running this DAG, create the Variable in the UI:
  Admin -> Variables -> +  ->  Key: my_greeting   Val: Hello from a Variable!

(A Connection example is shown in code but commented, so the DAG still parses
 even if you haven't created one yet.)
"""
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


def use_config(**context):
    # default_var avoids a crash if you haven't created the Variable yet.
    greeting = Variable.get("my_greeting", default_var="(variable not set — create it in Admin->Variables)")
    print(f"Variable my_greeting = {greeting}")

    # --- How you'd read a Connection (uncomment after creating conn 'my_api') ---
    # from airflow.hooks.base import BaseHook
    # conn = BaseHook.get_connection("my_api")
    # print(f"Connection host: {conn.host}, login: {conn.login}")


with DAG(
    dag_id="06_variables_and_connections",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase2", "basics"],
) as dag:

    PythonOperator(task_id="use_config", python_callable=use_config)
