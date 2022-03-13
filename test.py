import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from BlackScholes import Model

bs = Model(1, 1, 1, 1, 1)

def motion(t, x=0, y=1):
    mu, sigma = x*t, y*t, 
    val = np.random.normal(mu, sigma)
    return(val)

time = np.linspace(0,1,2000)
pathx = np.zeros(len(time))

for i in np.arange(1, len(time)):
    pathx[i] = pathx[i-1]+motion(time[i])

plt.plot(time,pathx)
plt.xlabel('time($s$)')
plt.ylabel('space(=$\mathbb{R}$)')
plt.savefig('1dbrown.png')
plt.show()