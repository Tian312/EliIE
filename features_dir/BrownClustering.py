#import gensim
import sys,os,re,string,codecs

def read_bcindex(directory):
    myfile = codecs.open(directory,'r')
    index={}
    for line in myfile:
        info=line.split()
        index[info[0].lower()]=info[1]

    return index


#======impletment=====
def bc_indexing(term,index_dic):
    term=re.sub('\W$','',term)
    if term.lower() in index_dic.keys():
        return(index_dic[term.lower()])
    else:
        return('0')
