#!/usr/bin/env python
import sys, re
# from valence import clean_text, get_word_valence, get_sent_dict
import os
import requests
import string

pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = list(set(stopwords_list.decode().splitlines()))


sentiment_list = requests.get('https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt').content
sentiments = list(set(sentiment_list.decode().splitlines()))

# helper function that builds dictionary when given a list of sentiments
def get_sent_dict(sents):
    result =  {}
    for s in sents:
        # s = pattern.findall(s)
        # print(s)
        # print(' '.join(s[:-2]))
        temp = s.split()
        num = temp[-1]
        word = s.replace(num, "")
        try:
            result[word[:-1]] = int(num)
        except:
            print('ERROR OCCURRED ------------------------')
    return result

sentiment_dictionary = get_sent_dict(sentiments)

def remove_stopwords(words):
    list_ = re.sub(r"[^a-zA-Z0-9]", " ", words.lower()).split()
    return [itm for itm in list_ if itm not in stopwords]


def clean_text(text):
    if not type(text) is str:
        print('text is not of type string:',text)
        return None
    else:
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub('[\d\n]', ' ', text)
        return ' '.join(remove_stopwords(text))

def get_word_valence(word):
    if not (type(word) is str) or word is None:
        # print('text is not of type string:',word)
        return 0
    # checks if input has length > 0
    elif len(word) == 0:
        return 0
    # checks if input is printable
    elif not word.isprintable():
        # print('Text contains on printable characters')
        return 0
    else:
        try:
            return sentiment_dictionary[word]
        except:
            # print('word not found')
            return 0
# is there something wrong with how I'm reading the file
# to precess all the prz speeches in hadoop, can I use tar files instead of untarring all of the tar files?

def main(argv):

    ##### to be uncommented ###########
    try:
        try:
            file = os.environ['mapreduce_map_input_file']
        except KeyError:
            file = os.environ['map_input_file']
        name = file.split('/')[-1]
        prez_name = name.split('_')[0]

    except:
        prez_name = 'adams'
    # prez_name = 'adams'
    # prez_name = file[:-17]
    line = sys.stdin.readline()
    # pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        while line:
            line = clean_text(line).split()
            for word in line:
                # print("LongValueSum:" + 'adams' + "\t" + str(get_word_valence(word)))
                ##### to be uncommented ###########
                # testing
                # print("LongValueSum:" + prez_name + "\t" + '1')
                print("LongValueSum:" + prez_name + "\t" + str(get_word_valence(word)))
            line = sys.stdin.readline()
    except EOFError as error:
        return None

if __name__ == "__main__":
    # print(sentiment_dictionary.keys())
    main(sys.argv)
    # print(os.environ['USER'])


