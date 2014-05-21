#encoding:utf-8 
'''
Created on Oct 28, 2013
python 2.7.3 
@author: hadyelsahar 
'''
import tweepy
import sys
import argparse
import regex
import subprocess
from Vectors.CosineSim import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import threading
from Classes.Tweet import *
from TweetGrapper.TweetGrapper import * 


#common usages:
#1- search keywords from file in twitter and add to file 
#2- subscribe to stream of keywords and write to file

# command line arguments:
parser = argparse.ArgumentParser(description='tool to Grap tweets from twitter API - show on console or write to  output file- giving some input words from text file - or search keywords -- [[optional]] clean tweets')
parser.add_argument('-mode','--mode', help='either "search" or "stream" ',required=True)
parser.add_argument('-i','--input', help='Input file name contains keywords to search for',required=True)
parser.add_argument('-o','--output',help='Output file name - print in console if not specified', required= False)
parser.add_argument('-c','--clean',help='clean tweets by removal or  RT  , Twitter username , Elongations and non alphanumericals', required= False , action="store_true")
parser.add_argument('-kw','--showkw',help='show keyword that was used to get the tweet before the tweet itself separated by a tab', required= False , action="store_true")
parser.add_argument('-id','--showid',help='show id of the tweet before the tweet itself separated by a tab', required= False , action="store_true")
parser.add_argument('-u','--uniq',help='extract uniq list of tweets of input file to outputfile based on cosine Similarity', required= False, action="store_true")
parser.add_argument('-l','--lang',help='specify language of the tweets', required= False)
parser.add_argument('-loc','--location', help='activate search mode and capture keyword for search',required=False)
parser.add_argument('-sep','--separator',help='separator used to separate between tweets , otherwise newline is used ', required= False)

args = parser.parse_args()

if args.uniq is True and args.output is None:
  parser.error('must specify output file when choosing --uniq [-u]  option')

if args.showkw is True and args.mode.lower() in "stream":
  parser.error('showing keyword is not implemented yet with streaming mode')


######--- Helper functions

def writeTweet(tweet):

  if args.clean is True :  
    tweetText = tweet.clean()
  else :
    tweetText = tweet.simpleText()


  if args.showid is True : 
    tweetText = str(tweet.id) +'\t'+ tweetText
      
  if args.showkw is True and tweet.searchKeyword is not None: 
    tweetText = tweet.searchKeyword +'\t'+ tweetText

  separator = ("\n" if args.separator is None else args.separator)      
  
  if args.output is not None :
    with open(args.output, "a") as myfile:
      tweetText = tweetText+separator
      myfile.write(tweetText.encode('utf-8'))           
  else :
    print tweetText


keywords = []
# reading keywords from input file 
with open(args.input) as f:
    kws = f.read().split("\n")    
    keywords = [kw.strip() for kw in kws if len(kw) > 0]        

grap = TweetGrapper()

#Search Mode
#------------------
if  "search" == args.mode.lower():   
  print "Activating search mode"
  grap.search(keywords,writeTweet)
#STREAM Mode
#------------------
elif "stream"  == args.mode.lower():
  print "Activating stream mode"
  grap.stream(keywords,writeTweet)

#Streamloop Mode
#------------------
elif "streamloop" == args.mode.lower():
  print "Activating streamloop mode"
  grap.streamloop(keywords,writeTweet)
