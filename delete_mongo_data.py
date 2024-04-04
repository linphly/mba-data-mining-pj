"""This file is to delete mongoDB collection if u want"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collection = mydb['marketBasket']

mydb.drop_collection(collection)
print('collection deleted')
