#encoding:utf-8 
'''
Created on Dec 27, 2013
python 2.7.3 
@author: hadyelsahar 
'''

import argparse
import regex
import ConfigParser
import re
import math


#Helpers
#-------------------------------------

def takeWindow(tweet,word,windowsize):

    if tweet.startswith(word+" ") or " "+word+" " in tweet or tweet.endswith(" "+word):

        #if window size = -1 that means no window
        if windowsize == -1 :
            return tweet

        pos = tweet.find(word)
        startpos = pos
        endpos = pos+len(word)
    
        #if word occur in the start of the sentence 
        if tweet.startswith(word+" "):
            subwindow = " ".join([i for i in tweet[endpos+1:].split(" ") if len(i)>0][0:windowsize])
            window = word+" "+subwindow
            return window

        #if word occur in the end of the sentence 
        elif tweet.endswith(" "+word):
            subwindowlist = [i for i in tweet[0:startpos].split(" ") if len(i) > 0 ]
            subwindow = " ".join(subwindowlist[len(subwindowlist)-windowsize:])
            window = subwindow+" "+word
            return  window

        #if word occur in the middle of the sentence 
        elif " "+word+" " in tweet:
            subwindowafter = " ".join([i for i in tweet[endpos+1:].split(" ") if len(i)>0][0:windowsize])
            subwindowlistbefore = [i for i in tweet[0:startpos].split(" ") if len(i) > 0 ]
            subwindowbefore = " ".join(subwindowlistbefore[len(subwindowlistbefore)-windowsize:])
            window = subwindowbefore+" "+word+" "+subwindowafter
            return window

    else : return ""

# command line arguments parsing 
##################################

parser = argparse.ArgumentParser(description='tool to extract set of Subjecitve Words and idioms depending on set of Patterns written in Config File')
parser.add_argument('-c','--config', help='Input Config file name',required=True)
parser.add_argument('-sl','--seedlexicon', help='Input classified lexicon file name',required=False)
parser.add_argument('-l','--lexicon', help='Input lexicon file name to be classified',required=False)
parser.add_argument('-i','--input', help='Input Tweets files to Extract subjective words from',required=True)
parser.add_argument('-o','--output',help='Output file name that contains lexicon after classification with PMI values', required= False)
parser.add_argument('-t','--tag',help='option for tagging tweets data dump if an unannotated dump is given as input', required= False , action="store_true")
parser.add_argument('-pmi','--pmi',help='option calculating pmi from tagged tweets dump', required= False , action="store_true")
parser.add_argument('-pmit','--pmit',help='option calculating pmi by counting number of tags from tagged tweets dump', required= False , action="store_true")
parser.add_argument('-w','--window',help='window size to take around the seed lexicon word', required= False )
parser.add_argument('-wd','--windowDelimiter',help='take window around the word starting and ending with delimiters', required= False, action="store_true")
args = parser.parse_args()

##todo : make set of verifications on the Args in both screnarios , tagging and pmi 

if args.window is not None:
    if not args.window.isdigit(): 
        parser.error('must specify window size in integer form')

# loading config file
#######################

