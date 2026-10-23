# Phase 2 — 10 Hands-On Basics

> Goal: get your hands dirty. Each task = one DAG file in `dags/`. Do them in
> order. For each one: read the file's docstring → unpause it in the UI →
> trigger it → read the logs. Learning happens in the **Logs** tab.

| # | File | What you learn |
|---|------|----------------|
| 01 | `dags/01_hello_bash.py` | A DAG with one BashOperator task |
| 02 | `dags/02_hello_python.py` | PythonOperator — run a function |
| 03 | `dags/03_dependencies_chain.py` | Order tasks with `>>` (extract→transform→load) |
| 04 | `dags/04_fan_out_fan_in.py` | Parallel tasks (1→many→1) |
| 05 | `dags/05_xcom_passing_data.py` | Pass data between tasks via XCom |
| 06 | `dags/06_variables_and_connections.py` | Config with Variables & Connections |
| 07 | `dags/07_retries_and_failure.py` | Retries & watching a task fail/recover |
| 08 | `dags/08_scheduling_and_catchup.py` | Schedules, cron, logical date, catchup |
| 09 | `dags/09_taskflow_api.py` | Modern `@task` decorator style |
| 10 | `dags/10_sensor_wait_for_file.py` | Sensors — wait for a file to appear |

## How to run each one
1. Open http://localhost:8080 (login `airflow` / `airflow`).
2. Find the DAG by its `dag_id` (matches the filename). Use the `phase2` tag filter.
3. Toggle it **on** (unpause) — the switch on the left.
4. Click the **▶ Trigger** button (top right) to run it now.
5. Click the DAG → **Grid** view → click the latest run's task square → **Logs**.

## Special instructions for a few tasks
- **Task 06** — before running, create the Variable:
  `Admin → Variables → +` → Key `my_greeting`, Value anything.
- **Task 07** — trigger it a few times; sometimes it fails & retries (yellow),
  sometimes succeeds first try. Open Logs to read the simulated error.
- **Task 10** — after triggering, the sensor waits. In a terminal run:
  `touch data/trigger.txt` in the project root. The sensor then succeeds.

## Things to try (cement the learning)
- In task 03, change `e >> t >> l` to `e >> [t, l]` and watch the Graph change.
- In task 08, set `catchup=True` and `start_date` to 5 days ago, unpause, and
  watch Airflow backfill 5 runs at once. Then set it back to False.
- Break a DAG on purpose (add a typo) and see the import error banner in the UI.

## ✅ Phase 2 done when:
- You've run all 10 and read their logs.
- You can read a DAG file and predict its Graph view.
- You understand XCom vs Variable vs Connection (small runtime data vs config vs creds).

➡️ Then move to `phase3-projects.md`.
