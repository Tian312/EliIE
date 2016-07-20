from negex import *
import csv


def main():
    #rfile = open(r'negex_triggers.txt')
    rfile = open(r'EC_triggers.txt')
    irules = sortRules(rfile.readlines())
    #reports = csv.reader(open(r'Annotations-1-120.txt','rb'), delimiter = '\t')
    reports = csv.reader(open(r'test.txt','rb'), delimiter = '\t')
    reports.next()
    reportNum = 0
    correctNum = 0
    ofile = open(r'negex_output.txt', 'w')
    error=open(r'error_report.txt','w')
    output = []
    outputfile = csv.writer(ofile, delimiter = '\t')
    for report in reports:
        print "report:",report
        tagger = negTagger(sentence = report[2], phrases = [report[1]], rules = irules, negP=False)
       # print "tagger:",tagger
        report.append(tagger.getNegTaggedSentence())
        print "tagger.getNegTaggedSentence()", tagger.getNegTaggedSentence()
        report.append(tagger.getNegationFlag())
        print "tagger.getNegationFlag()",tagger.getNegationFlag()
        report = report + tagger.getScopes()
        print "report=tagger.getNegationFlag()",tagger.getNegationFlag()
        print 
        reportNum += 1
        print reportNum
        if report[3].lower() == report[5]:
            correctNum +=1
        else :
            print >>error,[report[1]],report[2],report[3],report[5]
        output.append(report)
    outputfile.writerow(['Percentage correct:', float(correctNum)/float(reportNum)])
    for row in output:
        if row:
            outputfile.writerow(row)
    ofile.close()

if __name__ == '__main__': main()
