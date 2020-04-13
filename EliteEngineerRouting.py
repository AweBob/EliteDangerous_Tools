
#This is attempt #2 at Elite.CoriolisToEngineers
#All code done by:   CMDR AweBob    AweBob#3309
#I'm cool about sharing code, just ask permission on Discord.... I've got no clue about copyright, so if you wanna "borrow" it, go for it...

from EliteLogParser import getParsedLog

from glob import glob
import json
from os import path

#======================================================================================================================================

def howManyLogFiles () :
    location = path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               
    logFiles = glob(location)
    amountLogFiles = len(logFiles)
    return(amountLogFiles)

def getCmdrName (whichFile) :
    try :
        convLog = getParsedLog(whichFile)
    except Exception :
        return('Log File Glitched')
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('No CMDR Name Found')
    
def getCorrectFinalCmdrName (amountLogFiles) :
    allCmdrNames = []
    for numbers in range(0,amountLogFiles) :
        cmdrName = getCmdrName(numbers)
        if cmdrName not in allCmdrNames :
            charectorYorN = input('Is your CMDR name  ' + cmdrName + '  (y/n) - ')
            if charectorYorN=='n' or charectorYorN=='N' or charectorYorN=='No' or charectorYorN=='no' :
                allCmdrNames.append(cmdrName)
            else :
                return(cmdrName , True, numbers)
    return('No Other Cmdr Names Not Found' , False, 0)

#======================================================================================================================================

def refineEngineers (bigEngineers) :
    unlockedEngineerList = []
    for engineer in bigEngineers :
        if engineer['Progress']=='Unlocked' :
            unlockedEngineerList.append( engineer['Engineer'].upper() )
    return(unlockedEngineerList)

#======================================================================================================================================

def main() :
    print('\n' + '\n' + 'Program Initialized' + '\n' + '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    amountLogFiles = howManyLogFiles()
    cmdrName , isCmdrNameFound, logNumber = getCorrectFinalCmdrName(amountLogFiles)
    if isCmdrNameFound==False :
        input(cmdrName + " - Press Enter To Close")

    currentLogFile = getParsedLog(logNumber)
    for line in reversed(currentLogFile) :
        if line["event"]=='EngineerProgress' :
            bigEngineers = line["Engineers"]
            break
    unlockedEngineerList = refineEngineers(bigEngineers)


#======================================================================================================================================
def start () :
    try :
        main ()
    except Exception as error :
        input('ERROR: ' + '\n \n' + str(error) + '\n' + str(error.args) + '\n \n' + 'Report this issue to GitHub to help me resolve this!' + '\n' + 'Thank You, press Enter to close!' + '\n')                               

if __name__ == "__main__":
    start()             #Uncomment for normal operation
    #main()             #Uncomment for finding exact error messages in testing: obtain log and build before testing
