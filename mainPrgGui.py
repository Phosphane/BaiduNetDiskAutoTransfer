#coding : utf-8
#Author : VinylChloride
#Version : 0.0.1 Alpha

import sys
import os
import json
import time
import threading

from lang import Lang

#from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QAction,QPushButton,QGridLayout,QLabel,QTextEdit,QToolButton,QStyle,QMessageBox,QGridLayout,QComboBox,QCheckBox,QFileDialog
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import pyqtSlot,QCoreApplication


	#Main Framework Class Vars : 
	#	self.linkCount
	#	self.errLinkCount
	#	self.errLinkList
	#	self.bannedLinkCount
	#	self.bannedLinkList
	#	self.doneLinkCount

	#Main Framework Class run function requires a callback function :
	#	callback(self,panLink,status,needUpdateGui = True)



class MainConfigUpdater(object):
	def __init__(self,configFile = "config.json"):
		if ((not os.path.exists(configFile)) or (not os.path.isfile(configFile))):
			print ("Console Configuration File Not Found.")
			sys.exit(0)

		self.__configFile = configFile
		with open(self.__configFile,"r+") as f:
			self.__configData = json.load(f)
			f.close()

	def save(self):
		with open(self.__configFile,"w+") as f:
			f.writelines(json.dumps(self.__configData,sort_keys = True,indent = 4,separators = (',',':')))
			f.close()
	#	return True

	def update(self,key,value):
		if (self.__configData.__contains__(key)):
			self.__configData[key] = value

	def get(self,key):
		if (self.__configData.__contains__(key)):
			return self.__configData[key]
		else:
			return None






