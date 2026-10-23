# Phase 1 — Airflow Concepts & Jargon (the "what / why / where")

> Goal of this phase: understand the words and the mental model. Don't write
> code yet — just read this and click around the UI.

## What Airflow actually is (and isn't)

Airflow is a **workflow orchestrator**: a smart scheduler that runs your tasks
in the right order, on a schedule, with retries, logging, and a UI to watch it.

**It does NOT process your data itself.** It tells *your* code (Python, SQL,
bash, API calls) when to run and in what order. Think "conductor", not "musician".

### Why teams use it instead of cron + scripts
| Plain cron | Airflow |
|---|---|
| No dependencies ("run B only after A") | First-class dependencies |
| Fails silently | Retries + alerts + visible failures |
| No history | Full run history & logs in a UI |
| Hard to backfill past dates | Built-in backfill |
| Config scattered in scripts | Variables/Connections managed centrally |

### Where it's used
ETL/ELT pipelines, data warehouse loading, ML training pipelines, report
generation, periodic API syncs — anything scheduled with multiple steps.

## Coming from Django — translation table
| Django | Airflow |
|---|---|
| Celery beat / cron management commands | Airflow scheduler |
| A view / function | A **task** |
| `urls.py` (wiring) | A **DAG** (wiring tasks in order) |
| Celery worker | Airflow worker / executor |
| Django admin | Airflow web UI |
| `settings.py` values | **Variables** |
| `DATABASES` / external creds | **Connections** |

## The core vocabulary (memorize these)

- **DAG** — *Directed Acyclic Graph*. Your workflow, defined in a `.py` file.
  "Directed" = arrows have direction. "Acyclic" = no loops (A→B→A is illegal).
- **Task** — one unit of work in a DAG.
- **Operator** — a *template* for a task. You pick one: `BashOperator`,
  `PythonOperator`, `PostgresOperator`, etc. A task is an operator with settings.
- **Task Instance (TI)** — one specific *run* of a task for a specific date.
- **DAG Run** — one execution of the whole DAG for a specific logical date.
- **Scheduler** — the brain. Decides what should run now and queues it.
- **Executor** — *how* tasks run. `LocalExecutor` (our setup) runs them as local
  processes. `CeleryExecutor`/`KubernetesExecutor` scale across machines.
- **Webserver** — serves the UI at localhost:8080.
- **Metadata DB** — Postgres storing all state/history (NOT your business data).
- **schedule** — when a DAG runs (`@daily`, cron, timedelta, or `None`=manual).
- **start_date** — earliest date the DAG may run for.
- **logical date / `ds`** — the date a run *represents* (often "yesterday's data"),
  NOT the wall-clock time it ran. ⭐ The thing beginners trip on.
- **catchup / backfill** — running for past dates. Keep `catchup=False` while learning.
- **XCom** — cross-communication: pass *small* data between tasks.
- **Sensor** — a task that *waits* for a condition (file arrives, time passes...).
- **Hook** — a reusable client for an external system (DB, API), uses a Connection.
- **Connection** — stored credentials for an external system (`conn_id`).
- **Variable** — a key/value config setting, editable in the UI.
- **retries / retry_delay** — auto re-run failed tasks N times.
- **Pool** — limit concurrency (e.g. "max 3 tasks hit this DB at once").
- **SLA** — "this task should finish within X"; alerts if it doesn't.
- **Trigger Rule** — when a task runs relative to upstream (default: all_success).

## Task states you'll see in the UI (by color)
`queued` → `running` → `success` (green) / `failed` (red) / `up_for_retry`
(yellow) / `skipped` / `upstream_failed`.

## The UI tabs worth knowing
- **DAGs** list — pause/unpause (toggle on the left), trigger (▶).
- **Grid** — runs over time; click a cell → **Logs** (your best friend).
- **Graph** — visual of task dependencies.
- **Admin → Variables / Connections** — config & credentials.

## ✅ Phase 1 done when you can answer:
1. What's the difference between a DAG, a task, and an operator?
2. Why is `logical date` not the same as "now"?
3. What does the scheduler do vs the executor?
4. Where would you store a database password? (→ Connection)
5. Why use Airflow over a cron job?

➡️ Then move to `phase2-tasks.md`.
