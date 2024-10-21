import requests
import re
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

# creating the sentiment dictionary
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


# takes in a line and returns its valence
def calc_valence(text):
    # checks if input is a string
    if not type(text) is str or text is None:
        print('text is not of type string:',text)
        return None
    # checks if input has length > 0
    elif len(text) == 0:
        return None
    # checks if input is printable
    elif not text.isprintable():
        print('Text contains on printable characters')
        return None
    else:
        result = 0
        wordlist = text.split()
        for w in wordlist:
            try:
                # print(w,str(sentiment_dictionary[w]))
                result += sentiment_dictionary[w]
            except:
                pass
                # print('word not found in dictionary:',w)
        return result



# wrapper function for checking the valence of a text snippet
def valence(text):
    return calc_valence(clean_text(text))

# testing
if __name__ == "__main__":
    # print(get_word_valence('abandon'))
    print(valence('today great acclaim gather featival abandon to my pleasure'))
    b = 'I am a string'.encode('ASCII')
    print(valence(b))