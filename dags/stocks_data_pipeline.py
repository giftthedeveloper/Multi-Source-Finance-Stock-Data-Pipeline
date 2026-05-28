from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from ingest import fetch_fx_rates, load_data_to_postgres, fetch_stock_data, check_db_connection


with DAG(
    dag_id='stocks_data_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 5, 28),
    catchup=False,
) as dag:
  
  check_db = PythonOperator(
    task_id='check_db_connection',
    python_callable=check_db_connection
  )

  fetch_stock = PythonOperator(
    task_id='fetch_closing_stock_prices',
    python_callable=fetch_stock_data
  )

  fetch_fxrates = PythonOperator(
    task_id='fetch_fx_rates',
    python_callable=fetch_fx_rates
  )

  load_stock = PythonOperator(
    task_id='load_stock_data_to_postgres',
    python_callable=load_data_to_postgres,
    op_kwargs={
        'table_name': 'raw_stocks',
        'fetch_task_id': 'fetch_closing_stock_prices'
    }
  )

  load_fxrates = PythonOperator(
    task_id='load_fx_rates_to_postgres',
    python_callable=load_data_to_postgres,
    op_kwargs={
        'table_name': 'raw_fx_rates',
        'fetch_task_id': 'fetch_fx_rates' 
    }
  )

  transform = BashOperator(
    task_id='transform_data',
    bash_command='dbt run --project-dir /opt/airflow/stocks_pipeline --profiles-dir /opt/airflow/stocks_pipeline'
  )

  check_db >> [fetch_stock, fetch_fxrates]
  fetch_stock >> load_stock
  fetch_fxrates >> load_fxrates
  [load_stock, load_fxrates] >> transform

