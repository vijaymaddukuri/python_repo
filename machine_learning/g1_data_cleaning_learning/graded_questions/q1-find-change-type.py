#Import the required Libraries.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Read the data in pandas
inp0= pd.read_csv("Attribute+DataSet.csv")
inp1= pd.read_csv("Dress+Sales.csv")


"""
Q1:

You have “Attribute DataSet” which contains a column named “Price”. Choose the correct statement from the following about its data type and variable type.

Integer type and numerical variable
Object type and categorical ordinal variable
Object type and categorical nominal variable
Float type and categorical variable.
Ans: Object type and categorical ordinal variable
"""
print(inp0.info())

"""
Fixing the Rows and Columns
As you can see, there is a column in “Attribute Dataset” named as ‘Size’. 
This column contains the values in abbreviation format. Write a code in Python to convert the followings:

M into “Medium”
L into “Large”
XL into “Extra large”
free into “Free”
S, s & small into “Small”.
Now once you are done with changes in the dataset, what is the value of the lowest percentage, 
the highest percentage and the percentage of Small size categories in the column named “Size”?
Ans:
2.9%, 35.7%, 7.5%
"""

# Column fixing, correcting size abbreviation. count the percentage of each size category in "Size" column.
print(pd.unique(inp0['Size']))

inp0['Size'].replace(['XL','L','M','S','s','small','free'], ['Extra Large','Large','Medium','Small','Small','Small','Free'], inplace=True)

print(pd.unique(inp0['Size']))

# Print the value counts of each category in "Size" column.
# What is the value of the lowest percentage, the highest percentage and the percentage of Small size categories in the column named “Size”?

print(inp0['Size'].value_counts(normalize=True)*100)


"""
You are given another dataset named “Dress Sales”. Now if you observe the datatypes of the columns using ‘inp1.info()’ 
command, you can identify that there are certain columns defined as object data type though they primarily consist of 
numeric data.

Now if you try and convert these object data type columns into numeric data type(float), you will come across an error 
message. Try to correct this error.

Because there is a string value in each of these columns, an error occurs. You cannot convert a string into float type, 
and once you replace a string with a null value, you will be able to convert it into float type.
"""

# Print the data types information of inp1 i.e. "Dress Sales" data.
print(inp1.info())

# Try to convert the object type into float type of data. YOU GET ERROR MESSAGE.
# inp1['09-12-2013'] = pd.to_numeric(inp1['09-12-2013'])

inp1.loc[inp1['09-12-2013']== 'Removed',"09-12-2013"] = np.NaN

inp1.loc[inp1['14-09-2013']== 'removed',"14-09-2013"] = np.NaN

inp1.loc[inp1['16-09-2013']== 'removed',"16-09-2013"] = np.NaN

inp1.loc[inp1['18-09-2013']== 'removed',"18-09-2013"] = np.NaN

inp1.loc[inp1['20-09-2013']== 'removed',"20-09-2013"] = np.NaN

inp1.loc[inp1['22-09-2013']== 'Orders',"22-09-2013"] = np.NaN


# Convert the object type columns in "Dress Sales" into float type of data type.
inp1['09-12-2013'] = pd.to_numeric(inp1['09-12-2013'], downcast='float')
inp1['14-09-2013'] = pd.to_numeric(inp1['14-09-2013'], downcast='float')
inp1['16-09-2013'] = pd.to_numeric(inp1['16-09-2013'], downcast='float')
inp1['18-09-2013'] = pd.to_numeric(inp1['18-09-2013'], downcast='float')
inp1['20-09-2013'] = pd.to_numeric(inp1['20-09-2013'], downcast='float')
inp1['22-09-2013'] = pd.to_numeric(inp1['22-09-2013'], downcast='float')

print(inp1.info())

"""
Handling Missing Values
When you observe the null counts in the 'Dress Sales Dataset' after performing all the operations that have 
been mentioned in the Jupyter Notebook, you will find that there are some columns in the 'Dress Sales' 
dataset where the number of missing values is more than 40%. 
Based on your understanding of dealing with missing values, 
select the most appropriate statement from those given below, with the reason.

Answer:

You should remove these columns because they have a huge number of missing values. Moreover, 
if you see, the number of sales (numerical values) in such columns is not high as compared with other Date 
columns. Hence, it is safe to remove such columns.

Feedback :
The huge number of missing values in such columns is one of the criteria, but another major criterion is 
that these dates have extremely small sales values, and it is safe to remove them. You can refer to the 
following code to perform this operation.
"""
# Print the null percetange of each column of inp1.
print(inp1.isnull().sum()/len(inp1.index)*100)

