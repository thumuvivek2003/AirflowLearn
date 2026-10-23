# AirflowLearn 🚀

A hands-on workspace to learn Apache Airflow in 3 phases, built for a Python/Django
developer who is brand new to Airflow.

## What's here

```
AirflowLearn/
├── docker-compose.yaml      # The Airflow stack (Postgres + scheduler + webserver)
├── .env                     # UID + extra pip packages
├── requirements.txt         # Extra Python libs for the DAGs (pandas, requests)
├── notes/
│   ├── phase1-concepts.md   # Phase 1: jargon & mental model (READ FIRST)
│   ├── phase2-tasks.md      # Phase 2: the 10 hands-on basics
│   └── phase3-projects.md   # Phase 3: real projects
├── dags/
│   ├── 01_hello_bash.py ... 10_sensor_wait_for_file.py   # the 10 basics
│   └── projects/
│       └── etl_weather_pipeline.py                       # Phase 3 starter ETL
└── data/                    # mapped into the container at /opt/airflow/data
```

## Quick start

```bash
# 1. Start everything (first run pulls images + installs pandas/requests — give it 1-2 min)
docker compose up -d

# 2. Watch it become healthy
docker compose ps

# 3. Open the UI
#    http://localhost:8080      login: airflow / airflow
```

Then follow the notes **in order**: Phase 1 → 2 → 3.

## Daily commands

| Command | What it does |
|---|---|
| `docker compose up -d` | Start the stack in the background |
| `docker compose ps` | See service health |
| `docker compose logs -f airflow-scheduler` | Tail scheduler logs |
| `docker compose down` | Stop (keeps your DB & history) |
| `docker compose down -v` | Stop AND wipe the database (fresh start) |
| `docker compose restart airflow-scheduler` | Reload after weird states |

## How the learning loop works
1. Edit/read a DAG in `dags/` (changes appear in the UI within ~30s — no restart needed).
2. In the UI: **unpause** the DAG, click **▶ Trigger**.
3. Open **Grid → click task → Logs** to see output.

## Common gotchas (you'll hit these)
- **DAG not showing up?** Check the UI's "Import Errors" banner — usually a Python
  typo. Or wait ~30s for the scheduler to rescan.
- **Everything ran 100 times at once?** That's `catchup`. We default it off; see
  Phase 2 task 08.
- **Permission errors on `logs/`?** Make sure `AIRFLOW_UID` in `.env` matches
  `id -u` (yours is already set to 1000).
- **Port 8080 busy?** Change `"8080:8080"` to e.g. `"8081:8080"` in docker-compose.yaml.

## Login
- URL: http://localhost:8080
- Username: `airflow`  Password: `airflow`

---
This is a *learning* setup (single-machine, LocalExecutor, default password).
Don't use it as-is in production.
