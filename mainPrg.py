
import sys
import getopt
from autoTransfer import MainFramework

def main(argv):
	helpMsg = """Usage : 
	python <file.py>
Arguments:
	-h,--help : Show This Message
	-e,--errorCheck : Only Recheck The Error Link (Status Code == -1)
	-d,--databse : Use Custom Database
"""
	runMode = 0
	dbFile = "moehui.db"
	try:
		opts,args = getopt.getopt(argv,"hed:",["help","errorCheck","database="])
	except getopt.GetoptError:
		print (helpMsg)
		sys.exit(2)
	for opt,arg in opts:
		if (opt == "-h" or opt == "--help"):
			print (helpMsg)
			sys.exit(0)
		elif (opt == "-e" or opt == "--errorCheck"):
			runMode = -1
		elif(opt == "-d" or opt == "--database"):
			dbFile = arg

	mf = MainFramework(dbFile,runMode)
	mf.run()
	#dbTest = dbOperation("moehui.db")
	#dbTest.getDataFromDB()


if (__name__ == "__main__"):
	main(sys.argv[1:])