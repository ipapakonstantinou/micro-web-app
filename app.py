# Import modules & libraries
import sys, csv, talib
import numpy as np
import pandas as pd

from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_cors import CORS, cross_origin
from binance.client import Client
from binance.enums import *


# Append all the relevant paths
sys.path.append('./.config')
sys.path.append('./scripts')
# Import the relevant scripts & config.py
import config
from get_data import get_balances


# Default parameters
title = 'CoinView'
# Create Flask application
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = b'dsfjfadohufphp357429hinfue297313hrufune'



# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)

@app.route('/')
def index():

    df_balances, symbols = get_balances()

    return render_template('index.html', title = title, df_balances = df_balances, symbols = symbols)

@app.route('/buy', methods=['POST'])
def buy():

    print(request.form)

    # try:
    #     order = client.create_order(
    #     symbol=request.form['symbol'],
    #     side=SIDE_BUY,
    #     type=ORDER_TYPE_MARKET,
    #     quantity=request.form['quantity'])
    # except Exception as e:
    #     flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/history')
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jul, 2020", "12 Jul, 2020")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0]/1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)
