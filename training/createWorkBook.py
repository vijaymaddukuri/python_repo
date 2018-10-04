import openpyxl
import os
import xlrd
fileLocation=r'D:\new\vijay.xls'
wb = xlrd.open_workbook(fileLocation)
headers = []
sdata = []
sdata1 = []

for s in wb.sheets():
    print("Sheet:",s.name)

    for row in range(s.nrows):
        values = []
        values1 = []
        for col in range(s.ncols):
            data = s.cell(row,col).value
            if row == 0:
                headers.append(data)
            else:
                values.append(data)
                values1.append(data)
        sdata.append(values)
        values1=" ".join(values1)
        sdata1.append(values1)
header=" ".join(headers)
data = "\n".join(sdata1)

table="".join((header,data))

print('\n')
print(table)
print(sdata)
print(headers)

sdata=sdata[1:3]
print(sdata)
newDict= dict(zip(headers,zip(*sdata)))
print(newDict)
