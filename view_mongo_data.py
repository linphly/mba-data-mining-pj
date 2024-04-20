"""This file is just to view data"""

import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['marketBasket']

result = collect.find({}, {'Mã sản phẩm': 1, '_id': 0})

# Chuyển kết quả thành một danh sách
# Tạo DataFrame từ danh sách
data = pd.DataFrame(list(result))

# Thiết lập hiển thị tất cả các cột
pd.set_option('display.max_columns', None)

print(data)

