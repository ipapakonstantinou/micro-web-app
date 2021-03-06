import sys
import talib
import numpy as np

np.set_printoptions(threshold=sys.maxsize)

# Get data from CSV
my_data = np.genfromtxt('./exports/201712-202001.csv', delimiter=',')

# Only the close value
close = my_data[:,4]
# print(close)

rsi = talib.RSI(close, timeperiod=14)
print(rsi)


# close = np.random.random(100)
#
# print(close)
#
# ma = talib.SMA(close, timeperiod=10)
# print(ma)
#
#
