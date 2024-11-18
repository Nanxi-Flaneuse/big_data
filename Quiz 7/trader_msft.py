from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession
spark = SparkSession.builder.appName("NewStreams").getOrCreate()

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# create two streams from the incoming stream
msftPrice = lines.withColumns({"date": substring("value", 21, 10), "msft": substring("value", 32, 8)})  # Extract msft data

# calculate 10 and 40 day averages for each string.




# Write the output to a sink
# query = aaplPrice \
#     .writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start()

query = msftPrice \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()