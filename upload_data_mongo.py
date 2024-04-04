
import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')



# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['data_mining']
collection = db['Basket_Market']

# Đọc tập tin Excel và chỉ lấy các cột cần thiết
excel_files = ['data/MỸ-KHỞI-BG-TK-PHỞ-ĐỆ-NHẤT-T3.2023.xlsb',
               'data/MỸ-KHỞI-TỔNG-KẾT-MÌ-ZEPPIN-GÓI-MÌ-LY-ZEPPIN-T2.2023.xlsb',
               'data/MỸ-KHỞI-BG-TK-PHỞ-ĐỆ-NHẤT-T3.2023.xlsb',
               'data/MỸ-KHỞI-FORM-TK-PHỞ-ĐỆ-NHẤT-HỦ-TIẾU-KM-T4.2023.xlsb']

columns_indexes_to_keep = [0,1,11]
for i in excel_files:
    df = pd.read_excel(i, sheet_name='DATA AGENT', usecols=columns_indexes_to_keep, header=2)
    filtered_df = df[(df['Thành tiền'] != 0.0) & (~df['Thành tiền'].isna())]
    # Nhóm các hàng theo cột "Mã đơn hàng" và kết hợp các giá trị của cột "Mã sản phẩm"
    grouped_df = filtered_df.groupby('Mã đơn hàng')['Mã sản phẩm'].apply(','.join).reset_index()
    # Chuyển dữ liệu từ DataFrame thành dictionary để đẩy vào MongoDB
    data = grouped_df.to_dict(orient='records')
    # Đẩy dữ liệu vào MongoDB
    result = collection.delete_many({})
    collection.insert_many(data)

print("Dữ liệu đã được đẩy vào MongoDB.")

# Truy vấn dữ liệu từ MongoDB
cursor = collection.find()

# Chuyển kết quả truy vấn thành một danh sách của các bản ghi
data = list(cursor)

# Chuyển danh sách các bản ghi thành DataFrame
df = pd.DataFrame(data)

df.drop(columns='_id')
# df.drop(columns='')

# Thiết lập hiển thị tất cả các cột
pd.set_option('display.max_columns', None)

# Hiển thị 5 hàng đầu tiên của DataFrame
print(df.head())



