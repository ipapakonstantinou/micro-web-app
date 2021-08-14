import ccxt
import os
import sys
import warnings
import numpy

from tensortrade.exchanges.live import CCXTExchange

def warn(*args, **kwargs):
    pass


warnings.warn = warn
warnings.simplefilter(action='ignore', category=FutureWarning)
numpy.seterr(divide='ignore')

sys.path.append(os.path.dirname(os.path.abspath('')))



coinbase = ccxt.coinbasepro()
exchange = CCXTExchange(exchange=coinbase, base_instrument='USD')
print(exchange)