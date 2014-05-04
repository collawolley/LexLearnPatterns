#encoding:utf-8 
'''
Created on Dec 27, 2013
python 2.7.3 
@author: hadyelsahar 
'''

import argparse
import regex
import ConfigParser
import re
from Classes.Tweet import *
from Classes.Word import * 
from Config import * 

class PatternMatcher:

	def __init__(self,inputFile,config,variable=None):
		self.inputFile = inputFile	
		self.config = config
		if variable is not None :
			self.config.addVariable(variable)
 
	def applyPatterns(self,patternSectionName):
		in_file = open(self.inputFile, 'r')	

		for line in in_file:	
			for pname, p in self.config.Patterns[patternSectionName].items():
				# line = autoNormalizeSentence(line)
				res = p.search(line)		
				if res is not None:				
					for capture in res.groups():			
						if capture is not None and len(capture) > 0 :				
							c = capture.split(" ")																					
							yield Word(" ".join(c),pname)	

		in_file.close()		


	def verifyPatterns(self,patternSectionName,variable):
		self.config.addVariable(variable)
		self.config.reloadConfig()

		in_file = open(self.inputFile, 'r')	
			
		for line in in_file:		

			for pname, p in self.config.Patterns[patternSectionName].items():
				# line = autoNormalizeSentence(line)
				res = p.search(line)		
				if res is not None:				
					for capture in res.groups():			
						if capture is not None and len(capture) > 0 :				
							c = capture.split(" ")														
							yield Word(" ".join(c),pname)

		in_file.close()		
		self.config.removeVariable(variable)		


# command line arguments parsing 
##################################
# parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
# parser.add_argument('-c','--config', help='Input Config file name',required=True)
# parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
# parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= True)
# parser.add_argument('-uf','--uniqandfilter',help='filter extracted lexicon words and save them to clean_uniq_output file with counts', required= False , action="store_true")
# parser.add_argument('-sl','--seedlexicon', help='Input classified lexicon file name',required=False)
# args = parser.parse_args()

# if args.uniqandfilter is True and args.seedlexicon is None:
#   parser.error('must specify seedlexicon when choosing [-uf] option')



# normalize helper functions based on config file
# or run this in command line (faster)  cat filename | sed 's/ة/ه/g'  | sed  's/ى/ي/g'  | sed  's/أ/ا/g'  | sed  's/إ/ا/g'  | sed  's/آ/ا/g'  | sed  's/الأ/الا/g'  | sed  's/الإ/الا/g'  | sed  's/الآ/الا/g'  | sed  's/ﻷ/لا/g'




#######FILTER WORDS
# if args.uniqandfilter:
	
# 	uniq_out_file = open("uniq_filter"+args.output, 'w')
# 	filter_out_file = open("filter"+args.output, 'w')
# 	uniqCleanExtractedLex	= set()

# 	# loading Lexicon file 
# 	########################

# 	lex_file = open(args.seedlexicon, 'r')
# 	lex = lex_file.read().split("\n")
# 	seedLexicon = set()

# 	for line in lex:		
# 	    if len(line) > 0  and "\t" in line:
# 	        w = line.split("\t")	       
# 	        seedLexicon.add(w[0].strip())	       	        
# 	del lex 


# 	for i,lexword in enumerate(extractedLex):
			
# 		# print lexword
# 		execludeWords =  set(list(Options["intensifier_extend"])+list(Options["take_another_word_extend"]))
# 		execludeAnywhere = ["ـ","؟",".","!","-","_","@","#","%","^","&",":","?","،","(",")",",",";","*","~","/","\\"]
# 		#execludeAll =  set(list(Options["female_entity"])+list(Options["entity"])+list(Options["male_entity"])+list(Options["negators"])+list(Options["intensifier"])+list(Options["person_pointer"])+list(Options["take_another_word"])+list(Options["stopword"])+list(Options["negators"])+list(seedLexicon))
# 		execludeAll =  set(list(Options["female_entity"])+list(Options["entity"])+list(Options["male_entity"])+list(Options["negators"])+list(Options["intensifier_extend"])+list(Options["pointer"])+list(Options["take_another_word_extend"])+list(Options["stopword"])+list(Options["negators"]))

# 		#remove elongation more than two occurrences:
# 		# rgxPart = "(?:"+"|".join(Options["longation"])+")"
# 		# lexword =  re.sub(r"("+rgxPart+")\1\1+",r"\1\1",lexword)			

# 		#removing all occurrence of sub execlude words
# 		for w in execludeWords:
# 			pattern =  "(\s|^)"+w+"(?=\s|$)"
# 			lexword =  re.sub(pattern," ",lexword).strip()
				
# 		#removing anywhere occurrences like dots and commans ..etc
# 		for w in execludeAnywhere:			
# 			if w in lexword:
# 				lexword = lexword.replace(w," ");					
# 				lexword = " ".join(lexword.split()).strip()  #remove extra spaces

# 		#remove if it matches neutral words of intensifiers ..etc			
# 		rgxPart = "(?:"+"|".join(execludeAll)+")"			
# 		patternStr = "^"+rgxPart+"(?:\s+"+rgxPart+")*$"
# 		pattern = re.compile(patternStr)

# 		#remove vowel elongation and check that it doesn't exist also 
# 		rgxPart = "(?:"+"|".join(Options["vowel"])+")"
# 		lexwordshorten =  re.sub(r'('+ rgxPart +')\1+',r"\1",lexword)

# 		if re.match(patternStr,lexword) is None and re.match(patternStr,lexwordshorten) is None :				
# 			if len(lexword) > 1 :
# 				uniqCleanExtractedLex.add(lexword)
# 				extractedLex[i] = lexword
# 				lexWithPatterns[i] = [lexWithPatterns[i][0],lexword,lexWithPatterns[i][1]]


# 	#put all occurrrence of couts of LearntLex in dictionary
# 	learnLexCount = {}
# 	for w in uniqCleanExtractedLex:
# 		learnLexCount[w] = extractedLex.count(w)

# 	#sort and add to file 
# 	for w in sorted(learnLexCount, key=learnLexCount.__getitem__, reverse=True):		
# 		s = (w  + "\t" + str(learnLexCount[w])+"\n")
# 		uniq_out_file.write(s)

# 	for k in lexWithPatterns:
# 		if len(k) == 3 :
# 			s = (k[1]  + "\t" + k[2]+"\n")
# 			filter_out_file.write(s)

# 	uniq_out_file.close()
# 	filter_out_file.close()