inp1 = inp1.drop(['26-09-2013','30-09-2013','10-02-2013','10-04-2013','10-08-2013','10-10-2013' ],axis=1)
print(inp1.info())

print(inp1.isnull().sum()/len(inp1.index)*100)

"""
Handling Missing Values
You need to categorise the dates into seasons in the 'Dress Sales Dataset' data to 
simplify the analysis according to the following criteria:

June, July and August: Summer

September, October and November: Autumn

December, January and February: Winter

March, April and May: Spring

Which of the seasons has the lowest sales among all the seasons, and what is its value?

Ans: Spring, 143600
"""

# Create the four seasons columns in inp1, according to the above criteria.
inp1['Spring'] = inp1.apply(lambda x: x['09-04-2013'], axis=1)

inp1['Summer'] = inp1.apply(lambda x: x['29-08-2013'] + x['31-08-2013']+ x['09-06-2013']+ x['09-08-2013']+ x['10-06-2013'], axis=1)

inp1['Winter'] = inp1.apply(lambda x: x['09-02-2013'] + x['09-12-2013']+ x['10-12-2013'], axis=1)

inp1['Autumn'] = inp1.apply(lambda x: x['09-10-2013'] + x['14-09-2013']+ x['16-09-2013']+ x['18-09-2013']+ x['20-09-2013']+ x['22-09-2013']+ x['24-09-2013']+ x['28-09-2013'], axis=1)

# calculate the sum of sales in each seasons in inp1 i.e. "Dress Sales".
print(inp1[['Summer','Autumn','Winter','Spring']].sum())

# Now let's merge inp1 with inp0 with left join manner, so that the information of inp0 should remain intact.
inp0 = pd.merge(left=inp0,right=inp1, how='left', left_on='Dress_ID', right_on='Dress_ID')
inp0.head()

"""
Missing Values Handling
You can see that there are two types of variables: One with a large number of missing values and 
another with a less number of missing values. These two columns can be categorised as follows:

Type-1: Missing values are extremely less (around 2 or 3 missing values): 
Price, Season, NeckLine, SleeveLength, Winter and Autumn

Type-2: Missing values are large in number (more than 15%): 
Material, FabricType, Decoration and Pattern Type

Based on your understanding, which is the best method to deal with the missing values 
in the Type-1 and Type-2 columns?
"""
# Drop the missing values of the Type-1 columns as shown below:

inp0 = inp0[~inp0.Price.isnull()]

inp0 = inp0[~inp0.Season.isnull()]

inp0 = inp0[~inp0.NeckLine.isnull()]

inp0 = inp0[~inp0.SleeveLength.isnull()]

inp0 = inp0[~inp0.Winter.isnull()]

inp0 = inp0[~inp0.Autumn.isnull()]

# Create a separate category named ‘Missing’ in the Type-2 column as shown below:
inp0.Material= inp0.Material.replace(np.nan, "Missing")

inp0.FabricType= inp0.FabricType.replace(np.nan, "Missing")

inp0.Decoration= inp0.Decoration.replace(np.nan, "Missing")

inp0['Pattern Type']= inp0['Pattern Type'].replace(np.nan, "Missing")

"""
Standardise value
In the given dataset, there are certain discrepancies with the categorical names such as 
irregular spellings. Choose the correct option of columns with irregular categories and update them.

Season, NeckLine
Price, Material
fabricType, Decoration
Season, SleeveLength
"""
#correcting the spellings.
print(inp0['Season'].unique())

inp0['Season'].replace(['Automn','winter'], ['Autumn','Winter'], inplace=True)
print(inp0['Season'].unique())

print(inp0['SleeveLength'].unique())
inp0['SleeveLength'].replace(['thressqatar'], ['threequarter'], inplace=True)
print(inp0['SleeveLength'].unique())