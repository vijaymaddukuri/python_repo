import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# sales = pd.read_excel("sales.xlsx")
# set two columns as index
sales = pd.read_excel("sales.xlsx", index_col=[1])

# Print sales columns
print(sales["Sales"])

print(sales.Sales)

# Print dtype of column
print(type(sales.Sales))

# ROw indexing
print(sales.loc["Southern Asia"])
print(sales.loc["Southern Asia", "Sales"])

# Row indexing using row num
print(sales.iloc[6, 3])

#Type your code for selecting columns 'month', 'day' , 'temp' , 'area'
df = pd.read_csv('https://query.data.world/s/vBDCsoHCytUSLKkLvq851k2b8JOCkF')
df_2 = df[["month", "day", "temp", "area"]]
# print(df_2.head(20))