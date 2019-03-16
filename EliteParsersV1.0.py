
from os import *
import os
from glob import *
import glob
import json

#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================

def grabLog ( whichNum ) :                                                                                   #input the logFil you want, 0 for latest, 1 for the second latest, and so on
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               #Won't work for linux users
    logFiles = glob.glob(location)
    logFilesNums = []
    for file in logFiles :
        nums = ''
        for charector in file :
            if charector=='0' or charector=='1' or charector=='2' or charector=='3' or charector=='4' or charector=='5' or charector=='6' or charector=='7' or charector=='8' or charector=='9' :
                nums = nums + charector
        logFilesNums.append(nums)
    orderedNums = sorted(logFilesNums, key=int, reverse=True)
    specificNum = orderedNums[whichNum]

    for files in logFiles :
        nums = ''
        for charector in files :
            if charector=='0' or charector=='1' or charector=='2' or charector=='3' or charector=='4' or charector=='5' or charector=='6' or charector=='7' or charector=='8' or charector=='9' :
                nums = nums + charector
        if nums==specificNum :
            latestFile = files
    return(latestFile)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logTransformer ( logFile ) :
    openLog = open(logFile,O_RDONLY)
    importedLog = read(openLog,9999999)
    close(openLog)

    log = str(importedLog)
    log = log[1:]
    log = log[1:]
    log = log.replace('\\n',', ')
    log = log.replace("\\'The Blaster\\'", " The Blaster")
    log = log[:-3]
    log = "[" + log + "]"
    return(logConverter( log ))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logConverter ( cleanLogFile ) :
    try:
        global convLog
        convLog = json.loads(cleanLogFile)
    except ValueError as error:
        error = str(error)
        nums = ''
        for charector in error :
            if charector=='0' or charector=='1' or charector=='2' or charector=='3' or charector=='4' or charector=='5' or charector=='6' or charector=='7' or charector=='8' or charector=='9' :
                nums = nums + charector
        errorChar = nums[1:]
        lengthError = int(-1 * (len(errorChar)/2))
        errorChar = errorChar[:lengthError]
        errorChar = int(errorChar)
        logCleaner( cleanLogFile , errorChar )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logCleaner ( dirtyLogFile , errorPos ) :
    beginningPos = int(errorPos) - 1
    endingPos = int(errorPos) + 0
    cleanLogFile = dirtyLogFile[:beginningPos] + dirtyLogFile[endingPos:]
    logConverter( cleanLogFile )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#logTransformer(grabLog(0))     #updates convLog variable with latest log file
#print(convLog)                 #prints out the entire latest log file
#print(convLog[-1])             #Prints latest line
#print(convLog[0]['event'])     #prints first line event

#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================

#from os import *
#import os
#from glob import *
#import glob
import xml.etree.ElementTree as ET

def grabBind () :
    location = os.path.expanduser('~\AppData\Local\\frontier developments\elite dangerous\options\\bindings\*.binds') #File path different for linux
    bindFilePath = glob.glob(location)
    if len(bindFilePath) == 0 :
        nothing = input('No binds found!')

    bindFileName = str(bindFilePath[0])
    bindText = openBind( bindFileName )   #tree = 

    root = ET.fromstring( bindText )  #root = 
    bindsDictionary = { }
    for child in root :
        for grandChild in child :
            try :
                if grandChild.attrib['Key'] != '' :
                    bindsDictionary[child.tag] = [ grandChild.attrib['Key'] , grandChild.tag ]
            except :
                pass
    return( bindsDictionary )

def openBind ( bindFileName ) :
    openText = open(bindFileName , O_RDONLY)
    importedBindText = read(openText , 9999999)
    close(openText)
    return( importedBindText )

#binds = grabBind ()                          #Grabes dictionary
#print(binds['YawAxisRaw'])                   #prints list of info for bind called that
#print(binds['CommanderCreator_Undo'][0])     #prints the bind key for that bind
#print(binds['Joy_XAxis'][1])                 #prints the bind type for that bind

#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================
#=======================================================================================================================================================================================================================

#USAGE GUIDE:
#Each parser, seperated by three lines of equals signs
#At the start of each it has things you need to import, if you copy the entire thing, leave the commented and uncommented ones as is; if you only copy one parser, uncomment all the imports at the start of it
#Copy and paste the functions as in, if you want to change the output method for them
#At the bottom there are a few examples of how to use them in other programs, they are just examples, use the output any way necessary for your script

