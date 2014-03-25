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

# t = Tweet(u"اصلها \n\n لو عرفت تخليك بني ادم محترم و عارف ربنا .. اوعي تسيبها !",language="ar",searchKeyword="محترم")

# print t.clean()
# print t.clean()
# print t.cleanText

# grap = TweetGrapper()
# l = grap.search("محترم")

# for i in l :
# 	print i.clean().encode("utf-8")


parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= True)
parser.add_argument('-uf','--uniqandfilter',help='filter extracted lexicon words and save them to clean_uniq_output file with counts', required= False , action="store_true")
parser.add_argument('-sl','--seedlexicon', help='Input classified lexicon file name',required=False)
args = parser.parse_args()
	

if args.uniqandfilter is True and args.seedlexicon is None:
  parser.error('must specify seedlexicon when choosing [-uf] option')



matcher = PatternMatcher(args.input,args.output,args.config)

print matcher.Patterns

candidateWords = matcher.applyPatterns("patterns_closed")

for i in candidateWords:
	print i 

