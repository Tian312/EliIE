# -*- encoding: utf-8 -*-
# Extract quantitative variables and their values from free texts -- core algorithm (reusable)
# Created by Tony HAO, th2510@columbia.edu

import os, sys, re, string, math
import retrieve_texts
#--------------------------Define representative logics and their candidate representations 

greater = "higher than|greater than|greater|above|more than|over|superior to|exceeding|exceed|>|larger than|older than|prior"
greater_equal = "more than or equal to|equal to or greater than|equal to or higher than|equal to or more than|equal or greater than|equal to or above|superior or equal to|greater than or equal to|greater or equal to|higher or equal than|higher or equal to|greater than or equal|great or equal to|greater / equal|above or equal to|minimum|> or equal to|≥|> =|= >|> or = to|= or >|> or =|> / =|at least|\+"
greater_equal2 ="or higher|or above|or greater|or more|and above|or over|or older|or bigger|and older|and over"
lower = "less than|lesser than|below|under|within|<|lower than|worse than|younger than"
lower_equal = "below or equal to|lower or equal to|small than or equal to|less than or equal to|less than or equal|less or equal to|lesser than or equal to|lesser or equal to|lower than or equal to|equal to or lower than|equal to or below|equal to or less than|equal or less than|up to and including|smaller / equal|at most|up to|maximum|max|< or equal to|= <|< =|≤|< or = to|< or =|< / =|< -|= or <"
lower_equal2 ="or lower|or below|or less|or lesser|at most|or younger|and younger"
equal = "equal to|=|is"
between = "range of X to X|range X to X|range X - X|between X to X|between X and X|between Xand X|between X - X|between X & X|from X to X|within X to X|start X and X|X through X|of X and X|>= X and X|> X and X|of X to X|>= X to <= X|>= X to X|X - <= X|X to X|X - X"
select = "X \( X \)|X \( equal to X \)|X \( = X\)"
connect = "but|and|or|"
features = "\d+(\.\d+|) x \d+(\.\d+|)|\d+(\^| \^ )\d+|\d+(\.\d+|)"
temporal = "msec|second|minute|min|hour|h|daily|day|week|month|year|yr|y|consecutive day|night"
temporal = temporal + '|' + temporal.replace('|','s|') + 's'
temporal_con = "last|past|previous|recent|next|following|upcoming|preceding"
error1 = "type|typ|stage|appendix|section|group|visit|part|version|grade|category|phase|class|number|no."
error2 = "\+/ -|\+ -|±"
symbols = r"≥|>|≤|<|=|/|\\|\(|\)|\[|\]|\{|\}"
numbers = "one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion"
unit_special = 'mmol l-1|miu/ml minimum|9/l|ml/min/1\.73 m2|ml/min1|ml/min - 1|ml/min per 1\.73 m2|ml/min/m2\{1\.73\}|ml/min/1\.73m2|signs/symptoms'
unit_ori ='mmol li+|mmol l|mol l|miu/ml minimum|miu/ml|centimetre of water|centimeter of water|cmH2O|cm H2O|x institutional upper limit of normal|x the upper limit of normal|x upper limits of normal|x upper limit of normal|x normal upper limit|x uln|the upper limit of normal|upper limits of normal|upper limit of normal|normal upper limit|uln|mm\^3|mm3|kg2|ng ml|ng|ug|mmol|mol|percentiu|nmol|m\^2|\.m2|m\(2\)|kg m2|m2|kgm-2|in2|micromol|umol|mmhg|mm hg|millimeters of mercury|mm|hg|pmol|%|percent|uiu|iu|ul|ml min|ml|mg day|mg kg|g dl|mg dl|mg|dl|uln|gm|cm3|cc\'s|cm|mcg|microns|rads|pg|um|torr|u|g|l|m|%|times|iuln|mcl|study|studies|cns|nyha|d|ptt|pt|inr|nsaid|copy|copies|iud|giga|F|C|v|fsh|wbc|plt|hgb|hpf|vwd|category|categories|oads'
unit_ori_s ='liquid stool|pack year|pack - year|kilogram|square meter|meter|platelet|millimole|liter|kg|gram|beat|lb|mile|cell|degree|drink|protein|msec|patient|quadrant|reading|lesion|regimen|foot|cigarette|crise|device|dose|diameter|agent|unit|scan|episode|method|movement|site|sign|event|symptom|egg|dosage|subject|joint|item|examination|exam|point|course|form|measurement|feature|criterion|high power field|example|sample|occasion|person|incident'
unit = (unit_ori+'|'+unit_ori_s.replace('|','s|')+'s|'+unit_ori_s+'|'+temporal)
unit_exp = 'st|nd|rd|th'
negation = "not able to|not allowed to|not to|not|none|non|no|never|unlikely"


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

