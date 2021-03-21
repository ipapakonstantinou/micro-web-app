import backtrader as bt
import pandas as pd
import datetime

# RSI & Loss-Stop
class BaseStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

class AutoStopOrStopTrail(BaseStrategy):
    params = dict(
        stop_loss=0.01,  # price is 2% less than the entry point
        trail=False,
        buy_limit=False,
    )

    buy_order = None  # default value for a potential buy_order
    print()

    def notify_order(self, order):
        if order.status == order.Cancelled:
            print('\n', self.data.datetime.date(0),
                  " ", self.data.datetime.time())
            print('CANCEL@price: {:.2f} {}'.format(
                order.executed.price, 'buy' if order.isbuy() else 'sell'))
            return

        if not order.status == order.Completed:
            return  # discard any other notification

        if not self.position:  # we left the market
            print('\n', self.data.datetime.date(0),
                  " ", self.data.datetime.time())
            print('SELL@price: {:.2f}'.format(order.executed.price))
            return

        # We have entered the market
        print('\n', self.data.datetime.date(0), " ", self.data.datetime.time())
        print('BUY @price: {:.2f}'.format(self.data.close[0]))

    def next(self):
        if not self.position and self.rsi < 30:
            if self.buy_order:  # something was pending
                self.cancel(self.buy_order)

            # not in the market and signal triggered
            percentage = 0.8
            cash = self.broker.get_cash()
            # stop_price = round(self.data.close[0]*0.95, 2)
            qty = (percentage*cash)/self.data.close[0]
            if not self.p.buy_limit:
                # print('BUY HERE @price: {:.2f}'.format(self.data.close[0]))
                self.buy_order = self.buy(transmit=False, size=qty)
            else:

                price = self.data.close[0] * (1.0 - self.p.buy_limit)

                # transmit = False ... await child order before transmission
                self.buy_order = self.buy(price=price, exectype=bt.Order.Limit,
                                          transmit=False, size=qty)

            # Setting parent=buy_order ... sends both together
            if not self.p.trail:
                stop_price = self.data.close[0] * (1.0 - self.p.stop_loss)
                self.sell(exectype=bt.Order.Stop, price=stop_price,
                          parent=self.buy_order,
                          size=qty)
            else:
                self.sell(exectype=bt.Order.StopTrail,
                          trailamount=self.p.trail,
                          parent=self.buy_order,
                          size=qty)
        if self.position and self.rsi > 70 and self.buy_order:
            # print('Close order')
            self.close()
            # self.cancel(self.buy_order)


# Only RSI
class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):        
        
        if not self.position:
            if self.rsi < 30:
                percentage = 0.8
                cash = self.broker.get_cash()
                # self.buy(size=.025)
                stop_price = round(self.data.close[0]*0.95, 2)
                qty = (percentage*cash)/self.data.close[0]
                print('\n', self.data.datetime.date(0),
                      " ", self.data.datetime.time())
                print('BUY @price: {:.2f}'.format(self.data.close[0]))
                self.buy(size=qty)

        else:
            if self.rsi > 70:
                print('\n',  self.data.datetime.date(0),
                      " ", self.data.datetime.time())
                print('SELL@price: {:.2f}'.format(self.data.close[0]))
                self.close()


# # Specify period 
# fromdate = datetime.datetime.strptime('2019-05-01', '%Y-%m-%d')
# todate = datetime.datetime.strptime('2021-04-08', '%Y-%m-%d')
# data = bt.feeds.GenericCSVData(dataname='./data/backtest/5m.csv', dtformat=lambda x: datetime.datetime.utcfromtimestamp(float(x) / 1000.0), compression=5, timeframe=bt.TimeFrame.Minutes, fromdate = fromdate, todate = todate)

# All available period
data = bt.feeds.GenericCSVData(dataname='./data/backtest/5m.csv', dtformat=lambda x: datetime.datetime.utcfromtimestamp(float(x) / 1000.0), compression=5, timeframe=bt.TimeFrame.Minutes)

# Initialize backtrader
cerebro = bt.Cerebro()

# Add parameters
cerebro.broker.set_cash(1000)
cerebro.adddata(data)
# cerebro.addstrategy(AutoStopOrStopTrail)
cerebro.addstrategy(RSIStrategy)

# Run cerebro
print('\n', 'Starting Portofolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('\n', 'Final Portofolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()

