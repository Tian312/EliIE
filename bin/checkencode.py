__author__ = 'kangtian'

import codecs
import os, sys

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"

def check(s):
    try:
        str(s)
    except UnicodeDecodeError:
        print "it may have unicode problem"
    except SyntaxError:
        print "Non-ASCII character"


myfile=codecs.open("/Users/kangtian/Documents/NER_data/negation_ann/13.txt")

for line in myfile:
    whatisthis(line)
    check(line)
    line.decode('ascii')