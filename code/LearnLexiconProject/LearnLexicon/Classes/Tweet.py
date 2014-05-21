#encoding:utf-8 
'''
Created on 24 March, 2014
python 2.7.3 
@author: hadyelsahar 
'''
import regex


class Tweet:
	def __init__(self,id,text,language="ar",polarity=None,searchKeyword=None):
		self.id = id 
		self.text = text
		self.language = language
		self.polarity= polarity
		self.searchKeyword = searchKeyword
		self.cleanText = None


	def __str__(self):
		return self.text
	
	def simpleText(self):
		return regex.sub(r'[\t\n\s]+',' ',self.text)


	def clean(self):
		if self.cleanText is not None:
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
	  		return tweet