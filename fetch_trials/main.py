__author__ = 'kangtian'
import os
import sys,string,re,csv
import unidecode
import encodings
import fetch_disease_trial_mapping as fetch_id

import retrieve_texts as retrieve
#from variable_extraction import preprocessing, extract_candidates_numeric, formalize_expressions, identify_variable, map_variable_values, context_validation, normalization, hr_validation
from variable_extraction import preprocessing

fea_dict_dk = {}
'''
def load_fea_dict_dk():
    global fea_dict_dk
    if fea_dict_dk is None or len(fea_dict_dk)==0:
        # Iterating over a csv file
        file = open(os.path.join(os.path.dirname(__file__), 'variable_features_dk.csv'))
        fileReader = csv.reader(file)
        for row in fileReader:
            if row[0] != "Variable name": fea_dict_dk[row[0]] = row[1:]

fea_dict_umls = {}
def load_fea_dict_umls():
    global fea_dict_umls
    if fea_dict_umls is None or len(fea_dict_umls)==0:
        # Iterating over a csv file
        file = open(os.path.join(os.path.dirname(__file__), 'variable_features_umls.csv'))
        fileReader = csv.reader(file)
        for row in fileReader:
            if row[0] != "Variable name": fea_dict_umls[row[0]] = row[1]
'''

ids=open(sys.argv[1])
output_text=open(sys.argv[2],"w")
#out_text=open (sys.argv[2],"w")
for id in ids:
    id=id.rstrip('\n')
    #t=retrieve.extract_criteria(id)
    t=retrieve.extract_description(id)
    #print "++"+id
    #global fea_dict_dk, fea_dict_umls

#    load_fea_dict_dk()
#   load_fea_dict_umls()

    # get feature info
    features, feature_dict_dk = {}, {}
    features = fea_dict_dk
    var="All"
    global csv_result
    csv_result = []
    input, output = "", ""
    options, var_options =[], ''
    text=preprocessing(t)
    text = text.encode('ascii', 'ignore')

    lines=text.split("#")
    print >>output_text,">>"+id
    for line in lines:
        line=re.sub("\.$","",line)
        #print line
        output_text.write(line+".\n")
    print >>output_text

'''
    (sections_num, candidates_num) = extract_candidates_numeric(text) # extract candidates containing numeric
    #print sections_num
    for i in xrange(len(candidates_num)): # for each candidate
        #print i
        exp_text = formalize_expressions(candidates_num[i]) # identify and formalize values
        (exp_text, key_ngrams) = identify_variable(exp_text, fea_dict_dk, fea_dict_umls) # identify variable mentions and map to names
        (variables, vars_values) = map_variable_values(exp_text)
        #print variables , '=='

        #print vars_values
        all_exps = []
        for k in xrange(len(variables)):
            curr_var = variables[k]
            curr_exps = vars_values[k]
            if curr_var in features:
                fea_list = features[curr_var]
                curr_exps = context_validation(curr_exps, fea_list[1], fea_list[2])
                curr_exps = normalization(fea_list[3], curr_exps) # unit conversion and value normalization
                curr_exps = hr_validation (curr_exps, float(fea_list[4]), float(fea_list[5])) # heuristic rule-based validation
            if len(curr_exps) > 0:
                all_exps += curr_exps

        if len(all_exps) > 0:
            output += "<span style=color:blue>Text section</span>: " + str(sections_num[i]) + "<br>"
            candidates_num2 = re.sub('<','&lt;', re.sub('>','&gt;', candidates_num[i]))
            output += "<span style=color:blue>Sentence</span>: " + str(candidates_num2) + "<br>"
            ori_text=exp_text
            exp_text = re.sub('<','&lt;', re.sub('>','&gt;', exp_text))
            output += "<span style=color:red>Representation</span>: " + exp_text + "<br>"
            output += "<span style=color:red>Normalized variables and values</span>: "
            for exp in all_exps:
                output += "<span class=bg_var>" +exp[0] + "</span> "+"<span class=bg_logic>" +exp[1] + "</span> "+"<span class=bg_value>" +exp[2] + "</span> "+"<span class=bg_unit>" +exp[3] + "</span>; "
                csv_result.append([sections_num[i], str(candidates_num[i])]+exp)
        #       if len(key_ngrams) > 0: output += "<span style=color:blue>Constraints</span>: " + str(key_ngrams).replace("u'", "'") + "<br>"
            output += "<br><br>"
            #print "=+++"+output
            #print candidates_num2
            #print str(sections_num[i])
            #print ori_text
            for exp in all_exps:
                print >>output_text,id+","+str(sections_num[i])+","+exp[0]+","+exp[1]+","+exp[2]+","+exp[3]

'''