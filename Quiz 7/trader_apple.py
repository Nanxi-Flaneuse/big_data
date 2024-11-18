from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, FloatType, TimestampType, StringType
# from pyspark.sql.streaming import GroupState, GroupStateTimeout
import datetime

# problem
'''using curr time stamp, I can't get the date
using date as time stamp, the average calculated is not correct'''
# Create a SparkSession
spark = SparkSession.builder.appName("NewStreams").getOrCreate()

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()


# why is the price output not the average but the same day price?


#### method: use time of data streaming as timestamp ########################################

# Define the Schema
# schema = StructType([
#     StructField("date", StringType(), True),
#     StructField("price", FloatType(), True)
# ])

# # Apply the schema to the streaming data
# stock_data = lines.selectExpr("CAST(value AS STRING)") \
#     .selectExpr("split(value, '\t') as parts") \
#     .selectExpr("CAST(parts[0] AS STRING) as date", 
#                 "CAST(parts[1] AS FLOAT) as price")
# # add timestamp 2020-12-30 00:00:00
# stock_data = stock_data.withColumn("window", current_timestamp())

# # Define Watermark
# # Add a watermark to the timestamp column
# stock_data = stock_data.withWatermark("window", "10 seconds")

# # Group the data by window and word and compute the count of each group
# # print(stock_data.groupBy(
# #     window(stock_data.timestamp, "5 seconds", "1 second")))
# moving_avg_10 = stock_data.groupBy(
#     window(stock_data.window, "5 seconds", "1 second")).agg(avg("price").alias("5_day_moving_avg"))

# moving_avg_10 = moving_avg_10.join(stock_data, "window")
# moving_avg_10 = stock_data.groupBy(
#     window(stock_data.window, "5 seconds", "1 second"),col('date')).agg(avg("price").alias("5_day_moving_avg"))

    # window(stock_data.timestamp, "5 seconds", "1 second"),col('date')).agg(avg("price").alias("5_day_moving_avg"))
####################################################################################################################

#### method: use date info in data streaming as timestamp ##############################################################################################

#Define the Schema
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("price", FloatType(), True)
])

# Apply the schema to the streaming data
stock_data = lines.selectExpr("CAST(value AS STRING)") \
    .selectExpr("split(value, '\t') as parts") \
    .selectExpr("CAST(parts[0] AS TIMESTAMP) as timestamp", 
                "CAST(parts[1] AS FLOAT) as price")
# schema = StructType([
#     StructField("date", StringType(), True),
#     StructField("price", FloatType(), True)
# ])

# # Apply the schema to the streaming data
# stock_data = lines.selectExpr("CAST(value AS STRING)") \
#     .selectExpr("split(value, '\t') as parts") \
#     .selectExpr("CAST(parts[0] AS STRING) as date", 
#                 "CAST(parts[1] AS FLOAT) as price")

# Define Watermark
# Add a watermark to the timestamp column
# stock_data = stock_data.withColumn("date_long", col("date").cast("long"))
stock_data_with_watermark = stock_data.withWatermark("timestamp", "40 days")
# # window_spec = Window.orderBy("date_long").rowsBetween(-3, -1)
# moving_avg_10 = stock_data_with_watermark.withColumn("avg", avg("price").over(window_spec))
# Calculate Moving Averages
# 10-day moving average
# moving_avg_10 = stock_data_with_watermark \
#     .groupBy(window(col("timestamp"), "10 days", "1 day")) \
#     .agg(avg("price").alias("10_day_moving_avg"))
### testing
moving_avg_10 = stock_data_with_watermark \
    .groupBy(window("timestamp", "10 days",'1 day')) \
    .agg(avg("price").alias("10_day_moving_avg"))
moving_avg_10 = moving_avg_10.select(moving_avg_10.window.end.cast("string").alias("end-date"), "10_day_moving_avg")
# moving_avg_10 = stock_data_with_watermark \
#     .groupBy(window("timestamp", "10 days", "1 day"))
# moving_avg_10 = stock_data_with_watermark.orderBy(col('timestamp').cast('long')).rowBetween(-days(3), -days(1)).agg(avg("price").alias("10_day_moving_avg"))

# # 40-day moving average
# moving_avg_40 = stock_data_with_watermark \
#     .groupBy(window(col("timestamp"), "3 days", "1 day")) \
#     .agg(avg("price").alias("40_day_moving_avg"))
### testing
moving_avg_40 = stock_data_with_watermark \
    .groupBy(window("timestamp", "40 days",'1 day')) \
    .agg(avg("price").alias("40_day_moving_avg"))
moving_avg_40 = moving_avg_40.select(moving_avg_40.window.end.cast("string").alias("end-date"), "40_day_moving_avg")

# # Join the two moving averages on the timestamp window
moving_avgs = moving_avg_10.join(moving_avg_40, "end-date")

# # Step 5: Define the Signal Logic
moving_avgs_with_signal = moving_avgs.withColumn(
    "signal",
    when(col("10_day_moving_avg") > col("40_day_moving_avg"), "buy")
    .when(col("10_day_moving_avg") < col("40_day_moving_avg"), "sell")
    .otherwise("hold")
)

# create two streams from the incoming stream

# aaplPrice = lines.withColumns({"date": substring("value", 1, 10), "aapl": substring("value", 12, 8)})  # Extract aapl data
# date = lines['value']


# n to partition the data into groups of 10 rows
# window = Window.orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)

# # Calculate the average for every 10 rows
# df = aaplPrice.withColumn("row_num", row_number().over(window)) \
#     .withColumn("group", floor((row_number().over(window) - 1) / 10)) \
#     .groupBy("group").agg(avg("value").alias("avg_value"))




# Write the output to a sink
# query = moving_avg_10\
#     .writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start()

query = moving_avgs_with_signal \
    .select('end-date',"signal") \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()