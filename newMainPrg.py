#coding : utf-8
#Author : VinylChloride
#Version : 1.0 Stable

from selenium import webdriver,common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import sys
import sqlite3
import json

# Define Log Moudle
import logging
logFileName = (str(time.ctime())+"_LOG.log").replace(":","-").replace(" ","")
logger = logging.getLogger(__name__)
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler(logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)
#Log Level
logger.setLevel(logging.DEBUG)


"""
	Database Col:
		Name TEXT , In this program is unicode.
		PanLink TEXT , In this program is string.
		PanPwd TEXT , In this program is string.
		isTransfered INT , In this program is bool.
	
"""


class dbOperation(object):
	def __init__(self,dbFile = None):
		if (not dbFile):
			logger.critical("Database Not Found.Exiting...")
			print("Database Not Found.Exiting...")
			sys.exit(1)
		self.dbConn = sqlite3.connect(dbFile)
		if (not self.dbConn):
			logger.critical("Can not connect to databse,Exiting...")
			print("Can not connect to databse,Exiting...")
			sys.exit(1)
		self.dbCursor = self.dbConn.cursor()
		if (not self.dbCursor):
			logger.critical("Can not get databse cursor,Exiting...")
			print(("Can not get databse cursor,Exiting..."))
			sys.exit(1)
		logger.info("Databse Initilized.")
		
		#Resources List : 
		#	element is dict
		#	dict contains key:
		#		Name , unicode
		#		PanLink , string
		#		PanPwd , string


		self.resList = []

		self.__getDataFromDB()


	def __getDataFromDB(self):
		try:
			for dbItem in self.dbCursor.execute("SELECT * FROM Resources"):#dbItem Type : tuple
				if (dbItem[3] != 0):continue
				resDict = {}
				resDict["Name"] = dbItem[0]
				resDict["PanLink"] = str(dbItem[1])
				resDict["PanPwd"] = str(dbItem[2])
				self.resList.append(resDict)
		except:
			logger.exception("Error On Reading Database")
			print ("Error On Reading Database , Please Check Log File.")
			sys.exit(1)



"""
Config.json:
	{
		"codeTextBoxXPath" : "XXX", #By XPath
		"codeEnterBtnXPath" : "XXX",	#By XPath
		"transferBtnClassName" : "XXX",
		"checkBoxClassName" : "XXX"

	}

"""


