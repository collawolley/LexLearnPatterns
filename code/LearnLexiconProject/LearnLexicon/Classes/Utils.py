#encoding:utf-8 
'''
Created on 24 March, 2013
python 2.7.3 
@author: hadyelsahar 
'''
from Vectors.CosineSim import *

def uniq(iterator):
	previous = ""  # Not equal to anything
	cosim  = CosineSim()
	for value in iterator:                    
	  	cos = cosim.get_cosine(previous,value.text)     
	  	if  cos < 0.7 :
		    yield value      
		    previous = value.text



def clean(tweet) : 
	#remove usernames
	tweet = regex.sub(r'@[A-Za-z0-9_]+', '', tweet,flags=regex.UNICODE)
	#discarding twitter RT or RTTTT or any of it's elongations
	tweet = regex.sub(r'R+T+\s*:*\s', ' ', tweet,flags=regex.UNICODE)
	#Removing links 
	tweet = regex.sub(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+', ' ', tweet)
	#replace underscores with spaces
	tweet = tweet.replace("_"," ")
	#remove elongations
	tweet = regex.sub(r'(.)\1{2,}',r'\1\1\1', tweet,flags=regex.UNICODE)
	#Convert hashtags into words
	tweet = regex.sub(r'[#_]+',' ', tweet,flags=regex.UNICODE)

	tweet  = " ".join(tweet.split()).strip()
	return tweet