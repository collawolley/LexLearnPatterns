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
["2mTxwXl2N2PSS9q0753KClYz8","vKJw0QRaeq7ohMIQ4ubsLjwf8wDSswwaPBVyzMiUhrJwGkSU9z","158681231-bd6lLKj34S2DVEU4FonO6lb86xLC2PnDEbj4kjYK","cpKIxPci94NaSc9QF10JRM99las8Nx05UtthvHkvTK2u2"],
["IVGTcvVHafHAieO1mQ7tkNR9C","OUtW8Ce1UC9N5ihL9GjMhwSG94eyaOURtoUkI1ksJ3MrpB9Ksw","158681231-LPztIzse604LkQmWmthnemkB3l71Bp4GsEp5ulf7","ao1eKOONDPxKp1xIdm4z42pl77kwxRfxL9AEmrHYkRQDC"],
["cXA1X446gnZVNFCUuWYavod6U","j9lUDCUyIibJpMF1p29mX5DiFMNbcvuk580q6O0ftp8UAJWW9Y","2512427384-RDkrZCuvVamZckF446FLfXSRYMjAmOCZI4rayfF","RTTSVZKNoPBfq4l6GxRL6bWLanTvCPYwnIMyp9TnZVTiH"],
["UaoUUazXQerf7lXVQyBofwojf","oyPDO1xqbbWpaF5Bi1sL1KYd0eWkUr9WFoPsh30QvIpAjNivB8","2512427384-YS9fudbQbLAVVb73nmViNOjDQKdQcsOmVgTSm4k","jAf4Fy8qtY6ALg0hwTtche5vl8XOX5Jm4jzKf07pMeL6R"],
["VJwKpL0Lx90RbtHcLTqTrZSpR","K5u0TA01s0CTwcbDjR9ehZ6ryGaNT0AaeonIV6PBkdb5WqADJC","2512515884-uJitqG6443AbEVQDq5SAUDb2N2IGjHzwv0dJT0J","lw7EkiVaLc7waWGQpW9p6H6xqASxTKNekgHBPIAxkffzQ"],
["MsI2UNEWsDj4LXjsL0cNveHvh","Fn6g3sirU8BBt65B6bJpoBrzN1x3aLV6HAc3BfpGG0p2d8uYAI","2512633687-bPQtSlC1OrXz4vfHq8oo3Uf8XGlrVBqT1ORb65v","u58LN8VhuDC0zPlZ5YMDL8mV8822iavtn7MItjva0x4Pb"],
["JVg5hvFv7QEkGz87JPOh28jdc","I69unoJD9bWm3Nmq0J4Gqut6Vz39RmrRjqDxgp4pbQLpwpJZjN","2512633687-NSVZHJ2NHsWAPREVjGcrUTU8Cr29YdJJncPvaWw","5CCK3XhOLHe004pDlNJWku2sH0FW8zWGCz0VuvxitiaxX"],
["B8Hyp2CMBh4ymVdKlmMdyR6RR","TC8AO4c0MQPn5BSihGkwgjaqE8oL4gNSZ7fRXtdNw1xD9kQLr2","2512633687-h5nYNWaq2KYXIhju7cyMwXYlrpPB8FWFtCBhKte","futpoDmzy55M7nhJzPlOkYd9pM2YOUOUHJu4yP9PKRdq5"],
["4WtoSaSUwwWuziIaBEMNsvWh0","4O0yH33ivMCO0ZuIq3TlZe38N3Y8eqg9WzQkn3NSgVTrV6srZK","2512672214-yFRDDBJY1MESaIdS66MnFRg1ysoQgxUtshnmV11","SdWo9RgEEATLlQD7jJzSelLSMpgzDYgJWpgarS5VnFUXo"],
["BFu6JIuczLsSeCn1JqTqauKic","jZNXTprHGoJ4rxBrvhhCP6MjnnPxASVLtwIe3nntwee7aq7VGD","2512672214-4Lv7sq1a2zJZMPxihvI5xjcUndD1FHIf3lK7Z1q","tCPXolJ6cDYTCCoAFXuBiVsTRqXUWSHanZwxyBDAU9ENJ"]
]


class TweetGrapper:
  
  def  __init__ (self,streamSleep=1):
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

  
  #if method = None , return tweets collected as tweets objects
  def search(self,keywords,method,clean=False,uniq=True,loc="egypt",lang="ar"):
    
    tweetList = []
    keyword = "OR".join(keywords)
    try :
      tweets = self.api.search(keyword,count=1000,lang=lang,locale=loc)  
    
      if uniq is True:
        tmp = tweets
        tweets = []
        for line in Utils.uniq(sorted(tmp)):
          tweets.append(line)

      if method is not None:  
        for tweet in tweets:
          method(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))
      else:
        toReturn = []
        for tweet in tweets:      
          toReturn.append(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))
      
        return toReturn

    except tweepy.TweepError as e:
      print e      
      if e.message[0]['code'] == 88:  
        print "changedkeys"
        self.shiftAuthKeys()
        return []


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
            if tweet.id > lastID:        
              method(Tweet(tweet.id,tweet.text,language=lang,searchKeyword=keyword))
              lastID = tweet.id
          time.sleep(self.streamSleep)
      except tweepy.TweepError as e:
        print tweepy.error.TweepError[0].code
        if str(e.message[0]['code']) in "88":
          self.shiftAuthKeys()
