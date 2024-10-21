#!/usr/bin/env python
import sys, re
import random

def main(argv):
    line = sys.stdin.readline()
    pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
    try:
        while line:
            # print(pattern.findall(line))
            line = line.strip()
            line = line.split()
            # print(line)
            if len(line) > 2:
                print("LongValueSum:" +line[5][1:].lower() + "\t" + "1")
                # print ("LongValueSum:" + word.lower() + "\t" + "1")
                # x = 1 / random.randint(0,99)
            line = sys.stdin.readline()
    except EOFError as error:
        return None

if __name__ == "__main__":
    main(sys.argv)

# cmd prompt
'echo' '''13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"''' '| python3 -m mapper_1 '
# def main(strings):
#     line = strings.strip()
#     words = line.split()
#     print(words)
#     # line = strings
#     pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
#     try:
#         # while line:
#         print(words[3].lower() + "\t" + "1")
#         # for word in pattern.findall(line):
#         #     print ("LongValueSum:" + word.lower() + "\t" + "1")
#             # x = 1 / random.randint(0,99)
#         line = strings
#     except EOFError as error:
#         return None

# if __name__ == "__main__":
#     main('''13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"''')


# def main(argv):
#     line = sys.stdin.readline()
#     line = line.strip()
#     pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
#     try:
#         while line:
#             print(line[4].lower() + "\t" + "1")
#             # for word in pattern.findall(line):
#             #     print ("LongValueSum:" + word.lower() + "\t" + "1")
#                 # x = 1 / random.randint(0,99)
#             line = sys.stdin.readline()
#     except EOFError as error:
#         return None

# if __name__ == "__main__":
#     main(sys.argv)

