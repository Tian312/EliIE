'''
 	Retrieve Disease - NCT associations starting from a list of diseases

 	@author: Praveen Chandar
'''
from collections import defaultdict
import logging
import xml.etree.ElementTree as xml_parser
import urllib2, urllib3, json
import argparse, sys
import cPickle as pickle
import os, sys, re, string, math


# define the script global logger
def strd_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

log = strd_logger('disease-nct-association')


# get the html source associated to a URL
def download_web_data(url):
    try:
        con = urllib3.connection_from_url(url)
        html = con.urlopen('GET', url, retries=500, timeout=10)
        con.close()
        return html.data
    except Exception as e:
        log.error('%s: %s' % (e, url))
        return None

def mine_disease_to_nct(ldisease, fout=None, ctmin=100):
    url = 'http://clinicaltrials.gov/search?cond=%s&displayxml=true&count=%s'
    log.info('found %d disease to process \n' % len(ldisease))
    ldisease = sorted(map(lambda x: ' '.join(x.lower().split()), ldisease))
    trial2disease = defaultdict(list)
    disease2trial = defaultdict(list)
    for d in sorted(ldisease):
        log.info('processing: "%s"' % d)
        d = d.replace(',', '')
        fd = d.replace(' ', '+')

        # number of trials
        xmltree = xml_parser.fromstring(download_web_data(url % (fd, '0')))
        nres = xmltree.get('count')
        try:
            if int(nres) < ctmin:
                log.info(' --- found only %s trials - skipping \n' % nres)
                continue
        except Exception as e:
            log.error(e)
            continue

        # list of trials
        xmltree = xml_parser.fromstring(download_web_data(url % (fd, nres)))
        lnct = xmltree.findall('clinical_study')
        for ct in lnct:
            try:
                cod = ct.find('nct_id')
                trial2disease[cod.text].append(d)
                disease2trial[d].append(cod.text)
            except Exception as e:
                log.error(e)

    return (disease2trial,trial2disease)


def read_file(filename, struct=1, logout=True):
    try:
        fid = open(filename, 'r')
        if struct == 2:
            # set
            data = set()
            for line in fid:
                if len(line) > 0:
                    data.add(line.strip())
        else:
            # default - list
            data = []
            for line in fid:
                if len(line) > 0:
                    data.append(line.strip())
        fid.close()
        return data
    except Exception as e:
        if logout is True:
            log.error(e)
        return None

#======================
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


#==============

def serialize_mapping(outpath, disease2trial, trial2disease):
    #pickle.dump(disease2trial, open(outFolder + '/disease2Trail.pkl', 'wb'))
    #pickle.dump(trial2disease, open(outFolder + '/trial2Disease.pkl', 'wb'))

    # Iterate over NCT trials
    outText = open(outpath, 'wb')

    for trial in trial2disease.keys():
        for diease in trial2disease[trial]:
            outText.write(trial+'\n')
    outText.close


'''
	main function
'''
# processing the command line options
def _process_args():
    parser = argparse.ArgumentParser(description='Download the Disease - NCT Association')

    # file with the list of disease
    parser.add_argument(dest='fdis', help='list of disease file')
    # output file
    parser.add_argument('-o', default=None, help='output Folder (default: None')
    # minimum number of trial allowed
    parser.add_argument('-m', default=100, type=int, help='minimum number of trial allowed (default: 100)')
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = _process_args()

    ldisease = read_file(args.fdis)
    if ldisease is not None:
        (disease2trial, trial2disease) = mine_disease_to_nct(ldisease, args.o, args.m)
        serialize_mapping(args.o, disease2trial, trial2disease)

    else:
        log.error('no disease found - interrupting')
    log.info('task completed \n')

