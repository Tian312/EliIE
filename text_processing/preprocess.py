__author__ = 'kangtian'

import sys,string,os,re

#from gensim import corpora

# preprocess before parsing; functions including:
#   1. remove irrelavant eligibiltiy criteira
#   2. normalize characters/punctuations



english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '>', '=']
keywords_filter=['consent','willing','agree','speak','informant','comply','in opinion of investigator','work','understand','study partner']

def ec_filtering(input_ec):
    for keyword in keywords_filter:
        match=re.search(keyword,input_ec)
        if match:
            return None
        else:
            return input_ec



def preprocess(rawtext):

    text=re.sub('>='," %%% ",rawtext.decode('utf-8'))
    #text=re.sub('\n',' ',text)
    text=re.sub('<=', ' @@@ ',text)
    text=re.sub('>>','~~~',text)
    text=re.sub(',',' ,',text)
    text=re.sub('>',' > ',text)
    text=re.sub('<',' < ',text)
    text=re.sub(';',' ; ',text)
    text=re.sub('~~~','>>',text)
    text=re.sub('=', ' = ',text)
    text=re.sub('\:',' : ',text)
    text=re.sub('\[', ' [ ', text)
    text=re.sub('\]', ' ] ',text)
    text=re.sub('\(', ' ( ',text)
    text=re.sub('\)', ' ) ',text)
    text=re.sub('%%%', '>=',text)
    text=re.sub('@@@', '<=',text)

    nums=re.findall('\d-\d',text)
    for num in nums:
        gang=re.search('(\d)-(\d)',num)
        text=re.sub(gang.group(1)+'-'+gang.group(2),gang.group(1)+' - '+gang.group(2),text)
    period=re.findall('\w\.\s?',text)
    for ps in period:
        p=re.search('(\w)\.\s?',ps)

        text=re.sub(p.group(1)+'\.',p.group(1)+' . ',text)
    return (text)

