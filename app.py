# Import modules & libraries
import sys, csv, talib
import numpy as np
import pandas as pd

from flask import Flask, render_template, request, flash, redirect
from binance.client import Client
from binance.enums import *


# Append all the relevant paths
sys.path.append('./.config')
sys.path.append('./scripts')
# Import the relevant scripts & config.py
import config


# Default parameters
title = 'CoinView'
# Create Flask application
app = Flask(__name__)
app.secret_key = b'dsfjfadohufphp357429hinfue297313hrufune'



# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)

@app.route('/')
def index():

    print(request.form)
    # Get balances
    account = client.get_account()
    balances = account['balances']
    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free != 0]

    # Get the list of all available symbols
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

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
