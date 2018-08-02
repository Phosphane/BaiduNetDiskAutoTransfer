#coding : utf-8
#Author : VinylChloride
#Version : 0.0.1 Alpha


#Language Parser Module (Develpoer State)


import os
import json
import sys

class Lang(object):

	def __init__(self,lang = "en"):
		self.__langFloder = "." + os.sep + "lang" + os.sep
		self.__langFile = self.__langFloder + lang + ".json"
		self.__langConfig = {}

		if (self.reload(lang) == -1):return -1


	def get(self,langKeyword):
		if (self.__langConfig.__contains__(langKeyword)):
			return self.__langConfig[langKeyword]
		else:
			print ("Warring : Language Key Word %s Not Found." % langKeyword)
			return None


	def reload(self,lang):
		self.__langFile = self.__langFloder + lang + ".json"
		if (self.__checkLang() == -1):return -1
		with open(self.__langFile,"r+") as langFile:
			self.__langConfig = json.load(langFile)
			langFile.close()

	def __checkLang(self):
		if ((not os.path.exists(self.__langFloder)) or os.path.isfile(self.__langFloder)):
			print ("Language Floder Not Found !")
			return -1
		if ((not os.path.exists(self.__langFile)) or (not os.path.isfile(self.__langFile))):
			print ("Language %s Configuration File Not Found." % lang)
			return -1
