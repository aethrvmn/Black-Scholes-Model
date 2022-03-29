import numpy as np
from scipy.stats import norm

class Model:

    def __init__(self, stock_p, ex_p, int_rate, time_to_exp, vol):
        self.stock_p = stock_p
        self.ex_p = ex_p
        self.int_rate = int_rate
        self.time_to_exp = time_to_exp
        self.vol = vol
        self.d1 = (np.log(stock_p/ex_p)+(int_rate+(vol**2/2))*time_to_exp)/(vol*np.sqrt(time_to_exp))
        self.d2 = self.d1 - vol*np.sqrt(time_to_exp)
        self.get()
        self.pay()
        
    def get(self):
        self.getcall = self.stock_p*norm.cdf(self.d1)
        self.getput = self.stock_p*norm.cdf(-self.d1)
        return self

    def pay(self):
        val = self.ex_p*np.exp(-self.int_rate*self.time_to_exp)
        self.paycall = val*norm.cdf(self.d2)
        self.payput = val*norm.cdf(-self.d2)
        return self

    def call(self):
        self.callval = self.getcall - self.paycall
        return self

    def put(self):
        self.putval = self.payput - self.getput