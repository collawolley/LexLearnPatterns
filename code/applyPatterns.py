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

# command line arguments parsing 
##################################

parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= True)
parser.add_argument('-uf','--uniqandfilter',help='filter extracted lexicon words and save them to clean_uniq_output file with counts', required= False , action="store_true")
parser.add_argument('-sl','--seedlexicon', help='Input classified lexicon file name',required=False)
args = parser.parse_args()

if args.uniqandfilter is True and args.seedlexicon is None:
  parser.error('must specify seedlexicon when choosing [-uf] option')


# loading config file
#######################

#print("loading config file ....")
Config = ConfigParser.ConfigParser()
Config.read(args.config)

def config(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
#loading Options  
Options = {}
init = config("variables")
for i in init :	
	Options[i] = set([x.strip() for x in init[i].split(",")])


# normalize helper functions based on config file
# or run this in command line (faster)  cat filename | sed 's/ة/ه/g'  | sed  's/ى/ي/g'  | sed  's/أ/ا/g'  | sed  's/إ/ا/g'  | sed  's/آ/ا/g'  | sed  's/الأ/الا/g'  | sed  's/الإ/الا/g'  | sed  's/الآ/الا/g'  | sed  's/ﻷ/لا/g'

def normalize(type,text):	
	norm = config("normalizers")[type]

	replaces =  {x[0].strip():x[1].strip()  for x in [x.split("-") for x in norm.split(",")]}

	for k,v in replaces.items():
		text = text.replace(k,v)		

	return text
def autoNormalize(text):
	norm = config("normalizers")["norm_start_letter"]
	replacesAtStart =  {x[0].strip():x[1].strip()  for x in [x.split("-") for x in norm.split(",")]}
	norm = config("normalizers")["norm_any_where"]
	replacesAnywhere = {x[0].strip():x[1].strip()  for x in [x.split("-") for x in norm.split(",")]}

	#normalize start of the words
	for k,v in replacesAtStart.items():
		text = " ".join([x.replace(k,v) if x.startswith(k) else x for x in text.split( )])

	for k,v in replacesAnywhere.items():
		text = " ".join([x.replace(k,v) if k in x else x for x in text.split( )])

	return text

def autoNormalizeSentence(text):
	return " ".join([autoNormalize(i) for i in text.split(" ")])


#Patterns loading and expantion
############################## 

#variables are the set of reserved Keywords defined in the config file
variables = [ "__"+k for k,v in Options.items()]

Patterns = {}

for name,pattern in config("patterns").items():
	if any( v in pattern for v in variables):
		#patterns has variables inside	
		for x in [v for v in variables if v in pattern]:			
			var = x.strip("__")
			# ?: for non capturing group in regex
			rgxPart = "(?:"+"|".join(Options[var])+")"
			pattern = pattern.replace(x,rgxPart)		
			Patterns[name] = re.compile(pattern)						
	else:
		Patterns[name] = re.compile(pattern)			
		
# for k,v in Patterns.items():
# 	print k +"\t" + str(v)
# 	print "\n\n"


# apply pattern and groups Extraction from input File
#######################################################

in_file = open(args.input, 'r')
out_file = open(args.output, 'w')

extractedLex = []

counter = 0 
tweets = in_file.read().split("\n")
for line in tweets:		
		
	counter +=1
	if counter % 1000 is 0: print str(counter) +"\t tweets parsed" 

	for pname, p in Patterns.items():
		# line = autoNormalizeSentence(line)
		res = p.search(line)		
		if res is not None:				
			for capture in res.groups():			
				if capture is not None and len(capture) > 0 :				
					c = capture.split(" ")
					s = " ".join(c)  + "\t" + pname+"\n"
					out_file.write(s)
					extractedLex.append(" ".join(c))

del tweets


if args.uniqandfilter:
	
	uniq_out_file = open("clean_filter"+args.output, 'w')
	uniqCleanExtractedLex	= set()

	# loading Lexicon file 
	########################

	lex_file = open(args.seedlexicon, 'r')
	lex = lex_file.read().split("\n")
	seedLexicon = set()

	for line in lex:		
	    if len(line) > 0  and "\t" in line:
	        w = line.split("\t")	       
	        seedLexicon.add(w[0])	       	        
	del lex 

	for i,lexword in enumerate(extractedLex):		
		if lexword not in seedLexicon and len(lexword) > 1:
			# print lexword
			execludeWords =  Options["intensifier"]
			execludeAnywhere = ["ـ","؟",".","!","-","_","@","#","%","^","&",":","?","،","(",")",",",";","*","~","/","\\"]
			execludeAll =  set(list(Options["female_entity"])+list(Options["entity"])+list(Options["male_entity"])+list(Options["negators"])+list(Options["intensifier"])+list(Options["person_pointer"])+list(Options["take_another_word"])+list(Options["stopword"]))

			#remove elongation more than two occurrences:
			rgxPart = "(?:"+"|".join(Options["longation"])+")"
			lexword =  re.sub(r"("+rgxPart+")\1+",r"\1",lexword)			

			#removing all occurrence of sub execlude words
			for w in execludeWords:
				if " "+w+" " in lexword:
					lexword = lexword.replace(" "+w+" "," ");

			#removing anywhere occurrences like dots and commans ..etc
			for w in execludeAnywhere:			
				if w in lexword:
					lexword = lexword.replace(w," ");					
					lexword = " ".join(lexword.split()).strip()  #remove extra spaces

			#remove if it matches neutral words of intensifiers ..etc			
			rgxPart = "(?:"+"|".join(execludeAll)+")"			
			patternStr = "^"+rgxPart+"(?:\s+"+rgxPart+")*$"
			pattern = re.compile(patternStr)

			#remove vowel elongation and check that it doesn't exist also 
			lexwordshorten =  re.sub(r'((?:و|ي|ا|إ|آ))\1+',r"\1",lexword)

			if re.match(patternStr,lexword) is None and re.match(patternStr,lexwordshorten) is None :				
				uniqCleanExtractedLex.add(lexword)
				extractedLex[i] = lexword

	#put all occurrrence of couts of LearntLex in dictionary
	learnLexCount = {}
	for w in uniqCleanExtractedLex:
		learnLexCount[w] = extractedLex.count(w)

	#sort and add to file 
	for w in sorted(learnLexCount, key=learnLexCount.__getitem__, reverse=True):
		s = (w  + "\t" + str(learnLexCount[w])+"\n")
		uniq_out_file.write(s)

	uniq_out_file.close()

in_file.close()
out_file.close()



def removeElongation():
