from prefect import flow, task
import requests
import pandas as pd
import time
import os


@task
def fetch_stock_data(ticker: str) -> float:
    headers = {
        "x-rapidapi-key": "884dfc0466msh2ed79dd4174ccddp1e3f2ejsn7a9336a21538",
        "x-rapidapi-host": "realstonks.p.rapidapi.com"
    }
    url = f"https://realstonks.p.rapidapi.com/stocks/{ticker}/advanced"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("lastPrice", None)


@flow(name="etl-flow")
def etl_flow():
    tickers = ['GOOGL', 'AAPL']
    data = {
        'Stock_Name': [],
        'Stock_Price': [],
        'time': []
    }

    for ticker in tickers:
        price = fetch_stock_data(ticker)
        data['Stock_Name'].append(ticker)
        data['Stock_Price'].append(price)
        data['time'].append(time.strftime("%Y-%m-%d %H:%M:%S"))

    df = pd.DataFrame(data)
    output_file = "financial_data.csv"
    file_exists = os.path.exists(output_file)

    df.to_csv(output_file, mode='a', header=not file_exists, index=False)
    print("✅ Script terminé. Fichier mis à jour.")


if __name__ == "__main__":
    etl_flow()


