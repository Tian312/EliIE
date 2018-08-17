# EliIE (Eligiblity Criteria Information Extraction)

__Introduction__
------------
A parser designed for free text clinical trial eligibility criteria (CTEC).
Parsing free text CTEC and formalizing into [OMOP CDM v5 table](http://omop.org/CDM)  
The parser was trained on 250 clinical trials on Alzheimer's. The annotation guidelines is in folder Supple Materials.  

Developed in [Dr. Chunhua Weng's lab](http://people.dbmi.columbia.edu/~chw7007) in Department of Biomedical Informatics at Columbia   


__Author__: Tian Kang  
__Affiliation__: Department of Biomedical Informatics, Columbia University    
__Contact Email__: tk2624@cumc.columbia.edu     
__Last update__: June 20, 2016  (add Negation detection in NER step)       
__Version__: 1.0      
__Citation__:[EliIE: An open-source information extraction system for clinical trial eligibility criteria](https://academic.oup.com/jamia/article/24/6/1062/3098256)

Primary steps:  
1. __Entity recogntion__     
2. __Attribute recognition__     
3. __Clinical relation identification__   
4. __Data standardization__  

Exmaple input:   
  
![](https://github.com/Tian312/CTEC_Parser/blob/master/Supp%20Materials/example_input.png)

Example output:   

![](https://github.com/Tian312/CTEC_Parser/blob/master/Supp%20Materials/example_output.png)

__User Guide__    
----------
First download all codes and decompress  

__Fast Usage:__  
1. open `wrapper_for_parsing.sh`    
2. set the parameter lists to your task-based ones  
3. run "`sh wrapper_for_parsing.sh`" and parsing results will be generated in XML files.      
(See example output directly running "`sh wrapper_for_parsing.sh`" without changing )


__Step-by-stey Usage:__       
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

1.  This parser assumes [MetaMap](https://metamap.nlm.nih.gov) is installed and requires that the MetaMap support services are running. If you have MetaMap installed in `$MM`, these can be started as:       
    `$MM/bin/skrmedpostctl start`  
    `$MM/bin/wsdserverctl start`        

    Go to `features_dir` and open `metamap_tag.sh`; follow the guidance to change the MetaMap root dir and start running  

2.  Python package required:   
    **nltk**  
    **networkx**  
    **codecs**  
    [**libsvm**](https://www.csie.ntu.edu.tw/~cjlin/libsvm)   
    [**practnlptools**](https://pypi.python.org/pypi/practnlptools/1.0)

3.  CRF ++   
Easy installation following the instruction: https://taku910.github.io/crfpp/

__Functions Under Developing__
-------

1. Stadardize entities and attributes concepts using [OHDSI standards](http://www.ohdsi.org/data-standardization/)  
2. Convert the final format into JSON  
3. Extend use case to more diseases  

[BACK TO TOP](#readme)



