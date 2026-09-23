# Weather Data Pipeline

A simple end-to-end data engineering project built as a practical learning exercise and portfolio project.

The pipeline collects current weather data for Ostrava from the Open-Meteo API, stores raw measurements in PostgreSQL, transforms the data with dbt, and produces a daily aggregated weather model for analytics.

## Architecture

```text
Open-Meteo API
      ↓
    Python
      ↓
 PostgreSQL
 weather_raw
      ↓
     dbt
      ↓
 stg_weather
      ↓
     dbt
      ↓
daily_weather_summary
```

## Technologies

* Python
* PostgreSQL
* Docker
* dbt
* Git
* GitHub
* SQL

## Pipeline

The Python script:

1. Requests current weather data from the Open-Meteo API.
2. Extracts selected fields such as temperature, wind speed and measurement time.
3. Stores the data in PostgreSQL.
4. Prevents duplicate measurements using a unique constraint.
5. Writes execution information and errors to a log file.

dbt is used to transform the raw data into analytical models.

### `weather_raw`

Raw measurements loaded by the Python ingestion script.

### `stg_weather`

Staging model used to prepare and standardize the raw data.

### `daily_weather_summary`

Daily aggregation containing:

* number of measurements
* average temperature
* minimum temperature
* maximum temperature
* average wind speed

## Data Quality

dbt tests are used to validate important fields such as:

* unique IDs
* non-null city values
* non-null measurement timestamps

PostgreSQL also enforces uniqueness of the combination:

```text
city + measured_at
```

to prevent duplicate measurements.

## Running the project

Start PostgreSQL:

```bash
docker compose up -d
```

Run the ingestion script:

```bash
python main.py
```

Run dbt models:

```bash
cd weather_dbt
dbt run
```

Run data quality tests:

```bash
dbt test
```

## Project purpose

This project was created to gain practical experience with data engineering concepts including:

* API ingestion
* Python data processing
* relational databases
* SQL
* ELT pipelines
* dbt models and sources
* data quality testing
* Docker
* version control

Future improvements include automated scheduling, CI/CD with GitHub Actions, and deployment to a cloud environment.
