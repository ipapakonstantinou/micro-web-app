import sys
import csv
import talib
import numpy as np
import pandas as pd
from binance.client import Client

# Import the relevant scripts & config.py
sys.path.append('../.config')
import config


# Write CSV file
def backtest_to_csv(csv_name, table):

    csv_name = '../data/backtest/' + csv_name
    csvfile = open(csv_name, 'w', newline='')
    data_writer = csv.writer(csvfile, delimiter=',')

    # Loop & write rows into csv
    for line in table:
        data_writer.writerow(line)
    csvfile.close()

# Get balances
def get_balances():

    account = client.get_account()
    balances = account['balances']
    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]

    # Get the list of all available symbols
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return df_balances, symbols

# Function for getting klines
def klines():

    prices = client.get_all_tickers()
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Dec, 2016", "7 Mar, 2021")

    backtest_to_csv('5m.csv', candlesticks)

    df_candlesticks = pd.DataFrame.from_dict(candlesticks)
    df_candlesticks = df_candlesticks.iloc[:, : 6]
    df_candlesticks.columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    df_candlesticks["Timestamp"] = pd.to_datetime(df_candlesticks["Timestamp"], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    print(df_candlesticks)


# Function for testing
def testing():

    tickers = client.get_all_tickers()
    df_tickers = pd.DataFrame.from_dict(tickers)
    df_tickers.to_csv('../data/person/tickers.csv')
    print(df_tickers)

    df_balances, symbols = get_balances()
    df_balances.to_csv('../data/person/balances.csv')
    print(df_balances)

    for index, row in df_balances.iterrows():
        # print(row['asset'])
        try:
            symbol = row['asset'] + 'EUR'
            orders = client.get_all_orders(symbol=symbol)
            df_orders = pd.DataFrame.from_dict(orders)
            # print(df_orders)
            df_orders.to_csv('../data/orders/' + symbol + '.csv')
        except Exception as e:
            print(e)
            print(symbol)




# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)
testing()
