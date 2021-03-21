# python -m virtualenv -p /usr/bin/python3.8 venv
# source venv/bin/activate
# python -m ipykernel install --user --name=venv


import pandas as pd
import numpy as np
import tensortrade.env.default as default

import matplotlib
matplotlib.use('Agg')

from tensortrade.data.cdd import CryptoDataDownload
from tensortrade.feed.core import Stream, DataFeed
from tensortrade.oms.exchanges import Exchange
from tensortrade.oms.services.execution.simulated import execute_order
from tensortrade.oms.instruments import USD, BTC, ETH, EUR
from tensortrade.oms.wallets import Wallet, Portfolio
from tensortrade.agents import DQNAgent
from statsmodels.tsa.stattools import adfuller


cdd = CryptoDataDownload()

data = cdd.fetch("Bitstamp", "USD", "BTC", "1h")


# data = pd.read_csv('./data/klines/5m.csv')
# data.columns =['unix', 'open', 'high', 'low', 'close', 'volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
#
# data['date'] = pd.to_datetime(data["unix"], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
#
# data = data[['date', 'unix', 'open', 'high', 'low', 'close', 'volume']]
# data['unix'] = data['unix'].div(1000).astype('int64')
#
# data['diffed'] = data['close'] - data['close'].shift(1)
# data['logged_and_diffed'] = np.log(data['close']) - np.log(data['close'].shift(1))
# print(data)

# data['logged_and_diffed'] = np.log(data['close']) - np.log(data['close']).shift(1)
# result = adfuller(data['logged_and_diffed'].values[1:], autolag="AIC")
# print('p-value: %f' % result[1])




def rsi(price: Stream[float], period: float) -> Stream[float]:
    r = price.diff()
    upside = r.clamp_min(0).abs()
    downside = r.clamp_max(0).abs()
    rs = upside.ewm(alpha=1 / period).mean() / downside.ewm(alpha=1 / period).mean()
    return 100*(1 - (1 + rs) ** -1)


def macd(price: Stream[float], fast: float, slow: float, signal: float) -> Stream[float]:
    fm = price.ewm(span=fast, adjust=False).mean()
    sm = price.ewm(span=slow, adjust=False).mean()
    md = fm - sm
    signal = md - md.ewm(span=signal, adjust=False).mean()
    return signal


features = []
for c in data.columns[1:]:
    s = Stream.source(list(data[c]), dtype="float").rename(data[c].name)
    features += [s]

cp = Stream.select(features, lambda s: s.name == "close")

features = [
    cp.log().diff().rename("lr"),
    rsi(cp, period=20).rename("rsi"),
    macd(cp, fast=10, slow=50, signal=5).rename("macd")
]

feed = DataFeed(features)
feed.compile()


for i in range(5):
    print(feed.next())

bitstamp = Exchange("bitstamp", service=execute_order)(
    Stream.source(list(data["close"]), dtype="float").rename("USD-BTC")
)

portfolio = Portfolio(USD, [
    Wallet(bitstamp, 10000 * USD),
    Wallet(bitstamp, 1 * BTC)
])


renderer_feed = DataFeed([
    Stream.source(list(data["date"])).rename("date"),
    Stream.source(list(data["open"]), dtype="float").rename("open"),
    Stream.source(list(data["high"]), dtype="float").rename("high"),
    Stream.source(list(data["low"]), dtype="float").rename("low"),
    Stream.source(list(data["close"]), dtype="float").rename("close"),
    Stream.source(list(data["volume"]), dtype="float").rename("volume")
])


env = default.create(
    portfolio=portfolio,
    action_scheme="managed-risk",
    reward_scheme="risk-adjusted",
    feed=feed,
    renderer_feed=renderer_feed,
    renderer=default.renderers.PlotlyTradingChart(),
    window_size=20
)

env.observer.feed.next()


agent = DQNAgent(env)

agent.train(n_steps=200, n_episodes=2, save_path="agents/")


print('Success')
