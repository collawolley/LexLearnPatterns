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

#consumer_token,consumer_secret,ACCESS_TOKEN,ACCESS_TOKEN_SECRET
KEYS = [
["HHb0Q4EwqUFhiOT9cuZw","wiUpi18szMmaBeDe3Xz0W8hTm4DSSSwRKSAdE5OTv0",'158681231-7iclqcgq8kFkPZBiQPK0AruMSKySUlNr0FethRFf','VisPcmHHE6ENNDspL48g15CloHNVmt0FRMPopCdphzpQb'],
["2mTxwXl2N2PSS9q0753KClYz8","vKJw0QRaeq7ohMIQ4ubsLjwf8wDSswwaPBVyzMiUhrJwGkSU9z","158681231-bd6lLKj34S2DVEU4FonO6lb86xLC2PnDEbj4kjYK","cpKIxPci94NaSc9QF10JRM99las8Nx05UtthvHkvTK2u2"],
["IVGTcvVHafHAieO1mQ7tkNR9C","OUtW8Ce1UC9N5ihL9GjMhwSG94eyaOURtoUkI1ksJ3MrpB9Ksw","158681231-LPztIzse604LkQmWmthnemkB3l71Bp4GsEp5ulf7","ao1eKOONDPxKp1xIdm4z42pl77kwxRfxL9AEmrHYkRQDC"]
]


class TweetGrapper:
  
  def  __init__ (self,streamSleep=30):
    self.consumer_token = KEYS[0][0]
    self.consumer_secret = KEYS[0][1]
    self.ACCESS_TOKEN = KEYS[0][2]
    self.ACCESS_TOKEN_SECRET = KEYS[0][3]
    self.auth = tweepy.OAuthHandler( self.consumer_token,self.consumer_secret )
    self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
    self.api = tweepy.API(self.auth)
    self.streamSleep = streamSleep
    self.keyid = 0 


  def shiftAuthKeys(self):
    self.keyid +=1 
    self.keyid = self.keyid % len(KEYS)
    i = self.keyid
    self.consumer_token = KEYS[i][0]
    self.consumer_secret = KEYS[i][1]
    self.ACCESS_TOKEN = KEYS[i][2]
    self.ACCESS_TOKEN_SECRET = KEYS[i][3]
    self.auth = tweepy.OAuthHandler( self.consumer_token,self.consumer_secret )
    self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
    self.api = tweepy.API(self.auth)


  def search(self,keywords,method,clean=False,uniq=True,loc="egypt",lang="ar"):
    
    tweetList = []
    keyword = "OR".join(keywords)

    tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)  

    if uniq is True:
      tmp = tweets
      tweets = []
      for line in Utils.uniq(sorted(tmp)):
        tweets.append(line)
        
    for tweet in tweets:      
      method(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))


  def stream(self,keywords,method,loc="egypt",lang="ar"):

    #for each 400 keywords , initialize stdoutlistener object for it (because limit of streaming api for twitter is 400)

    l = StdOutListener(method)
    l.keywords = keywords

    #todo implement locations
    locs = LOCATIONS[loc]
    langs = [lang]
    
    stream = Stream(self.auth, l)
    stream.filter(track=l.keywords,languages=langs,locations=locs)


  def streamloop(self,keywords,method,loc="egypt",lang="ar"):
    lastID = 0
    keyword = " OR ".join(keywords)
    print keyword
        
    while 1 :
      try :
          tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)    
          tweets = sorted(tweets, key=lambda x: x.id)

          for tweet in tweets:
            if True :#tweet.id > lastID:        
              method(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))
              lastID = tweet.id
          time.sleep(self.streamSleep)
      except tweepy.TweepError as e:
        if str(e.message[0]['code']) == "88":
          self.shiftAuthKeys()
