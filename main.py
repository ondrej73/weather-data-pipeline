import json
import os
import logging
import requests
import psycopg

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 49.8209,
    "longitude": 18.2625,
    "current_weather": True
}

connection = None
cursor = None

try:
    logging.info("Pipeline started.")

    # 1. EXTRACT
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather = data["current_weather"]

        record = {
            "city": "Ostrava",
            "time": weather["time"],
            "temperature": weather["temperature"],
            "windspeed": weather["windspeed"],
            "is_day": weather["is_day"]
        }

        logging.info("Weather data downloaded successfully.")

    except requests.RequestException:
        logging.exception("API request failed.")
        raise

    except (KeyError, ValueError):
        logging.exception("API response has unexpected structure.")
        raise

    # 2. LOAD
    try:
        connection = psycopg.connect(
            host="localhost",
            port=5432,
            dbname="weather_db",
            user="weather_user",
            password="weather_password"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO weather_raw (
                city,
                measured_at,
                temperature,
                windspeed,
                is_day
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (city, measured_at) DO NOTHING
            """,
            (
                record["city"],
                record["time"],
                record["temperature"],
                record["windspeed"],
                record["is_day"]
            )
        )

        connection.commit()

        logging.info("Data saved to PostgreSQL successfully.")

    except psycopg.Error:
        logging.exception("Database operation failed.")

        if connection is not None:
            connection.rollback()

        raise

    logging.info("Pipeline finished successfully.")

except Exception:
    logging.exception("Pipeline failed.")

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None:
        connection.close()

    logging.info("Database connection closed.")