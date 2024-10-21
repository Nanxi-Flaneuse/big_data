#!/usr/bin/env python
import sys, re
import random

def main(argv):
    line = sys.stdin.readline()
    # pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        while line:
            # print(line.split())
            if len(line.split()) > 1:
                res = int(line.split()[8])
                # print(res)
                if 100 <= res <= 199:
                    output = 'Informational'
                elif 400 <= res <= 499:
                    output = 'Client error'
                elif 200 <= res <= 299:
                    output = 'Successful'
                elif 300 <= res <= 399:
                    output = 'Redirection'
                elif 500 <= res <= 599:
                    output = 'Server error'
                print("LongValueSum:" +output + "\t" + "1")
                # print ("LongValueSum:" + word.lower() + "\t" + "1")
                # x = 1 / random.randint(0,99)
            line = sys.stdin.readline()
    except EOFError as error:
        return None

if __name__ == "__main__":
    main(sys.argv)

