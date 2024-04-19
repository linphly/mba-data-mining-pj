import pandas as pd
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['marketBasket']

result = collect.find({}, {'Mã sản phẩm': 1, '_id': 0})

# Chuyển kết quả thành một danh sách
data = list(result)

# Tạo DataFrame từ danh sách
product_data = pd.DataFrame(data)

print(product_data)