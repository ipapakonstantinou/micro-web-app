# ToDo

  Save your portofolio locally
  get_all_tickers
  display amount in the relevant symbol (EUR, BTC, USD)
  Display portofolio
  Get all trades
  display them in /transactions


# TradingBot
  This is a attempt of trading bot for crypto


# Informations
  The base endpoint is: wss://stream.binance.com:9443
  Streams can be accessed either in a single raw stream or in a combined stream
  Raw streams are accessed at /ws/<streamName>

# KLINE_INTERVAL
  [
    [
        1499040000000,      # Open time
        "0.01634790",       # Open
        "0.80000000",       # High
        "0.01575800",       # Low
        "0.01577100",       # Close
        "148976.11427815",  # Volume
        1499644799999,      # Close time
        "2434.19055334",    # Quote asset volume
        308,                # Number of trades
        "1756.87402397",    # Taker buy base asset volume
        "28.46694368",      # Taker buy quote asset volume
        "17928899.62484339" # Can be ignored
    ]
]

# Examples
  Stream Name: <symbol>@trade
  wscat -c wss://stream.binance.com:9443/ws/btceur@trade
  Stream Name: <symbol>@kline_<interval>
  wscat -c wss://stream.binance.com:9443/ws/btceur@kline_1m

# Requirements
python-binance
ta-talib
numpy
flask
