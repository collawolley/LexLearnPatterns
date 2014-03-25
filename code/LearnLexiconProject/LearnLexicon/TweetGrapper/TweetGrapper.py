#encoding:utf-8 
'''
Created on Oct 28, 2013
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


class StdOutListener(StreamListener): 
  counter = 0 
  printevery = 100

  """ A listener handles tweets are the received from the stream.
  This is a basic listener that just prints received tweets to stdout.
  """
  def __init__(self):     
    self.run = True
    self.keywords = []

  def on_data(self, data):                
    tweet = regex.sub(r'[\t\n\s]+',' ',json.loads(data)['text'])           
    writeTweet("", tweet)
    StdOutListener.counter += 1 
    if StdOutListener.counter % StdOutListener.printevery == 0 and args.output is not None:
      print str(StdOutListener.counter) + "tweets collected"

    if self.run:                  
      return True

    else :
      return False

  def on_error(self, status):
    print status


class TweetGrapper:
  
  def  __init__ (self,consumer_token = "HHb0Q4EwqUFhiOT9cuZw",
  consumer_secret = "wiUpi18szMmaBeDe3Xz0W8hTm4DSSSwRKSAdE5OTv0",
  ACCESS_TOKEN = '158681231-7iclqcgq8kFkPZBiQPK0AruMSKySUlNr0FethRFf',
  ACCESS_TOKEN_SECRET = 'VisPcmHHE6ENNDspL48g15CloHNVmt0FRMPopCdphzpQb'):
    self.consumer_token = consumer_token
    self.consumer_secret = consumer_secret
    self.ACCESS_TOKEN = ACCESS_TOKEN
    self.ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler( consumer_token,consumer_secret )
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    self.api = tweepy.API(auth)

  def search(self,keyword,clean=False,uniq=True,loc="egypt",lang="ar"):
    
    tweetList = []

    tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)  

    if uniq is True:
      tmp = tweets
      tweets = []
      for line in Utils.uniq(sorted(tmp)):
        tweets.append(line)
        
    for tweet in tweets:      
      tweetList.append(Tweet(tweet.text,language=lang,searchKeyword=keyword))

    return tweetList
