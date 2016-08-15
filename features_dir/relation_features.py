__author__ = 'Tian Kang'


import re,os
from practnlptools.tools  import Annotator

import networkx as nx
import nltk



# label index:
# 0: no relation
# 1: has value
# 2: has_temporal measurement
# 3: modified by
left_labels={'Condition':1,'Observation':2,'Procedure_Device':3,'Drug':4} # delete 'Qualifier':0,
right_labels={'Qualifier':0,'Temporal_measurement':-1,'Measurement':-2}

def generate_pairs (sent_node,relation_scale,relation_hash={}): # After NER, generate all possible relation pairs and features.
    '''
    exmample : sent_node.tag= text or entity
    <sent>
		<text>- Cognitive Global Rating consistent with mild impairment or deterioration from premorbid baseline .</text>
		<entity class='Observation' index='T3' start='1'> Cognitive Global Rating </entity>
		 <entity class='Qualifier' index='T4' start='6'> mild </entity>
		 <entity class='Condition' index='T5' start='7'> impairment </entity>
		 <entity class='Condition' index='T6' start='9'> deterioration </entity>

    </sent>
    '''
    pairs=[]
    entity={}
    group={}
    index={}
    starts=[]

    for child in sent_node:
        #print child.text,"=="

        if child.tag=="text":
            sent=child.text
            sent=re.sub('\(',' LRB ',sent)
            sent=re.sub('\)',' RRB ',sent)

        if child.tag=="entity" or child.tag=='attribute':
            starts.append(child.attrib['start'])
            entity[child.attrib['start']]=child.text
            group[child.attrib['start']]=child.attrib['class'] # group[location]=entity_class
            index[child.attrib['start']]=child.attrib['index'] # group[location]=entity_index
                                                                  # relation_hash[index1_index2]=relaiton_class
    words=sent.split()
    len_start=len(starts)
    if  len(starts)<1:
        return 0
    for i in range(0,len(starts)): # process every possiblity of comibination of the entities
        #print i,
        #if i+1==1 and len_start==1:
         #   len_start=2
        for j in range(i,len_start):
            if i==j:
                continue
            #print i,j,len(starts)
            i_start=starts[i]
            j_start=starts[j]
            i_class=group[i_start]
            j_class=group[j_start]
            i_entity=entity[i_start]
            j_entity=entity[j_start]
            i_index=index[i_start]
            j_index=index[j_start]

            j_words=j_entity.split()
            i_words=i_entity.split()
            j_word=j_words[-1]
            i_word=i_words[-1]
            j_loc=int(j_start)+len(j_words)-1
            i_loc=int(i_start)+len(i_words)-1

        #===    print i,j,i_index,j_index,i_class,j_class
            possible=0
            onlyentity_right=0
            onlyentity_left=0
            left_label=0
            right_label=0
            shortestpath=0
            feature_line=""

            '''
            Features lable:
                1. left entity label (0/1/2/3/4)
                2. right entity label (0/-1/-2)
              #  3. Possible relation (0/1)
                3. only entity left (0/1)
                4. only entity right (0/1)
                5. shortest path in depenency tree (integer)
            '''

            if i_class in left_labels.keys():
                if j_class in right_labels.keys():        # 1. i - possible left entity, j - possible right enetity

    #====                print "===",m,i_index,i_class,j_index,j_class
                    left_label=left_labels[i_class]
                    right_label=right_labels[j_class]
                    possible=1
                    onlyentity_left=is_onlyentity(i_class,group)
                    onlyentity_right=is_onlyentity(j_class,group)

                    #print i_word,i_loc,i_index,j_word,j_loc,j_index
                    shortestpath=generate_shortestpath(sent,i_word,i_loc,j_word,j_loc)
                    truelabel=get_truelabel(i_index,j_index,relation_hash)
                    pair_index=i_index+"_"+j_index
                    feature_line="0\t1:"+str(left_label)+"\t2:"+str(right_label)+"\t3:"+str(onlyentity_left)+"\t4:"+str(onlyentity_right)+"\t5:"+str(shortestpath)
                    print >>relation_scale,feature_line

                    pairs.append(str(i_index)+"_"+str(j_index))
                    #print feature_line


            if i_class in right_labels.keys():
                if j_class in left_labels.keys():        # 2. i - possible right entity, j - possible left enetity

    #===                print "----",n,j_index,i_index,j_class,i_class
                    left_label=left_labels[j_class]
                    right_label=right_labels[i_class]
                    possible=1
                    onlyentity_left=is_onlyentity(j_class,group)
                    onlyentity_right=is_onlyentity(i_class,group)

                    #print i_word,i_loc,i_index,j_word,j_loc,j_index
                    shortestpath=generate_shortestpath(sent,j_word,j_loc,i_word,i_loc)
                    truelabel=get_truelabel(j_index,i_index,relation_hash)
                    pair_index=j_index+"_"+i_index
                    feature_line="0\t1:"+str(left_label)+"\t2:"+str(right_label)+"\t3:"+str(onlyentity_left)+"\t4:"+str(onlyentity_right)+"\t5:"+str(shortestpath)
                    print >>relation_scale,feature_line
                    pairs.append(str(j_index)+"_"+str(i_index))
                    #print feature_line
                                       # no possible relation

    return pairs

def is_onlyentity(entity_class,class_hash):
    i=0
    is_only=0
    left_class=['Condition','Observation','Procedure_Device','Drug']
    right_class=['Temporal_measurement','Measurement']

    if entity_class in left_class:
        entity_class=left_class
    if entity_class in right_class:
        entity_class=right_class
    if entity_class =='Qualifier':
        entity_class=['Qualifier']

    for c in class_hash.values():
        if c in entity_class:
            i+=1
    if i>1:
        is_only=0
    else:
        is_only=1
    return is_only


