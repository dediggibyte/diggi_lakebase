# Databricks notebook source
# MAGIC %pip install dbldatagen
# MAGIC %pip install faker

# COMMAND ----------

# MAGIC %run ./00_Utility

# COMMAND ----------

# DBTITLE 1,DATA GENERATOR
from pyspark.sql import functions as F
from dbldatagen import DataGenerator,fakerText
from pyspark.sql.window import Window 


state_codes = ["MH", "KA", "MP", "TN", "DL", "UP", "GJ", "RJ", "WB", "PB", 
               "HR", "CH", "JK", "BR", "AP", "TS", "KL", "OR", "CG", "UT"]

alpha_codes = [f"{chr(65+i)}{chr(65+j)}" for i in range(10) for j in range(5)]

state_codes_data_spec = (DataGenerator(spark, rows=20, partitions=8)
    .withColumn("state_code", "string", values=state_codes, uniqueValues=20)  
    .withRowCount(20)  
)

alpha_code_data_spec = (DataGenerator(spark, rows=50, partitions=8)
    .withColumn("alpha_code", "string", values=alpha_codes, uniqueValues=10000)  
    .withRowCount(50)  
)

distirct_code_data_spec = (DataGenerator(spark, rows=50, partitions=8)
     .withColumn("district_code", "int", minValue=10, maxValue=60, random=True) 
    .withRowCount(50)  
)

numeric_code_data_spec = (DataGenerator(spark, rows=50, partitions=8)
     .withColumn("numeric_code", "int", minValue=0, maxValue=9999, uniqueValues=10000) 
     .withColumn("vehicle_type", "string", values=["Sedan", "SUV", "Truck", "Motorcycle"], weights=[1, 3, 2, 4]) 
    .withRowCount(100)  
)
    
state_df = state_codes_data_spec.build()
alpha_df = alpha_code_data_spec.build()
distirct_df = distirct_code_data_spec.build()
numeric_df = numeric_code_data_spec.build()

df_x = state_df.join(alpha_df, how="full").join(distirct_df, how="full").join(numeric_df, how="full").withColumn("vehicle_number",F.concat(
        F.col("state_code"),
        F.lpad(F.col("district_code").cast("string"), 2, "0"), 
        F.col("alpha_code"),
        F.lpad(F.col("numeric_code").cast("string"), 4, "0") 
    ) ).drop( "alpha_code", "numeric_code").withColumn("idx", F.monotonically_increasing_id()) 
w = Window.orderBy("idx")
df_index = df_x.withColumn("id", F.row_number().over(w))
df2_index = df_index.drop("idx")
#.withColumn("name", percentNulls=0.1, text=fakerText("name") )


person_data_spec = (DataGenerator(spark, rows=50, partitions=8)
     .withIdOutput() 
     .withColumn("name", percentNulls=0.1, text=fakerText("name") )
     .withColumn("Customer_ID", "int", expr="101 + id")  
     .withColumn("insurance_no", "int", expr="500000 + id")  
    .withRowCount(4000000)  
)

person_df = person_data_spec.build()
dff = person_df.join(df2_index, on=person_df['id'] == df2_index['id'], how="inner").drop("id")
print(dff.count())

# COMMAND ----------

from pyspark.sql.types import *
from datetime import date

def sample_orders():
    schema = StructType(
        [
            StructField("order_key", StringType(), nullable=False),
            StructField("customer_key", StringType(), nullable=False),
            StructField("total_price", FloatType(), nullable=False),
            StructField("order_date", DateType(), nullable=False),
        ]
    )
    data = [
        ("order1", "customer1", 100.0, date(2023, 1, 1)),
        ("order1", "customer1", 150.0, date(2023, 1, 2)),
        ("order2", "customer2", 200.0, date(2023, 1, 3)),
        ("order2", "customer2", 250.0, date(2023, 1, 4)),
    ] 
    return spark.createDataFrame(data, schema)

df = sample_orders()

table = "sc_lakebase_demo.customer_orders"
url = f"jdbc:postgresql://{database_host}:{database_port}/{database_name}"
print(url)
(df.write.format("jdbc")
     .option("driver", driver)
     .option("url", url)
     .option("dbtable", table)
     .option("user", user)
     .option("password", password)  # Ensure 'password' variable is set with the correct password
     .mode("append")
.save())
