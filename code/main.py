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
args = parser.parse_args()


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
	Options[i] = [x.strip() for x in init[i].split(",")]




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

counter = 0 
tweets = in_file.read().split("\n")
for line in tweets:		
		
	counter +=1
	if counter % 1000 is 0: print str(counter) +"\t tweets parsed" 

	for pname, p in Patterns.items():
		# line = autoNormalizeSentence(line)
		res = p.search(line)		
		if res is not None:				
			capture = res.groups()[0]				
			if len(capture) > 0 :				
				c = capture.split(" ")
				out_file.write(" ".join(c[0:2])  + "\t" + pname+"\n")


del tweets

in_file.close()
out_file.close()