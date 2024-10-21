#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys

current_word = None
# prez_freq = 0
current_valence = 0
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # print('printing out line')
    # print(line)
    # parse the input we got from mapper.py
    word, valence = line.split('\t', 1)
    count = 1

    # convert count (currently a string) to int
    try:
        valence = int(valence)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
        current_valence += valence
        # prez_freq += 1
    else:
        if current_word:
            # write result to STDOUT
            print ('%s\t%s' % (current_word, current_valence/current_count))
        current_count = count
        current_word = word
        current_valence = 0
        # prez_freq = 1

# do not forget to output the last word if needed!
if current_word == word:
    print ('%s\t%s' % (current_word, current_valence/current_count))
