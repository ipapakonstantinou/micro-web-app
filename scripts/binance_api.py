# %%
import json
import requests
import hashlib
import hmac
import sys
import time
import pandas as pd
import numpy as np

# Import the relevant scripts & config.py
sys.path.append('../.')
from config.config import *

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

def get_account():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "timestamp={}".format(timestamp)
    signature = generate_signature(query_string)

    url = "{}/api/v3/account?{}&signature={}".format(
        URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)).balances[0])

    return df

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


def get_all_coins_api():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "timestamp={}".format(timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/capital/config/getall?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_exchange_info():
    
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "timestamp={}".format(timestamp)
    signature = generate_signature(query_string)

    url = "{}/api/v3/exchangeInfo".format(URI)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_asset_dividend():
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "startTime={}&endTime={}&limit={}&timestamp={}".format(1615000000000, 1630000000000, 500, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/asset/assetDividend?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)).rows[0])

    return df
    
def get_dust_log():

    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "startTime={}&endTime={}&timestamp={}".format(1600000000000, 1630000000000, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/asset/dribblet?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)).userAssetDribblets[0])

    return df

def get_myTrades(symbol):
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "symbol={}&limit={}&timestamp={}".format(symbol, 1000, timestamp)
    signature = generate_signature(query_string)

    url = "{}/api/v3/myTrades?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_swap_history():

    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "timestamp={}".format(timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/bswap/swap?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_liquidityOps():

    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "limit={}&timestamp={}".format(100, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/bswap/liquidityOps?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    df = pd.DataFrame(pd.json_normalize(json.loads(requests.request("GET", url, headers=headers, data=payload).text)))

    return df

def get_liquidity(poolId):

    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "poolId={}&timestamp={}".format(poolId, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/bswap/liquidity?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

def get_asset_transfer(type):

    '''ENUM of transfer types:
        # MAIN_C2C Spot account transfer to C2C account
        # MAIN_UMFUTURE Spot account transfer to USDⓈ-M Futures account
        # MAIN_CMFUTURE Spot account transfer to COIN-M Futures account
        # MAIN_MARGIN Spot account transfer to Margin（cross）account
        # MAIN_MINING Spot account transfer to Mining account
        # C2C_MAIN C2C account transfer to Spot account
        # C2C_UMFUTURE C2C account transfer to USDⓈ-M Futures account
        # C2C_MINING C2C account transfer to Mining account
        # C2C_MARGIN C2C account transfer to Margin(cross) account
        # UMFUTURE_MAIN USDⓈ-M Futures account transfer to Spot account
        # UMFUTURE_C2C USDⓈ-M Futures account transfer to C2C account
        # UMFUTURE_MARGIN USDⓈ-M Futures account transfer to Margin（cross）account
        # CMFUTURE_MAIN COIN-M Futures account transfer to Spot account
        # CMFUTURE_MARGIN COIN-M Futures account transfer to Margin(cross) account
        # MARGIN_MAIN Margin（cross）account transfer to Spot account
        # MARGIN_UMFUTURE Margin（cross）account transfer to USDⓈ-M Futures
        # MARGIN_CMFUTURE Margin（cross）account transfer to COIN-M Futures
        # MARGIN_MINING Margin（cross）account transfer to Mining account
        # MARGIN_C2C Margin（cross）account transfer to C2C account
        # MINING_MAIN Mining account transfer to Spot account
        # MINING_UMFUTURE Mining account transfer to USDⓈ-M Futures account
        # MINING_C2C Mining account transfer to C2C account
        # MINING_MARGIN Mining account transfer to Margin(cross) account
        # MAIN_PAY Spot account transfer to Pay account
        # PAY_MAIN Pay account transfer to Spot account
        # ISOLATEDMARGIN_MARGIN Isolated margin account transfer to Margin(cross) account
        # MARGIN_ISOLATEDMARGIN Margin(cross) account transfer to Isolated margin account
        # ISOLATEDMARGIN_ISOLATEDMARGIN Isolated margin account transfer to Isolated margin account
    '''
    timestamp = int(time.time() * 1000 + get_timestamp_offset())
    query_string = "type={}&size={}&timestamp={}".format(type, 100, timestamp)
    signature = generate_signature(query_string)

    url = "{}/sapi/v1/asset/transfer?{}&signature={}".format(URI, query_string, signature)

    payload = {}
    headers = {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
    }

    return json.loads(requests.request("GET", url, headers=headers, data=payload).text)

# display(get_asset_transfer('PAY_MAIN'))

# # display(get_liquidityOps())s
# df_asset = get_asset_dividend()
# display(df_asset)
# df_asset.to_csv('./data_output/asset_dividend.csv')

# get_liquidity(93)

# '''
# 18
# 21
# 23
# 24
# 25
# 28
# 50
# 76
# 93
# '''

