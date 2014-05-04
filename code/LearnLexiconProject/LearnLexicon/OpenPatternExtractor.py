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
from Config import * 


parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
parser.add_argument('-o','--output',help='output file name , print to console if not specified',required=False)
args = parser.parse_args()

config = Config(args.config)
matcher = PatternMatcher(args.input,config)
candidateWords = []

#building ngrams for each for the candidate sections 
for candidate in matcher.applyPatterns("patterns_open"):
	words = candidate.text.split()
	max = 4 if len(words) > 4 else len(words)
	
	for i in range(1,max):
		ngram = " ".join(words[0:i])
		print ngram
		candidateWords.append(ngram)


# #ngram filteration:
# #getting unique words
# candidateWords = list(set(candidateWords))

# filteredCandidates = []



#split candidate ngrams

splitOn =  [ " "+i+" " for i in list(config.Options["conjunction"])]+["..",".",","]



for lexword in candidateWords:
	for sep in splitOn:
		lexword = lexword.replace(sep,"{SEP}")

	lexword.split("{SEP}")



candidatewords = temp

#clean candidate words
execludeWords =  set(list(config.Options["intensifier_extend"])+list(config.Options["take_another_word_extend"]))
execludeAnywhere = ["ـ","؟",".","!","-","_","@","#","%","^","&",":","?","،","(",")",",",";","*","~","/","\\"]	
execludeAll =  set(list(config.Options["female_entity"])+list(config.Options["entity"])+list(config.Options["male_entity"])+list(config.Options["negators"])+list(config.Options["intensifier_extend"])+list(config.Options["pointer"])+list(config.Options["take_another_word_extend"])+list(config.Options["stopword"])+list(config.Options["negators"]))

for lexword in candidateWords:		

	#removing all occurrence of sub execlude words
	for w in execludeWords:
		pattern =  "(\s|^)"+w+"(?=\s|$)"
		lexword =  re.sub(pattern," ",lexword).strip()
			
	#removing anywhere occurrences like dots and commas ..etc
	for w in execludeAnywhere:			
		if w in lexword:
			lexword = lexword.replace(w," ");					
			lexword = " ".join(lexword.split()).strip()  #remove extra spaces

	#remove if it matches neutral words of intensifiers ..etc			
	rgxPart = "(?:"+"|".join(execludeAll)+")"			
	patternStr = "^"+rgxPart+"(?:\s+"+rgxPart+")*$"
	pattern = re.compile(patternStr)

	#remove vowel elongation and check that it doesn't exist also 
	rgxPart = "(?:"+"|".join(Options["vowel"])+")"
	lexwordshorten =  re.sub(r'('+ rgxPart +')\1+',r"\1",lexword)

	if re.match(patternStr,lexword) is None and re.match(patternStr,lexwordshorten) is None :				
		if len(lexword) > 1 :
			uniqCleanExtractedLex.add(lexword)
			extractedLex[i] = lexword
			lexWithPatterns[i] = [lexWithPatterns[i][0],lexword,lexWithPatterns[i][1]]







#for each of the candidate results , get 1 gram , bigram , trigram and Quadro grams. 
# candidatengrams = [] 
# for candidate in candidateWords:
# 	words = candidate.text.split()
# 	max = 4 if len(words) > 4 else len(words)
# 	for i in range(1,max):
# 		candidatengrams.append(" ".join(words[0:i]))

# filteredCandidatengrams = []
# # print candidatengrams

# # for i in set(candidatengrams):
# # 	res = matcher.verifyPatterns("patterns_open_verify",{"candidatewords":[i]})
# # 	if len(res) > 1 :
# # 		print i +"\t"+ str(len(res))

# print len(set(candidatengrams))
# candidatengrams = list(set(candidatengrams))

# for i in candidatengrams:
# 	print i 


# res = matcher.verifyPatterns("patterns_open_verify",{"candidatewords":set(candidatengrams)})

# print len(res)

# for i in res:
# 	print i 

# for candidate in candidatengrams:
# 	grap = TweetGrapper()
# 	l = grap.search("\" "+candidate+" و خول \"")
# 	if len(l) > 0:
# 		print candidate + "\t" + str(len(l))






