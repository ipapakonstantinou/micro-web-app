# TradingBot
  This is a attempt of trading bot for crypto


# Informations
  The base endpoint is: wss://stream.binance.com:9443
  Streams can be accessed either in a single raw stream or in a combined stream
  Raw streams are accessed at /ws/<streamName>

# Examples
  Stream Name: <symbol>@trade
  wscat -c wss://stream.binance.com:9443/ws/btceur@trade
  Stream Name: <symbol>@kline_<interval>
  wscat -c wss://stream.binance.com:9443/ws/btceur@kline_1m

# Requirements
  python-binance
  ta-talib
  numpy