def preprocessing (text):
    # handle special characters
    text = text.strip().replace('\n\n', '#')
    text = text.replace ('\n', '')
    text = text.replace(u'＝','=').replace(u'＞', '>').replace(u'＜','<').replace(u'≤','<=').replace (u'≥','>=').replace(u'≦','<=').replace(u'≧','>=').replace(u'mm³','mm^3').replace(u'µl','ul').replace(u'µL','ul').replace(u'·','').replace(u'‐','-').replace(u'—','-')

    text = text.replace('((', '(').replace('))', ')')
    text = re.sub('(\d+)( |)(~|/|&|\|)( |)(\d+)',r'\1 - \5',text) # e.g., '10~20' to '10 ~ 20'
    text = re.sub(r"(\d+),(\d{3})", r'\1\2', text) # 10,123 to 10123
    text = re.sub(r"(\d+),(\d{1,2})", r'\1.\2', text) # 10,1 to 10.1
    text = re.sub(r"between (\d+), (\d{1,2}) (and|or) ", r'between \1.\2 \3 ', text) # 'between 7, 5 and ' to 'between 7.5 and '
    while '  ' in text:
        text = text.replace('  ',' ')
    # avoid connected values separated by splitting, e.g., ", but below 10%"
    text = re.sub(", ("+connect+") ", r' \1 ', text) # 

    #return text.lower()
    return text

a="abc＝1,abc=1"
c=preprocessing(a.decode('utf-8'))
print c

def split_text_inclusion_exclusion(otext):
    in_fea = 'inclusion criteria:|key inclusion criteria|inclusion criteria [^:#;\.]+:|inclusion:|(?<!(\w| ))inclusion criteria\W\W|inclusion for'
    ex_fea = 'exclusion criteria:|key exclusion criteria|exclusion criteria [^:#;\.]+:|exclusion:|(?<!(\w| ))exclusion criteria\W\W|exclusion for'
    
    in_text, ex_text = '', ''
    in_bool = True

    text = otext.lower()
    while text != '':
        if in_bool:
            n_pos = re.search('('+ex_fea+')',text)
            if n_pos is not None:
                in_text += text[0:n_pos.start()]
                text = text[n_pos.start():]
            else:
                in_text += text[0:]
                text = ''
        else:
            n_pos = re.search('('+in_fea+')',text)
            if n_pos is not None:
                ex_text += text[0:n_pos.start()]
                text = text[n_pos.start():]
            else:
                ex_text += text[0:]
                text = ''
        in_bool = False if in_bool else True
    
    sections_text =[]
    if in_text !='': sections_text.append(["Inclusion", in_text])
    if ex_text !='': sections_text.append(["Exclusion", ex_text])    
    return sections_text


#====find expression candidates according to pre-defined feature list
def extract_candidates_numeric (text):
    # process text
    sections_text = split_text_inclusion_exclusion(text)
    
    sections_num = []
    candidates_num = []
      
    for section_text in sections_text:        
        sentences = sentence_splitting_symbols(section_text[1], "[#!?.;]\s", 1)
        for sent in sentences:
            sent = sent.strip().strip('- ')
            if sent == '':
                continue
                
            digit = re.search("(?<!(\w))\d+", sent)
            if digit:
                sections_num.append(section_text[0])
                candidates_num.append(sent)

    return (sections_num, candidates_num)



