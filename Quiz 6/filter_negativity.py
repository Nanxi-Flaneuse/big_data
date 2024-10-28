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
## testing
import math
import mmh3
from bitarray import bitarray
import requests
import base64

# step 1: load -4 -5 words from AFINN list
sentiment_list = requests.get('https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt').content
sentiments = list(set(sentiment_list.decode().splitlines()))

# helper function that builds dictionary when given a list of sentiments
def get_sent(sents):
    result =  []
    for s in sents:
        # s = pattern.findall(s)
        # print(s)
        # print(' '.join(s[:-2]))
        temp = s.split()
        num = temp[-1]
        word = s.replace(num, "")
        if int(num) < -3:
            result.append(word[:-1])
    return result

neg_sents = get_sent(sentiments)

# step 2: create filter class
class filter(object):

    def __init__(self, items_count, size):
        '''
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        '''

        # Size of bit array to use
        self.size = size
        # number of hash functions to use
        self.hash_count = self.get_hash_num(self.size, items_count)

        # Bit array of given size
        self.bit_array = bitarray(self.size)
        # setting all bits as 0
        self.bit_array.setall(0)

    # adding element to filter
    def add(self, item):
        # creating hashed items using all hash functions
        for i in range(self.hash_count):
            word = mmh3.hash(item, i) % self.size
            # set the bit True in bit_array
            self.bit_array[word] = True

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
    
    # returns the filter vector as a string of 0 and 1 saved to file
    def get_array_64(self, file):
        vec = base64.b64encode(self.bit_array.to01().encode("ascii"))
        print(vec)
        try:
            with open(file,"w+") as f:
                    f.write(vec.decode("utf-8"))
        except Exception as e:
            print(str(e))

# spark = SparkSession \
#     .builder \
#     .appName("DetectNegativity") \
#     .getOrCreate()

# class filter(object):

#     def __init__(self, items_count, size, fil):
        
#         # Size of bit array to use
#         self.size = size
#         # number of hash functions to use
#         self.hash_count = self.get_hash_num(self.size, items_count)

#         # Bit array of given size
#         self.bit_array = fil

#     # check if item is in filter
#     def check(self, item):
#         for i in range(self.hash_count):
#             digest = mmh3.hash(item, i) % self.size
#             # if false bit detected, return false
#             if self.bit_array[digest] == False:
#                 return False
#         return True

#     # return the number of hash functions needed. Number is calculated based on size of the array and number of input words
#     def get_hash_num(self, s, n):
#         k = (s/n) * math.log(2)
#         return int(k)

## testing
bloom = filter(len(neg_sents), 1024)
for w in neg_sents:
    bloom.add(w)
def filter_negativity(word):
    ## testing
    return bloom.check(word)


    # with open('vector.txt', 'r') as file:
    #     file_content = file.read()
    #     file_content = base64.b64decode(file_content)

    # fil = bitarray(file_content.decode("utf-8"))
    # bloom = filter(63, 1024, fil)
    # return bloom.check(word)
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

words = lines.tail(1)[0]['value']
for word in words:
    if filter_negativity(word):
        words = ''
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
query = words \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()