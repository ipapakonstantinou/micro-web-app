# %%

#TODO
'''
    Define universal structures
    Create new project or fix this one
        Find a name
    Make scripts as generic as possible
    Find out if there is a liquidation history
    Use api myTrades to work as well as it does for the orders
    Include in the balances the fees
    Include in the balances the asset dividend
    Use get_swap in combination with the myTrades
    Found out which API calls have limits and adjust the output
    Find BTCEUR for each time in order to calcualte the cost in EUR when the pair is e.g. DOTBTC
'''

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
def get_balances():

    # Get all asset where you have value > 0
    df_balances = get_account()    
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]

    df_balances['asset'] = df_balances['asset'].apply( lambda x: x[2:] if x[0:2] == "LD" else x)
    df_balances = df_balances.groupby(by=['asset']).sum().reset_index()

    return df_balances

def get_trading_symbols():

    if L_SYMBOLS != '':
        trading_symbols = L_SYMBOLS
    else:
        print('No symbols found in config file')
        sys.exit()

    df_exchage_info = pd.DataFrame.from_dict(get_exchange_info()['symbols'])

    return trading_symbols, df_exchage_info

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

def get_df_all_transactions(symbol):

    df = pd.json_normalize(get_all_transactions(symbol))
    if df.empty:
        return df
    df = df.query('status != "CANCELED"')

    df['cummulativeQuoteQty'] = df['cummulativeQuoteQty'].astype(float)
    df['cost'] = np.where(df['side']=='SELL', -1*df['cummulativeQuoteQty'], df['cummulativeQuoteQty'])
    df['cummulativeQuoteQty'] = df['cost']

    df['executedQty'] = df['executedQty'].astype(float)
    df['cost_qty'] = np.where(df['side']=='SELL', -1*df['executedQty'], df['executedQty'])
    df['executedQty'] = df['cost_qty']

    display(df.cummulativeQuoteQty.sum())

    return df

def get_df_all_trades(symbol):
    
    df = pd.json_normalize(get_myTrades(symbol))
    df = pd.json_normalize(get_myTrades('SXPBNB'))
    # df.to_csv('./data_output/SXPBTC.csv')
    display(df)
    sys.exit()


    if df.empty:
        return df

    df = df.query('status != "CANCELED"')

    df['cummulativeQuoteQty'] = df['cummulativeQuoteQty'].astype(float)
    df['cost'] = np.where(df['side']=='SELL', -1*df['cummulativeQuoteQty'], df['cummulativeQuoteQty'])
    df['cummulativeQuoteQty'] = df['cost']

    df['executedQty'] = df['executedQty'].astype(float)
    df['cost_qty'] = np.where(df['side']=='SELL', -1*df['executedQty'], df['executedQty'])
    df['executedQty'] = df['cost_qty']

    display(df.cummulativeQuoteQty.sum())

    return df

def get_data():

    trading_symbols, df_exchage_info = get_trading_symbols()

    df = pd.DataFrame()
    for s in range(len(trading_symbols)):
        print(trading_symbols[s])
        df_temp = get_df_all_transactions(trading_symbols[s])
        # df_temp = get_df_all_trades(trading_symbols[s])
        df = df.append(df_temp, ignore_index=True)
        if s % 10 == 0:
            print(s, 'out of', len(trading_symbols))

    df.dropna()
    # df = df[df.code != -1121]
    df.to_csv('./data_output/trades.csv')
    df_trades = df[['symbol', 'price', 'executedQty', 'cummulativeQuoteQty', 'status', 'type', 'side', 'time']].copy()
    # display(df_trades)

    df_index = get_weighted_average(df)

    return df_trades, df_index, df_exchage_info
    

def get_all_coins():

    coins = []
    api_coins = get_all_coins_api()
    for i in range(len(api_coins)):
        coins.append(api_coins[i]['coin'])

    return coins

def get_balance_coins(df_indexes, df_exchange_info):

    print('Get balance based on the trading symbols')

    # df_indexes.drop(df_indexes.iloc[:, 0:1], inplace = True, axis = 1)

    df_indexes = df_indexes.merge(df_exchange_info[['symbol', 'baseAsset', 'quoteAsset']], how = 'inner', on = 'symbol')

    df_temp1 = pd.DataFrame(columns=['coin', 'quantity'])
    df_temp = df_indexes[['executedQty', 'cummulativeQuoteQty', 'baseAsset', 'quoteAsset']]
    # df_temp['executedQty'] = df_temp[['executedQty']].abs()
    df_temp['cummulativeQuoteQty'] = df_temp[['cummulativeQuoteQty']]*-1

    df_temp1 = df_temp.copy()
    df_temp2 = df_temp.copy()
    df_temp1 = df_temp1.groupby(['baseAsset'])['executedQty'].sum().reset_index()
    df_temp2 = df_temp2.groupby(['quoteAsset'])['cummulativeQuoteQty'].sum().reset_index()

    df_temp1 = df_temp1.rename(columns={"baseAsset": "coin", "executedQty": "quantity"})
    df_temp2 = df_temp2.rename(columns={"quoteAsset": "coin", "cummulativeQuoteQty": "quantity"})

    df_balance = df_temp1.append(df_temp2)
    df_balance = df_balance.groupby(['coin']).sum().reset_index()

    return df_balance

# df_balances = get_balances()
# display(df_balances)

# df_dividend = get_asset_dividend()
# display(df_dividend.query('asset == "SXP"'))

# df_dust_log = pd.DataFrame(get_dust_log().userAssetDribbletDetails)
# display(df_dust_log)

# df_trades = pd.read_csv('./data_output/trades.csv')
# df_indexes = pd.read_csv('./data_output/indexes.csv')
# display(get_flexible_savings_balance('BNB'))

# df_bswap_records = get_liquidityOps()
# df_bswap_records.to_csv('./data_output/bswap_records.csv')
df_trades, df_indexes, df_exchange_info = get_data()

df_price = get_price_ticket()
df_price = df_price.rename(columns={"price": "current_price"})
df_price['current_price'] = df_price[['current_price']].astype({'current_price': 'float'})

df_indexes = df_indexes.merge(df_price[['symbol', 'current_price']], how = 'inner', on = 'symbol')
df_indexes['current_value'] = df_indexes['executedQty']*df_indexes['current_price']

df_current_value = df_indexes.groupby(by=['symbol']).sum()
df_current_value = df_current_value.reset_index()
df_current_value = df_current_value[['symbol', 'executedQty', 'current_price', 'current_value']]
display('All trades:', df_trades)
display('Indexes: ', df_indexes)
display('Current value', df_current_value)


# Get balance based on the trading symbols
df_balance = get_balance_coins(df_indexes, df_exchange_info)
df_balance.to_csv('./data_output/balance.csv')
display('Current balances:', df_balance)

