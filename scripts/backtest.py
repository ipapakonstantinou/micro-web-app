import backtrader as bt
import pandas as pd

import datetime

class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        if self.rsi > 70 and self.position:
            self.close()



data = bt.feeds.GenericCSVData(dataname='../data/backtest/5m.csv', dtformat=lambda x: datetime.datetime.utcfromtimestamp(float(x) / 1000.0), compression=5, timeframe=bt.TimeFrame.Minutes)


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(RSIStrategy)
cerebro.run()
cerebro.plot()
