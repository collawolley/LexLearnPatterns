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
from Classes.Config import * 
from Vectors.CosineSim import *
from tweepy.streaming import StreamListener
import threading
from tweepy import Stream
import json
import time
from TweetGrapper.TweetGrapper import * 
import argparse


parser = argparse.ArgumentParser(description='tool to Grap tweets from twitter API - show on console or write to  output file- giving some input words from text file - or search keywords -- [[optional]] clean tweets')
# parser.add_argument('-mode','--mode', help='either "search" or "stream" ',required=True)
# parser.add_argument('-i','--input', help='Input file name contains keywords to search for',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= True)
parser.add_argument('-c','--config', help='Input Config file name',required=True)
#parser.add_argument('-c','--clean',help='clean tweets by removal or  RT  , Twitter username , Elongations and non alphanumericals', required= False , action="store_true")
# parser.add_argument('-kw','--showkw',help='show keyword that was used to get the tweet before the tweet itself separated by a tab', required= False , action="store_true")
# parser.add_argument('-id','--showid',help='show id of the tweet before the tweet itself separated by a tab', required= False , action="store_true")
# parser.add_argument('-u','--uniq',help='extract uniq list of tweets of input file to outputfile based on cosine Similarity', required= False, action="store_true")
# parser.add_argument('-l','--lang',help='specify language of the tweets', required= False)
# parser.add_argument('-loc','--location', help='activate search mode and capture keyword for search',required=False)
# parser.add_argument('-sep','--separator',help='separator used to separate between tweets , otherwise newline is used ', required= False)

args = parser.parse_args()

config = Config(args.config)
reservedKeywords = list(config.Options["female_entity"])+list(config.Options["entity"])+list(config.Options["male_entity"])+list(config.Options["negators"])+list(config.Options["intensifier_extend"])+list(config.Options["take_another_word_extend"])+list(config.Options["skip_if"])+list(config.Options["pointer"])+list(config.Options["person_pointer"])+list(config.Options["stopword"])+list(config.Options["stop_letter"])+list(config.Options["call"])+list(config.Options["conjunction"])+ ["ال"+i for i in list(config.Options["take_another_word_extend"])] 

def writeToFile(text):
	with open(args.output, "a") as myfile:		
		myfile.write(text.encode("utf-8")) 


def isReserved(word):
	return word in reservedKeywords


#GoodKeywords = ["محترم","جميل","محترمة"] 
GoodKeywords = ["حصري","حلو","طيب","رائع","عادي","خلوق","مختلف","مميز","سهل","لطيف","سعيد","سلس","بسيط","الحمد","نعم","خاص","كويس","متألق","خفيف","راقي","متواضع","يسر","راح","جميل","محترم","رايق","محترمة","مؤدب","حلوة","ممتع","جديد","مبدع","فايق","متميز","حبوب"]

#GoodKeywords = ["و","انت","يا","ا"]

grap = TweetGrapper()

iteration = 0 

while True: 

	newGoodKeywords = []	
	for w in GoodKeywords:	
		searchString = "\""+w + " و \"" 
		result = grap.search([searchString],None)
		if len(result) > 0 :
			#find 1grams of the resulted word
			for tweet in result:
				r = tweet.clean(True)
				searchString = w + " و "				 							
				pos = r.find(searchString.decode("utf-8"))
				w2 = ""				

				if pos is not -1 :					
					pos2 = r[pos+len(searchString.decode("utf-8")):].find(" ")
					if pos2 is not -1 :
						# print r 
						# print r[pos+len(searchString.decode("utf-8")):]
						# print pos
						# print pos2
						# print len(searchString.decode("utf-8"))
						w2 = r[pos+len(searchString.decode("utf-8")):pos+len(searchString.decode("utf-8"))+pos2] 
						# print "word is : "+ w2
					else :
						w2 = r[pos+len(searchString):] 

					w2 = w2.strip()
					if len(w2) > 1 and w2.encode("utf-8") not in GoodKeywords and w2.encode("utf-8") not in newGoodKeywords and isReserved(w2.encode("utf-8")) is not True :
						searchString2 = "\""+ w2.encode("utf-8") + " و " + w +"\""			
						r2 = grap.search([searchString2],None)
						if len(r2) > 5 :
							searchString2 = w2.encode("utf-8") + " و " + w
							found = False 
							for t in r2:
								text = t.clean(True)
								if text.find(searchString2.decode("utf-8")) is not -1 :
									found = True							

							if found is True:
								newGoodKeywords.append(w2.encode("utf-8"))						
								newGoodKeywords = list(set(newGoodKeywords))
								print "-- \t " + w2 + " \t  --" + w.decode("utf-8")

	GoodKeywords = GoodKeywords + newGoodKeywords
	GoodKeywords = list(set(GoodKeywords))
	
	s = "iteration: " + str(iteration) + "\n number of words:  " + str(len(GoodKeywords)) + "\n ----------------- \n "
	for k in GoodKeywords:
		s += k.decode("utf-8") + "\n" 

	s += "------------------------\n"
	writeToFile(s)
	iteration += 1 








