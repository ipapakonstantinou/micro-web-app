import sys
import csv
import talib
import os
import numpy as np
import pandas as pd
from binance.client import Client

# print(__file__)
# cwd = os.getcwd()
# print(cwd)
# os.chdir('.')
# cwd = os.getcwd()
# print(cwd)

# Import the relevant scripts & config.py
sys.path.append('./.config')
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

# Get tickets
def get_tickers():
    tickers = client.get_all_tickers()
    df_tickers = pd.DataFrame.from_dict(tickers)

    return df_tickers

# Calculate total values
def calculate_totals(df_balances):

    # Get current prices
    df_tickers = get_tickers()

    # Get pairs in EUR & BTC
    df_balances['inUSDT'] = df_balances.apply(lambda row: row.asset + 'USDT' if row.asset != 'USDT' else row.free, axis=1)
    df_balances['inEUR'] = df_balances.apply(lambda row: row.asset + 'EUR' if row.asset != 'EUR' else row.free, axis=1)
    df_balances['inBTC'] = df_balances.apply(lambda row: row.asset + 'BTC' if row.asset != 'BTC' else row.free, axis=1)

    # Calculate values
    df_balances = df_balances.merge(df_tickers, how='left', right_on='symbol', left_on='inUSDT')
    df_balances = df_balances.rename(columns={'symbol': 'symbol_usdt', 'price': 'price_usdt'})
    df_balances = df_balances.merge(df_tickers, how='left', right_on='symbol', left_on='inEUR')
    df_balances = df_balances.rename(columns={'symbol': 'symbol_eur', 'price': 'price_eur'})
    df_balances = df_balances.merge(df_tickers, how='left', right_on='symbol', left_on='inBTC')
    df_balances = df_balances.rename(columns={'symbol': 'symbol_btc', 'price': 'price_btc'})
    df_balances['USDT'] = df_balances.apply(lambda row: row.free*float(row.price_usdt) if row.price_usdt != 'NaN' else ' ', axis=1)
    df_balances['EUR'] = df_balances.apply(lambda row: row.free*float(row.price_eur) if row.price_eur != 'NaN' else ' ', axis=1)
    df_balances['BTC'] = df_balances.apply(lambda row: row.free*float(row.price_btc) if row.price_btc != 'NaN' else ' ', axis=1)

    # Take only relevant columns
    df_balances = df_balances[['asset', 'free', 'USDT', 'EUR', 'BTC']]
    df_balances['USDT'] = df_balances.apply(lambda row: row.free if row.asset == 'USDT' else row.USDT, axis=1)
    df_balances['EUR'] = df_balances.apply(lambda row: row.free if row.asset == 'EUR' else row.EUR, axis=1)
    df_balances['BTC'] = df_balances.apply(lambda row: row.free if row.asset == 'BTC' else row.BTC, axis=1)

    total_usdt = df_balances['USDT'].sum()
    total_eur = df_balances['EUR'].sum()
    total_btc = df_balances['BTC'].sum()

    return df_balances, total_usdt, total_eur, total_btc

# Get balances
def get_balances():

    # Get the list of all available symbols
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    df_symbols = pd.DataFrame.from_dict(symbols)
    print('\nsymbols\n', df_symbols)

    # Get all asset where you have value > 0
    account = client.get_account()
    balances = account['balances']
    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]
    print('\nbalances\n', df_balances)

    # Get the assets that you own with the relevant values in EUR & BTC
    df_balances, total_usdt, total_eur, total_btc  = calculate_totals(df_balances)

    return df_balances, df_symbols, total_usdt, total_eur, total_btc

# Function for getting klines
def klines():

    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 Dec, 2016", "20 Mar, 2021")

    backtest_to_csv('1m.csv', candlesticks)

    df_candlesticks = pd.DataFrame.from_dict(candlesticks)
    df_candlesticks = df_candlesticks.iloc[:, : 6]
    df_candlesticks.columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume"]
    df_candlesticks["Timestamp"] = pd.to_datetime(df_candlesticks["Timestamp"], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
    print(df_candlesticks)

# Function for getting all orders
def get_orders():


    df_tickers = get_tickers()
    # df_tickers.to_csv('./data/person/tickers.csv')

    df_balances, symbols = get_balances()
    df_balances.to_csv('./data/person/balances.csv')
    print(df_balances)

    df_symbols = pd.DataFrame.from_dict(symbols)
    print(df_symbols)
    df_symbols.to_csv('./data/symbols.csv')

    for index, row in df_balances.iterrows():
        # print(row['asset'])
        symbol = row['asset'] + 'EUR'
        print(symbol)
        if symbol in df_symbols.symbol.values:
            try:
                orders = client.get_all_orders(symbol=symbol)
                df_orders = pd.DataFrame.from_dict(orders)
                # print(df_orders)
                if df_orders.empty == False:
                    df_orders.to_csv('./data/orders/eur/' + symbol + '.csv')
            except Exception as e:
                print(e, '\n', symbol, '\n')


        symbol = row['asset'] + 'BTC'
        if symbol in df_symbols.symbol.values:
            try:
                orders = client.get_all_orders(symbol=symbol)
                df_orders = pd.DataFrame.from_dict(orders)
                # print(df_orders)
                if df_orders.empty == False:
                    df_orders.to_csv('./data/orders/btc/' + symbol + '.csv')
            except Exception as e:
                print(e, '\n', symbol, '\n')

    return


# Test function
def testing():
    print('testing')



# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)
klines()
# get_orders()
# testing()
