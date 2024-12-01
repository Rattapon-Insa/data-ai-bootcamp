import logging
import os
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

# REPLACE_BUCKET_NAME_HERE !!!
BUCKET_NAME = "deb-gemini-code-assist-data-ai-tao-001"

# REPLACE_DESTINATION_PROJECT_DATASET_TABLE_HERE !!!
DESTINATION_PROJECT_DATASET_TABLE = "dataai_tao_34.coingecko_price"

# Define default arguments for the DAG
default_args = {
    'owner': 'gemini-code-assist',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Get DAG directory
dag_path = os.path.dirname(os.path.abspath(__file__))


# Define the DAG
with DAG(
    'customer_feedback_dag',
    default_args=default_args,
    description='Ingest customer feedback data from JSON to BigQuery',
    schedule_interval=None,  # Set your desired schedule, e.g., '@daily'
    start_date=datetime(2023, 12, 18),
    catchup=False,
) as dag:

    # Task 1: Extract data from JSON, convert to CSV, and upload to GCS
    def extract_and_upload_to_gcs(**kwargs):
        bucket_name = kwargs['bucket_name']
        file_name = 'customer_feedback.json'  # Update with your actual file path
        gcs_folder = 'raw/customer_feedback'
        full_file_path = os.path.join(dag_path, file_name)

        # Log all files in the DAG directory
        logging.info(f"Files in DAG directory: {os.listdir(dag_path)}")


             # Read JSON data into a Pandas DataFrame
        df = pd.read_json(full_file_path)

        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)

        # Upload CSV data to GCS
        gcs_hook = GCSHook()
        gcs_hook.upload(
            bucket_name=bucket_name,
            object_name=f'{gcs_folder}/customer_feedback.csv',
            data=csv_data,
        )


    extract_task = PythonOperator(
        task_id='extract_and_upload_to_gcs',
        python_callable=extract_and_upload_to_gcs,
        op_kwargs={'bucket_name': BUCKET_NAME},  # Replace with your bucket name
    )

    # Task 2: Transform data using Pandas
    def transform_data(**kwargs):
        bucket_name = kwargs['bucket_name']
        gcs_folder = 'raw/customer_feedback'
        transformed_folder = 'processed/customer_feedback'

        # Download CSV data from GCS
        gcs_hook = GCSHook()
        file_content = gcs_hook.download(
            bucket_name=bucket_name,
            object_name=f'{gcs_folder}/customer_feedback.csv',
        )

        # Decode bytes to string and create a StringIO object
        file_content_str = file_content.decode('utf-8')
        file_like_object = StringIO(file_content_str)

        # Read CSV data into a Pandas DataFrame
        df = pd.read_csv(file_like_object)

        # Data Cleaning and Transformation
        df['feedback'] = df['feedback'].str.strip()  # Example: Remove leading/trailing spaces
        df['count_character'] = df['feedback'].str.len()

        # Assuming 'birthdate' column exists in your data
        df['birthdate'] = pd.to_datetime(df['birthdate'])
        now = datetime.now()
        df['age'] = (now - df['birthdate']).dt.days // 365.25

        # Define age generation logic
        def get_age_generation(age):
            if 18 <= age <= 25:
                return 'Gen Z'
            elif 26 <= age <= 41:
                return 'Millennial'
            elif 42 <= age <= 57:
                return 'Gen X'
            elif 58 <= age <= 67:
                return 'Baby Boomers'
            else:
                return 'Other'

        df['age_generation'] = df['age'].apply(get_age_generation)

        # Upload transformed data to GCS
        transformed_csv_data = df.to_csv(index=False)
        gcs_hook.upload(
            bucket_name=bucket_name,
            object_name=f'{transformed_folder}/transformed_customer_feedback.csv',
            data=transformed_csv_data,
        )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'bucket_name': BUCKET_NAME},
    )

    # Task 3: Load data from GCS to BigQuery
    load_to_bq_task = GCSToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket=BUCKET_NAME,  # Replace with your bucket name
        source_objects=['processed/customer_feedback/transformed_customer_feedback.csv'],
        destination_project_dataset_table=DESTINATION_PROJECT_DATASET_TABLE,
        project_id='dataaibootcamp',
        write_disposition='WRITE_TRUNCATE',  # Change to 'WRITE_APPEND' if needed
        source_format='CSV',
        skip_leading_rows=1,
        autodetect=True,
    )

    # Set task dependencies
    extract_task >> transform_task >> load_to_bq_task
 