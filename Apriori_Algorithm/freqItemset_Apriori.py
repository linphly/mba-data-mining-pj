import pandas as pd
from pymongo import MongoClient
import warnings
import numpy as np
from collections import Counter

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collection = mydb['general_data']


# Lấy dữ liệu
def getDataFromMGDB(collectName, colName):
    data = collectName.find({}, colName)
    dataFrame = pd.DataFrame(data)
    return dataFrame


colName = ['OrderID', 'ProductID']
data = getDataFromMGDB(collection, colName).drop(columns='_id')
transactions = data.groupby('OrderID')['ProductID'].agg(list).reset_index()


# Xây dựng thuật toán apriori
def getItemsets(transactions = transactions, minimum_support = 0):
    init = set()
    for transaction in transactions['ProductID']:
        init.update(transaction)
    init = np.array(list(init))

    sp = minimum_support
    s = int(sp * len(transactions))
    n = len(transactions)
    # print(s, n)

    itemsets = []

    c = Counter()
    for i in init:
        for d in transactions['ProductID']:
            if (i in d[1:]):
                c[i] += 1

    l = Counter()
    for i in c:
        if (c[i] >= s):
            l[frozenset([i])] += c[i]

    for i in l:
        itemsets.append((list(i), l[i]/n))

    pl = l
    pos = 1
    for count in range(2, 1000):
        nc = set()
        temp = list(l)
        for i in range(0, len(temp)):
            for j in range(i + 1, len(temp)):
                t = temp[i].union(temp[j])
                if (len(t) == count):
                    nc.add(temp[i].union(temp[j]))
        nc = list(nc)
        c = Counter()
        for i in nc:
            c[i] = 0
            for q in transactions['ProductID']:
                temp = set(q[1:])
                if (i.issubset(temp)):
                    c[i] += 1

        l = Counter()
        for i in c:
            if (c[i] >= s):
                l[i] += c[i]

        for i in l:
            itemsets.append((list(i), l[i] / n))

        if (len(l) == 0):
            break
        pl = l
        pos = count
    print("Result: ")
    print("L" + str(pos) + ":")
    for i in pl:
        print(str(list(i)) + ": " + str(pl[i]))
    print()

    itemsets = sorted(itemsets, key=lambda i: i[1], reverse=True)   # xắp xếp theo support giảm dần
    return itemsets


if __name__ == '__main__':
    freq_itemsets = getItemsets(minimum_support=0.015)

    for itemset, support in freq_itemsets[:10]:
        print(str(itemset) + ' ' + str(support))