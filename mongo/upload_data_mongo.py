"""this file is to upload data to mongoDB"""

import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collection = mydb['marketBasket']   # gộp chung 4 file vào 1 collection
collection.delete_many({})      # xóa dữ liệu cũ trong collection


# Đọc tập tin Excel và chỉ lấy các cột cần thiết
excel_files = ['data/MỸ-KHỞI-TK-MÌ-CAO-CẤP-KM-T1.2023.xlsb',
               'data/MỸ-KHỞI-TỔNG-KẾT-MÌ-ZEPPIN-GÓI-MÌ-LY-ZEPPIN-T2.2023.xlsb',
               'data/MỸ-KHỞI-BG-TK-PHỞ-ĐỆ-NHẤT-T3.2023.xlsb',
               'data/MỸ-KHỞI-FORM-TK-PHỞ-ĐỆ-NHẤT-HỦ-TIẾU-KM-T4.2023.xlsb']


for i in excel_files:
    sheet_index = 1
    # Đọc sheet từ file Excel
    df = pd.read_excel(i, sheet_name=sheet_index, header=2)
    df['Mã đơn hàng'] = df['Mã đơn hàng'].astype(str)
    df['Khuyến mãi / Trả thưởng'].fillna(0, inplace=True)
    v = ['Mã đơn hàng', 'Mã sản phẩm', 'Khuyến mãi / Trả thưởng']
    df = df[v]

    # Lọc ra các hàng có 'Khuyến mãi / Trả thưởng' = 0
    df_filtered = df[df['Khuyến mãi / Trả thưởng'] == 0]
    df_filtered.dropna(inplace=True)
    # In ra dữ liệu đã lọc
    data = df_filtered.iloc[:, [0, 1]]

    grouped = data.groupby('Mã đơn hàng')['Mã sản phẩm'].agg(list).reset_index()

    # Chuyển DataFrame thành danh sách các bản ghi dạng dict
    data_records = grouped.to_dict(orient='records')

    # Chèn dữ liệu vào MongoDB
    collection.insert_many(data_records)

print("Dữ liệu đã được đẩy vào MongoDB.")


