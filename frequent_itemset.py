import pandas as pd
from pyspark.sql import SparkSession
from pymongo import MongoClient
from pyspark.ml.fpm import FPGrowth
import warnings
warnings.filterwarnings('ignore')


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
mydb = client['customer_data']
collect = mydb['marketBasket']

result = collect.find({}, {'Mã sản phẩm': 1, '_id': 0})

# Chuyển kết quả thành một danh sách
data = list(result)

# Tạo DataFrame từ danh sách
product_data = pd.DataFrame(data)

# Chuyển thành spark dataframe
spark = SparkSession.builder.appName("mba").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")

df = spark.createDataFrame(product_data).withColumnRenamed('Mã sản phẩm', 'basket')
# df.show()

# frequent itemset - cách 1
freq_items1 = df.freqItems(['basket'], 0.001)

# frequent itemset - cách 2: spark ML - FPGrowth
fp = FPGrowth(minSupport=0.001, minConfidence=0.001, itemsCol='basket', predictionCol='prediction')
model = fp.fit(df)
freq_items2 = model.freqItemsets

# show result
# freq_items1.show(10, False)
# freq_items2.show(10, False)


# association rule
model.associationRules.filter(model.associationRules.confidence>0.15).show(20, False)

