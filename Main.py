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

# Import the relevant scripts & config.py
sys.path.append('./.config')
from config import config

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
URI = config.URI

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

    # # Get coins into a list
    # coins_balances = df.asset.tolist()
    #
    # trading_symbols = []
    # for c in range(len(coins_balances)):
    #     if coins_balances[c] != 'BTC' and coins_balances[c] != 'EUR':  
    #         trading_symbols.append(coins_balances[c] + 'BTC')
    #         trading_symbols.append(coins_balances[c] + 'EUR')

    # trading_symbols.append('BTCEUR')


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
    df_temp = df[['symbol', 'side', 'executedQty', 'cummulativeQuoteQty', 'cost']].copy()
    df_mean = df_temp.groupby(by=['symbol', 'side']).sum()
    df_mean['weightedAvg'] = df_mean.cummulativeQuoteQty / df_mean.executedQty
    df_temp2 = df_temp.groupby(by=['symbol']).sum()
    df_temp2['overallWeightedAvg'] = df_temp2.cost /df_temp2.executedQty
    df_temp2['overallCost'] = df_temp2.cost

    df_mean = df_mean.reset_index()
    df_mean = df_mean.merge(df_temp2[['overallCost', 'overallWeightedAvg']], how = 'inner', on = 'symbol')

    display(df_mean)
    df_mean.to_csv('./data_output/indexes.csv')
    
    return df_mean

def get_data():

    client = Client(config.API_KEY, config.API_SECRET)
    
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

    df_index = get_weighted_average(df)

    return df, df_index
    

def get_timestamp_offset():
    url = "{}/api/v3/time".format(URI)

    payload = {}
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(response.text)["serverTime"] - int(time.time() * 1000)

def generate_signature(query_string):
    m = hmac.new(API_SECRET.encode("utf-8"),
                 query_string.encode("utf-8"), hashlib.sha256)
    return m.hexdigest()

def get_all_flexible_savings_balance():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "timestamp={}".format(timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/lending/daily/token/position?{}&signature={}".format(
        URI, query_string, signature)
    print(url)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_flexible_savings_balance(asset):
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "asset={}&timestamp={}".format(asset, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/lending/daily/token/position?{}&signature={}".format(
        URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_locked_savings_balance(asset, project_id):
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "asset={}&projectId={}&status=HOLDING&timestamp={}".format(
        asset, project_id, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/lending/project/position/list?{}&signature={}".format(
        URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
      "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

# def get_fixed_savings_balance(asset):
#     timestamp = int(time.time() * 1000 + get_timestamp_offset())
#     query_string = "asset={}&timestamp={}".format(
#         asset, timestamp)
#     signature = generate_signature(query_string)

#     url = "{}/sapi/v1/lending/project/position/list?{}&signature={}".format(
#         URI, query_string, signature)
#     print(url)

#     payload = {}
#     headers = {
#         "Content-Type": "application/json",
#         "X-MBX-APIKEY": API_KEY
#     }

#     return json.loads(requests.request("GET", url, headers=headers, data=payload).text)


def get_all_transactions(symbol):
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "symbol={}&limit={}&timestamp={}".format(symbol, 1000, timestamp)
    signature = generate_signature(query_string)

    url = "{}/api/v3/allOrders?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_df_all_transactions(symbol):

    df = pd.json_normalize(get_all_transactions(symbol))
    if df.empty or len(df) <= 1:
        return df

    df['cummulativeQuoteQty'] = df['cummulativeQuoteQty'].astype(float)
    df['cost'] = df.cummulativeQuoteQty
    df['cost']= np.where(df['side']=='SELL', -1*df['cost'], df['cost'])
    df = df.query('status == "FILLED"')
    
    display(df.cost.sum())

    return df

def get_deposit_history():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "transactionType={}&beginTime={}&limit={}&timestamp={}".format(0, 1514764800000,1000, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/fiat/orders?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)).data[0])
    
    df['amount'] = df['amount'].astype(float)

    return df

def get_price_ticket():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())

    url = "{}/api/v3/ticker/price?".format(URI)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)))

    return df

# client = Client(config.API_KEY, config.API_SECRET)

# get_all_flexible_savings_balance()
# get_flexible_savings_balance('BUSD')


# # Get current balances from spot
# df_balances = get_balances(client)
# display(df_balances)

df_deposit = get_deposit_history()
display(df_deposit.amount.sum())

df_price = get_price_ticket()

df_trades = pd.read_csv('./data_output/trades.csv')
df_indexes = pd.read_csv('./data_output/indexes.csv')

df_trades = df_trades.merge(df_price, how = 'inner', on = 'symbol')
df_indexes = df_indexes.merge(df_price, how = 'inner', on = 'symbol')

# df_trades = df_trades.price * df_trades.cost


df_indexes.to_csv('./data_output/indexes.csv')
display(df_trades, df_indexes)

display





