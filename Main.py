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
import config

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
URI = config.URI

# Get balances
def get_balances(client):

    # Get the list of all available symbols
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    df_symbols = pd.DataFrame.from_dict(symbols)
    # print('\nsymbols\n', df_symbols)

    # Get all asset where you have value > 0
    account = client.get_account()
    display(df_balances)
    balances = account['balances']
    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]
    # print('\nbalances\n', df_balances)

    # Get the assets that you own with the relevant values in EUR & BTC
    # df_balances, total_usdt, total_eur, total_btc  = calculate_totals(df_balances)
    display(df_balances)

    info = client.get_account_snapshot(type='SPOT')
    # display(info)


    # return df_balances, df_symbols, total_usdt, total_eur, total_btc

def get_data():

    # api_key, api_secret = load_config()
    client = Client(config.API_KEY, config.API_SECRET)
    get_balances(client)

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
    print(url)

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

    df['price'] = df['price'].astype(float)
    df['executedQty'] = df['executedQty'].astype(float)
    df['cost'] = df.price*df.executedQty
    df['cost']= np.where(df['side']=='SELL', -1*df['cost'], df['cost'])
    df = df.query('status == "FILLED"')

    return df

df = get_df_all_transactions('BTCEUR')
display(df.cost.sum())



# get_data()
