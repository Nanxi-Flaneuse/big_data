#!/usr/bin/env python
import sys, re
import random

def main(argv):
    line = sys.stdin.readline()
    
    # pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        
        while line:
            # print(line.split())
            line = line.split()
            if len(line) > 1:
                res = int(line[8])

                if 400 <= res <= 499:
                    print("LongValueSum:" +line[0] + '\t' + '1')

                    # print ("LongValueSum:" + word.lower() + "\t" + "1")
                    # x = 1 / random.randint(0,99)
            line = sys.stdin.readline()
    except EOFError as error:
        return None

if __name__ == "__main__":
    main(sys.argv)

