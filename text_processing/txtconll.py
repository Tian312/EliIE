__author__ = 'tian kang'
import os, re,  string
import sys,codecs


# Feb. 2016
# This function is to transform format between raw text and  CoNLL format

def txt2conll(text_line,label_sign):

# clean text; punctuation problems

    text_line=text_line.strip()
    if re.search("[\:|\?]\.$",text_line):
        text_line=re.sub("\.$","",text_line)
    end=re.search("\.(\s)",text_line)
    if end:
        text_line=re.sub("\.\s"," ."+end.group(1),text_line)

 # text could be raw text or labelled text from annotation
    if label_sign == 0: # is the raw text without the annotation, only need to return one term list
        term_list=text_line.split()
        return(term_list)
    if label_sign == 1: # is the labelled text, need to return two lists: term list & label list
        raw_list=text_line.split()
        term_list=list()
        label_list=list()
        index_list=list()
        for term in raw_list:
            if re.search('__[B|I]',term):
                #print term
                info=term.split("__")
                term_list.append(info[0])
                label_list.append(info[1])
                index_list.append(info[2])
            else:
                term_list.append(term)
                label_list.append("O")
                index_list.append("O")
        return term_list,label_list,index_list

def conll2txt (conll_file):
    sent_flag=0 #

    term_flag=0 #
    term_label="O"
    entitiy_count=0;
    sents=[]
    entity=[]
    raw_terms=[]
    terms=[]
    i=0
    for line in conll_file:
        line=line.strip()
        line=re.sub(">>NCT","##NCT",line)
        line=re.sub("<=","smaller_equal_than",line)
        line=re.sub(">=","larger equal_than",line)
        line=re.sub("<","smaller_than",line)
        line=re.sub(">","larger_than",line)



        if not line.strip():
            if term_flag>0:
                last_label="</entity>\n\t\t"
                terms.append(last_label)
                term_flag=0
            new_line=" ".join(raw_terms)



            concept=" ".join(terms)
            entity.append(concept)
            sents.append(new_line)
            terms=[]
            term_flag=0
            raw_terms=[]
            i=0
        else:

            if re.search("##NCT",line):
                line=re.sub("##","",line)
            #line=re.sub("\<=","is_less_equal_than",line)
            line=re.sub("\:","",line)
            #line=re.sub("\>=","is_greater_equal_than",line)
            #line=re.sub("\<","is_less_than",line)
            #line=re.sub("\>","is_greater_than",line)
            line=re.sub("&","and",line)
            info=line.split()
            word=info[0]

            raw_terms.append(word)
            is_entity=re.search('B\-',info[-1])
            if is_entity:
                entitiy_count+=1
                index="T"+str(entitiy_count)
            else:
                index=" "
            label=info[-1]
            raw_index=info[-2]

            if term_flag > 0 and re.search("^B",label):
                last_label="</entity>\n\t\t"
                terms.append(last_label)
                term_flag=0


            if label=="O":
                if term_flag>0:
                    word="</entity>\n\t\t"
                    term_flag=0
                    terms.append(word)

            else:
                term_flag+=1
                if re.search("^B\-",label):
                    match=re.search("^B\-(.*)$",label)
                    term_label=match.group(1)
                    word="<entity "+ "class="+"\'"+term_label+"\'"+" index="+"\'"+index+"\'"+" start="+"\'"+str(i)+"\'"+"> "+word

                terms.append(word)
            i+=1
    return sents,entity




def clean_txt(tagged_text): # from tagged_text to raw_text

   # clean_text=re.sub("index=\'T\d+\'","",tagged_text)
    clean_text=re.sub("\<\w+\ >","",tagged_text)
    clean_text=re.sub("\<\/\w+\>","",clean_text)
    return clean_text

