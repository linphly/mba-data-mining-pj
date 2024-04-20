import time
import pandas as pd
from pymongo import MongoClient
from FPTree import find_frequent_itemsets

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['marketBasket']

# Lấy dữ liệu
result = collect.find({}, {'Mã sản phẩm': 1, '_id': 0})
data = pd.DataFrame(list(result))
transactions = data['Mã sản phẩm']

# Lấy ra frequent itemset
miSupp = 0.01

start = time.time()
n = len(transactions)
frequent_itemsets = find_frequent_itemsets(transactions, minimum_support=miSupp*n, include_support=True)

result = []
for itemset, support in frequent_itemsets:
    result.append((itemset, support))

result = sorted(result, key=lambda i: i[1], reverse=True)   # xắp xếp theo support giảm dần

# bỏ những itemset chỉ có 1 item
# for i_s in result[:]:
#     if len(i_s[0]) == 1:
#         result.remove(i_s)

print(len(result))
for itemset, support in result:
    print(str(itemset) + ' ' + str(support))

end = time.time()
print('Thời gian chạy', str(end - start))