class AutoTransferGUI(QWidget):
	def __init__(self):
		super(AutoTransferGUI,self).__init__()

		self.__consoleConfig = MainConfigUpdater("config.json")


		self.__tableName = ""
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

		self.__langFloder = "." + os.sep + "lang" + os.sep
		self.__langList = []
		self.__config = {}
		self.__curLang = "en"

		self.__getLangList()
		self.__loadConfig()

		self.__isTransferStarted = False
		self.__transferFramework = None
		self.__transferDBFile = ""
		self.__runMode = 0

		self.__lang = Lang(self.__curLang)
		if (self.__lang.reload(self.__curLang) == -1):
			print ("Language Pack Error.")
			sys.exit(1)
		

		self.__title = self.__lang.get("title")
		self.__left = 50
		self.__top = 50
		self.__width = 500
		self.__heigth = 600
		self.__widgetList = []

		self.__initUI()

		self.show()

	def __initUI(self):
		self.setWindowTitle(self.__title)
		self.setGeometry(self.__left,self.__top,self.__width,self.__heigth)
	#	self.setWindowIcon(QIcon(IconFile))

		self.__createLabel()
		self.__createTextBox()
		self.__createButton()
		self.__createComboBox()
		self.__createCheckBox()
		self.__createStatusTextBox()
		self.__createStatusLabel()

		self.__gridLayout = QGridLayout()
		self.__gridLayout.setSpacing(8)

		
		self.__gridLayout.addWidget(self.__destLabel,0,0,1,2)
		self.__gridLayout.addWidget(self.__destTextBox,0,2,1,2)
		self.__gridLayout.addWidget(self.__codeTBLabel,1,0,1,2)
		self.__gridLayout.addWidget(self.__codeTBTextBox,1,2,1,2)
		self.__gridLayout.addWidget(self.__codeBtnXPathLabel,2,0,1,2)
		self.__gridLayout.addWidget(self.__codeBtnXPathTextBox,2,2,1,2)
		self.__gridLayout.addWidget(self.__transferBtnSelectorLabel,3,0,1,2)
		self.__gridLayout.addWidget(self.__transferBtnSelectorTextBox,3,2,1,2)
		self.__gridLayout.addWidget(self.__checkBoxClassLabel,4,0,1,2)
		self.__gridLayout.addWidget(self.__checkBoxClassTextBox,4,2,1,2)
		self.__gridLayout.addWidget(self.__fileTreeNodeClassLabel,5,0,1,2)
		self.__gridLayout.addWidget(self.__fileTreeNodeClassTextBox,5,2,1,2)
		self.__gridLayout.addWidget(self.__fileTreeDialogXPathLabel,6,0,1,2)
		self.__gridLayout.addWidget(self.__fileTreeDialogXPathTextBox,6,2,1,2)
		self.__gridLayout.addWidget(self.__fileTreeCfmClassLabel,7,0,1,2)
		self.__gridLayout.addWidget(self.__fileTreeCfmClassTextBox,7,2,1,2)
		self.__gridLayout.addWidget(self.__notFoundLabel,8,0,1,2)
		self.__gridLayout.addWidget(self.__notFoundTextBox,8,2,1,2)
		self.__gridLayout.addWidget(self.__runModeCheckBox,9,0,1,2)
		self.__gridLayout.addWidget(self.__langLabel,9,2,1,1)
		self.__gridLayout.addWidget(self.__langSelectBox,9,3,1,1)
		self.__gridLayout.addWidget(self.__tableNameLabel,10,0,1,2)
		self.__gridLayout.addWidget(self.__tableNameTextBox,10,2,1,2)
		self.__gridLayout.addWidget(self.__saveButton,11,0,2,2)
		self.__gridLayout.addWidget(self.__startButton,11,2,2,2)
		self.__gridLayout.addWidget(self.__selectDBFileButton,13,0,1,1)
		self.__gridLayout.addWidget(self.__dbLocationTextBox,13,1,1,3)
		self.__gridLayout.addWidget(self.__statusLabel,14,0,1,2)
		self.__gridLayout.addWidget(self.__errLabel,14,2,1,2)
		self.__gridLayout.addWidget(self.__statusTextBox,15,0,3,4)

		for widget in self.__widgetList:
			widget.setMaximumHeight(30)

		self.setLayout(self.__gridLayout)

	def __createStatusLabel(self):
		self.__statusLabel = QLabel()
		self.__statusLabel.setText(self.__lang.get("doneLink"))
		self.__errLabel = QLabel()
		self.__errLabel.setText(self.__lang.get("errorLink"))
		self.__widgetList.append(self.__statusLabel)
		self.__widgetList.append(self.__errLabel)


	def __createTextBox(self):
		self.__tableNameTextBox = QTextEdit()
		self.__tableNameTextBox.setText(self.__tableName)
		self.__widgetList.append(self.__tableNameTextBox)
		self.__destTextBox = QTextEdit()
		self.__destTextBox.setText(self.__destnationPath)
		self.__widgetList.append(self.__destTextBox)
		self.__codeTBTextBox = QTextEdit()
		self.__codeTBTextBox.setText(self.__codeTextBoxXPath)
		self.__widgetList.append(self.__codeTBTextBox)
		self.__codeBtnXPathTextBox = QTextEdit()
		self.__codeBtnXPathTextBox.setText(self.__codeEnterBtnXPath)
		self.__widgetList.append(self.__codeBtnXPathTextBox)
		self.__transferBtnSelectorTextBox = QTextEdit()
		self.__transferBtnSelectorTextBox.setText(self.__transferBtnSelector)
		self.__widgetList.append(self.__transferBtnSelectorTextBox)
		self.__checkBoxClassTextBox = QTextEdit()
		self.__checkBoxClassTextBox.setText(self.__checkBoxClassName)
		self.__widgetList.append(self.__checkBoxClassTextBox)
		self.__fileTreeNodeClassTextBox = QTextEdit()
		self.__fileTreeNodeClassTextBox.setText(self.__fileTreeNodeClassName)
		self.__widgetList.append(self.__fileTreeNodeClassTextBox)
		self.__fileTreeDialogXPathTextBox = QTextEdit()
		self.__fileTreeDialogXPathTextBox.setText(self.__fileTreeDialogXPath)
		self.__widgetList.append(self.__fileTreeDialogXPathTextBox)
		self.__fileTreeCfmClassTextBox = QTextEdit()
		self.__fileTreeCfmClassTextBox.setText(self.__fileTreeConfirmClassName)
		self.__widgetList.append(self.__fileTreeCfmClassTextBox)
		self.__notFoundTextBox = QTextEdit()
		self.__notFoundTextBox.setText(self.__notFoundID)
		self.__widgetList.append(self.__notFoundTextBox)
		self.__dbLocationTextBox = QTextEdit()
		self.__dbLocationTextBox.setText("")
		self.__widgetList.append(self.__dbLocationTextBox)

