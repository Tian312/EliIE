__author__ = 'kangtian'
import os,sys,re,codecs
from xml.etree import ElementTree as ET

tree = ET.ElementTree(file='/Users/kangtian/Documents/NER_data/Negation.xml')
root = tree.getroot()
myann = codecs.open("/Users/kangtian/Documents/NER_data/NER/parser_code/negation/all_new.ann")
negate_list=[]
for line in myann:
    line=line.rstrip()
    info=line.split("\t")
    if info[1] == "is_negated":
        tag=info[2].split(":")
        index=tag[1]
        negate_list.append(index)

for child in root:

    for child2 in child.findall('entity'):
        node_index=child2.attrib['index']
        child2.attrib['negated']='N'
        if node_index in negate_list:
            child2.attrib['negated']='Y'

new_tree=codecs.open("/Users/kangtian/Documents/NER_data/NER/parser_code/negation/NER_Negation_230.xml",'w')
tree.write(new_tree)