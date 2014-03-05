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
import itertools


# command line arguments parsing 
##################################

parser = argparse.ArgumentParser(description='tool to expand set of regex patterns to all possible twitter search queries')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
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
    Options[i] = set([x.strip() for x in init[i].split(",")])



#Patterns loading and expantion
############################## 

#variables are the set of reserved Keywords defined in the config file
reserved_variables = [ "__"+k for k,v in Options.items()]

Patterns = {}

for name,pattern in config("searchquery").items():

    if any( x in pattern for x in reserved_variables):
        #patterns has variables inside  
        variables = {}

        for x  in [v for v in reserved_variables if v in pattern]:            
            var = x.strip("__")

            variables[var]= Options[var]        
        

        permutations = [v for v in itertools.product(*variables.values())]

        for p in permutations:
            new_pattern = pattern
            for i,key in enumerate(variables.keys()):
                new_pattern = new_pattern.replace("__"+key,p[i])
            print new_pattern


out_file = open(args.output, 'w')