#	def __guiCallback(self,)

	def closeEvent(self,event):
		sys.exit(0)

	def __createStatusTextBox(self):
		self.__statusTextBox = QTextEdit()
		self.__statusTextBox.setText(self.__lang.get("defaultStatusTextBox"))
		#self.__statusLabel.setText("Status Label Test")

	def __outputToTextBox(self,newInfo):
		newInfo += '\n'
		oriTextBoxData = self.__statusTextBox.toPlainText()
		oriTextBoxData += newInfo
		self.__statusTextBox.setText(oriTextBoxData)

	def __createButton(self):
		self.__saveButton = QPushButton(self.__lang.get("saveChangeButton"),self)
		self.__saveButton.clicked.connect(lambda:self.__saveConfig())
		self.__startButton = QPushButton(self.__lang.get("startTransferButton"),self)
		self.__startButton.clicked.connect(lambda:self.__startTransfer())
		self.__selectDBFileButton = QPushButton(self.__lang.get("selectDBFileButton"))
		self.__selectDBFileButton.clicked.connect(lambda:self.__selectDB())

		self.__widgetList.append(self.__saveButton)
		self.__widgetList.append(self.__startButton)
		self.__widgetList.append(self.__selectDBFileButton)

	def __selectDB(self):
		self.__transferDBFile = QFileDialog.getOpenFileName(self,self.__lang.get("selectDBFileDialog"),os.getcwd(),"SQLite3 Database (*.db)")[0]
		self.__dbLocationTextBox.setText(self.__transferDBFile)

	def __createLabel(self):
		self.__tableNameLabel = QLabel()
		self.__tableNameLabel.setText(self.__lang.get("tableNameLabel"))
		self.__widgetList.append(self.__tableNameLabel)
		self.__destLabel = QLabel()
		self.__destLabel.setText(self.__lang.get("destPathLabel"))
		self.__widgetList.append(self.__destLabel)
		self.__codeTBLabel = QLabel()
		self.__codeTBLabel.setText(self.__lang.get("codeTextBoxXPathLabel"))
		self.__widgetList.append(self.__codeTBLabel)
		self.__codeBtnXPathLabel = QLabel()
		self.__codeBtnXPathLabel.setText(self.__lang.get("codeBtnXPathLabel"))
		self.__widgetList.append(self.__codeBtnXPathLabel)
		self.__transferBtnSelectorLabel = QLabel()
		self.__transferBtnSelectorLabel.setText(self.__lang.get("transferBtnSelectorLabel"))
		self.__widgetList.append(self.__transferBtnSelectorLabel)
		self.__checkBoxClassLabel = QLabel()
		self.__checkBoxClassLabel.setText(self.__lang.get("checkBoxClassLabel"))
		self.__widgetList.append(self.__checkBoxClassLabel)
		self.__fileTreeNodeClassLabel = QLabel()
		self.__fileTreeNodeClassLabel.setText(self.__lang.get("fileTreeNodeClassLabel"))
		self.__widgetList.append(self.__fileTreeNodeClassLabel)
		self.__fileTreeDialogXPathLabel = QLabel()
		self.__fileTreeDialogXPathLabel.setText(self.__lang.get("fileTreeDiaXPathLabel"))
		self.__widgetList.append(self.__fileTreeDialogXPathLabel)
		self.__fileTreeCfmClassLabel = QLabel()
		self.__fileTreeCfmClassLabel.setText(self.__lang.get("fileTreeCfmClassLabel"))
		self.__widgetList.append(self.__fileTreeCfmClassLabel)
		self.__notFoundLabel = QLabel()
		self.__notFoundLabel.setText(self.__lang.get("notFoundLabel"))
		self.__widgetList.append(self.__notFoundLabel)


	def __createCheckBox(self):
		self.__runModeCheckBox = QCheckBox(self.__lang.get("runModeCheckBox"),self)

		self.__widgetList.append(self.__runModeCheckBox)


	def __createComboBox(self):
		self.__langLabel = QLabel()
		self.__langLabel.setText(self.__lang.get("langLabel"))
		self.__langSelectBox = QComboBox()
		for langItem in self.__langList:
			self.__langSelectBox.addItem(langItem)
		self.__langSelectBox.setCurrentIndex(self.__langSelectBox.findText(self.__curLang))

		self.__widgetList.append(self.__langLabel)
		self.__widgetList.append(self.__langSelectBox)


	def __startTransfer(self):

		if (self.__isTransferStarted):
			pass
			#Error On Transfer Is Started
			return
		from autoTransfer import MainFramework
		if (self.__runModeCheckBox.isChecked()):
			self.__runMode = -1
		else:
			self.__runMode = 0
		self.__isTransferStarted = True
		self.__transferFramework = MainFramework(self.__transferDBFile,self.__runMode)
		self.__transferFramework.run(self.__guiCallback)
		self.__isTransferStarted = False
		del self.__transferFramework
		del MainFramework

	#	self.__transferThread = threading.Thread(target = self.__transferThreadFunc,args=())
	#	self.__transferThread.daemon = True
	#	self.__transferThread.start()
		
	def __guiCallback(self,panLink,retStatus):
		if (retStatus == 1):
			self.__outputToTextBox("Transfer : " + panLink + " Successed.")
		elif(retStatus == -1):
			self.__outputToTextBox("Transfer : " + panLink + " Failed.")
		elif(retStatus == -2):
			self.__outputToTextBox("Link : " + panLink + " Has Been Banned.")

		self.__statusLabel.setText(self.__lang.get("doneLink") + str(self.__transferFramework.doneLinkCount))

		self.__errLabel.setText(self.__lang.get("errorLink") + str(self.__transferFramework.errLinkCount))

	def __transferThreadFunc(self):
		self.__transferFramework = MainFramework(self.__transferDBFile,self.__runMode)
		self.__transferFramework.run(self.__guiCallback)
		self.__isTransferStarted = False

	def __saveConfig(self):
		self.__config["lang"] = self.__langSelectBox.currentText()


		with open("guiConfig.json","w+") as configFile:
			configFile.writelines(json.dumps(self.__config,sort_keys = True,indent = 4,separators = (',',':')))
			configFile.close()


		self.__consoleConfig.update("dbTableName",self.__tableNameTextBox.toPlainText())
		self.__consoleConfig.update("destnationPath",self.__destTextBox.toPlainText())
		self.__consoleConfig.update("codeTextBoxXPath",self.__codeTBTextBox.toPlainText())
		self.__consoleConfig.update("codeEnterBtnXPath",self.__codeBtnXPathTextBox.toPlainText())
		self.__consoleConfig.update("transferBtnSelector",self.__transferBtnSelectorTextBox.toPlainText())
		self.__consoleConfig.update("checkBoxClassName",self.__checkBoxClassTextBox.toPlainText())
		self.__consoleConfig.update("fileTreeNodeClassName",self.__fileTreeNodeClassTextBox.toPlainText())
		self.__consoleConfig.update("fileTreeDialogXPath",self.__fileTreeDialogXPathTextBox.toPlainText())
		self.__consoleConfig.update("fileTreeConfirmBtnClassName",self.__fileTreeCfmClassTextBox.toPlainText())
		self.__consoleConfig.update("notFoundID",self.__notFoundTextBox.toPlainText())
		self.__consoleConfig.save()


		self.__outputToTextBox("Configuration Saved.")


	def __loadConfig(self):
		if (not os.path.exists("guiConfig.json")):
			print ("Can not find configuration file.")
			sys.exit(1)
		with open("guiConfig.json","r+") as configFile:
			self.__config = json.load(configFile)
			configFile.close()

		self.__curLang = self.__config["lang"]

		self.__tableName = self.__consoleConfig.get("dbTableName")
		self.__destnationPath = self.__consoleConfig.get("destnationPath")
		self.__codeTextBoxXPath = self.__consoleConfig.get("codeTextBoxXPath")
		self.__codeEnterBtnXPath = self.__consoleConfig.get("codeEnterBtnXPath")
		self.__transferBtnSelector = self.__consoleConfig.get("transferBtnSelector")
		self.__checkBoxClassName = self.__consoleConfig.get("checkBoxClassName")
		self.__fileTreeNodeClassName = self.__consoleConfig.get("fileTreeNodeClassName")
		self.__fileTreeDialogXPath = self.__consoleConfig.get("fileTreeDialogXPath")
		self.__fileTreeConfirmClassName = self.__consoleConfig.get("fileTreeConfirmBtnClassName")
		self.__notFoundID = self.__consoleConfig.get("notFoundID")


	#	self.__outputToTextBox("Configuration Loaded.")

	def __getLangList(self):
		if (not os.path.exists(self.__langFloder)):
			print ("Language Pack Not Found.")
			sys.exit(1)
		if (os.path.isfile(self.__langFloder)):
			print ("Language Pack Not Found.")
			sys.exit(1)
		for root,dirs,files in os.walk(self.__langFloder):
			for file in files:
				self.__langList.append(os.path.splitext(file)[0])



def main():
	app = QApplication(sys.argv)
	autoTransferGui = AutoTransferGUI()
	sys.exit(app.exec_())

if (__name__ == "__main__"):
	main()
