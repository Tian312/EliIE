__author__ = 'kangtian'

import os, sys,re,string
import codecs
import read_file

ann_files=read_file.get_file_list('/Users/kangtian/Documents/NER_data/Shruti_Alzh_check_175/',['ann'])

t_index=0;
r_index=0;



for ann_file in ann_files:
    match=re.search('^(.*)\.ann',ann_file)
    name=match.group(1)
    command_term="grep \'^T\' "+ann_file+" |wc -l"
    command_relation="grep \'^R\' "+ann_file+" |wc -l"
    num_term=os.popen(command_term).read()
    new_num_term=re.search("(\d+)",num_term)
    num_relation=os.popen(command_relation).read()
    new_num_relation=re.search("(\d+)",num_relation)

   #=====
    myann=codecs.open(ann_file)
    #print "==="+myann
    new_annname=name+'_new.ann'
    myann_new=codecs.open(new_annname,'w')
    for line in myann:
        line=line.rstrip()
        info=line.split()
        #print "line:== "+line

        if re.search("^T",info[0]):
            #print "ori:   "+info[0]
            match=re.search('^T(\d+)$',info[0])
            index=int(match.group(1))+t_index
            new_index="T"+str(index)
            info[0]=new_index
            #print "after: "+ info[0]
        if re.search('^R',info[0]):
            match=re.search('^R(\d+)$',info[0])
            index=int(match.group(1))+r_index
            new_index="R"+str(index)
            info[0]=new_index

            match1=re.search("Arg1\:T(\d+)$",info[2])
            arg1=int(match1.group(1))+t_index
            match2=re.search("Arg2\:T(\d+)$",info[3])
            arg2=int(match2.group(1))+t_index
            info[2]="Arg1:T"+str(arg1)
            info[3]="Arg2:T"+str(arg2)

            #print "after: "+ info[0]
        new_line= "\t".join(info)
        #print new_line
        print >>myann_new,new_line




   # add new terms
    t_index=t_index+int(new_num_term.group(1))
    r_index=r_index+int(new_num_relation.group(1))

  #  myraw=codecs.open(ann_file).read()
  #  match=re.search('^(.*)\.ann',ann_file)
  #  name=match.group(1)
