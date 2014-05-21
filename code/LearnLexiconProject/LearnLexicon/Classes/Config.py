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
from Tweet import *
from Word import * 

class Config:
	Patterns = {}
	Options = {}
	variables = []

	def __init__(self,configFile):
		self.configFile = configFile
		self.__loadConfig();

	def __loadConfig(self):
		Config = ConfigParser.ConfigParser()
		Config.read(self.configFile)
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
		init = config("variables")
		for i in init :	
			self.Options[i] = set([x.strip() for x in init[i].split(",")])

		#loading variable names
		self.variables = [ "__"+k for k,v in self.Options.items()]
		
		#loading patterns
		patternSecNames = [p  for p in Config.sections() if "patterns" in p]		
		for secName in patternSecNames:
			self.Patterns[secName] = {}

			for name,pattern in config(secName).items():
				if any( v in pattern for v in self.variables):
					#patterns has variables inside	
					for x in [v for v in self.variables if v in pattern]:			
						#capture parts of patterns that has variables names and remove the dunderscore
						var = x.strip("__")
						#build regex for variables, (?: is for non capturing group in regex)
						rgxPart = "(?:"+"|".join(self.Options[var])+")"				
						pattern = pattern.replace(x,rgxPart)							

						self.Patterns[secName][name] = re.compile(pattern)						
				else:
					#if pattern doesn't have variables inside , just write it 
					self.Patterns[secName][name] = re.compile(pattern)			

	def reloadConfig(self):
		Config = ConfigParser.ConfigParser()
		Config.read(self.configFile)
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


		#loading patterns
		patternSecNames = [p  for p in Config.sections() if "patterns" in p]		
		for secName in patternSecNames:
			self.Patterns[secName] = {}

			for name,pattern in config(secName).items():
				if any( v in pattern for v in self.variables):
					#patterns has variables inside	
					for x in [v for v in self.variables if v in pattern]:			
						#capture parts of patterns that has variables names and remove the dunderscore
						var = x.strip("__")
						#build regex for variables, (?: is for non capturing group in regex)
						rgxPart = "(?:"+"|".join(self.Options[var])+")"				
						pattern = pattern.replace(x,rgxPart)							

						self.Patterns[secName][name] = re.compile(pattern)						
				else:
					#if pattern doesn't have variables inside , just write it 
					self.Patterns[secName][name] = re.compile(pattern)		

	def addVariable (self,variable):
		if variable is not None :
			for k,v in variable.items():
				self.variables.append("__"+k)
				self.Options[k] = set(v)

	def removeVariable(self,variable):
		if variable is not None :
			for k,v in variable.items():
				if "__"+k in self.variables and self.Options[k] is not None:
					self.variables.remove("__"+k)
					del self.Options[k]