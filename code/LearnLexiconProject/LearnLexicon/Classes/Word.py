#encoding:utf-8 
'''
Created on 24 March, 2013
python 2.7.3 
@author: hadyelsahar 
'''

class Word:
	def __init__(self,text,polarity=None,pattern=None):
		self.text = text
		self.polarity = polarity
		self.pattern = pattern
		
	def __str__(self):
		return self.text




	


	

