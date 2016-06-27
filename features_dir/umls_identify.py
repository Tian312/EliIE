__author__ = 'Tian Kang'

import sys,os,re,string,codecs



# gengerate input trial format for MetaMap: (input is generated from t2c.text2conll, sents are seperated by '####')
def formating_for_metamap(sent):
    id=0
    temp_output=codecs.open('/Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_input.temp','w')
    print >>temp_output,str(id)+'|'+sent

    os.system('sh /Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_tag.sh /Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_input.temp >/dev/null')
    metamap_output=codecs.open("/Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_input.temp.out")
    os.system("rm /Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_input.temp.out /Users/kangtian/Documents/NER_data/NER/parser_code/features/metamap_input.temp")
    return(metamap_output)

#lable terms with B: begin of UMLS concept, I : in the concept, O, no
def label_umls_cui(metamap_output,sent):
    start_pos={}
    changed_location={}
    for line in metamap_output:
        info=line.split('|')
        #if info[1] != 'MM':
        #    continue

        try :
            if info[1] != 'MM':
                continue
        except IndexError:
            print "INDEX ERROR!!!!!!"

        type=info[5]
        position=info[8]

        if len(info)>=10:
            add=re.search(":",info[9])
            if add:
                position=position+','+info[9]

        positions=position.split(',')
        for pos in positions:
            coor=pos.split(":")
            start=int(coor[0])-2
            end=start+int(coor[1])
            flag=0
            for s in start_pos.keys(): # when overlap, choose the term with higher score (show up ealier)
                if start in range(s,start_pos[s]+1):
                    flag+=1
            if flag>0:
                continue
            terms=sent[start:end].split()
            flag=0
            tagged_term=""
            for term in terms:
                if flag==0:
                    tagged_term=term+'__B-'+type
                    flag+=1
                else:
                    tagged_term=tagged_term+" "+term+'__I-'+type
                #print tagged_term
            start_pos[start]=end

            new_coor=str(start)+":"+str(end)
            changed_location[start]=tagged_term
    #print sorted(changed_location.keys())
    new_sent=""
    context_start=0
    for i in sorted(changed_location.keys()):
        #print "context: ", context_start
        #print "tagged: ", i,start_pos[i]
        if i<=context_start:
            new_sent=new_sent+changed_location[i]+" "
            context_start=start_pos[i]+1
        else:
            context_end=i-1
            new_sent=new_sent+sent[context_start:context_end]+" "+changed_location[i]+" "
            context_start=start_pos[i]+1
    #print context_start,len(sent.rstrip())
    if context_start<=len(sent.rstrip()):
        #print "context: ", context_start
        new_sent=new_sent+sent[context_start:]
    #print new_sent
    new_terms=new_sent.split()
    term_list=[]
    type_list=[]
    for term in new_terms:
        tag=re.search("__",term)
        if tag:
            term_list.append(term.split("__")[0])
            type_list.append(term.split("__")[1])
        else:
            term_list.append(term)
            type_list.append("O")

    #os.system("rm /Users/kangtian/Documents/NER_data/NER/code/features/metamap_input.temp /Users/kangtian/Documents/NER_data/NER/code/features/metamap_input.temp.out")
    return term_list,type_list

