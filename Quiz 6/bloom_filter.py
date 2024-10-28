
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

# step 3: create filter object using AFINN list
if __name__ == '__main__':
    # print(neg_sents)
    print(len(neg_sents))
    # bloom = filter(len(neg_sents), 1024)
    # for w in neg_sents:
    #     bloom.add(w)
    # print(bloom.check('happy'))
    # print(bloom.check('dead'))
    # print(bloom.check('damned'))
    # print(bloom.check('sad'))
    # print(bloom.get_array_64('vector.txt'))


'''references
1. https://stackoverflow.com/questions/53651409/writing-a-base64-string-to-file-in-python-not-working
2. https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/'''


