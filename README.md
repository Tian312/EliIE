# CTEC_Parser

__INTRODUCTION__
------------
A parser designed for free text clinical trial eligibility criteria (CTEC).
Parsing free text CTEC and formalizing into [OMOP CDM v5 table](http://omop.org/CDM)
Developed in [Dr. Chunhua Weng's lab](http://people.dbmi.columbia.edu/~chw7007) in Department of Biomedical Informatics at Columbia   


__Author__: Tian Kang  
__Affiliation__: Department of Biomedical Informatics, Columbia University    
__Contact Email__: tk2624@cumc.columbia.edu     
__Last updated__: June 2016      
__Version__: 1.0      

Including 3 primary steps:  
1. __Entity recogntion__     
2. __Attribute recognition__     
3. __Clinical relation identification__     


__USER GUIDE__
----------

`Fast Usage`:  
1. open parsing.sh    
2. set the parameter lists to your task-based ones  
3. run "`sh parsing.sh`" and parsing results will be generated in XML files.      
(Directly running "sh parsing.sh" without changing see example output)


`Step-by-stey Usage`:        
1. NER step: run  
    `python NamedEntityRecognition.py $1:<input directory> $2:<input text name> $3:<output directory>`     
2. Clinical Relation:  run   
    `python Relation.py $3:<output directory> $2:<input text name>`   

(Example commands:      
    1. `python NamedEntityRecognition.py Tempfile test.txt Tempfile`      
    2. `python Relation.py Tempfile test.txt`     
The example output would be Tempfile/test_NER.xml and Tempfile/test_Parsed.xml)     


__Prerequired Installation:__  
-------

1.  this script assumes MetaMap is installed and requires that the MetaMap support services are running. If you have MetaMap installed in `$MM`, these can be started as:       
    `$MM/bin/skrmedpostctl start`  
    `$MM/bin/wsdserverctl start`  


2.  python package:   
    **nltk**  
    **networkx**  
    **codecs**  
    [**libsvm**](https://www.csie.ntu.edu.tw/~cjlin/libsvm)   
    [**practnlptools**](https://pypi.python.org/pypi/practnlptools/1.0)

[BACK TO TOP](#readme)