#====identify expressions and formalize them into labels "<VML(tag) L(logic, e.g., greater_equal)=X U(unit)=X>value</VML>"
def formalize_expressions (candidate):
    text = candidate
    text = re.sub(r'('+symbols+')',r' \1 ',text) # 'A1c<3' to 'A1c < 3'
    text = re.sub(r'-(\d+)',r'- \1',text) # '-10' to '- 10'   
    text = re.sub(r'(--|- -| -|- |~~|~ ~|~)',' - ',text) # ' - -' to ' - '
    
    # process special unit first as they contain numerical values
    text = re.sub(r'(?<!(\w|<|>|=))('+unit_special.replace('/', ' / ').replace('-',' - ')+')(?!(\w|-))',r'<Unit>\2</Unit>',text)
    matchs = re.findall('<Unit>([^<>]+)</Unit>', text)
    for match in matchs: text = text.replace(match, match.replace(' / ', '/').replace(' - ','-'))

    # process numerical values with certain features and their exceptions
    text = re.sub(r'(?<!(\w|<|>|=|/|\.|\+|:|\^|x))('+features+')(?!(\d|-|/|\+\d|:))',r'<VML>\2</VML> ',text) # process all numerical values
    while '  ' in text: text = text.replace('  ', ' ') # clean text, particularly remove spaces brought by the previous step (separated numerics and the following units)
    text = re.sub(r'<VML>([^<>]+)</VML> ('+unit_exp+')(?!(\w))',r'\1\2',text) # remove exception, e.g., '3rd'
    text = re.sub(r'(\w - )<VML>([^<>]+)</VML>',r'\1\2',text) # process connected entities containing numerics, e.g., 'icd - 9'
    text = re.sub(r'(\A|\( |\[ |\{ |,|, |;|; )<VML>([^<>]+)</VML> (\)|\]|\})',r'\1\2 \3',text) # process special numerics, e.g., '2 )'
    text = re.sub(r'<VML>([^<>]+)</VML> (-|/|\\) <VML>([^<>]+)</VML> (-|/|\\) <VML>([^<>]+)</VML>',r'\1\2\3\4\5',text) # process three connected numerics,e.g., '12/12/2013'
    text = re.sub(r' (around|about) <VML>([^<>]+)</VML>',r' <VML>\2</VML>',text) # process numerics with "around",e.g., 'around 13'

    # process all the other units
    text = re.sub(r'(?<!(\w|=|<|>|/))('+unit+')(?!(\w|<|>|/))', r'<Unit>\2</Unit>', text) # process all units
    text = re.sub(r'<Unit>([^<>]+)</Unit> (/|\\) <Unit>([^<>]+)</Unit>', r'<Unit>\1/\3</Unit>', text) # combine units together, e.g., 'kg / m^2'
    text = re.sub(r'/VML> ([a-z]+) (/|\\) (\w+)(?!(\w|<|>))', r'/VML> <Unit>\1/\3</Unit>', text) # recognize units with format '10 xx/yy'
    text = re.sub(r'<Unit>([^<>]+)</Unit> (per|a|every|each) (\w*)( |)<Unit>([^<>]+)</Unit>', r'<Unit>\1/\3\4\5</Unit>', text) # combine units together, e.g., 'mg per day'

    # merge numerics and unit tags
    text = re.sub(r'<VML>([^<>]+)</VML>( -| of|) <Unit>([^<>]+)</Unit>', r'<VML Unit=\3>\1</VML>', text) # unit not connected with value, e.g., '12 of kg/m^2'
    text = re.sub(r'<VML>([^<>]+)</VML>( /| \\) <Unit>([^<>]+)</Unit>', r'<VML Unit=/\3>\1</VML>', text) # unit with incomplete unit, e.g., '12 / mm3'
    text = re.sub(r'<VML>([^<>]+)</VML> ([^ \(\[\{]+) <Unit>([^<>]+)</Unit>', r'<VML Unit=\2 \3>\1</VML>', text) # unit with additional word from numerics, e.g., '12 stable dose'
    text = re.sub(r'<VML([^<>]*)>([^<>]+)</VML> (daily|monthly|weekly|hourly|yearly)(?!(\w|<|>))', r'<VML\1 \3>\2</VML>', text) # unit connected with temporal unit, e.g., '12 mg daily'
    text = re.sub(r'<VML>([^<>]+)</VML>', r'<VML Unit=>\1</VML>', text) # numberic without any unit following, e.g., 'age 20'
    
    # process 'select' expression, use the first one
    selects = select.split('|')
    for selec in selects:
        selec = selec.replace('X', '<VML Unit([^<>]+)>([^<>]+)</VML>')
        text = re.sub(selec, r'<VML Unit\1>\2</VML>', text) # 
    
   # process 'between' expressions
    betweens = between.split('|')
    for betw in betweens:
        betw = betw.replace('X', '<VML Unit([^<>]+)>([^<>]+)</VML>')
        text = re.sub(betw, r'<VML Logic=greater_equal Unit\1>\2</VML> - <VML Logic=lower_equal Unit\3>\4</VML>', text) # 

    # process special logics (e.g., '7%<A1C' (lower than) should be 'A1C>7%' (greater than))
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (< =|= <) ([^<>\(\[\{,]+) (< =|= <|<) <VML Unit([^<>]+)>', r'<VL Label=\4 Source=Context>\4</VL> <VML Logic=greater_equal Unit\1>\2</VML> - \5 <VML Unit\6>', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (<) ([^<>\(\[\{,]+) (< =|= <|<) <VML Unit([^<>]+)>', r'<VL Label=\4 Source=Context>\4</VL> <VML Logic=greater Unit\1>\2</VML> - \5 <VML Unit\6>', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (> =|= >) ([^<>\(\[\{,]+) (> =|= >|>) <VML Unit([^<>]+)>', r'<VL Label=\4 Source=Context>\4</VL> <VML Logic=lower_equal Unit\1>\2</VML> - \5 <VML Unit\6>', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (>) ([^<>\(\[\{,]+) (> =|= >|>) <VML Unit([^<>]+)>', r'<VL Label=\4 Source=Context>\4</VL> <VML Logic=lower Unit\1>\2</VML> - \5 <VML Unit\6>', text)

    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (< =|= <) ([a-z]\w+)', r'<VML Logic=greater_equal Unit\1>\2</VML> \4', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (<) ([a-z]\w+)', r'<VML Logic=greater Unit\1>\2</VML> \4', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (> =|= >) ([a-z]\w+)', r'<VML Logic=lower_equal Unit\1>\4', text)
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (>) ([a-z]\w+)', r'<VML Logic=lower Unit\1>\2</VML> \4', text)
    
    # process speical temporal
    text = re.sub(r' (the|this|these|those) ('+temporal_con+') <VML Unit=([^<>]*)>([^<>]+)</VML>', r' <VML Unit=\2 \3>\4</VML>', text) # e.g., ' the 1 year'
    text = re.sub(r' (the|this|these|those) <VML Unit=([^<>]*)>([^<>]+)</VML>', r' <VML Unit=\2>\3</VML>', text) # e.g., ' the 1 year'
    text = re.sub(r' (in|during|for|of|) ('+temporal_con+') <VML Unit=([^<>]*)>([^<>]+)</VML>', r' <VML Logic=lower_equal Unit=\2 \3>\4</VML>', text) # e.g., 'during the past 2 year'

    # process logic (e.g., 'greater than')    
    text = re.sub(r'(?<!(\w|<|>|=))('+greater_equal+')(?!(\w|<|>))', r'<Logic>greater_equal</Logic>', text)
    text = re.sub(r'(?<!(\w|<|>|=))('+greater+') <VML', r'<Logic>greater</Logic> <VML', text)
    text = re.sub(r'(VML>|Unit>) ('+greater_equal2+')(?!(\w|<|>))', r'\1 <Logic>greater_equal</Logic>', text)
    text = re.sub(r'(?<!(\w|<|>|=))('+lower_equal+')(?!(\w|<|>))', r'<Logic>lower_equal</Logic>', text)
    text = re.sub(r'(?<!(\w|<|>|=))('+lower+') <VML', r'<Logic>lower</Logic> <VML', text)
    text = re.sub(r'(VML>|Unit>) ('+lower_equal2+')(?!(\w|<|>))', r'\1 <Logic>lower_equal</Logic>', text)
    text = re.sub(r'(?<!(\w|<|>|=))('+equal+')(?!(\w|<|>))', r'<Logic>equal</Logic>', text)

    # process other special logics
    text = re.sub(r'<VML>([^<>]+)</VML> <Logic>([^<>]+)</Logic> <Unit>([^<>]+)</Unit>', r'<VML Logic=\2 Unit=\3>\1</VML>', text) # e.g., 'age 20 or older years'
    text = re.sub(r'<Logic>([^<>]+)</Logic> <Logic>equal</Logic>', r'<Logic>\1</Logic>', text) # remove equal if it connected with another logic
    text = re.sub(r'<Logic>([^<>]+)</Logic> <VML Unit([^<>]+)>([^<>]+)</VML>', r'<VML Logic=\1 Unit\2>\3</VML>', text) # e.g., 'greater than 20 mmol'
    text = re.sub(r'<VML Logic=equal Unit([^<>]+)>([^<>]+)</VML> <Logic>([^<>]+)</Logic>', r'<VML Logic=\3 Unit\1>\2</VML>', text) # e.g., 'A1c = 10% or higher'
    text = re.sub(r'<VML Unit([^<>]+)>([^<>]+)</VML> (|of [^ ]+ |[^ ]+ )<Logic>([^<>]+)</Logic>', r'<VML Logic=\4 Unit\1>\2</VML>\3', text) # e.g., 'A1c 10% of first visit or higher' to 'A1c greater_equal 10% of first visit'
    text = re.sub(r'<Logic>equal</Logic> <VML Logic=([^<>]+)>([^<>]+)</VML>', r'equal <VML Logic=\1>\2</VML>', text) # e.g., 'A1c = 10% or higher'
    text = re.sub(r'<Logic>([^<>]+)</Logic> <VML Logic=greater_equal Unit=([^<>]*)>([^<>]+)</VML> - <VML Logic=lower_equal Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=\1 Unit=\2>\3</VML> - <VML Logic=\1 Unit=\4>\5</VML>', text) # e.g., "bp < 100-120" to 'bp < 100 and bp < 120'
    
    # process speical temporal
    text = re.sub(r' (in|during) <VML Unit=([^<>]*)>([^<>]+)</VML>', r' <VML Logic=lower_equal Unit=\2>\3</VML>', text) # e.g., 'during the past 2 year'

    text = re.sub(r'<VML Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=equal Unit=\1>\2</VML>', text) # no logic
    
    # context-based validation    
    text = re.sub(r'<VML ([^<>]+) Unit=>([^<>]+)</VML> (-|and|or|to) <VML ([^<>]+) Unit=([^<>]+)>([^<>]+)</VML>', r'<VML \1 Unit=\5>\2</VML> - <VML \4 Unit=\5>\6</VML>', text) # guess unit according to context ([unknow] and [known unit])
    text = re.sub(r'<VML ([^<>]+) Unit=([^<>]+)>([^<>]+)</VML> (-|and|or|to) <VML ([^<>]+) Unit=>([^<>]+)</VML>', r'<VML \1 Unit=\2>\3</VML> - <VML \5 Unit=\2>\6</VML>', text) # guess unit according to context ([known] and [unknow unit])
    text = re.sub(r'<VML ([^<>]+) Unit=>([^<>]+)</VML> <Unit>([^<>]+)</Unit>', r'<VML \1 Unit=\3>\2</VML>', text) # get unit according to following context
    text = re.sub(r'<Unit>([^<>]+)</Unit> <VML Logic=([^<>]+) Unit=>([^<>]+)</VML>', r'<VML Logic=\2 Unit=\1>\3</VML>', text) # get unit in front of the numerics
    
    # process negations
    text = re.sub(r'(?<!(\w|<|>|=))('+negation+') <VML Logic=greater Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=lower_equal Unit=\3>\4</VML>', text) # negation
    text = re.sub(r'(?<!(\w|<|>|=))('+negation+') <VML Logic=greater_equal Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=lower Unit=\3>\4</VML>', text) # negation
    text = re.sub(r'(?<!(\w|<|>|=))('+negation+') <VML Logic=lower Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=greater_equal Unit=\3>\4</VML>', text) # negation
    text = re.sub(r'(?<!(\w|<|>|=))('+negation+') <VML Logic=lower_equal Unit=([^<>]*)>([^<>]+)</VML>', r'<VML Logic=greater Unit=\3>\4</VML>', text) # negation
    
    # process speical numerics
    text = re.sub(r'(?<!(\w|<|>|=))('+error1+')( - | of | )<VML Logic=([^<>]+) Unit=>([^<>]+)</VML>( to | - | and | or | )<VML Logic=([^<>]+) Unit=>([^<>]+)</VML>', r'\2\3\5\6\8', text) # e.g, 'type 1-2 diabetes'
    text = re.sub(r'(?<!(\w|<|>|=))('+error1+')( - | of | )<VML Logic=equal Unit=>([^<>]+)</VML>', r'\2\3\4', text) # e.g, 'type 1 diabetes'
    text = re.sub(r'<VML Logic=([^<>]+) Unit=(x|times|time)>([^<>]+)</VML> <Unit>([^<>]+)</Unit>', r'<VML Logic=\1 Unit=times \4>\3</VML>', text) # e.g., 'AAA lower than 3x uln'
    text = re.sub(r'('+error2+')( |)<VML Logic=([^<>]+) Unit=([^<>]*)>([^<>]+)</VML>', r'\1 \3 \5', text) # e.g., '+/- 0.3'
    text = re.sub(r'<VML Logic=([^<>]+) Unit=( |)(-|~|of|)([^<>]+)(\)|]|}|,|\.|;|:|-)( |)>([^<>]+)</VML>', r'<VML Logic=\1 Unit=\4>\7</VML>\5\6', text) # move part of the unit outside
    
    # remove tags cannot combined
    text = re.sub(r'<Unit>([^<>]+)</Unit>', r'\1', text)
    text = re.sub(r'<Logic>([^<>]+)</Logic>', r'\1', text)  
    text = re.sub(r'<VML>([^<>]+)</VML>', r'\1', text)  
                    
    return text


add_mentions_front = 'total|absolute|mean|average|abnormal|gross'
add_mentions_back = 'test results|test result|test scores|test score|tests|test|scores|score|results|result|values|value|levels|level|ratios|ratio|counts|count|volume'
def identify_variable (exp_text, fea_dict_dk, fea_dict_umls):
    # find candidate string
    if exp_text.find('<VML') == -1:
        return (exp_text, [])
    can_texts = re.findall('(\A|VML>)(.+?)(<VML|\Z)',exp_text) 
    
    # generate n-grams
    first_ngram, key_ngrams = '', [] # first ngram; key ngrams are the ngrams except the ngrams match with domain knowledge and umls
    match = False
    for cantext in can_texts:
        if '<VL Label' in cantext[1]: 
            ngrams = re.findall('<VL Label=([^<>]+) Source', cantext[1])
            for ngram in ngrams:# judge if they are potential variables
                if ngram in fea_dict_dk:
                    exp_text = re.sub(r'<VL Label='+ngram+' Source=', r"<VL Label=%s Source=" % fea_dict_dk[ngram], exp_text)
                elif ngram in fea_dict_umls:
                    exp_text = re.sub(r'<VL Label='+ngram+' Source=', r"<VL Label=%s Source=" % fea_dict_umls[ngram], exp_text)
            match = True
        else:
            ngrams = keywords_ngrams_reverse(cantext[1].replace(' - ', '-').strip())
            if len(ngrams) > 0:
                longest_str = max(ngrams, key=len)
                key_ngrams.append(longest_str)
                if first_ngram == '': first_ngram = longest_str
            for ngram in ngrams:# judge if they are potential variables
                if ngram in fea_dict_dk:
                    if ngram in key_ngrams: key_ngrams.remove(ngram)
                    exp_text = re.sub(r'(?<!(\w|<|>))'+ngram+'(?!(\w|<|>))', r"<VL Label=%s Source=DK>%s</VL>" % (fea_dict_dk[ngram], ngram), exp_text, 1)
                    match = True
                    break
                elif ngram in fea_dict_umls:
                    if ngram in key_ngrams: key_ngrams.remove(ngram)
                    exp_text = re.sub(r'(?<!(\w|<|>))'+ngram+'(?!(\w|<|>))', r"<VL Label=%s Source=UMLS>%s</VL>" % (fea_dict_umls[ngram], ngram), exp_text, 1)
                    match = True
                    break

    exp_text = re.sub(r'<VL ([^>]+)<VL Label=[^<>]+>([^<>]+)</VL>',r'<VL \1\2', exp_text)
    exp_text = re.sub(r'(?<!(\w|<|>|=))('+add_mentions_front+') <VL Label=([^<>]+) Source=([^<>]+)>([^<>]+)</VL>', r"<VL Label=\2 \3 Source=\4>\2 \5</VL>", exp_text)
    exp_text = re.sub(r'</VL>'+' ('+add_mentions_back+r')(?!(\w|<|>))', r" \1</VL>", exp_text)

    if len(can_texts)>0 and not match and first_ngram.strip() != '': #guess variable
        exp_text = exp_text.replace(first_ngram, "<VL Label=%s Source=ngram>%s</VL>" % (first_ngram, first_ngram), 1)
#     marks =re.findall(r'<VL Label=([^<>]+)>[^<>]+</VL>', exp_text)

    return (exp_text, key_ngrams)
         
map_symbols = {'greater_equal':'greater than or equal to', 'lower_equal':'lower than or equal to', 'greater':'greater than', 'lower':'lower than', 'equal':'equal to'}   
def map_variable_values(exp_text):
    # reorder exp_text to arrange variable values in order
    can_str = exp_text
    can_str = re.sub(r'<VL ([^<>]+)>([^<>]+)</VL> <VML ([^<>]+)>([^<>]+)</VML> <VL ([^<>]+)>([^<>]+)</VL>', r'<VL \1>\2</VL> <VML \3>\4</VML>; <VL \5>\6</VL>', can_str) 
    can_str = re.sub(r'<VML ([^<>]+)>([^<>]+)</VML> (-|to|and) <VML ([^<>]+)>([^<>]+)</VML>( of| for) <VL ([^<>]+)>([^<>]+)</VL>', r'<VL \7>\8</VL> <VML \1>\2</VML> \3 <VML \4>\5</VML>', can_str) 
    can_str = re.sub(r'<VML ([^<>]+)>([^<>]+)</VML>( of| for) <VL ([^<>]+)>([^<>]+)</VL>', r'<VL \4>\5</VL> <VML \1>\2</VML>', can_str) 
    
    # find association    
    variables, vars_values = [], []
    start = 0
    while can_str.find('<VL') >-1 and can_str.find('<VML') >-1:
        con1 = can_str.find('<VL')
        start = 0 if start == 0 else con1
        end = can_str.find('<VL' , con1+1)
        if end > -1:
            text = can_str[start:end] # pos could be -1 so curr_str always ends with a space
            can_str = can_str[end:]
        else:
            text = can_str[start:] # pos could be -1 so curr_str always ends with a space
            can_str = ''
        # get all values in the range
        var =re.findall(r'<VL Label=([^<>]+) Source=([^<>]+)>([^<>]+)</VL>', text) # get last VL label as variable
        values =re.findall(r'<VML Logic=([^<>]+) Unit=([^<>]*)>([^<>]+)</VML>', text)
        if len(var) > 0 and len(values) > 0:
            variables.append(var[0][0])
            var_values = []
            for value in values:
                logic_for_view = map_symbols[value[0]] if value[0] in map_symbols else value[0]
                var_values.append([var[0][0], logic_for_view, value[2], value[1].strip()])
            vars_values.append(var_values)

    return (variables, vars_values)


def context_validation (var_values, allow_units, error_units):

    # unit based validation
    curr_exps = []
    allow_units = (str(allow_units).replace("TEMPORAL", temporal)).split('|')
    error_units = (str(error_units).replace("TEMPORAL", temporal)).split('|')
    for exp in var_values:
        if exp[3].startswith('x ') or exp[3].startswith('times'):
            condition = True
        elif error_units == ['ALL_OTHER']:
            condition = (exp[3]=='' or exp[3] in allow_units)
        else:
            condition = (exp[3]=='' or exp[3] in allow_units or exp[3] not in error_units)
        if condition:
            curr_exps.append(exp)

    return curr_exps
       
       
#====================normalize the unit and their corresponding values
def normalization (nor_unit, exps):
#     for i in xrange(len(exps)):
    exp_temp = []
    for exp in exps:
        if ' x ' in exp[2]: 
            temp = exp[2].strip().split(' x ')
            exp[2] = 1.0
            for tem in temp:
                exp[2] = exp[2] * float(tem)
        elif '^' in exp[2]:
            temp = exp[2].split('^')
            x,y = float(temp[0].strip()),float(temp[1].strip())
            exp[2] = math.pow(x, y)
        else:
            exp[2] = float(exp[2])
        # start define unit conversion
        if nor_unit == '%':
            if exp[3] == '' and exp[2] < 1:
                exp[2], exp[3] = exp[2]*100.0, nor_unit
            elif exp[3].startswith('percent'):
                exp[3] = nor_unit
            elif exp[3].startswith('mmol/mol'):
                exp[2], exp[3] = exp[2]/10.0, nor_unit  
            elif exp[3] =='':
                exp[3] = nor_unit
        elif nor_unit == 'mmol/l':
            if exp[3] == '' and exp[2] >= 60:
                exp[3] = 'mg'
            if exp[3].startswith('mg'):
                exp[2], exp[3] = exp[2]/18.0, nor_unit
            elif exp[3].startswith('g/l'):
                exp[2], exp[3] = exp[2]*7.745, nor_unit
        elif nor_unit == 'kg/m2':            
            if exp[3]<> '' and exp[3] <> 'kg/m2':
                exp[3] = nor_unit
            elif exp[3] == '':
                exp[3] = nor_unit
        elif nor_unit == 'mg/dl':
            if exp[3] == '' and exp[2] >= 100:
                exp[3] = 'mol'
            if exp[3].startswith('umol') or exp[3].startswith('mol') or exp[3].startswith('micromol'):
                exp[2], exp[3] = exp[2]/88.4, nor_unit
            elif exp[3] == 'mmol/l':
                exp[2], exp[3] = exp[2]*18.0, nor_unit
            elif exp[3].startswith('mg/g'):
                exp[2], exp[3] = exp[2]/1000.0, nor_unit
        elif exp[3] == '' and nor_unit != "":
            exp[3] = nor_unit
        exp[2] = "{0:.2f}".format(exp[2])
        exp_temp.append(exp)
#         exps[i] = exp_temp
    return exp_temp
        
   
# heuristic rule-based validation     
def hr_validation(exps_temp, min_value, max_value):
    # ------------------ judge an exp by its value comparing with average value. 100 mg/dl, 1 (day), in this case, 1 (day) will be removed
    exps = []
    tagg_temp = []
    # validation by comparing with average value step1. This has been tested to be not as valid as the previous validation method
#     total, num = 0.0, 0.0
#     for exp in exps_temp:
#         if exp[3] <> '':
#            total += float(exp[2])
#            num += 1
           
    thre1, thre2 = 2.0, 8.0 
    for exp in exps_temp:
        if exp[3].startswith('x ') or exp[3].startswith('times'):
            tagg_temp.append(exp)
            continue
        # validation by heuristic rules
        if float(exp[2]) < min_value/thre1 or float(exp[2]) > max_value*thre1: 
            continue

        # validation by comparing with average value step2. This has been tested to be not as valid as the previous validation method            
#         if exp[3] == '' and num > 0 and (total/num >= thre2*float(exp[2]) or float(exp[2]) >= thre2*total/num):
#             continue
        
        tagg_temp.append(exp)
    return tagg_temp



# =====================================ngrams

def keywords_ngrams_reverse(sentence):
    ngrams = []
    splitter=re.compile('[\(\){}\[\]?!,:;]')
    phrases = splitter.split(sentence)
    for phrase in reversed(phrases):
        if len(phrase) <= 1: # e.g.'ii'
            continue
        #     words = NLP_word.word_splitting(sentence.lower()) # method 1: NLP
        splitter=re.compile('[^a-zA-Z0-9_-]') # method 2: splitters
        words = splitter.split(phrase)
            
        stop_pos = [] # record all positions of stop  or non-preferred (POS) words in the phrase to increase efficiency
        for i in xrange(len(words)):
            type = word_checking_stop(words[i])
            stop_pos.append(type)
        
        # Generate n-gram
        for i in reversed(xrange(len(words))):
            if 0 < stop_pos[i]:
                continue
            for j in xrange(max(0, i-9), i+1): # the maximum length of a ngram is 10
                if 0 < stop_pos[j]:# check validity
                    continue
                ngram = ' '.join(words[j:i+1])
                if len(ngram)>1: # at least two characters
                    ngrams.append(ngram)

    return ngrams

from nltk.corpus import stopwords
stopwords = stopwords.words('english')
add_stopwords = ["must","within", "every", "each", "based"]

# check if a word is a stop word
def word_checking_stop(word):
    if len(word) < 1:
        return 1
    elif word[0] in string.punctuation:
        return 2
    elif word[0].isdigit():
        return 3
    elif word in stopwords: 
        return 4
    elif word in add_stopwords:
        return 5
    else:
        return 0
    
    

def sentence_splitting_symbols (texts, splitter = None, slen = 1):
    if len(texts) <= 0:
        return []
    
    if splitter is None:
        splitter = "[#!?.]\s"
    # splitting
    sentences = []
    text_sents = re.split(splitter, texts)
    if (text_sents != [''] and len(text_sents) >  0):
        for sent in text_sents:
            sent = sent.strip().split('\r') # split strings that contains "\r"
            for sen in sent:
                if (len(sen.split()) >= slen):
                    sentences.append(sen.strip('-').strip())

    return sentences
        

'''
#============
ids=open('files/DMII_ids.csv')


for id in ids:
    id=id.rstrip('\n')
    t=retrieve_texts.extract_criteria(id)
    text=preprocessing(t)
    text=split_text_inclusion_exclusion(text)
    print text
'''