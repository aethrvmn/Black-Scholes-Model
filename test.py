import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from BlackScholes import Model

df = pd.read_excel('ZNGA.xlsx', usecols=['Date', 'High (in $)', 'Low (in $)', 'Close/Last', 'Difference of High and Low'])
high = df['High (in $)'].array
low = df['Low (in $)'].array
close = df['Close/Last'].array
date = df.Date.array
volatility = (np.average(high - low, weights = close))
interest2 = np.random.uniform(0.005,0.01, len(close))
exercise_price = [close+(-0.1*close), close+(0.1*close)]
bs = []
for change in exercise_price:
    bs.append(Model(close,change,interest2,60,volatility))

bs[0].call()
print(bs[0].callval)







# interest2 = np.random.uniform(0.005,0.01, len(close))
# bscall = Model(close,close+(.23*close),interest2,60,volatility)
# bscall.call()
# bscall.put()
# plt.figure(1)
# plt.plot(date, close)#-bscall.callval)
# plt.plot(date, bscall.callval)
# plt.plot(date, bscall.putval)
# plt.legend(['Stock Price', ' Call Price', 'Put Price'])
# plt.savefig('call.png')
# plt.show()



# smoothcall = []
# for i in range(1, len(date)):
#     smoothcall.append(bscall.callval[i]- bscall.callval[i-1])
# plt.figure(2)
# plt.plot(date[1:], smoothcall)

# bsput = Model(close,close-(.7*close),interest2,60,volatility)
# bsput.put()
# bsput.call()
# plt.figure(3)
# plt.plot(date, close)
# plt.plot(date, bsput.callval)
# plt.plot(date, bsput.putval)
# plt.legend(['Stock Price', ' Call Price', 'Put Price'])
# plt.savefig('put.png')
# plt.show()