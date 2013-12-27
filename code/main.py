#encoding:utf-8 
'''
Created on Dec 27, 2013
python 2.7.3 
@author: hadyelsahar 
'''

import argparse
import regex
import ConfigParser


# command line arguments parsing 
parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= False)
args = parser.parse_args()

# loading config file
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
	if i in "norm_start_letter" or i in "norm_any_where" :
		Options[i] =  {x[0].strip():x[1].strip()  for x in [x.split("-") for x in init[i].split(",")]}			
	else :
		Options[i] = [x.strip() for x in init[i].split(",")]
norm = config("normalizers")


#loading Patterns to Regex

#variables are set of reserved Keywords
variables = [ "__"+k for k,v in Options.items()]
print variables 
print "\n\n\n\n"
Patterns = {}
for name,pattern in config("patterns").items():
	for x in [v for v in variables if v in pattern]:
		print x.strip("__")
	
	




