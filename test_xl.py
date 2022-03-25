import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from BlackScholes import Model

df = pd.read_excel('ZNGA.xlsx', usecols=['High (in $)', 'Low (in $)'])
s = df['High (in $)'].array
plt.plot(s)
plt.show()