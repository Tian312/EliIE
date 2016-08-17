from __future__ import unicode_literals
__author__ = 'kangtian'

import re,nltk
import xml.etree.ElementTree as xml_parser
from web import download_web_data
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

################# download train corpus : start ########################

def get_disease_clinical_trials (ldisease):     #retrieve Trial IDs from clincialtrials.gov
    disease_to_nct = {}
    stat = []
    #ldisease = sorted(map(lambda x:' '.join(x.lower().split()), ldisease))
    trial_ids = []

    i=1
    d = ldisease.replace (',', '')
    fd = d.replace(' ', '+')

    url = 'https://clinicaltrials.gov/ct2/results?cond=%s&displayxml=true'
       # num. of studies available
    if ldisease=='all':
        url='https://clinicaltrials.gov/ct2/results?%sdisplayxml=true'
        fd=''
    print url
    xml = download_web_data(url % (fd))
    xmltree = xml_parser.fromstring (xml)

    n = int(xmltree.get ('count'))
    print n

    i=i+1
    nct = set()
    url_final = url + '&start=%d&count=%s';
    for j in range(1, n, 1):
        if j % 5000 ==0:
            print "id: 0-",j," ..."
        xmltree = xml_parser.fromstring (download_web_data(url_final % (fd, j, 1)))
        lnct = xmltree.findall ('clinical_study')
        for ct in lnct:
            cod = ct.find ('nct_id')
            if cod is None:
                continue
           #print "trial %s"%cod.text
            trial_ids.append((cod.text))

    return trial_ids




def extract_criteria(cid):   #Using IDs to retrieve eligibility criteria
    output = ""
    if cid is not None:
        url_trial = 'http://clinicaltrials.gov/show/%s?displayxml=true'
        #url_trial ='http://clinicaltrials.gov/search?term=%s&displayxml=true'
        page = download_web_data(url_trial % cid)
        #with codecs.open('temp.txt', 'w','utf8') as writer:
        #    writer.write(page)
        #with codec.open('temp.txt', 'r', 'utf8') as reader:
        if page is not None:
            ct_xml = xml_parser.fromstring (page)
            ec = ct_xml.find ('eligibility')
            if ec is not None:
                # parse to get criteria text
                d = ec.find ('criteria')
                if d is not None:
                    txt = d.find ('textblock')
                    if txt is not None:
                        output = txt.text
    return output


def extract_description(cid):   #Using IDs to retrieve eligibility criteria
    output = ""
    if cid is not None:
        url_trial = 'http://clinicaltrials.gov/show/%s?displayxml=true'
        #url_trial ='http://clinicaltrials.gov/search?term=%s&displayxml=true'
        page = download_web_data(url_trial % cid)
        #with codecs.open('temp.txt', 'w','utf8') as writer:
        #    writer.write(page)
        #with codec.open('temp.txt', 'r', 'utf8') as reader:
        if page is not None:
            ct_xml = xml_parser.fromstring (page)
            summary = ct_xml.find ('brief_summary')
            if summary is not None:
                txt = summary.find ('textblock')
                if txt is not None:
                     output = txt.text
            description = ct_xml.find('detailed_description')
            if description is not None:
                txt2 = summary.find('textblock')
                if txt2 is not None:
                    output = output+txt2.text

    return output

def sentence_splitting (texts, slen = 1):           # Split ec into seperated sentences.
    if len(texts) <= 0:
        return []

    # splitting
    sentences = []
    text_sents = nltk.sent_tokenize(texts)
    if (text_sents != [''] and len(text_sents) >  0):
        for sent in text_sents:
            sent=re.sub('e.g.','eg',sent)
            sent = sent.strip().split('\r') # split strings that contains "\r"
            for sen in sent:
                se = re.split('[.;]',sen)

                for s in se:
                    ss=s.split('-  ')
                    for final in ss:
                        #print final

                        match=re.match('^\d+\.\s*$',final)
                        if match:
                            continue
                        final=re.sub('\s+$','',final)
                        final=re.sub('\d+\.','',final)
                        final=final.encode('utf-8').decode('utf-8','ignore').encode("utf-8")
                        words=final.decode('ascii', 'ignore').split(' ')
                        new_words=[]
                        for w in words:
                            if w:
                                #print "=="+w+"=="
                                match=re.search('(\(*\w+\)*,*.*)',w)
                                if match:
                                    #print match.group(1)
                                    new_words.append(match.group(1))
                        new_sent=' '.join(new_words)
                        if new_sent:
                            sentences.append(new_sent)
                            #print new_sent


    return sentences


def retrieve_train_corpurs(input_condition,new_trian_addresss): # Main function, retrieve ec and stemmed the words, save into files
    myfile=open(new_trian_addresss,'w')
    print '...retrieving the train corpus on ' + input_condition + '...'
    list=get_disease_clinical_trials(input_condition)
    print "...trial_id retrieved!"
    i=0
    for id in list:
        i+=1
        if i%10000==0:
            print "...0- ",i," texts retrieved..."
        print >>myfile,'>>'+id
       # print id
        ec=extract_criteria(id)

        sents=preprocessing(ec,slen=1)
        for s in sents:
            #print s
            print >>myfile,s
    print 'train corpus are successfully retrieved !'

################# download train corpus : END ########################


#retrieve_train_corpurs('type II diabetes','files/DMII.txt')
#a=extract_criteria("NCT00000105")
#print a

def stem_sent(sent):        # stem the words and remove the numbers and other symbols
    words=sent.split(' ')
    stem=[]
    for w in words:
        W=re.match('^[\W+|\d+]$',w)
        if W:
            continue
        #stem.append(st.stem(w))
        stem.append(w)
    stemmed_sent=' '.join(stem)
    return stemmed_sent

def remove_stopwords(sent):# remove the English stop words in the sentence
    stopwords_list=(stopwords.words('english'))
    list=['years','year','months','month','day','days']
    for w in list:
        stopwords_list.append(w)
    new_sent = ' '.join([word for word in sent.decode('ascii', 'ignore').split() if word not in stopwords_list])
    return new_sent

