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

    print "started Tagging Tweets...."
    tweets = in_file.read().split("\n")
    tag_file = open("tagged_"+args.input, 'w+')
    
    counter  = 0 

    for line in tweets:
        taggedLine = line
        for w in posLexicon:

            # rgx = "("+"|".join(Options["simplenegators"])+")" + "\s"+ w + "\s"
            # taggedLine = re.sub(rgx,"[NEG]",taggedLine)

            if " "+w+" " in taggedLine :             
                taggedLine = taggedLine.replace(w,"[POS]") + "\n"

        for w in negLexicon:

            # rgx = "("+"|".join(Options["simplenegators"])+")" + "\s"+ w + "\s"
            # taggedLine = re.sub(rgx,"[POS]",taggedLine)

            if " "+w+" " in taggedLine :             
                taggedLine = taggedLine.replace(w,"[NEG]") + "\n"


        tag_file.write(taggedLine)

        counter += 1 
        if counter % 1000 == 0 : print str(counter) +" tweets Tagged in Thread " 

    del tweets


#Calculating PMI
###################

if args.pmi:

    words_file = open(args.lexicon, 'r')
    words = [w.strip() for w in words_file.read().split("\n") if len(w) > 0 and w not in posLexicon and w not in negLexicon]

    pmi_count = {}
    print "started calculating pmi for "+str(len(words)) +" extracted words"

    #initializing pmi index {"word":[poscount negcount]}
    for word in words:        
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


            for word in words:
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

            pXpos = float(p[0])/allTweets
            pXneg = float(p[1])/allTweets        
            pPos = float(poscount)/allTweets
            pNeg = float(negcount)/allTweets

            den_pos = -1 * math.log(pXpos,2)
            den_neg = -1 * math.log(pXneg,2)
            pmi_pos = math.log(float(pXpos)/(pPos*pNeg))
            pmi_neg = math.log(float(pXneg)/(pPos*pNeg))


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
        out_file.write(w + "\t"+ str(p[0]+p[1]) + "\t" +str(norm_pmi_pos) +"\t"+ str(norm_pmi_neg) +"\t"+ ("POS" if norm_pmi_pos > norm_pmi_neg else "NEG") + "\n")


in_file.close()
out_file.close()



