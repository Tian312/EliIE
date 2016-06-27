__author__ = 'kangtian'
import os,nltk


sent='patients aged  >= 20 years who undergo a screening , surveillance or diagnostic colonoscopy and are subsequently found to have colorectal polyps measuring 3 - 9 mm in size. ( 2 ) Patients who signed an informed consent .'
os.popen("echo '"+sent+"' > ~/stanfordtemp.txt")
parser_out = os.popen("~/stanford-parser-full-2015-12-09/lexparser.sh ~/stanfordtemp.txt >~/output").readlines()
print parser_out
#for i in parser_out:
#    print i.strip()
#parser_outbracketed_parse = " ".join( [i.strip() for i in parser_out if i.strip()[0] == "("] )

#print parser_outbracketed_parse