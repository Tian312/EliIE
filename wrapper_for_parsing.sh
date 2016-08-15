#!/bin/bash
# author: Tian Kang (tk2624@cumc.columbia.edu)

# Simple wrapper for the eligibility criteria parser.
# Before running the parser, please change the @arguements to your personal dir and files
#
# NOTE: this script assumes MetaMap is installed and requires that
# the MetaMap support services are running. If you have
# MetaMap installed in $MM, these can be started as
#
#    $MM/bin/skrmedpostctl start
#    $MM/bin/wsdserverctl start
#
# Required python pacakage:
#   nltk suites
#   networkx
#   codecs
#   libsvm  (https://www.csie.ntu.edu.tw/~cjlin/libsvm , https://github.com/cjlin1/libsvm/tree/master/python)
#   practnlptools   (https://pypi.python.org/pypi/practnlptools/1.0)

#!!!! Personalize your parameters before parsing !!!!#

INPUT_DIR='Tempfile'        # change to your input dir
INPUT_TEXT='temp.txt'          # change to your input .txt file name
OUTPUT_DIR='Tempfile'        # change to your output dir


python NamedEntityRecognition.py $INPUT_DIR $INPUT_TEXT $OUTPUT_DIR
echo "Named Entity Recognition Finished!"
python Relation.py  $OUTPUT_DIR $INPUT_TEXT
echo "Parsing Finished!"
