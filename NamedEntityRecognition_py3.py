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
# for python 3 and metampa 2016 version

import os.path
_PATH = os.path.join( *os.path.split(__file__)[:-1] )
import sys,string,os,re,csv
import codecs
from text_processing import txtconll as t2c
from text_processing import preprocess
from features_dir import POS,BrownClustering,umls_identify
from text_processing import label_from_annotation as labeling
import nltk
#import screen
from nltk.stem.lancaster import LancasterStemmer
from bin import readfromdir
from bin.negex import *
from xml.etree import ElementTree as ET


def txt2matrix_fortest(sent,crf_matrix,filename):
    sent=sent.rstrip()
    metamap_output=umls_identify.formating_for_metamap(curpath,sent,filename)
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
        #print >>crf_matrix, t+"\t"+lemma+"\t"+pos_list[term_id]+"\t"+type_list[term_id]+"\t"+bc
        crf_matrix.write(t+"\t"+lemma+"\t"+pos_list[term_id]+"\t"+type_list[term_id]+"\t"+bc+"\n")
        term_id+=1
    #print >>crf_matrix
    crf_matrix.write("\n")

def txt2matrix_fortrain(ann_dir,mytrain,tag_included,filename,curpath):
    txt_files=readfromdir.get_file_list(ann_dir,['txt'])
    print ("there's "+ str(len(txt_files))+" in total!")

    i=0
    for txt_file in txt_files:
        i+=1

        # read files

        myraw=codecs.open(txt_file).read()
        match=re.search('^(.*)\.txt',txt_file)
        name=match.group(1)
        #ann_file=name+'_new.ann'
        ann_file=name+'.ann'
        print ("reading file from",txt_file,ann_file,"...")
        myann=codecs.open(ann_file,"r")

        # output features
        text_tagged=labeling.ann_tagging(myann,myraw,tag_included)
        lines=" ".join(text_tagged.split(r'[;\n]'))
        sents=nltk.sent_tokenize(lines)
        lines=" ### ".join(sents)
        term_list, tag_list,index_list=t2c.txt2conll(lines,1)  # "1" here represents it's a training texts with annoatioin; "0" represents raw texts
        sents=" ".join(term_list).split("###")
        type_list=[]
        pos_list=[]
        # extract umls concepts:
        j=0
        for sent in sents:
            if j>=len(term_list):
                break

            one_sent_list = sent.split()
            metamap_output=umls_identify.formating_for_metamap(curpath,sent,filename)
            one_sent_term,type_list=umls_identify.label_umls_cui(metamap_output,sent)

            pos_list=POS.pos_tagging(one_sent_term)
            #pos_list= POS.pos_tagging(one_sent_list)
            #pos_list.append(".")
            #type_list.append("O")
            terms=sent.split()

            sent_id=0
            for t in terms:
                if term_list[j]== "###":
                    j=j+1
                term=term_list[j]
                lemma=st.stem(term)
                #vector=word2vec.ouput_embedding(model,term.lower(),50)
                #bc=BrownClustering.bc_indexing(term.lower(),bc_index)
                mytrain.write(
                    term_list[j] + "\t" + lemma + "\t" + pos_list[sent_id] + "\t" + type_list[sent_id] + "\t" +
                    tag_list[j] + "\n")
                #mytrain.write(term_list[j]+"\t"+lemma+"\t"+pos_list[sent_id]+"\t"+type_list[sent_id]+"\t"+tag_list[j]+"\n")
                #mytrain.write(term_list[j] + "\t" + lemma + "\t" + pos_list[sent_id]  + "\t" +bc+"\t"+ tag_list[j] + "\n")
                sent_id+=1
                j=j+1
            mytrain.write("\n")

    if i%5==0:
        print (str(i) +" files finished")

def generate_XML(crfresult_input,NERxml_output):
    sents,entity=t2c.conll2txt(crfresult_input)
    entity_lists=['Condition','Observation','Drug','Procedure_Device']
    attribute_lists=['Qualifier','Measurement','Temporal_measurement']
    #print >>NERxml_output,"<?xml version=\"1.0\"?>"
    #print >>NERxml_output,"<root>"
    NERxml_output.write("<?xml version=\"1.0\"?>\n")
    NERxml_output.write("<root>\n")
    j=0

    for sent in sents:
        if sent == "":
            continue
        clean_sent=t2c.clean_txt(sent)
       # clean_sent = re.sub('>=', " largerequalthan ", clean_sent.decode('utf-8'))
       # clean_sent = re.sub('<=', " smallerequalthan ", clean_sent)
        #print sent
        #print "===",entity[j]
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
        #print >>NERxml_output,"\t"+"<sent>\n"+"\t\t<text>"+clean_sent+"</text>"
        #print  >>NERxml_output,"\t\t"+entity[j]
        #print >>NERxml_output,"\t"+"</sent>"
        NERxml_output.write("\t"+"<sent>\n"+"\t\t<text>"+clean_sent+"</text>\n")
        NERxml_output.write("\t\t"+entity[j]+"\n")
        NERxml_output.write("\t"+"</sent>\n")
        j+=1
    #print >>NERxml_output,"</root>"
    NERxml_output.write("</root>\n")

