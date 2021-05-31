
#===========================================================================================================================================================================================================

#Python 3.8.6 (Although doesn't use any of the latest syntax so should work in most versions of Python 3)
#By: AweBob#6221 aka CMDR AweBob
#Only tested on windows (I am almost positive log files are handled differently on different systems)

#===========================================================================================================================================================================================================

from os.path import expanduser as expandUser
from glob import glob as getFilesInDirectory
from json import loads as jsonLoads
import logging

#===========================================================================================================================================================================================================

def getAllLogNamesOrdered () :                                                               #note: order is latest to oldest
    logDirectory = expandUser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')   #expand to include proper user
    logFileNames = getFilesInDirectory(logDirectory)                                         #grab all the files in the exact directory that end in "".log"
    orderedLogFileNames = sorted(logFileNames, reverse=True)                                 #will error on date "2099-12-31", if your playing elite by then, just don't :)
    return( orderedLogFileNames )

def getLogName ( index ) : 
    logFileName = getAllLogNamesOrdered()[int(index)]
    return( logFileName )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getLogJson ( logName=0 ) :
    if type(logName) == type(str()) :
        openFile = open(str(logName), "r")     
    elif type(logName) == type(int()) :
        openFile = open(str(getLogName(logName)), "r")  
    else :
        logging.critical(f"logName excepting str or int, not {type(logName)}")
        raise ValueError("logName must be int or str") 
    jsonLog = []
    for lineNum, rawLine in enumerate(openFile) :
        try :
            jsonLog.append(jsonLoads(str(rawLine)))
        except ValueError : #Line failed to be converted to json
            logging.warning(f"failed to convert line number {lineNum} within {logName} which contained \"{str(rawLine)}\"")
            #print(f"failed to convert line number {lineNum} within {logName} which contained \"{str(rawLine)}\"")               #Here for easier testing
    openFile.close()
    return(jsonLog)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def testCases () :
    #print( str(getLogJson()) )                                         #Print latest log file
    #print( str(getLogJson()[-1]) )                                     #Print latest line of latest log file
    #print( str(getLogJson()[-1]["event"]) )                            #Print latest event name of latest line of latest log file
    #print( str(getLogJson(logName=1)[1]["event"]) )                    #Print event of second earliest line of second to latest log file
    #print( str(getLogJson(logName=getLogName(1))[0]["timestamp"]) )    #Print ealiest/first timestamp of earliest line of the second to latest log file
    #print(getLogName(0))                                               #Print exact directory of latest log file
    return()

#===========================================================================================================================================================================================================

if __name__ == "__main__" :
    testCases()

#===========================================================================================================================================================================================================
