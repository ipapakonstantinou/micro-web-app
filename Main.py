# %%

'''
Initial Run
%load_ext autoreload
%autoreload 2
'''


import json
import requests
import hashlib
import hmac
import sys
import time
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from binance.client import Client

from scripts.binance_api import *
from config.config import *

pd.options.mode.chained_assignment = None  # default='warn'

# Get balances
def get_balances(client):

    # Get all asset where you have value > 0
    account = client.get_account()
    balances = account['balances']
    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]

    return df_balances

def get_trading_symbols(df, client):

    if L_SYMBOLS != '':
        trading_symbols = L_SYMBOLS
    else:
        sys.exit()
        trading_symbols = get_exchange_info(client)
        display(len(trading_symbols))

    return trading_symbols

def get_exchange_info(client):

    trade_symbols = []
    exchange_info = client.get_exchange_info()
    pair_symbols = []
    for i in range(len(exchange_info['symbols'])):
        trade_symbols.append(exchange_info['symbols'][i]['symbol'])

    # trade_symbols.sort()

    return trade_symbols

# Get weighted average for buy/sell price
def get_weighted_average(df):

    df['executedQty'] = df['executedQty'].astype(float)
    df['cummulativeQuoteQty'] = df['cummulativeQuoteQty'].astype(float)
    df_temp = df[['symbol', 'side', 'executedQty', 'cummulativeQuoteQty']].copy()
    df_mean = df_temp.groupby(by=['symbol', 'side']).sum()
    df_mean['priceWAvg'] = df_mean.cummulativeQuoteQty / df_mean.executedQty
    df_temp2 = df_temp.groupby(by=['symbol']).sum()
    df_temp2['overallPriceWAvg'] = df_temp2.cummulativeQuoteQty /df_temp2.executedQty
    df_temp2['overallCost'] = df_temp2.cummulativeQuoteQty

    df_mean = df_mean.reset_index()
    df_mean = df_mean.merge(df_temp2[['overallCost', 'overallPriceWAvg']], how = 'inner', on = 'symbol')

    # display(df_mean)
    df_mean.to_csv('./data_output/indexes.csv')
    
    return df_mean

def get_data():

    client = Client(API_KEY, API_SECRET)
    
    # Get current balances from spot
    df_balances = get_balances(client)

    trading_symbols = get_trading_symbols(df_balances, client)
    print(trading_symbols)

    df = pd.DataFrame()
    for s in range(len(trading_symbols)):
        print(trading_symbols[s])
        df_temp = get_df_all_transactions(trading_symbols[s])
        df = df.append(df_temp, ignore_index=True)
        if s % 10 == 0:
            print(s, 'out of', len(trading_symbols))

    df.dropna()
    # df = df[df.code != -1121]
    df.to_csv('./data_output/trades.csv')
    df_trades = df[['symbol', 'price', 'executedQty', 'cummulativeQuoteQty', 'status', 'type', 'side', 'time']].copy()
    # display(df_trades)

    df_index = get_weighted_average(df)

    return df_trades, df_index
    
def get_df_all_transactions(symbol):

    df = pd.json_normalize(get_all_transactions(symbol))
    if df.empty or len(df) <= 1:
        return df
    df = df.query('status != "CANCELED"')

    df['cummulativeQuoteQty'] = df['cummulativeQuoteQty'].astype(float)
    df['cost'] = np.where(df['side']=='SELL', -1*df['cummulativeQuoteQty'], df['cummulativeQuoteQty'])
    df['cummulativeQuoteQty'] = df['cost']

    display(df.cummulativeQuoteQty.sum())

    return df


# df_trades = pd.read_csv('./data_output/trades.csv')
# df_indexes = pd.read_csv('./data_output/indexes.csv')
df_trades, df_index = get_data()

df_price = get_price_ticket()
df_price = df_price.rename(columns={"price": "current_price"})

df_index = df_index.merge(df_price[['symbol', 'current_price']], how = 'inner', on = 'symbol')
display(df_trades, df_index, df_price)

