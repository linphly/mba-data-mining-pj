# Market Basket Analysis - Data mining project

add this 2 rows to fix error in converting pandas dataframe to spark dataframe
>spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
>spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")