#! /bin/usr/python 

import sys,os,re,codecs
from xml.etree import ElementTree as ET



tree=ET.ElementTree(file='/Users/kangtian/Documents/NER_data/NER/parser_code/negation/NER_Negation_230.xml')
root = tree.getroot()
negex_input=codecs.open("/Users/kangtian/Documents/NER_data/NER/parser_code/negation/NER_negex_230.input",'w')

for child in root :
    sent=''
    for child2 in child.findall('text'):
        sent=child2.text
    for child2 in child.findall('entity'):
        if child2.attrib['class']=='Negation_cue':
            continue
        index=child2.attrib['index']
        entity=child2.text
        if child2.attrib['negated']=="Y":
            print >>negex_input, str(index)+"\t"+entity+"\t"+sent+"\tnegated"
        elif child2.attrib['negated']=="N":
            print >>negex_input, str(index)+"\t"+entity+"\t"+sent+"\taffirmed"

