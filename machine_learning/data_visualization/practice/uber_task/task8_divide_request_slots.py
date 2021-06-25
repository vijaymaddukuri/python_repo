"""
Now that you’ve observed that the number of requests across all the days is similar,
you need to check it across the pick-up points as well.
Analyse the distribution of requests across each of the pick-up points exclusively and choose the correct option:

"""

#Import the libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np

#Write code to load the dataset here
df = pd.read_csv("Uber+Request+Data.csv")

# Use the pd.to_datetime() function to convert the given time stamps to a date-time object.

df['Request timestamp']=pd.to_datetime(df['Request timestamp'])
df['Drop timestamp']=pd.to_datetime(df['Drop timestamp'])

# After that use dt.hour to extract the hour and store it in a new column of the same dataframe df.
# Then do a value_counts() and you’ll find that at 18:00-19:00 hours the maximum number of requests were made (510).

df['Request hour']=df['Request timestamp'].apply(lambda x: x.hour)


print(df['Request hour'][df['Pickup point']=='Airport'].value_counts().sort_index())

print(df['Request hour'][df['Pickup point']=='City'].value_counts().sort_index())

#best way to do this is to plot the histograms for all dates
#we first get the unique dates
df['Request date']=df['Request timestamp'].apply(lambda x: x.date())
unique_dates=df['Request date'].unique()

# For 'City' as the pickup point

for i in unique_dates:
    sns.distplot(df[(df["Request date"]==i) & (df['Pickup point']=='City')]['Request hour'], bins=24)
    plt.title(str(i))
    plt.show()

# and for 'Airport' as the pickup point

for i in unique_dates:
    sns.distplot(df[(df["Request date"]==i) & (df['Pickup point']=='Airport')]['Request hour'], bins=24)
    plt.title(str(i))
    plt.show()




