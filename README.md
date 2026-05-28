# Multi-Source Finance & Stock Data Pipeline

Pulls stock prices and FX rates, loads to postgres, transforms with dbt, visualises in Metabase.

## How to run

**1. Create a `.env` file in the root**
```bash
STOCKS_DB_URL=postgresql+psycopg2://my_user:your_password@localhost:5732/stocks_db
```
don't commit this file.

**2. Start everything**
```bash
docker compose up -d
```

**3. Services**

| Service  | URL                   | Login         |
|----------|-----------------------|---------------|
| Airflow  | http://localhost:8080 | admin / admin |
| Metabase | http://localhost:3100 | —             |

**4. Run dbt**
```bash
cd stocks_pipeline
dbt build
```

**5. Metabase DB connection**
- Host: `localhost`, Port: `5732`
- Database: `stocks_db`, User: `my_user`
