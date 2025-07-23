from prefect import flow, task
import requests
import pandas as pd
import time
import os

@task
def fetch_stock_data(ticker):
    headers = {
        "x-rapidapi-key": "884dfc0466msh2ed79dd4174ccddp1e3f2ejsn7a9336a21538",
        "x-rapidapi-host": "realstonks.p.rapidapi.com"
    }
    url = f"https://realstonks.p.rapidapi.com/stocks/{ticker}/advanced"
    response = requests.get(url, headers=headers)
    return response.json().get("lastPrice", None)

@flow(name="etl-flow")
def etl_flow():
    tickers = ['GOOGL', 'AAPL']
    dict_data = {'Stock_Name': [], 'Stock_Price': [], 'time': []}
    for ticker in tickers:
        price = fetch_stock_data(ticker)
        dict_data['Stock_Name'].append(ticker)
        dict_data['Stock_Price'].append(price)
        dict_data['time'].append(time.time())

    df = pd.DataFrame.from_dict(dict_data)
    file_exists = os.path.isfile("financial_data.csv")
    df.to_csv("financial_data.csv", mode='a', header=not file_exists, index=False)
    print("✅ Script terminé.")

if __name__ == "__main__":
    etl_flow()



