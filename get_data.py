import sys
import csv
import numpy as np
import talib
from binance.client import Client

# Import the relevant scripts & config.py
sys.path.append('./.config')
import config


# Write CSV file
def tocsv(csv_name, table):

    csv_name = './exports/' + csv_name
    csvfile = open(csv_name, 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')

    # Loop & write rows into csv
    for line in table:
        writer.writerow(line)
        print(line)
    csvfile.close()

# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)

# prices = client.get_all_tickers()
# for price in prices:
#     print(prices)


# # Get candlesticks with max length 500
# candles = client.get_klines(symbol='BTCEUR', interval=Client.KLINE_INTERVAL_15MINUTE)
# tocsv('15min.csv', candles)

# Get historical data & write them to csv
candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Dec, 2016", "31 Jan, 2021")
tocsv('201612-202101.csv', candlesticks)
