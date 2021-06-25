

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import scipy.stats as stats
warnings.filterwarnings("ignore")

# reading cryptocurrency files
btc = pd.read_csv("crypto_data/bitcoin_price.csv")
ether = pd.read_csv("crypto_data/ethereum_price.csv")
ltc = pd.read_csv("crypto_data/litecoin_price.csv")
monero = pd.read_csv("crypto_data/monero_price.csv")
neo = pd.read_csv("crypto_data/neo_price.csv")
quantum = pd.read_csv("crypto_data/qtum_price.csv")
ripple = pd.read_csv("crypto_data/ripple_price.csv")

"""
## 1. Correct Statements
Q1) Combine all the datasets by merging on the date column and create a dataframe with only the closing prices 
for all the currencies. Next, create a pair plot with all these columns and choose the correct statements 
from the given ones:

I)There is a good trend between litecoin and monero, one increases as the other

II)There is a weak trend between bitcoin and neo.

$\color{green} {a) I}$

b) II

c)Both I and II

d) None of the above.
"""

# putting a suffix with column names so that joins are easy
btc.columns = btc.columns.map(lambda x: str(x) + '_btc')
ether.columns = ether.columns.map(lambda x: str(x) + '_et')
ltc.columns = ltc.columns.map(lambda x: str(x) + '_ltc')
monero.columns = monero.columns.map(lambda x: str(x) + '_mon')
neo.columns = neo.columns.map(lambda x: str(x) + '_neo')
quantum.columns = quantum.columns.map(lambda x: str(x) + '_qt')
ripple.columns = ripple.columns.map(lambda x: str(x) + '_rip')

# merging all the files by date
m1 = pd.merge(btc, ether, how="inner", left_on="Date_btc", right_on="Date_et")
m2 = pd.merge(m1, ltc, how="inner", left_on="Date_btc", right_on="Date_ltc")
m3 = pd.merge(m2, monero, how="inner", left_on="Date_btc", right_on="Date_mon")
m4 = pd.merge(m3, neo, how="inner", left_on="Date_btc", right_on="Date_neo")
m5 = pd.merge(m4, quantum, how="inner", left_on="Date_btc", right_on="Date_qt")
crypto = pd.merge(m5, ripple, how="inner", left_on="Date_btc", right_on="Date_rip")

# Subsetting only the closing prices column for plotting
curr = crypto[["Close_btc", "Close_et", 'Close_ltc', "Close_mon", "Close_neo", "Close_qt"]]
curr.head()

sns.pairplot(curr)
"""
As you can see the corelation between Close_ltc and Close_mon is positive and a good trend

And Close_btc and Close_neo also show a strong trend positive line
"""
print(plt.show())

"""
## 2. Heatmap
Q2)As mentioned earlier, Heat Maps are predominantly utilised for analysing Correlation Matrix. 
A high positive correlation (values near 1) means a good positive trend - if one increases, 
then the other also increases. A negative correlation on the other hand(values near -1) indicate good negative trend
 - if one increases, then the other decreases. 
A value near 0 indicates no correlation, as in one variable doesn’t affect the other. 
"""
cor = curr.corr()
round(cor, 3)
sns.heatmap(cor, cmap="Greens", annot=True)

"""
Close_et and Close_qt have high corr (0.79)

Close_neo and Close_btc have a high corr (0.73)

Close_et and Close_ltc have corr of (0.49)

Close_et and Close_neo have a corr of (0.48)
"""
print(plt.show())