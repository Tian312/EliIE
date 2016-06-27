__author__ = 'Tian Kang'

#============ Parser step 1: Entity&Attribute recognition     =====#
#                                                                  #
#   sys.argv 1: input dir  (input)                                 #
#   sys.argv 2: input text name (input)                            #
#   sys.argv 3: output NER xml dir                                 #
#
#   email: tk2624@cumc.columbia.edu (Tian)                         #
#   June, 2016                                                     #
#                                                                  #
#==================================================================#

import sys,string,os,re
import codecs
from text_processing import txtconll as t2c
from text_processing import preprocess
from features_dir import POS,BrownClustering,umls_identify
import nltk
from nltk.stem.lancaster import LancasterStemmer

# read files:
input_dir=sys.argv[1]+"/"+sys.argv[2]
print "Reading text from ",input_dir
mytrial=codecs.open(input_dir).read()
match=re.search('^(.*)\.txt',sys.argv[2])
filename=sys.argv[2]
if match:
    filename=match.group(1)


nerxmlname=filename+"_NER.xml"
output_dir=sys.argv[3]+'/'+nerxmlname

myxml=codecs.open(output_dir,'w')


# load models
st = LancasterStemmer()
bc_index=BrownClustering.read_bcindex("trained_models/brownclustering.index")





mymatrix=codecs.open('Tempfile/test.matrix','w')

entity_lists=['Condition','Observation','Drug','Procedure_Device']
attribute_lists=['Qualifier','Measurement','Temporal_measurement']

def add_feature(sent,crf_matrix):
    sent=sent.rstrip()
    metamap_output=umls_identify.formating_for_metamap(sent)
    one_sent_term,type_list=umls_identify.label_umls_cui(metamap_output,sent)
    pos_list=POS.pos_tagging(one_sent_term)
    pos_list.append(".")
    type_list.append("O")
    terms=sent.split()
    term_id=0

    for t in one_sent_term:
        term=t
        lemma=st.stem(term)
        #vector=word2vec.ouput_embedding(model,term.lower(),50)
        bc=BrownClustering.bc_indexing(term.lower(),bc_index)
        print >>crf_matrix, t+"\t"+lemma+"\t"+pos_list[term_id]+"\t"+type_list[term_id]+"\t"+bc
        term_id+=1
    print >>crf_matrix



def generate_XML(crfresult_input,NERxml_output):
    sents,entity=t2c.conll2txt(crfresult_input)
    print >>NERxml_output,"<?xml version=\"1.0\"?>"
    print >>NERxml_output,"<root>"
    j=0

    for sent in sents:
        if sent == "":
            continue
        clean_sent=t2c.clean_txt(sent)
        pattern='class=\'(\w+)\''
        entities=entity[j].split('\n\t\t')
        new_entities=[]
        for e in entities:
            if e =='':
                new_entities.append('\n')
                continue
            match=re.search(pattern,e)
            if match.group(1) in attribute_lists:

                p1='\<entity'
                p2='entity\>'
                new=re.sub(p1,'<attribute',e)
                new=re.sub(p2,'attribute>',new)
                new_entities.append(new)
            else:
                new_entities.append(e)
        entity[j]="\n\t\t".join(new_entities)


        #clean_sent=re.sub("\'"," POSSESS ",clean_sent)
        print >>myxml,"\t"+"<sent>\n"+"\t\t<text>"+clean_sent+"</text>"

        print  >>myxml,"\t\t"+entity[j]
        print >>myxml,"\t"+"</sent>"
        j+=1
    print >>myxml,"</root>"


def run_crf( model_dir, matrix_dir, output_dir):
    command='crf_test -m '+model_dir+' '+matrix_dir+' > '+output_dir
    os.system(command)


#========== test ==========
sents=nltk.sent_tokenize(mytrial)
for sent in sents:

    cleansent=preprocess.preprocess(sent)
    filteredsent=preprocess.ec_filtering(cleansent)
    if filteredsent:
        add_feature(filteredsent,mymatrix)


run_crf('trained_models/bc_umls_pos_lemma_bow.model', 'Tempfile/test.matrix' ,'Tempfile/test_crf.result')
myconll=codecs.open("Tempfile/test_crf.result","r")
generate_XML(myconll,myxml)
os.system('rm Tempfile/test.matrix Tempfile/test_crf.result')

