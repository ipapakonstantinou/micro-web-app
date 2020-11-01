import urllib.request
import json
import pandas as pd

api_key = '9CLVUFCFCRRO3HKQ'

from_currency = 'BTC'
to_currency = 'USD'

symbol = 'BTC'
market = 'EUR'

def main():
    
    url_now = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + from_currency + '&to_currency=' + to_currency + '&apikey=' + api_key
    print(url_now)
    data_now = json.loads(urllib.request.urlopen(url_now).read())
    df_now = pd.DataFrame(data_now)
    display(df_now)
    
    url_daily = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=' + symbol + '&market=' + market + '&apikey=' + api_key
    print(url_daily)
    data_daily = json.loads(urllib.request.urlopen(url_daily).read())
    
    map = [
        {'1a. open (EUR)':''},
        {'1b. open (USD)':''},
        {'2a. high (EUR)':''},
        {'2b. high (USD)':''},
        {'3a. low (EUR)':''},
        {'3b. low (USD)':''},
        {'4a. close (EUR)':''},
        {'4b. close (USD)':''},
        {'5. volume':''},
        {'6. market cap (USD)':''},
    ]
    
#     print(data_daily['Time Series (Digital Currency Daily)']['2020-11-01'])
    
    for date in data_daily['Time Series (Digital Currency Daily)']:
        print(date)
        print(data_daily['Time Series (Digital Currency Daily)'][date])

#     for value in 
#         for d in data_daily:
#             print(dates)
#             print(date['1a. open (EUR)'], date['1b. open (USD)'], date['2a. high (EUR)'], date['2b. high (USD)'], date['3a. low (EUR)'], date['3b. low (USD)'], date['4a. close (EUR)'], date['4b. close (USD)'], date['5. volume'], date['6. market cap (USD)'])
            
    df_daily = pd.DataFrame(data_daily)
    display(df_daily)
    
main()




















# import urllib.request
# import ssl
# import json
# import time
# import tweepy
# import pandas


# ssl._create_default_https_context = ssl._create_unverified_context


 
# api_key = "faeb15f2-0c7f-41ad-b146-623bf7871dbf"

# # Allows adding as many coins as desired
# coin_list = [
#      "BTC"
# ]
# coins = ','.join(coin_list)


# map = [
#     {"name":""},
#     {"symbol": ""},
#     {"price": " Price: "},
#     {"percent_change_24h": " - 24 Hour Percent Change: "},
#     {"market_cap": " Market Cap: "},
#     {"volume_24h": " 24 Hour Volume: "},
#     {"url_shares": " URL Shares: "},
#     {"reddit_posts": " Reddit Posts: "},
#     {"tweets": " Tweets: "},
#     {"galaxy_score": " Galaxy Score: "},
#     {"volatility": " Volatility: "},
#     {"social_volume": " Social Volume: "},
#     {"news": " News: "},
#     {"close": " Close: "},
#     {'time': ' Time:'},
# ]

# fields = [list(key.keys())[0] for key in map]
# coins_df = pandas.DataFrame(columns=fields)

# def final_render(asset_coin, value, key, asset):
#     if key == 'symbol':
#         asset_coin += " (" + asset[key] + ")"
#     elif key == 'percent_change_24h':
#         asset_coin += value + str(asset[key]) + "%"
#     else:
#         asset_coin += value + str(asset[key])
#     return asset_coin


# # Iterates over each of the fields from Lunar Crush, gets the value from Lunar Crush and renders it with the field name
# def main():

#     url = "https://api.lunarcrush.com/v2?data=assets&key=" + api_key + "&symbol=" + coins
#     print(url)
#     assets = json.loads(urllib.request.urlopen(url).read())
# 
#     for asset in assets['data']:
#         asset_coin = ""
#         for field in map:
#             key = list(field.keys())[0]
#             value = list(field.values())[0]
#             asset_coin = final_render(asset_coin, value, key, asset)
#         print(asset_coin)
#         print(len(asset_coin))
#         
#         return assets
#         
# def create_coins_df(assets):
#     global coins_df
#     
#     for n in range(len(coin_list)):
#         data = assets['data'][n]
#         required_data = [{key: data[key] for key in fields}]
#         
#         coins_df = coins_df.append(required_data, ignore_index = True)
#         
#         coins_df['time'] = pandas.to_datetime(coins_df['time'], unit='s')
#         
#     return coins_df
# 
# create_coins_df(main())

