"""
PHASE 3 PROJECT — A real ETL pipeline
=====================================
This pulls live data from a FREE public API (no key needed), transforms it with
pandas, and writes a CSV. It uses the TaskFlow API (task 09) and runs on a daily
schedule (task 08). This is a realistic shape for production work.

API: Open-Meteo (https://open-meteo.com) — current weather for a few cities.

Flow:
    extract (call API)  ->  transform (pandas)  ->  load (write CSV)

The output lands in data/output/ on your host (mapped into the container).

THIS is where you graduate from "examples" to "I built a pipeline." From here,
swap the API for your Django app's data, and the CSV for a Postgres table.
"""
from datetime import datetime

from airflow.decorators import dag, task

CITIES = {
    "Bengaluru": (12.97, 77.59),
    "London": (51.51, -0.13),
    "New York": (40.71, -74.01),
}
OUTPUT_DIR = "/opt/airflow/data/output"


@dag(
    dag_id="etl_weather_pipeline",
    description="Phase 3: extract weather from an API, transform, load to CSV",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["phase3", "project", "etl"],
)
def etl_weather():

    @task
    def extract():
        """Call the API for each city. Returns raw rows (small -> ok for XCom)."""
        import requests

        rows = []
        for city, (lat, lon) in CITIES.items():
            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}&current_weather=true"
            )
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            cw = resp.json()["current_weather"]
            rows.append(
                {
                    "city": city,
                    "temperature_c": cw["temperature"],
                    "windspeed_kmh": cw["windspeed"],
                    "observed_at": cw["time"],
                }
            )
        print(f"Extracted {len(rows)} city records")
        return rows

    @task
    def transform(rows):
        """Clean / enrich with pandas. Returns rows again."""
        import pandas as pd

        df = pd.DataFrame(rows)
        df["temperature_f"] = (df["temperature_c"] * 9 / 5 + 32).round(1)
        df = df.sort_values("temperature_c", ascending=False).reset_index(drop=True)
        print("Transformed data:\n", df.to_string(index=False))
        return df.to_dict(orient="records")

    @task
    def load(rows, **context):
        """Write a dated CSV. In a real project this would be a DB INSERT."""
        import os
        import pandas as pd

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        ds = context["ds"]  # the run's logical date
        path = f"{OUTPUT_DIR}/weather_{ds}.csv"
        pd.DataFrame(rows).to_csv(path, index=False)
        print(f"Wrote {len(rows)} rows to {path}")
        return path

    load(transform(extract()))


etl_weather()
