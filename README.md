::: {#f8e4ad19-2b8c-45dc-93c6-54ed9c79b51e .cell .markdown}
# Black Scholes Model

**Amandeep Singh, Vasilis Valatsos**

We attempt to make a program that predicts optional premiums, using the
Black-Scholes model, introduced in 1973.
:::

::: {#586ad980-a552-4a6e-841d-7d377e625755 .cell .markdown}
To start off, we first install all the required modules, (We have the
cell commented, but in the case that one or more modules aren\'t
installed, uncomment and run once the cell below.)
:::

::: {#e9fc4108-d0d4-4031-b3cb-b18be00481e7 .cell .code execution_count="1"}
``` python
# pip install -r "requirements.txt"
```
:::

::: {#ba04e53c-37c2-4b42-8609-4a3acfafa829 .cell .markdown}
where the module scipy.stats is not imported here but is needed in the
class that we import.
:::

::: {#388fb95b-ac66-407f-af52-ac3c5135fcdd .cell .code execution_count="2"}
``` python
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from BlackScholes import Model
```
:::

::: {#554a24ff-738d-4ffc-b887-e455e82b0e46 .cell .markdown}
### Section 1

#### Testing
:::

::: {#fca01f35-0d73-49bf-ac74-1d482635dac4 .cell .markdown}
To check whether the class functions work, as well as to explain the
process, we can create a Brownian motion to simulate a possilbe stock
price over four years (1460 days) and calculate all the needed
variables.
:::

::: {#b8e110e6-11c4-4526-b4f8-d75c6e5313d8 .cell .code execution_count="3"}
``` python
def brownian(time_range, mean=0, sd=1):
    time = np.linspace(0,1,time_range)
    path = np.zeros(time_range)
    for i in np.arange(1, time_range):
        path[i] = path[i-1]+np.random.normal(mean*time[i], sd*time[i])
    
    volatility = max(path)-min(path)
    return time, path#, volatility
```
:::

::: {#4e917c6f-cc1a-4179-8dd8-c29d464b3f86 .cell .markdown}
where time has a range from 0 to 1, because we can always scale the
dates of the hypothetical stock to fit those values with an appropriate
transformation. Below we see the graph of the motion
:::

::: {#e9910094-e4ad-446f-9ff1-1c778ba093db .cell .code execution_count="4"}
``` python
time_range = 1460 #in days
walk = brownian(time_range)
time = walk[0]
stock_price = walk[1] - min(walk[1]) +1
plt.plot(time, stock_price)
```

::: {.output .execute_result execution_count="4"}
    [<matplotlib.lines.Line2D at 0x7ff3d3526790>]
:::

::: {.output .display_data}
![](6cf5f79a9e5742e5e6fa0a24c946d322f504ef45.png)
:::
:::

::: {#c003b8a6-8d54-4186-8bfd-8ce96a16a8bd .cell .markdown}
Next, we define the exercise price, where here we choose a \"smooth\"
deviation from the original stock price, essentially taking a stable
function and adding noise, defined by a uniform distribution over an
arbitrary, probably non-realistic range. Likewise, the interest rate
should float between 0% and 1%, and finally the range of the time to
expiration was made 1, 2, 3, 4, and 5 months.
:::

::: {#52c47d77-89b1-4f9a-a53b-5e83ffbbfe8d .cell .code execution_count="5"}
``` python
variance=np.random.uniform(0.005, 0.01)
exercise_price = stock_price + 0.1*stock_price
interest = np.random.uniform(0.005,0.01, time_range)
expiration_date = 30 #days
volatility = 0.23
```
:::

::: {#fbaa62b8-186f-40b0-985a-d22efd5efc24 .cell .markdown}
Finally, we can initialize the Model class, using the above as inputs
and executing the call and put functions.
:::

::: {#2ad6bf1b-6a7c-45be-91a0-532f60d10f6f .cell .code execution_count="6"}
``` python
option = Model(stock_price, exercise_price, interest, expiration_date, volatility)
option.call()
option.put()
```
:::

::: {#fd8d00d2-8d69-436d-8d66-9d0c9a722e55 .cell .code execution_count="7"}
``` python
plt.plot(stock_price)
plt.plot(option.callval)
plt.plot(option.putval)
plt.legend(['Stock Price', ' Call Price', 'Put Price'])
plt.savefig('example.png')
plt.show()
```

::: {.output .display_data}
![](b33542957ffece5f4c031725c41acc3ec7a38337.png)
:::
:::

::: {#aa9a7b55-f1e7-48d7-8285-7de9eb66ba75 .cell .markdown}
Since we see that the behaviour is as expected and since we want to
reuse the names of variables, we clear everything and move to Section 2.
(We could just skip this step since the variables would simply get
replaced, but it is easier during working to just clear everything.
There were many instances where we unknowingly used variables that we
didn\'t replace and were puzzled at the plots no changing etc.)
:::

::: {#be65391b-cb16-4b2d-a5c7-106caf324d09 .cell .code execution_count="8"}
``` python
del option, stock_price, exercise_price, interest, variance, volatility, walk, time_range, time, expiration_date
```
:::

::: {#e8ce8a83-677e-43bf-9a7f-c0a5033157de .cell .markdown}
### Section 2

#### Application using real-world data
:::

::: {#d4162bb6-23c0-4656-a6d2-352dd6e459b0 .cell .markdown}
Having checked that the idea works, we begin by opening the .xlsx file
we wish to use and defining our parameters before initializing our
class.
:::

::: {#6bb7b7e5-079a-43c0-9a8a-8185b798cc26 .cell .code execution_count="9"}
``` python
df = pd.read_excel('ZNGA.xlsx', usecols=['Date', 'High (in $)', 'Low (in $)', 'Close/Last', 'Difference of High and Low'])
high = df['High (in $)'].array
low = df['Low (in $)'].array
close = df['Close/Last'].array
date = df.Date.array
interest = np.random.uniform(0.005,0.01, len(close))
volatility = (np.average(high - low, weights = close))
expiration_date = 60
```
:::

::: {#63102d97-0d1e-43f5-8b1c-fdf7adf341c7 .cell .markdown}
Because we want to check what happens for an exercise price both higher
and lower than the original stock price (say ±10%), we create a vector
containing those two values and we initialize both instances with a
simple forloop
:::

::: {#36dbffea-6757-4eda-b205-0b3a75710add .cell .code execution_count="10"}
``` python
exercise_price = [close-(0.1*close), close+(0.1*close)]
option = []
for change in exercise_price:
    option.append(Model(close, change, interest, expiration_date, volatility))
```
:::

::: {#755a4a86-330e-4ebf-961e-6ff75bd71135 .cell .markdown}
Now we call the call() and put() functions for each of the instances to
generate the data, which we have plotted below.
:::

::: {#0e2d2d65-faee-4be9-bfde-359b9f16dc62 .cell .code execution_count="11"}
``` python
for model in option:
    model.call()
    model.put()
    
    plt.plot(date, close)
    plt.plot(date, model.callval)
    plt.plot(date, model.putval)
    plt.legend(['Stock Price', ' Call Price', 'Put Price'])
    plt.xlabel('time')
    plt.ylabel('price')
    
    if model.ex_p[0] < model.stock_p[0]:
        plt.title('Behaviour with a lower exercise price than stock price')
        plt.savefig('lower.png')
    else:
        plt.title('Behaviour with higher exercise price than stock price')
        plt.savefig('higher.png')
    
    plt.show()
```

::: {.output .display_data}
![](4db846c0b1e6710a884c1d80510fd1ea6814e09b.png)
:::

::: {.output .display_data}
![](8c046cf079676aeb4b66be5a151105df8a909a5f.png)
:::
:::

::: {#f9fafcd8-1110-4708-8370-eeaa7e88916d .cell .markdown}
Finally, we use pandas to export all of the information we have gathered
and created into an excel file. The model genrates the data frame of
values of change in option prices which can be converted into an xlsx
file which can then be passed onto/be communicated to a non python user
for further interpretation and decision making.
:::

::: {#1ac62b5d-2c74-428a-857b-5bf69e58dab7 .cell .code execution_count="12"}
``` python
data = []
for i in np.arange(len(exercise_price)):
        dict = {'Date': date,
        'Stock Price': option[i].stock_p,
        'Exercise Price': option[i].ex_p,
        'Interest': option[i].int_rate,
        'Time to Expiration': option[i].time_to_exp,
        'Volatility': option[i].vol,
        'Call Price': option[i].callval,
        'Put Price': option[i].putval}
        data.append(pd.DataFrame(dict, index = None))
        
with pd.ExcelWriter('assignment.xlsx') as writer:  
    data[0].to_excel(writer, sheet_name='Sheet 1', header = True, index = False)
    data[1].to_excel(writer, sheet_name='Sheet 2', header = True, index = False)
```
:::
