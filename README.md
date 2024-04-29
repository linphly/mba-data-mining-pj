# Market Basket Analysis - Data mining project

## **Flow**  
* folder mongo  
* folder algorithm   
    * freqItemset   
    * association rule  
* recommend


## Fix error
add this 2 rows to fix error in converting pandas dataframe to spark dataframe
>spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
>spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled", "true")