class MainFramework(dbOperation):
	def __init__(self,dbFile = None):

		#Parent:
		#	self.resList
		#	self.__getDataFromDB()

		dbOperation.__init__(self,dbFile)

		self.__webDri = None
		self.__linkCount = 0
		self.__linkCount = len(self.resList)
		self.__errLinkCount = 0
		self.__errLinkList = []
		self.__doneLinkCount = 0
		self.__codeTextBoxXPath = ""
		self.__codeEnterBtnXPath = ""
		self.__transferBtnClassName = ""
		self.__transferBtnSelector = ""
		self.__checkBoxClassName = ""
		self.__fileTreeNodeClassName = ""
		self.__fileTreeDialogXPath = ""
		self.__destnationPath = ""
		self.__fileTreeConfirmClassName = ""
		self.__notFoundID = ""

		self.__loadConfig()

		if (self.__linkCount == 0):
			print ("No Link Found , Exiting...")
			logger.info("No Link Found , Exiting...")
			sys.exit(0)
		print ("Found %d Links." % self.__linkCount)
		logger.info("Found %d Links." % self.__linkCount)
		print ("Starting Chrome.")
		logger.info("Starting Chrome.")
		self.__webDri = webdriver.Chrome() #This Script Only Tested On Chrome
		logger.info("Chrome Started.")

	#Resources List : 
	#	element is dict
	#	dict contains key:
	#		Name , unicode
	#		PanLink , string
	#		PanPwd , string
	def run(self):
		self.__login()
		for linkItem in self.resList:
			resName = linkItem["Name"]
			panLink = linkItem["PanLink"]
			panPwd = linkItem["PanPwd"]
			retCode = self.__transfer(panLink,panPwd)
			if (retCode == -1):
				self.__updateLinkStatus(panLink,-1)
				print ("Error On Transfer Link : %s" % panLink)
				logger.error("Error On Transfer Link : %s" % panLink)
				continue
			elif (retCode == -2):
				logger.warn("Link %s Has Been Banned." % panLink)
				print ("Link %s Has Been Banned." % panLink)
				self.__updateLinkStatus(panLink,-2)
			self.__updateLinkStatus(panLink,1)

	def __transfer(self,panLink,panPwd):
		print ("Starting Transfer With Link : %s , Pwd : %s" % (panLink,panPwd))
		logger.info("Starting Transfer With Link : %s , Pwd : %s" % (panLink,panPwd))
		self.__webDri.get(panLink)
		try:
			enterCodeBtn = WebDriverWait(self.__webDri,3).until(
				EC.presence_of_element_located(
					(By.XPATH,self.__codeEnterBtnXPath)
				)
			)
		except common.exceptions.TimeoutException:
			try:
				WebDriverWait(self.__webDri,5).until(
					EC.presence_of_element_located(
						(By.ID,self.__notFoundID)
					)
				)
				return -2
			except common.exceptions.TimeoutException:
				pass

			logger.exception("Locate Code Enter Button Timeout.")
			print ("Locate Code Enter Button Timeout.")
			return -1

		logger.debug("Code Enter Button Raw Data : %s" % str(enterCodeBtn))

		try:
			codeTextBox = WebDriverWait(self.__webDri,3).until(
				EC.presence_of_element_located(
					(By.XPATH,self.__codeTextBoxXPath)
				)
			)
		except common.exceptions.TimeoutException:
			logger.exception("Locate Code Text Box Timeout.")
			print (("Locate Code Text Box Timeout."))
			return -1

		logger.debug("Code Text Box Raw Data : %s" % str(codeTextBox))

		if (codeTextBox != None):
			codeTextBox.send_keys(panPwd)
			logger.debug("Code %s Has Enter" % panPwd)
			enterCodeBtn.click()
		else:
			logger.error("Can not find code text box.")
			print ("Can not find code text box.")
			return -1

		try:
			checkBox = WebDriverWait(self.__webDri,2).until(
				EC.presence_of_element_located(
					(By.CLASS_NAME,self.__checkBoxClassName)
				)
			)
		except common.exceptions.TimeoutException:
			logger.exception("No Check Box Found Or Page Load Timeout.")
			print ("No Check Box Found Or Page Load Timeout.")
		except:
			logger.exception("Error On Locating Check Box.")
			return -1
		else:
			logger.info("Located Check Box.")
			logger.debug("Check Box Raw Data : %s" % checkBox)
			checkBox.click()
		"""
		try:
			retryCount = 0
			while (True):
				try:
					transferBtn = self.__webDri.find_elements_by_class_name(self.__transferBtnClassName)
				except common.exceptions.NoSuchElementException:
					retryCount += 1
					if (retryCount > 4):
						logger.error("Locate Transfer Button Timeout.")
						print ("Locate Transfer Button Timeout.")
						return -1
					logger.warn("Can not Locate Transfer Button , Trying %d Times." % retryCount)
					time.sleep(1)
					continue
				except:
					logger.exception("Error On Locating Transfer Button.")
					print ("Error On Locating Transfer Button.")
					return -1
				break
		except:
			pass

		"""
		try:
	#		transferBtn = WebDriverWait(self.__webDri,2).until(
	#			EC.presence_of_element_located(
	#				(By.CLASS_NAME,self.__transferBtnClassName)
	#			)
	#		)
			transferBtn = WebDriverWait(self.__webDri,2).until(
				EC.presence_of_element_located(
					(By.CSS_SELECTOR,self.__transferBtnSelector)
				)
			)
		except common.exceptions.TimeoutException:
			logger.exception("Locate Transfer Button Timeout.")
			print ("Locate Transfer Button Timeout.")
			return -1
		

		logger.debug("Transfer Button Raw Data : %s" % str(transferBtn))

		if (transferBtn == None):
			logger.error("Transfer Button Not Found.")
			print ("Transfer Button Not Found.")
			return -1
		"""
		for btnItem in transferBtn:
			print repr(btnItem.get_attribute("title"))
			print btnItem.get_attribute("title")
			#Waiting for get raw unicode data
		"""
		logger.info("Located Transfer Button.")
		try:
			transferBtn.click()
		except:
			logger.exception("Error On Clinking Transfer Button.")
			print ("Error On Clinking Transfer Button.")
			return -1

		try:
			WebDriverWait(self.__webDri,5).until(
				EC.presence_of_element_located(
					(By.XPATH,self.__fileTreeDialogXPath)
				)
			)
		except common.exceptions.TimeoutException:
			logger.error("Locate File Tree Dialog Timeout.")
			print ("Locate File Tree Dialog Timeout.")
			return -1

		try:
			path = ""
			nodeList = self.__destnationPath.split("/")
			for i in range(1,len(nodeList)):
				path += ("/" + nodeList[i])
				logger.debug("Current Path : %s " % path)
				if (self.__findPath(path)):
					continue
				else:
					logger.error("Error On Link : %s panLink")
					print ("Error On Link : %s panLink")
					return -1
			"""
			try:
				pathConfirmBtn = WebDriverWait(self.__webDri,2).until(
					EC.presence_of_element_located(
						(By.XPATH,self.__fileTreeConfirmBtnXPath)
					)
				)
			except common.exceptions.TimeoutException:
				logger.error("Can not locate path confirmation buttion.")
				print ("Can not locate path confirmation buttion.")
				return -1

			pathConfirmBtn.click()


			return
			"""
		except:
			logger.exception("Error On Finding Path.")
			print ("Error On Finding Path.")
			return -1

		retryCount = 0
		while (True):
			try:
				pathConfirmBtn = self.__webDri.find_elements_by_class_name(self.__fileTreeConfirmBtnClassName)
			except common.exceptions.NoSuchElementException:
				retryCount += 1
				if (retryCount > 4):
					logger.error("Locate Path Confirmation Button Timeout.")
					print ("Locate Path Confirmation Button Timeout.")
					return -1
				logger.warn("Can not Locate Path Confirmation Button , Trying %d Times." % retryCount)
				time.sleep(1)
				continue
			except:
				logger.exception("Error On Locating Path Confirmation Button.")
				print ("Error On Locating Path Confirmation Button.")
				return -1
			break

		for tmpItem in pathConfirmBtn:
			if (tmpItem.get_attribute("title") == u'\u786e\u5b9a'):
				pathConfirmBtn = tmpItem
				break
		pathConfirmBtn.click()

			
	def __findPath(self,Path):
		try:
			isFound = False
			retryCount = 0
			while True:
				try:
					nodePaths = self.__webDri.find_elements_by_class_name(self.__fileTreeNodeClassName)
					if (retryCount > 3):
						logger.error("Can not loacte destnation path %s" % Path)
						print ("Can not loacte destnation path %s" % Path)
						return isFound
					if (len(nodePaths) == 1):
						time.sleep(0.5)
						retryCount += 1
						continue
					for nodeItem in nodePaths:
						if (nodeItem.get_attribute("node-path") == Path):
							print ("Located Destnation Path %s " % Path)
							logger.info("Located Destnation Path %s " % Path)
							logger.debug("Destnation Path Raw Data : %s" % str(nodeItem))
							nodeItem.click()
							isFound = True
							return isFound
					if (not isFound):
						retryCount += 1
						time.sleep(1)
				except common.exceptions.NoSuchElementException:
					retryCount += 1
					if (retryCount > 4):
						logger.error("Destnation path %s not found." % Path)
						print ("Destnation path %s not found." % Path)
						return False
					logger.debug("Destnation Path Not Found , Trying %d Times" % retryCount)
					time.sleep(0.5)
					continue
		except:
			logger.exception("Error On Locate Path %s " % Path)
			return False



	def __login(self):
		self.__webDri.get("https://pan.baidu.com/")
		print ("Please Confirm Login And Switch The Page To Recyle Bin.")
		raw_input("[?] Hit The Fucking Enter When You Ready.")
		logger.info("User Login.")
		print ("User Login.")


	def __loadConfig(self):
		jsonData = {}
		with open("config.json") as configFile:
			jsonData = json.load(configFile)
			configFile.close()
		try:
			self.__codeTextBoxXPath = jsonData["codeTextBoxXPath"]
			self.__codeEnterBtnXPath = jsonData["codeEnterBtnXPath"]
			self.__transferBtnClassName = jsonData["transferBtnClassName"]
			self.__transferBtnSelector = jsonData["transferBtnSelector"]
			self.__checkBoxClassName = jsonData["checkBoxClassName"]
			self.__fileTreeDialogXPath = jsonData["fileTreeDialogXPath"]
		#	self.__fileTreeConfirmBtnXPath = jsonData["fileTreeConfirmBtnXPath"]
			self.__fileTreeNodeClassName = jsonData["fileTreeNodeClassName"]
			self.__destnationPath = jsonData["destnationPath"]
			self.__fileTreeConfirmBtnClassName = jsonData["fileTreeConfirmBtnClassName"]
			self.__notFoundID = jsonData["notFoundID"]


		except:
			logger.exception("Error On Load Configuartion File.")
			print ("Error On Load Configuartion File , Please Check The Log File.")
			sys.exit(1)


	#Link Status : 
	#	0 : Untransfer
	#	1 : Transfered
	#	-1 : Link Error
	def __updateLinkStatus(self,PanLink,status):
		try:
			sql = "UPDATE Resources SET isTransfered=\'%d\' WHERE PanLink = \'%s\'"
			data = (status,PanLink)
			cmd = (sql % data)
			logger.debug(cmd)
			self.dbCursor.execute(cmd)
			self.dbConn.commit()
		except:
			logger.exception("Error On Update Link Status With Link : %s" % PanLink)
			print ("Error On Update Link Status With Link : %s , Please Check The Log File" % PanLink)
			return -1





def main():
	mf = MainFramework("moehui.db")
	mf.run()
	#dbTest = dbOperation("moehui.db")
	#dbTest.getDataFromDB()


if (__name__ == "__main__"):
	main()
