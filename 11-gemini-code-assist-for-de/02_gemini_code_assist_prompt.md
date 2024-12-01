
# Gemini Code Assist for Data Engineering  - Prompt


## Generate unittest

Prerequisites

Before you begin, ensure the following:
- Gemini Code Assist is installed: Follow the installation guide in the official documentation.
- Configured project: Your project should be set up with a supported testing framework (e.g., pytest, unittest, etc.).
- Access to source code: The source code to be tested should be accessible and properly structured.

Step 1: Open the Code File
- Open the file you want to create unit tests for in your preferred editor.
- Ensure the file contains methods or classes that you intend to test.

Step 2: Launch Gemini Code Assist
- Open Gemini Code Assist within your IDE or development environment.
- Select the Unit Test Generation feature from the main menu.

Step 3: Select the Function or Class to Test
- Highlight the specific function or class you want to test.
- Right-click and select Generate Unit Test from the context menu (or use the shortcut specified in your environment).

Step 4: Configure the Test Parameters
- Gemini Code Assist allows you to configure the unit test generation process:
    - Select the testing framework: Choose your preferred framework (e.g., pytest, unittest, etc.).
    - Mocking preferences: Specify whether dependencies should be mocked automatically.

Step 5: Generate the Unit Test
- Click Generate.
- Review the auto-generated test cases. Gemini Code Assist will create test methods.

Step 6: Save and Review the Test File
- Save the generated test file in the appropriate test directory (e.g., tests/).
- Review the test cases to ensure they meet your project requirements.

Step 7: Run the Tests
- Execute the unit tests using your testing framework: python -m unittest tests/test_file_name.py
- Verify that all tests pass or address any failing tests.

## DAG_1 - ingest data from API to BigQuery

### 1. Prompt to Create Data Pipeline 

```
Write an Airflow DAG to extract cryptocurrency price data from the CoinGecko API and load it into Google BigQuery. The DAG should:

1. **Run hourly** starting from a specific date (e.g., November 30, 2024).
2. Extract data from the CoinGecko API using the following parameters:
   - Cryptocurrencies: Bitcoin, Ethereum, Tether.
   - Currencies: USD and THB.
   - Include additional metadata such as market cap, 24-hour volume, and last updated time.
3. Save the API response to Google Cloud Storage (GCS) in JSON format with the following structure:
   - **Bucket name**: `deb-gemini-code-assist-data-ai-tao-001`.
   - **Folder**: `raw/coingecko`.
   - **Filename format**: `coingecko_price_<execution_date>.json` (e.g., `coingecko_price_20241130.json`).
4. Load the JSON files into a BigQuery table:
   - **BigQuery table**: `dataai_tao_34.coingecko_price`.
   - **Configuration**:
     - Allow schema updates.
     - Append data to the table.
     - Use wildcard paths to load all relevant JSON files.

Include the following in the response:
- Necessary imports for Airflow, GCS, and BigQuery integration.
- Python functions or tasks for API data extraction, uploading to GCS, and loading to BigQuery.
- Proper operator configuration and task dependencies.
- Comments explaining each section of the code for clarity.
```

### 2. Chat with you code after prompt is done
```
Fix as the following 
- Add Schedule to interval to every hour at 21:00 
- DAG's owner to `gemini-code-assist`
```

## DAG_2 - ingest data from Json File to BigQuery

```
Write an Airflow DAG named customer_feedback_dag to process customer feedback data. The DAG should:

Default Arguments:

Owner: gemini-code-assist.
Retries: 2.
Retry delay: 5 minutes.
DAG Configuration:

Start date: December 18, 2023.
Schedule interval: None (manual execution).
Catchup: False.
Tags: customer_feedback.
Tasks:

Use PythonOperator for the first two tasks and GCSToBigQueryOperator for the third task.

Task 1: Extract and Upload to GCS:

Read a JSON file named customer_feedback.json from the DAG directory.
Convert the JSON data to a Pandas DataFrame.
Using dataframe to csv feature to convert json to csv.
Use the GCSHook to upload the CSV file to a GCS bucket named deb-gemini-code-assist-data-ai-tao-001 in the folder raw/customer_feedback/.
Clean up temporary files after uploading.

Task 2: Transform Data:

Download the raw CSV file from GCS (raw/customer_feedback/customer_feedback.csv) using the GCSHook.
Perform the following transformations using Pandas:
- Strip whitespace from the feedback column.
- Add a feedback_length column with the character count of feedback.
- Calculate an age column based on the birthdate column.
- Add an age_generation column by classifying ages using the following logic:
    - Gen Z: Age between 18 and 25.
    - Millennial: Age between 26 and 41.
    - Gen X: Age between 42 and 57.
    - Baby Boomers: Age between 58 and 67.
    - Other: Any other age not in the above ranges.
Upload the transformed CSV file to GCS in the folder processed/customer_feedback/.
Clean up temporary files after uploading.

Task 3: Load to BigQuery:

Use the GCSToBigQueryOperator to load the transformed CSV file from GCS (processed/customer_feedback/customer_feedback.csv) into the BigQuery table dataai_tao_34.customer_feedback.
    Configuration:
    write_disposition: WRITE_TRUNCATE.
    source_format: CSV.
    skip_leading_rows: 1.
    autodetect: True.

Task Dependencies:
    Task dependencies: extract_and_upload_to_gcs >> transform_data >> load_to_bigquery.
```