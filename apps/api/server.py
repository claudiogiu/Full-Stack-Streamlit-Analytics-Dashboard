from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import clickhouse_connect
import pandas as pd
import logging
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(
    title="ClickHouse Data Server",
    description="A FastAPI-powered backend service that serves structured real estate transaction data from ClickHouse to a Streamlit frontend."
)

try:
    client = clickhouse_connect.get_client(host="clickhouse", port=8123, database="uk")
except Exception as e:
    logging.error(f"Connection error to ClickHouse: {e}")
    raise RuntimeError("Unable to connect to ClickHouse. Please check the connection.")

def query_to_df(query: str):
    """Executes a SQL query on ClickHouse."""
    try:
        result = client.query(query)
        return pd.DataFrame(result.result_rows, columns=result.column_names)
    except Exception as e:
        logging.error(f"Error executing query: {query} - {e}")
        raise HTTPException(status_code=500, detail=f"Error executing query: {e}")


@app.get("/sales-per-month")
async def get_sales_per_month():
    try:
        query = '''
        SELECT toYear(date) AS year, toMonth(date) AS month, COUNT() AS num_sales
        FROM uk.uk_price_paid
        WHERE toYear(date) BETWEEN 1995 AND 2023
        GROUP BY year, month
        ORDER BY year, month
        '''
        df = query_to_df(query)
        df["date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-01").dt.strftime("%Y-%m-%d")
        return df.to_dict(orient="records")
    except Exception as e:
        logging.error(f"Error retrieving monthly sales data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving monthly sales data: {e}")


@app.get("/top-expensive-neighborhoods")
async def get_top_expensive_neighborhoods(date: str):
    try:
        query = f'''
        SELECT
            town,
            district,
            COUNT() AS c,
            ROUND(AVG(price)) AS price
        FROM uk.uk_price_paid
        WHERE date BETWEEN '{date}-01-01' AND '{date}-12-31'
        GROUP BY town, district
        HAVING c >= 100
        ORDER BY price DESC
        LIMIT 10
        '''
        
        df = query_to_df(query)
        return df.to_dict(orient="records")
    
    except Exception as e:
        logging.error(f"Error retrieving most expensive neighborhoods data: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving most expensive neighborhoods data: {e}")


@app.get("/health")
async def service_health():
    try:
        client.command("SELECT 1") 
        return {"status": "OK"}
    except Exception as e:
        logging.error(f"Error in service health check: {e}")
        raise HTTPException(status_code=500, detail="Error in service health check")


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)