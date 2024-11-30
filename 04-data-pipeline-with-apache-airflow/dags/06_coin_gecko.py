from __future__ import annotations

import json
import logging

import pendulum
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook

log = logging.getLogger(__name__)

with DAG(
    dag_id="coingecko_data_pipeline",
    schedule=None,
    start_date=pendulum.datetime(2023, 10, 26, tz="UTC"),
    catchup=False,
    tags=["coingecko", "api", "bigquery"],
) as dag:
    def _extract_data_from_api(**kwargs):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd,thb&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        execution_date = kwargs['execution_date']
        filename = f"coingecko_price_{execution_date.format('YYYYMMDD')}.json"
        bucket_name = "deb-gemini-code-assist-data-ai-tao-001"
        folder_name = "raw/coingecko"


        gcs_hook = GCSHook()

        gcs_hook.upload(
            bucket_name=bucket_name,
            object_name=f"{folder_name}/{filename}", # Construct full path
            data=json.dumps(data),
        )


    extract_data_task = PythonOperator(
        task_id="extract_data_from_api",
        python_callable=_extract_data_from_api,
        provide_context=True, 
    )

    load_data_to_bigquery_task = GCSToBigQueryOperator(
        task_id="load_data_to_bigquery",
        bucket="deb-gemini-code-assist-data-ai-tao-001",
        source_objects=["raw/coingecko/coingecko_price_*.json"], # Wildcard path
        source_format='NEWLINE_DELIMITED_JSON',
        destination_project_dataset_table="dataai_tao_34.coingecko_price_tao",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_APPEND",
        schema_update_options=["ALLOW_FIELD_ADDITION"],
    )

    extract_data_task >> load_data_to_bigquery_task