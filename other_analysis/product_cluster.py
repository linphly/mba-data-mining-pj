'''
Phân cụm sản phẩm dựa trên số lần mua
'''

import pandas as pd
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['general_data']


def getDataFromMGDB(collectName, colName):
    data = collectName.find({}, colName)
    dataFrame = pd.DataFrame(data).drop(columns='_id')
    return dataFrame

colName = ['OrderID', 'ProductID'] # Thay đổi các cột muốn lấy ở đây
data = getDataFromMGDB(collect, colName)

print(data.head(10))




