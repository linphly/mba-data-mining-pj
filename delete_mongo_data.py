"This file is to delete mongoDB data to remove duplicate"

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['data_mining']  # Thay 'mydatabase' bằng tên database của bạn
collection = db['Basket_Market']  # Thay 'mycollection' bằng tên collection của bạn

if collection:
    db.drop_collection(collection)
else:
    print('collection not found')