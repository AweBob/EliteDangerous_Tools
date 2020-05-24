
#Purpose is to sort out my log files to only get log files that are from my CMDR and not from my alt

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


from os import *
import os
from glob import *
import glob
import json
from shutil import copyfile

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def grabLog ( whichNum ) :                                                                                   #input the logFil you want, 0 for latest, 1 for the second latest, and so on
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               #Won't work for linux users
    logFiles = glob.glob(location)
    orderedLogs = sorted(logFiles, reverse=True)       #will error on date "2099-12-31", if your playing elite by then, just don't
    fileName = orderedLogs[whichNum]
    return( fileName )
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
            if charector.isdigit()==True :
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

def getCorrectFinalCmdrName (amountLogFiles) : #unused
    allCmdrNames = []
    for numbers in range(0,amountLogFiles) :
        cmdrName = getCmdrName(numbers)
        if cmdrName not in allCmdrNames :
            charectorYorN = input('Is your CMDR name  ' + cmdrName + '  (y/n) - ')
            if charectorYorN=='n' or charectorYorN=='N' or charectorYorN=='No' or charectorYorN=='no' :
                allCmdrNames.append(cmdrName)
            else :
                return(cmdrName , True, numbers)
    return('No Other Cmdr Names Not Found - Program Closing' , False, 0)

def howManyLogFiles () :
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               
    logFiles = glob.glob(location)
    amountLogFiles = 0
    for i in logFiles :
        amountLogFiles = amountLogFiles + 1
    return(amountLogFiles)

def getCmdrName (whichFile) : #unused
    try :
        logTransformer(grabLog(whichFile))
    except Exception :
        return('Log File Glitched')
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('None')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
def doIt (cmdrName , targetFolder) :
    listOfPathsToSelectedFiles = []
    for logNum in range( 0 , howManyLogFiles() ) : 
        try :
            logFilePath = grabLog(logNum)
            logTransformer( logFilePath )
            for line in convLog :
                if line['event']=='Commander' :
                    if (cmdrName == line['Name']) :
                        listOfPathsToSelectedFiles.append( logFilePath )
                    break #if the line of CMDR
        except :
            pass
    amountOfSelected = len(listOfPathsToSelectedFiles)

    for filePath in listOfPathsToSelectedFiles :
        pos = listOfPathsToSelectedFiles.index( filePath ) 
        head, tail = os.path.split(filePath)
        distinationPath = targetFolder + tail
        copyfile( filePath , distinationPath ) #source , destination

    return(amountOfSelected , howManyLogFiles() )

def main() :
    print("This code will grab all the log files from a CMDR and copy paste it into a directory")
    print("Prupose of this is for edsm!")
    folder = input("Enter the target folder or location of these copied log files - ")
    print("Process running, please wait about " + str(howManyLogFiles() / 10) + "seconds." ) #speed on my drive, speed may vary, but this is a good estimate
    cmdrName = input("Enter the CMDR name of log files you want - ")
    amount , total = doIt ( cmdrName , folder)
    print("Operation Sucessful, total of " + str(amount) + " files copied out of " + str(total) + " files total.")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

