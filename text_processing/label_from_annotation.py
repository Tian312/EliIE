__author__='tian kang'
import nltk
import sys,os,re,string


# Feb. 2016 by Tian Kang
# import the annotation from the .ann files
# and label the term with "__"
# now the labels include:
#Qualifier
#Condition
#Drug
#Observation
#Procedure_Device
#Temporal_measurement
#Measurement
#Location
#Person
#Negation_cue

def ann_tagging(ann_file,raw_text):
    letters=list(raw_text.rstrip())
# start tagging from annotation file
    for line in ann_file:
        if re.search("^R\d+",line):
            info=line.split()
            relation=info[1]
            arg1=info[2]
            arg2=info[3]

        if re.search("^T\d+",line):
            info=line.split()
# e.g.,
# T30	Condition 3109 3129	cognitive impairment
            tag=info[1]
            index=info[0]

            if tag=='Negation_cue':
                continue
            if tag=='Anatomic_location':
                continue
            if tag=='Person':
                continue
            #print "============"+tag
            pos1=int(info[2])-1
            pos2=int(info[3])
            del info[0]
            del info[0]
            del info[0]
            del info[0]
            begin=0
            term_tagged=""
            #print info
            old_term=' '.join(info)
            multi=re.search('\w\/\w', old_term)
            pun=re.search("([<>=])(\d)",old_term)
            brasket_left=re.search("\((\S)",old_term)
            brasket_right=re.search("(\S)\)",old_term)
            term_left=re.search("(\S)\(",old_term)
            right_term=re.search("\)(\S)",old_term)

            if multi:

                terms=old_term.split('/')
                #print terms
                new_term=terms[0]+' / '+terms[1]
            else:
                new_term=old_term
            if pun:
                new_term=re.sub(pun.group(1)+pun.group(2),pun.group(1)+" "+pun.group(2),new_term)
            if brasket_left:
                new_term=re.sub("\("+brasket_left.group(1),"( "+brasket_left.group(1),new_term)
            if brasket_right:
                new_term=re.sub(brasket_right.group(1)+"\)",brasket_right.group(1)+" )",new_term)
            if term_left:
                new_term=re.sub(str(term_left.end(1))+"\(",str(term_left.group(1))+" (",new_term)
            if right_term:
                new_term=re.sub("\)"+str(right_term.end(1)),") "+str(right_term.group(1)),new_term)


     #========================test==========
            unit=re.search("\[AV\]",new_term)
            if unit:
                print new_term
     #=============
            info=new_term.split()

            for term in info:
                '''
                term=re.sub('\(','\(',term)
                term=re.sub('\)','\)',term)
                term=re.sub('\[','\\\[',term)
                term=re.sub('\]','\\\]',term)
                term=re.sub('\+','<>',term)
                term=re.sub('\^','',term)
                term=re.sub('\*','',term)
                '''
                #self=re.search(term,term)
                if begin==0:
                    word_tagged=term+"__B-"+tag+"__"+index+" "
                    #========================test==========
                    if unit:
                        print term+"=="+word_tagged
                    #==============================================
                    begin+=1
                    term_tagged=term_tagged+" "+word_tagged
                else:
                    word_tagged=term+"__I-"+tag+"__O"
                     #========================test==========
                    if unit:
                        print term+"=="+word_tagged
                    #========================test==========
                    begin+=1
                    term_tagged=term_tagged+" "+word_tagged
                '''
                if begin==0:
                    word_tagged=re.sub(term,term+"__B-"+tag+" ",term)
                    #========================test==========
                    if unit:
                        print term+"=="+word_tagged
                    #==============================================
                    begin+=1
                    term_tagged=term_tagged+" "+word_tagged
                else:
                    word_tagged=re.sub(term,term+"__I-"+tag+" ",term)
                    #========================test==========
                    if unit:
                        print term+"=="+word_tagged
                    #========================test==========

                    begin+=1
                    term_tagged=term_tagged+" "+word_tagged
            '''

            #term_tagged=re.sub("\\\\",'',term_tagged)
            #term_tagged=re.sub('<>','+',term_tagged)
            letters[pos2-1]=term_tagged
            for i in range(pos1,pos2-1):
                letters[i]=" "
    text_tagged=''.join(letters)
    text_tagged=re.sub("e\.g\.","eg ",text_tagged)
    context_multi=re.findall('\w/\w',text_tagged)
    for m in context_multi:
        info=re.search('(\w)/(\w)',m)
        if info:
            text_tagged=re.sub(m,info.group(1)+' / '+info.group(2),text_tagged)

    #print text_tagged
    return text_tagged

def ann_relation(ann_file,relation_hash,term_index):
# modeified by 0
# has _value  1
# has TemMea  2
    for line in ann_file:
        if re.search("^T",line):
            info=line.split()
            del info[0]
            del info[0]
            del info[0]
            del info[0]
            term=" ".join(info)
            term_index[info[0]]=term

        if re.search("^R",line):
            info=line.split()
            match1=re.search("Arg1\:(T\d+$)",info[2])
            match2=re.search("Arg2\:(T\d+$)",info[3])
            key=match1.group(1)+"_"+match2.group(1)
            value=1
            if (info[1] == "has_TempMea"):
                value=2
            if (info[1] == "modified_by"):
                value=3
            if (info[1] == "has_value"):
                value=1
            relation_hash[key]=value
    return(relation_hash,term_index)