def generate_shortestpath (sent,left_term,left_start,right_term,right_start):
    annotator = Annotator()
    #print "========before:",left_term,left_start,right_term,right_start

    '''
    left_sent=" ".join(sent.split()[:left_start])
    right_sent=" ".join(sent.split()[:right_start])
    if re.search("[A-Za-z]-[A-Za-z]",left_term):
        info=left_term.split("-")
        left_term=info[-1]
        #left_start=left_start-1
    if re.search("[A-Za-z]-[A-Za-z]",right_term):
        info=right_term.split("-")
        right_term=info[-1]
       # right_start=right_start-1
    '''
    right_term=re.sub('\(','LRB',right_term)
    right_term=re.sub('\)','RRB',right_term)
    left_term=re.sub('\(','LRB',left_term)
    left_term=re.sub('\)','RRB',left_term)
    new_left_start,new_left_term,new_right_start,new_right_term=update_loc(sent,left_start,right_start)



    '''
    # adjust start coordination # denpendency parser wil split " - " and "'s"

   # print "left: ", left_sent
   # print "right: ",right_sent

    poss=re.compile('\w+\'s')
    conj=re.compile('[A-Za-z]+\-[A-Za-z]+')
    comma=re.compile('\w,')

    result_poss_left=poss.findall(left_sent)
    result_conj_left=conj.findall(left_sent)
    result_comma_left=comma.findall(left_sent)
    left_start=left_start+len(result_conj_left)*2+len(result_poss_left)+len(result_comma_left)
    #print "left:",len(result_conj_left),len(result_poss_left)

    result_poss_right=poss.findall(right_sent)
    result_conj_right=conj.findall(right_sent)
    result_comma_right=comma.findall(right_sent)
    right_start=right_start+len(result_conj_right)*2+len(result_poss_right)+len(result_comma_right)
   # print "right:", len(result_conj_right),len(result_poss_right),len(result_comma_right)

    print "after:",left_term,left_start,right_term,right_start
    '''

    left=new_left_term+"-"+str(new_left_start)
    right=new_right_term+"-"+str(new_right_start)
    #print "=====",left,right
    #sent=re.sub('\-',' - ',sent)
    #print sent

    sent=re.sub('\(','LRB',sent)
    sent=re.sub('\)','RRB',sent)

    #print sent
    dep_parse=annotator.getAnnotations(sent, dep_parse=True)['dep_parse']
    tree=annotator.getAnnotations(sent, dep_parse=True)['syntax_tree']
    #print dep_parse
    dp_list = dep_parse.split('\n')
    pattern = re.compile(r'.+?\((.+?), (.+?)\)')
    edges = []
    for dep in dp_list:

        #print dep

        m = pattern.search(dep)
        if m:
            edges.append((m.group(1), m.group(2)))
    graph = nx.Graph(edges)
    #print right
    if right not in graph.nodes():
        print "right",left_term, right_term
        return "right"
    if left not in graph.nodes():
        print "left", left_term, right_term
        return "left"
    shorttest_path=nx.shortest_path_length(graph, source=left, target=right)
   # print
    return  shorttest_path


def update_loc(sent,left_start,right_start):
    annotator = Annotator()
    sent=re.sub('\(','LRB',sent)
    sent=re.sub('\)','RRB',sent)
    words=sent.split()
    #print words[left_start],words[right_start]
    words[left_start]=words[left_start]+'aaaaa'
    words[right_start]=words[right_start]+'bbbbb'
  #  print words

    sent=' '.join(words)
    tags=annotator.getAnnotations(sent)
   # print "===", tags

   # print "chunks:      ", tags['chunk']
    i=0
    pre_word=''
    pre_pre_word=''
    j=0
    left_term = ''
    right_term = ''


    for word in tags['chunk']:
        i+=1
        left_pattern='^(.*)aaaaa$'
        right_pattern='^(.*)bbbbb$'
        left=re.search(left_pattern,word[0])
        right=re.search(right_pattern,word[0])


        if left:
            #print "ttleft"
            left_term=left.group(1)
            left_start=i
            if left_term=='':
                left_term=pre_word
                left_start=left_start-1
                j=1
                if pre_word=='-':
                    left_term=pre_pre_word
                    left_start=left_start-1


        if right:
            #print "rightright"
            right_term=right.group(1)
            right_start=i
            if right_term=='':
                right_term=pre_word
                right_start=right_start-1
                j=2
                if pre_word=='-':
                    right_term=pre_pre_word
                    right_start=right_start-1

        pre_pre_word=pre_word
        pre_word=word[0]
    if j==1:
        if right_start>left_start:
            right_start=right_start-1
    if j==2:
        if left_start>right_start:
            left_start=left_start-1
    #print j
    #print "=++++", left_start,left_term,right_start,right_term
    return (left_start,left_term,right_start,right_term)

#sent = '- co-medication with NSAIDs ( longterm medication ) ( ASS is not an exclusion criteria ) , Gingko- or other natural extracts , other anti-dementiva except of Donepezil .'
#print generate_shortestpath(sent,'Gingko-',17,'other',19)

def get_truelabel(left_index,right_index,relation_hash):
    key=left_index+"_"+right_index
    truelabel=0
    #print key
    if key in relation_hash.keys():
        truelabel=relation_hash[key]
    return truelabel
