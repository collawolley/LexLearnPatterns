#encoding:utf-8 
'''
Created on 24 March, 2013
python 2.7.3 
@author: hadyelsahar 
'''

import argparse

from Classes.Tweet import *
from TweetGrapper.TweetGrapper import * 
from PatternMatcher import * 
from nltk.util import ngrams



parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
args = parser.parse_args()
	

matcher = PatternMatcher(args.input,args.config)

candidateWords = matcher.applyPatterns("patterns_closed")

#for each of the candidate results , get 1 gram , bigram , trigram and Quadro grams. 
candidatengrams = [] 
for candidate in candidateWords:
	words = candidate.text.split()
	for i in range(1,4):
		candidatengrams.append(words[0:i])


filteredCandidatengrams = []

for candidate in candidatengrams:

	grap = TweetGrapper()
	l = grap.search(candidate)
	if len(l) > 3:
		print candidate






