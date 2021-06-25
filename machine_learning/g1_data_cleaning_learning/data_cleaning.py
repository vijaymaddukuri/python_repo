import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("bank_marketing_updated_v1.csv")

# df = pd.read_csv("bank_marketing_updated_v1.csv", skiprows=2)
df.drop("customerid", axis=1, inplace=True)
df['job'] = df.jobedu.apply(lambda x: x.split(',')[0])
df['eduction'] = df.jobedu.apply(lambda x: x.split(',')[1])
df.drop("jobedu", axis=1, inplace=True)
# df['month'] = df.month.apply(lambda x: x.split(',')[0])

inp1 = df[~df.age.isnull()].copy()

month_mode = inp1.month.mode()[0]
inp1.month.fillna(month_mode, inplace=True)
inp1.month.value_counts(normalize=True)

inp1.loc[inp1.pdays<0, "pdays"] = np.NaN
missing = inp1.response.isna()
miss_sum = missing.sum()

print(miss_sum/len(inp1)*100)

# outlier handling
print(inp1.balance.describe())
# inp1.age.plot()
# sns.boxplot(inp1.age)

plt.figure(figsize=[8,2])
sns.boxplot(inp1.balance)

print(inp1.balance.quantile([0.5, 0.7, 0.9, 0.95, 0.99]))

print(inp1.salary.describe())
sns.boxplot(inp1.salary)

inp1.duration = inp1.duration.apply(lambda x: float(x.split()[0])/60 if x.find("sec")>0 else float(x.split()[0]))
print(inp1.duration.describe())
# print(plt.show())