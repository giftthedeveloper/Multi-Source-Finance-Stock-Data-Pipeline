import yfinance as yf
from sqlalchemy import create_engine
import pandas as pd
import requests
import os

DB_URL = os.getenv(
    "STOCKS_DB_URL",
    "postgresql+psycopg2://my_user:password_132@postgres:5432/stocks_db"
)

exchange_rate_api_url="https://open.er-api.com/v6/latest/USD"

def fetch_stock_data():
    df = yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo')
    df = df['Close'].reset_index()
    df.rename(columns={'index': 'date'}, inplace=True)

    df_long = df.melt(
        id_vars='date',
        var_name='ticker',
        value_name='close_price'
    )
    df = df_long
    return df


def load_data_to_postgres(ti,table_name, fetch_task_id):
    df = ti.xcom_pull(task_ids=fetch_task_id)
    engine = create_engine(DB_URL)
    df.to_sql(table_name, engine, if_exists='replace', index=False)


def fetch_fx_rates():
    res = requests.get(exchange_rate_api_url)
    response = res.json()
    rates_df = pd.DataFrame({
        'currency': list(response['rates'].keys()),
        'value': list(response['rates'].values())
    })
    return rates_df

