__author__ = 'Tian Kang'

import sys

import nltk


import string,os
reload(sys)



def pos_tagging(term_list):
    #print term_list
    term_list_new=list()
    for term in term_list:
        term=term.decode('utf-8', 'ignore')
        term_list_new.append(term)
    tag=nltk.pos_tag(term_list_new)
    t=list()
    for ta in tag:
       t.append(ta[1])
    return t

s=['I','have']
#tag=pos_tagging(s)
#print tag