#print("loading config file ....")
Config = ConfigParser.ConfigParser()
Config.read(args.config)
def config(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

#loading Options  
Options = {}
init = config("variables")
for i in init :	
	Options[i] = set([x.strip() for x in init[i].split(",")])


# loading Lexicon file 
########################

lex_file = open(args.seedlexicon, 'r')
lex = lex_file.read().split("\n")

posLexicon = set()
negLexicon = set()

for line in lex:		
    if len(line) > 0  and "\t" in line:
        w = line.split("\t")
        if (w[1] == "positive"):
            posLexicon.add(w[0])
        else:
            negLexicon.add(w[0])

del lex 
################

in_file = open(args.input ,'r')
out_file = open(args.output, 'w+')


taggedTweets = ""

#annotating Tweets File:
########################
if args.tag:
    tag_file = open("tagged_"+args.input, 'w+')
    print "started Tagging Tweets...."
    tweets = in_file.read().split("\n")
    
    counter  = 0 

    # rgxpart = "("+"|".join(Options["simplenegators"])+")"

    for line in[line for line in tweets if len(line) > 0]:

        taggedLine = line
        for w in posLexicon:
            
            #way faster than regex
            if taggedLine.startswith(w+" ") or taggedLine.endswith(" "+w) or " "+w+" " in taggedLine:
                taggedLine = taggedLine.replace(w,"[POS]")

        for w in negLexicon:
            
            if taggedLine.startswith(w+" ") or taggedLine.endswith(" "+w) or " "+w+" " in taggedLine:
                taggedLine = taggedLine.replace(w,"[NEG]")

        tag_file.write(taggedLine+"\n")

        counter += 1 
        if counter % 1000 == 0 : print str(counter) +" tweets Tagged in Thread " 

    del tweets
    tag_file.close()

#Calculating PMI
###################

if args.pmi :

    words_file = open(args.lexicon, 'r')
    words = {}
    lextext= words_file.read().strip()
    for w in lextext.split("\n"):
        warr = w.split("\t")                
        if len(warr) == 2 :            
            words[warr[0].strip()]= warr[1]                        
        else:
            words[warr[0].strip()]= ""

    pmi_count = {}
    wordCount = {}

    print "started calculating pmi for "+str(len(words)) +" extracted words"

    #initializing pmi index {"word":[poscount negcount]}
    for word,p in words.items():        
        pmi_count[word] = [0,0,0]
        wordCount[word] = 0

    taggedTweets = in_file.read().split("\n")

    counter = 0

    poscount=0
    negcount=0
    norm_pmi_pos = 0 
    norm_pmi_neg = 0 
    allTweets = 0

    for tweet in taggedTweets:
        originalTweet = tweet

        #prevent tweets of mixed polarity or nagations 
        #because they are indicative    
        if not ("[POS]" in tweet and "[NEG]" in tweet ) and len(tweet) > 0:        
            
            #count all tweets
            allTweets += 1

            #counting total number of POS or NEG tweets 
            if "[POS]" in tweet:                        
                poscount +=1 
                
            elif "[NEG]" in tweet:                
                negcount +=1 

            #for each word to be classified take window , window with delimiter or do nothing
            for word,p in words.items():
                tweet = originalTweet                

                if args.windowDelimiter:
                    #tobe implemented
                    parser.error('WINDOW DELIMITER TO BE IMPLEMENTED')

                #if window size               
                elif args.window is not None:
                    windowsize = int(args.window)                    
                    tweet = takeWindow(tweet,word,windowsize)

                #if no window option selected 
                else :                
                    tweet = takeWindow(tweet,word,-1)

                if len(tweet) > 1 :
                    # all if conditions use takeWindow so if it's not "" then word in the the tweet:
                    #count number of occurrence of word to calculate p(w)
                    wordCount[word] +=1 

                    if "[POS]" in tweet:
                        pmi_count[word][0] +=1                                     
                    elif "[NEG]" in tweet:
                        pmi_count[word][1] +=1    
                    else:
                        pmi_count[word][2] +=1


        counter += 1 
        if counter % 1000 == 0 : print str(counter) + " pmi calculated out of " + str(len(taggedTweets)) 
    
#done counting now calculating Pmi      

    for w , p in pmi_count.items():
        #p(w)
        pw = float(wordCount[w])/allTweets        

        if (p[0] != 0):        
            #calculating pos pmi
            
            #p(w,pos)
            pXpos = float(p[0])/allTweets
            #P(pos)
            pPos = float(poscount)/allTweets    
            #Pmi pos

            pmi_pos = math.log((float(pXpos)/(pPos*pw)),2)
                    
            #normalize Pmi pos

            den_pos = -1 * math.log(pXpos,2)
            norm_pmi_pos = float(pmi_pos)/(den_pos)

        else :
            norm_pmi_pos = 0

        if(p[1] !=0):
            #p(w,neg)
            pXneg = float(p[1])/allTweets                        
            #P(neg)
            pNeg = float(negcount)/allTweets
            #pmi Neg
            pmi_neg = math.log((float(pXneg)/(pNeg*pw)),2)
            #normalize Pmi Neg
            den_neg = -1 * math.log(pXneg,2)
            norm_pmi_neg = (float(pmi_neg))/(den_neg)
    
        else:
            norm_pmi_neg = 0

        print str(wordCount[w]) +"\t" + str(p[0]+p[1]+p[2])
        out_file.write(w + "\t"+ str(p[0])+ "\t"+ str(p[1]) + "\t"+ str(p[2]) + "\t" +str(norm_pmi_pos) +"\t"+ str(norm_pmi_neg) +"\t"+ ("POS" if norm_pmi_pos > norm_pmi_neg else "NEG") +"\t" + words[w] + "\n")

in_file.close()
out_file.close()




