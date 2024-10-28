import pyspark as spark
from pyspark import SparkContext, SparkConf
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import split, col, udf, sum
from pyspark.sql.types import StringType
import base64
import math
import mmh3
from bitarray import bitarray

# spark = SparkSession \
#     .builder \
#     .appName("DetectNegativity") \
#     .getOrCreate()

class filter(object):

    def __init__(self, items_count, size, fil):
        
        # Size of bit array to use
        self.size = size
        # number of hash functions to use
        self.hash_count = self.get_hash_num(self.size, items_count)

        # Bit array of given size
        self.bit_array = fil

    # check if item is in filter
    def check(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            # if false bit detected, return false
            if self.bit_array[digest] == False:
                return False
        return True

    # return the number of hash functions needed. Number is calculated based on size of the array and number of input words
    def get_hash_num(self, s, n):
        k = (s/n) * math.log(2)
        return int(k)

def filter_negativity(word):
    
    with open('vector.txt', 'r') as file:
        file_content = file.read()
        file_content = base64.b64decode(file_content)

    fil = bitarray(file_content.decode("utf-8"))
    bloom = filter(63, 1024, fil)
    return bloom.check(word)
# print(filter_negativity('happy'))
# print(filter_negativity('damned'))
# negUDF = udf(lambda x:filter_negativity(x),StringType()) 

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

words = lines.split()
for word in words:
    if filter_negativity(word):
        lines = ''
        break
# # Split the lines into words
# words = lines.select(
#    F.explodse(
#        F.split(lines.value, " ")
#    ).alias("word")
# )

# # print(words)
# # apply filter to each word
# # negativity = words #words.withColumn('negative', negUDF(words.word))
# wordCounts = words.groupBy("word").count()
# # words.select(col("word"), negUDF(col("word")).alias("nagative") ).show()
                          
'''# Custom UDF with select()  
df.select(col("Seqno"), upperCaseUDF(col("Name")).alias("Name") ).show(truncate=False)'''

 # Start running the query that prints the words and their AFINN negativity aaffiliation to the console
query = lines \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()