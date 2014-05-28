#encoding:utf-8 
'''
Created on 24 March, 2014
python 2.7.3 
@author: hadyelsahar 
'''
import regex


class Tweet:
	def __init__(self,id,text,language=None,polarity=None,searchKeyword=None,country=None):
		self.id = id 
		self.text = text
		self.language = language
		self.polarity= polarity
		self.searchKeyword = searchKeyword
		self.cleanText = None
		self.normText = None
		self.country = country



	def __str__(self):
		return self.text
	
	def simpleText(self):
		return regex.sub(r'[\t\n\s]+',' ',self.text)


	#send True if wanted to Normalize otherwise wont normalize
	def clean(self,NORM = False ):
		
		if self.cleanText is not None :
			if NORM:
				return self.normalize(self.cleanText)
			else :
				return self.cleanText
		else :						
			tweet = self.text
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
		  	#remove unneeded puncituation
		  	tweet = regex.sub(r'[,\.@^%:"\']+',' ', tweet,flags=regex.UNICODE)
		  	#remove extra spaces
		  	tweet  = " ".join(tweet.split()).strip()

		  	self.cleanText = tweet

		  	if NORM:
		  		tweet = self.normalize(tweet)

	  		return tweet
	

	def normalize(self,text):					
		normTweet = text
	  	normLetters = {"ة":"ه","ى":"ي","أ":"ا","إ":"ا","آ":"ا","الأ":"الا","الإ":"الا","الآ":"الا","ﻷ":"لا"}
	  	for  k in normLetters.keys():
	  		w = k.decode("utf-8")
	  		R = normLetters[k].decode("utf-8")
	  		if w in normTweet:
	  			normTweet = normTweet.replace(w,R)
	  	
		return normTweet






