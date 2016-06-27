__author__="tian kang"

# notes: generate w2v feautures for the terms
# for those not in the training set, the vectors are rep(0,50)

import gensim
import sys,os,re,string,codecs
import numpy

from nltk import sent_tokenize
from nltk import word_tokenize

def tokenize_train(train_directory,tokenized_directory):
    with codecs.open(train_directory, "r", "utf-8") as file:
	    with codecs.open(tokenized_directory, "w", "utf-8") as writer:
		    new_sens = []
		    for line in file:
			    sentences = sent_tokenize(line.strip())
			    for sen in sentences:

				    sen = word_tokenize(sen.lower())
				    new_sen = ' '.join(sen)
				    new_sens.append(new_sen)
				    writer.write(new_sen)
				    writer.write("\n")
    sentences = gensim.models.word2vec.LineSentence(tokenized_directory)
    return sentences

def train_w2v(corpus_dir,token_dir,model_dir):
    sents=tokenize_train(corpus_dir,token_dir)
    model=gensim.models.Word2Vec(sents,min_count=2,size=100)
    model.save(model_dir)

def ouput_embedding(model,word,size):
    #model=gensim.models.Word2Vec.load(model_dir)
	if word in model.vocab:
		l_word=word.lower()
		#print l_word
		embedding=model[l_word]
		vector=list()
		for v in embedding:
			v=str(v)
			vector.append(v)
		vector=" ".join(vector)
	else:
		vector=numpy.repeat('0',size)
		vector=' '.join(vector)
	return vector



