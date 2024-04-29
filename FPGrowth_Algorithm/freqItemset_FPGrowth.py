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


def getItemsets(transactions = transactions, minimum_support = 0, include_support=False):
    frequent_itemsets = find_frequent_itemsets(transactions, minimum_support=minimum_support, include_support=include_support)

    result = []
    for itemset, support in frequent_itemsets:
        result.append((itemset, support))

    result = sorted(result, key=lambda i: i[1], reverse=True)   # xắp xếp theo support giảm dần

    # bỏ những itemset chỉ có 1 item
    # for i_s in result[:]:
    #     if len(i_s[0]) == 1:
    #         result.remove(i_s)

    return result


if __name__ == '__main__':
    # Lấy ra frequent itemset
    start = time.time()

    freq_itemsets = getItemsets(minimum_support=0.01, include_support=True)
    # print(type(freq_itemsets))

    for itemset, support in freq_itemsets:
        print(str(itemset) + ' ' + str(support))

    end = time.time()
    print('Thời gian chạy', str(end - start))