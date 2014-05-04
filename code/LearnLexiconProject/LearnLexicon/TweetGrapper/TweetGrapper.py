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
import threading
from tweepy import Stream
import json
import time

LOCATIONS = {
'egypt': [22.187405, 26.561508, 31.353637, 36.207504],
'cairo': [29.965643, 31.14682, 30.157002, 31.549194]
}


class StdOutListener(StreamListener): 
  counter = 0 
  printevery = 100

  """ A listener handles tweets are the received from the stream.
  This is a basic listener that just prints received tweets to stdout.
  """
  def __init__(self,method):     
    self.run = True
    self.keywords = []
    self.method = method

  def on_data(self, data):                
    text = json.loads(data)['text']
    id = json.loads(data)['id']    
    tweet = Tweet(id,text)
    self.method(tweet)
    StdOutListener.counter += 1

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
    self.auth = tweepy.OAuthHandler( consumer_token,consumer_secret )
    self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    self.api = tweepy.API(self.auth)

  def search(self,keyword,clean=False,uniq=True,loc="egypt",lang="ar"):
    
    tweetList = []

    tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)  

    if uniq is True:
      tmp = tweets
      tweets = []
      for line in Utils.uniq(sorted(tmp)):
        tweets.append(line)
        
    for tweet in tweets:      
      tweetList.append(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))

    return tweetList


  def stream(self,keywords,method,loc="egypt",lang="en"):

    #for each 400 keywords , initialize stdoutlistener object for it (because limit of streaming api for twitter is 400)

    l = StdOutListener(method)
    l.keywords = [keywords]

    #todo implement locations
    locs = LOCATIONS[loc]
    langs = [lang]
    
    stream = Stream(self.auth, l)
    stream.filter(track=l.keywords,languages=langs,locations=locs)


  def streamloop(self,keywords,method,loc="egypt",lang="ar"):
    lastID = 0
    keyword = "OR".join(keywords)
    
    while 1 :
      tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)    
            
      for tweet in tweets:
        if tweet.id > lastID:        
          method(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))
          lastID = tweet.id
      time.sleep(1)