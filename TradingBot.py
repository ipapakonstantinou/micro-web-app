import urllib.request
import json
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='./.config/.env')


def load_config():
  # If there is no env file ask for input
  if not os.path.isfile('./.config/.env'):
    api_key = input(str("Enter API Key: "))
    from_currency = input(str("Enter from currency: "))
    to_currency = input(str("Enter to currency: "))
    symbol = input(str("Enter symbol: "))
    market = input(str("Enter market: "))
  else:
    api_key = str(os.getenv('API_KEY'))
    from_currency = str(os.getenv('FROM_CURRENCY'))
    to_currency = str(os.getenv('TO_CURRENCY'))
    symbol = str(os.getenv('SYMBOL'))
    market = str(os.getenv('MARKET'))

  # Define Urls
  url_now = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + from_currency + '&to_currency=' + to_currency + '&apikey=' + api_key
  url_daily = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=' + symbol + '&market=' + market + '&apikey=' + api_key

  return url_now, url_daily

def main():

  # Load configurations
  url_now, url_daily = load_config()

  # Request, Build and Display the Now Rate
  data_now = json.loads(urllib.request.urlopen(url_now).read())
  df_now = pd.DataFrame(data_now)
  print(url_now)
  display(df_now)

  # Build Daily Rates
  data_daily = json.loads(urllib.request.urlopen(url_daily).read())
  map = {'Date', '1a. open (EUR)', '1b. open (USD)', '2a. high (EUR)', '2b. high (USD)', '3a. low (EUR)', '3b. low (USD)', '4a. close (EUR)', '4b. close (USD)', '5. volume', '6. market cap (USD)'}
  dict_daily = {}
  df_daily = pd.DataFrame(columns=map)
  value = []

  for m in map:
    print(m)
    for date in data_daily['Time Series (Digital Currency Daily)']:
      if m == 'Date':
        value.append(date)
      else:
        value.append(data_daily['Time Series (Digital Currency Daily)'][date][m])
    dict_daily[m] = value
    value = []

  df_daily = pd.DataFrame(dict_daily)
  print(url_daily)
  display(df_daily)

main()
