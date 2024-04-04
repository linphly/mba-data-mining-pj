import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['data_mining']  # Thay 'mydatabase' bằng tên database của bạn
collection = db['Basket_Market']  # Thay 'mycollection' bằng tên collection của bạn


# Truy vấn dữ liệu từ MongoDB
cursor = collection.find()

# Chuyển kết quả truy vấn thành một danh sách của các bản ghi
data = list(cursor)

# Chuyển danh sách các bản ghi thành DataFrame
df = pd.DataFrame(data)

# df.drop(columns='_id')
# df.drop(columns='')

# Thiết lập hiển thị tất cả các cột
pd.set_option('display.max_columns', None)

# Hiển thị 5 hàng đầu tiên của DataFrame
print(df.head())