def run_crf( model_dir, matrix_dir, output_dir):
    command='crf_test -m '+model_dir+' '+matrix_dir+' > '+output_dir
    os.system(command)

def detect_negation(concept,sent,irules):
        pattern="^\s?(\w?.*\w?)\s?"
        match=re.search(pattern,concept)
        clean_concept=match.group(1)
        words=re.split("\s+",clean_concept)
#        print concept,len(words)
        if len(words)>2:
            words=[words[-2],words[-1]]
            concept=" ".join(words)
           # print concept
        tagger = negTagger(sentence = sent, phrases =[concept], rules = irules, negP=False)
        tag=tagger.getNegationFlag()

        negation="N"
        if tag=="negated":
            negation="Y"

        return negation


# load models
st = LancasterStemmer()
bc_index=BrownClustering.read_bcindex("trained_models/brownclustering.index")

entity_lists=['Condition','Observation','Drug','Procedure_Device']
attribute_lists=['Qualifier','Measurement','Temporal_measurement']
PICO_lists = ['Intervention_Primary','Participant_Primary','Outcome_Primary','Intervention_detail',
              'Participant_detail','Outcome_detail']
tag_included=entity_lists
tag_included.append('Negation_cue')
curpath = os.path.abspath(os.curdir)




def main():


    #===== train =====
    # read file:

    annotation_dir='/Users/tian/Documents/EliIE-master/Tempfile/annotation/train'
    mytrain=codecs.open('/Users/tian/Documents/EliIE-master/Tempfile/pico_train.conll','w')
    txt2matrix_fortrain(annotation_dir,mytrain,PICO_lists,'picotrain',curpath)
    print ("matrix_finished!")

    #myxml=codecs.open('/Users/kangtian/Documents/NER_data/Negation.xml','w')
    #myconll=codecs.open('/Users/kangtian/Documents/NER_data/Negation.matrix')
    #generate_XML(myconll,myxml)
    #print "negation xml finished!"
    '''

    #========== predict ==========


# read files:
    input_dir=sys.argv[1]+"/"+sys.argv[2]
    print ("Reading text from ",input_dir)
    mytrial=codecs.open(input_dir).read()
    match=re.search('^(.*)\.txt',sys.argv[2])
    filename=sys.argv[2]
    if match:
        filename=match.group(1)


    nerxmlname=filename+"_NER_temp.xml"
    output_dir=sys.argv[3]+'/'+nerxmlname
    myxml=codecs.open(output_dir,'w')


    matrix_dir='Tempfile/test_'+filename+  '.matrix'
    mymatrix=codecs.open(matrix_dir,'w')
    crf_result_dir='Tempfile/test_'+filename+'_crf.result'

    ori_sents=mytrial.split("\n")
    sents=[]
    for sent in ori_sents:
        s=nltk.sent_tokenize(sent)
        sents.extend(s)

# make conll matrix
    for sent in sents:

        cleansent=preprocess.preprocess(sent)
        filteredsent=preprocess.ec_filtering(cleansent)
        if filteredsent:
            txt2matrix_fortest(filteredsent,mymatrix,filename)

# run crf to predict and generate temp xml file
    run_crf('trained_models/bc_umls_pos_lemma_bow.model', matrix_dir ,crf_result_dir)
    myconll=codecs.open(crf_result_dir,"r")
    generate_XML(myconll,myxml)


# final step:  predict negation for entities
    NER_tree=ET.ElementTree(file=output_dir)
    root = NER_tree.getroot()
    rfile = open(r'bin/EC_triggers.txt')
    irules = sortRules(rfile.readlines())
    for child in root:

        sent=''
        for child2 in child.findall('text'):
            sent=child2.text
        for child2 in child.findall('entity'):

            if child2.attrib['class']=='Negation_cue':
                continue
            child2.attrib['negated']="N"
            concept=child2.text
            neg_tag=detect_negation(concept,sent,irules)

            child2.attrib['negated']=neg_tag
    print ("negation finished!")
    new_tree_name=filename+"_NER.xml"
    new_output_dir=sys.argv[3]+'/'+new_tree_name
    NER_addneg_tree=codecs.open(new_output_dir,'w')

    NER_tree.write(NER_addneg_tree)
    rm_comand='rm '+matrix_dir+' '+crf_result_dir+' '+output_dir
    os.system(rm_comand)
    '''



if __name__ == '__main__': main()
