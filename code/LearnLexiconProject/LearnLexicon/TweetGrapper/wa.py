#encoding:utf-8 
'''
Created on May 15, 2014
python 2.7.3 
@author: hadyelsahar 
'''
import tweepy
import sys
import regex
from tweepy import OAuthHandler
from Classes.Tweet import * 
from Classes import Utils
from Vectors.CosineSim import *
from tweepy.streaming import StreamListener
import threading
from tweepy import Stream
import json
import time


def writeToFile(outfile,text):
	with open(outfile, "a") as myfile:		
		myfile.write(text.encode('utf-8')) 


GoodKeywords = ["محترم","خلوق","زي العسل"] 

grap = TweetGrapper()

while True: 
	for w in GoodKeywords:
		searchString = w + " و " 
		result = grap.search(searchString,None)
		if len(result) > 0 :
			#find 1grams of the resulted word
			for r in result:
				print "result: " + r 
				pos = r.find(searchString)
				if pos is not -1 :
					pos2 = r[pos+len(searchString):].find(" ")
					if pos2 is not -1 :
						w2 = r[pos+len(searchString):pos2] 
					else :
						w2 = r[pos+len(searchString):] 
				print w2
				# searchString2 = w2 + " و " + w 
				# if len(grap.search(searchString2,None)) > 0 :
				# 	GoodKeywords.append(w2)
				# 	GoodKeywords = List(set(GoodKeywords))










