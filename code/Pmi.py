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
parser.add_argument('-w','--window',help='take window size around the word', required= False )
parser.add_argument('-wd','--windowDelimiter',help='take window around the word starting and ending with delimiters', required= False, action="store_true")
args = parser.parse_args()

##todo : make set of verifications on the Args in both screnarios , tagging and pmi 

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
    for w in words_file.read().split("\n"):
        warr = w.split("\t")
        if len(warr) == 2 :
            words[warr[0]]= warr[1]
        else:
            words[warr[0]]= ""

    pmi_count = {}
    print "started calculating pmi for "+str(len(words)) +" extracted words"

    #initializing pmi index {"word":[poscount negcount]}
    for word,p in words.items():        
        pmi_count[word] = [0,0]

    taggedTweets = in_file.read().split("\n")

    counter = 0

    poscount=0
    negcount=0
    norm_pmi_pos = 0 
    norm_pmi_neg = 0 

    for tweet in taggedTweets:

        if not ("[POS]" in tweet and "[NEG]" in tweet ) :

            polarity = "None"

            if "[POS]" in tweet:
                polarity = "POS"            
                poscount +=1 
                
            if "[NEG]" in tweet:
                polarity = "NEG"
                negcount+=1 

            originalTweet = tweet
            for word,p in words.items():

                # if args.windowDelimiter:
                #to be implemented

                # if args.window is not None:
                    

                if word in tweet:
                    if "POS" in polarity:
                        pmi_count[word][0] +=1                                     
                    if "NEG" in polarity:
                        pmi_count[word][1] +=1                                     
            counter += 1 
            if counter % 1000 == 0 : print str(counter) + " pmi calculated out of " + str(len(taggedTweets)) 

    allTweets = len(taggedTweets)
    for w , p in pmi_count.items():

        if (p[0] != 0 and p[1] != 0 ):

            px = float(len([ line for line in taggedTweets if w in line]))/allTweets

            pXpos = float(p[0])/allTweets
            pXneg = float(p[1])/allTweets        
            pPos = float(poscount)/allTweets
            pNeg = float(negcount)/allTweets

            den_pos = -1 * math.log(pXpos,2)
            den_neg = -1 * math.log(pXneg,2)
            pmi_pos = math.log(float(pXpos)/(pPos*px))
            pmi_neg = math.log(float(pXneg)/(pNeg*px))

            norm_pmi_pos = float(pmi_pos)/den_pos
            norm_pmi_neg = float(pmi_neg)/den_neg

        else :
            if (p[0] == 0):
                norm_pmi_pos = 0
            if (p[1] == 0):
                norm_pmi_neg = 0

        print norm_pmi_pos
        print norm_pmi_neg
        print norm_pmi_pos > norm_pmi_neg
        out_file.write(w + "\t"+ str(p[0]+p[1]) + "\t" +str(norm_pmi_pos) +"\t"+ str(norm_pmi_neg) +"\t"+ ("POS" if norm_pmi_pos > norm_pmi_neg else "NEG") +"\t" + words[w] + "\n")


in_file.close()
out_file.close()



