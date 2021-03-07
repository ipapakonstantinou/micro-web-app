# Import modules & libraries
import sys, csv, talib
import numpy as np
import pandas as pd

from flask import Flask, render_template
from binance.client import Client

# Append all the relevant paths
sys.path.append('./.config')
# Import the relevant scripts & config.py
import config


# Default parameters
title = 'CoinView'


# Create Flask application
app = Flask(__name__)

# Connect to the API
client = Client(config.API_KEY, config.API_SECRET)

@app.route('/')
def index():

    info = client.get_account()
    balances = info['balances']

    df_balances = pd.DataFrame.from_dict(balances)
    df_balances = df_balances[['asset', 'free']].astype({'free': 'float'})
    df_balances = df_balances[df_balances.free > 0]
    print(df_balances)

    return render_template('index.html', title=title, balances=balances, df_balances=df_balances)

@app.route('/buy')
def buy():
    return 'buy'

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'
