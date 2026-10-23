# Phase 3 — Real Projects

> Goal: build end-to-end pipelines that look like production work. Start with the
> provided project, then build your own (ideally tied to your Django app).

## Project 0 (provided) — Weather ETL
File: `dags/projects/etl_weather_pipeline.py`

Pulls live weather from a free public API → transforms with pandas → writes a
dated CSV to `data/output/`. Run it, then check the CSV appeared on your host.

What to study in it:
- TaskFlow `@dag`/`@task` style (from Phase 2 task 09)
- A daily `schedule` (from task 08)
- `import` statements **inside** task functions — keeps DAG parsing fast and
  avoids import errors at the top level (a real best practice).
- Using `{{ ds }}` / `context["ds"]` to name output by run date.

## Project ideas to build yourself (in rough difficulty order)

### 1. API → Postgres pipeline
Replace the CSV `load` step with a real DB insert.
- Add a Postgres connection in `Admin → Connections` (you can reuse the bundled
  metadata Postgres for practice, or add a separate one).
- Use `PostgresHook` or the `apache-airflow-providers-postgres` operators.
- Make `load` idempotent: deleting+reinserting the day's rows so re-runs are safe.

### 2. Trigger your Django code from Airflow
This is your real-world payoff. Two clean patterns:
- **Management command**: `BashOperator` runs
  `python manage.py your_command` inside your Django container/venv.
- **HTTP**: expose a Django endpoint and call it with `SimpleHttpOperator`.
Use a Connection for the Django host/credentials — never hardcode.

### 3. Multi-source daily report
Fan-out (Phase 2 task 04): pull from 2–3 sources in parallel → join → email or
write a summary. Add `retries` and an SLA so you get alerted on slowness.

### 4. Sensor-driven pipeline
A `FileSensor` (task 10) or an external-task sensor waits for an upstream DAG /
dropped file, then kicks off processing. Models real "wait for the data" cases.

## Best practices to adopt as you build
- **Idempotency**: a task re-run for the same date must produce the same result
  (delete-then-insert, or upsert). This is the golden rule of pipelines.
- **Keep tasks small & single-purpose** — easier to retry just the broken step.
- **Don't pass big data via XCom** — write to a file/DB, pass the path.
- **Put heavy imports inside task functions**, not at module top level.
- **Use Connections/Variables** for all config & secrets, never hardcode.
- **Parametrize by `ds`** (the logical date) so backfills work correctly.
- One DAG = one `.py` file; group related project DAGs under `dags/projects/`.

## Where to go deeper
- Official docs: https://airflow.apache.org/docs/
- Astronomer guides (excellent, free): https://www.astronomer.io/docs/learn/
- Providers (DB/cloud integrations): search "apache-airflow-providers-<thing>".

## ✅ Phase 3 done when:
- You've run the weather ETL and seen the CSV.
- You've built at least one pipeline that loads into a database.
- You've triggered your own Django code from an Airflow DAG.
