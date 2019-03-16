from os import *
import os
from glob import *
import glob
import json
import sys
import clipboard
import pyperclip

#All code done by:   CMDR AweBob    AweBob#3309
#I'm cool about sharing code, just ask permission on Discord.... I've got no clue about copyright, so if you wanna "borrow" it, go for it...

#================================================================================================================================================================================================
#========================================================================================================================================================================================================
#================================================================================================================================================================================================================

def getEngineerData () : #All Module names are in Coriolis Format, if there is a coriolis update core ints won't work, so lemme know if/when that happens...
    data = {
        'ELVIRA MARTUUK': [ ['frameShiftDrive', 5] , ['Shield Cell Bank' , 1] , ['Shield Generator' , 3] , ['thrusters' , 2] ],
        'THE DWELLER' : [ ['Beam Laser',3], ['Burst Laser',3],['powerDistributor',5],['Pulse Laser',4] ],
        'LIZ RYDER': [ ['Hull Reinforcement Package',1],['bulkheads',1],['Mine Launcher',3],['Missile Rack',5],['Seeker Missile Rack',5],['Torpedo Pylon',5] ],
        'TOD THE BLASTER MCQUINN': [ ['Cannon',2],['Fragment Cannon',3],['Multi-cannon',5],['Rail Gun',5] ],
        'FELICITY FARSEER': [ ['Detailed Surface Scanner',3],['frameShiftDrive',5],['Frame Shift Drive Interdictor',1],['powerPlant',1],['sensors',3],['Shield Booster',1],['thrusters',3] ],
        'MEL BRANDON': [ ['Beam Laser',4],['Burst Laser',2],['frameShiftDrive',2],['Frame Shift Drive Interdictor',1],['Pulse Laser',4],['Shield Booster',4],['Shield Cell Bank',3],['Shield Generator',3],['thrusters',5] ],
        'ETIENNE DORN': [ ['Detailed Surface Scanner',1],['Frame Shift Wake Scanner',1],['Kill Warrant Scanner',1],['lifeSupport',3],['Manifest Scanner',1],['Plasma Accelerator',1],['powerDistributor',2],['powerPlant',1],['Rail Gun',1],['sensors',1] ],                                                                                              
        'PETRA OLMANOVA': [ ['Auto Field-Maintenance Unit',1],['Chaff Launcher',2],['Electronic Countermeasure',1],['Heat Sink Launcher',3],['Hull Reinforcement Package',3],['bulkheads',4],['Mine Launcher',1],['Missile Rack',1],['Point Defence',2],['Seeker Missile Rack',1],['Torpedo Pylon',1] ],
        'JURI ISHMAAK' : [ ['Detailed Surface Scanner',5],['Frame Shift Wake Scanner',3],['Kill Warrant Scanner',3],['Manifest Scanner',3],['Mine Launcher',5],['Missile Rack',3],['Seeker Missile Rack',3],['sensors',5],['Torpedo Pylon',3] ],
        'ZACARIAH NEMO' : [ ['Fragment Cannon',5],['Multi-cannon',3],['Plasma Accelerator',2] ],
        'LEI CHEUNG' : [ ['Detailed Surface Scanner',5],['sensors',5],['Shield Booster',3],['Shield Generator',5] ],
        'HERA TANI' : [ ['Detailed Surface Scanner',5],['powerDistributor',3],['powerPlant',5],['sensors',3] ],
        'SELENE JEAN' : [ ['Hull Reinforcement Package',5],['bulkheads',5] ],
        'COLONEL BRIS DEKKER' : [ ['frameShiftDrive',3],['Frame Shift Drive Interdictor',4] ],
        'MARCO QWENT' : [ ['powerDistributor',3],['powerPlant',4] ],
        'RAM TAH' : [ ['Chaff Launcher',5],['Collector Limpet Controller',4],['Electronic Countermeasure',5],['Fuel Transfer Limpet Controller',4],['Hatch Breaker Limpet Controller',3],['Heat Sink Launcher',5],['Point Defence',5],['Prospector Limpet Controller',4] ],
        'BROO TARQUIN' : [ ['Beam Laser',5],['Burst Laser',5],['Pulse Laser',5] ],
        'DIDI VATERMANN' : [ ['Shield Booster',5],['Shield Generator',3] ],
        'THE SARGE' : [ ['Cannon',5],['Collector Limpet Controller',5],['Fuel Transfer Limpet Controller',5],['Hatch Breaker Limpet Controller',5],['Prospector Limpet Controller',5],['Rail Gun',3] ],
        'PROFESSOR PALIN' : [ ['frameShiftDrive',3],['thrusters',5] ],
        'LORI JAMESON' : [ ['Auto Field-Maintenance Unit',4],['Detailed Surface Scanner',5],['Frame Shift Wake Scanner',3],['Fuel Scoop',4],['Kill Warrant Scanner',3],['lifeSupport',4],['Manifest Scanner',3],['Refinery',4],['sensors',5],['Shield Cell Bank',3] ],
        'TIANA FORTUNE' : [ ['Collector Limpet Controller',5],['Detailed Surface Scanner',3],['Frame Shift Drive Interdictor',3],['Frame Shift Wake Scanner',5],['Fuel Transfer Limpet Controller',5],['Hatch Breaker Limpet Controller',5],['Kill Warrant Scanner',5],['Manifest Scanner',5],['Prospector Limpet Controller',5],['sensors',5] ],
        'BILL TURNER' : [ ['Auto Field-Maintenance Unit',3],['Detailed Surface Scanner',5],['Frame Shift Wake Scanner',3],['Fuel Scoop',3],['Kill Warrant Scanner',3],['lifeSupport',3],['Manifest Scanner',3],['Plasma Accelerator',5],['Refinery',3],['sensors',5] ],
        'MARSHA HICKS' : [ ['Cannon',2],['Collector Limpet Controller',4],['Fragment Cannon',2],['Fuel Scoop',3],['Fuel Transfer Limpet Controller',1],['Hatch Breaker Limpet Controller',1],['Multi-cannon',3],['Prospector Limpet Controller',3],['Refinery',2] ]
        }

    distanceFromSol = [
        'COLONEL BRIS DEKKER',
        'MARCO QWENT',
        'THE DWELLER',
        'LORI JAMESON',
        'THE SARGE',
        'SELENE JEAN',
        'LIZ RYDER',
        'BILL TURNER',
        'TOD THE BLASTER MCQUINN',
        'DIDI VATERMANN',
        'JURI ISHMAAK',
        'LEI CHEUNG',
        'FELICITY FARSEER',
        'TIANA FORTUNE', 
        'ZACARIAH NEMO',
        'RAM TAH',
        'BROO TARQUIN',
        'ELVIRA MARTUUK',
        'HERA TANI',
        'PROFESSOR PALIN',
        'MARSHA HICKS',
        'ETIENNE DORN',
        'MEL BRANDON',
        'PETRA OLMANOVA'
        ]   

    engineerToLocation = {
        'COLONEL BRIS DEKKER': 0.0 ,
        'MARCO QWENT': 8.6 ,
        'THE DWELLER': 33.8 ,
        'LORI JAMESON': 64.43 ,
        'THE SARGE': 68.2 ,
        'SELENE JEAN': 74.1 ,
        'LIZ RYDER': 80.8 , 
        'BILL TURNER': 82.5 ,
        'TOD THE BLASTER MCQUINN': 89.4 , 
        'DIDI VATERMANN': 111.0 , 
        'JURI ISHMAAK': 113.1 ,
        'LEI CHEUNG': 118.2 ,
        'FELICITY FARSEER': 131.4 ,
        'TIANA FORTUNE': 139.4 ,
        'ZACARIAH NEMO': 145.8 ,
        'RAM TAH': 163.5 ,
        'BROO TARQUIN': 173.7 ,
        'ELVIRA MARTUUK': 181.9 ,
        'HERA TANI': 264.0 ,
        'PROFESSOR PALIN': 383.3 ,
        'MARSHA HICKS': 21994.0 ,
        'ETIENNE DORN': 22001.1 ,
        'MEL BRANDON': 22013.5 ,
        'PETRA OLMANOVA': 22016.6
        }

    moduleNamingSystem_Core = [ 'bulkheads' , 'powerPlant' , 'thrusters' , 'frameShiftDrive' , 'lifeSupport' , 'powerDistributor' , 'sensors' ]
    moduleNamingSystem_Util = [ 'Chaff Launcher' , 'Electronic Countermeasure' , 'Frame Shift Wake Scanner' , 'Heat Sink Launcher' , 'Kill Warrant Scanner' , 'Manifest Scanner' , 'Point Defence' , 'Shield Booster' ]
    moduleNamingSystem_Opti = [ 'Auto Field-Maintenance Unit' , 'Collector Limpet Controller' , 'Detailed Surface Scanner' , 'Frame Shift Drive Interdictor' , 'Fuel Scoop' , 'Fuel Transfer Limpet Controller' , 'Hatch Breaker Limpet Controller' , 'Hull Reinforcement Package' , 'Prospector Limpet Controller' , 'Refinery' , 'Shield Cell Bank' , 'Shield Generator' ]
    moduleNamingSystem_Hard = [ 'Beam Laser' , 'Burst Laser' , 'Cannon' , 'Fragment Cannon' , 'Mine Launcher' , 'Missile Rack' , 'Multi-cannon' , 'Plasma Accelerator' , 'Pulse Laser' , 'Rail Gun' , 'Seeker Missile Rack' , 'Torpedo Pylon' ]
    coriolisNamingSystem = [ moduleNamingSystem_Core , moduleNamingSystem_Util , moduleNamingSystem_Opti , moduleNamingSystem_Hard ]

    engineersInaraLinksDict = {
        'COLONEL BRIS DEKKER': 'https://inara.cz/galaxy-engineer/14/',
        'MARCO QWENT': 'https://inara.cz/galaxy-engineer/7/' ,
        'THE DWELLER': 'https://inara.cz/galaxy-engineer/4/',
        'LORI JAMESON': 'https://inara.cz/galaxy-engineer/20/',
        'THE SARGE': 'https://inara.cz/galaxy-engineer/17/',
        'SELENE JEAN': 'https://inara.cz/galaxy-engineer/8/',
        'LIZ RYDER': 'https://inara.cz/galaxy-engineer/5/',
        'BILL TURNER': 'https://inara.cz/galaxy-engineer/19/',
        'TOD THE BLASTER MCQUINN': 'https://inara.cz/galaxy-engineer/6/',
        'DIDI VATERMANN': 'https://inara.cz/galaxy-engineer/11/',
        'JURI ISHMAAK': 'https://inara.cz/galaxy-engineer/13/',
        'LEI CHEUNG': 'https://inara.cz/galaxy-engineer/10/',
        'FELICITY FARSEER': 'https://inara.cz/galaxy-engineer/1/',
        'TIANA FORTUNE': 'https://inara.cz/galaxy-engineer/16/', 
        'ZACARIAH NEMO': 'https://inara.cz/galaxy-engineer/9/',
        'RAM TAH': 'https://inara.cz/galaxy-engineer/18/',
        'BROO TARQUIN': 'https://inara.cz/galaxy-engineer/15/',
        'ELVIRA MARTUUK': 'https://inara.cz/galaxy-engineer/2/',
        'HERA TANI': 'https://inara.cz/galaxy-engineer/12/',
        'PROFESSOR PALIN': 'https://inara.cz/galaxy-engineer/3/',
        'MARSHA HICKS': 'https://inara.cz/galaxy-engineer/21/',
        'ETIENNE DORN': 'https://inara.cz/galaxy-engineer/23/',
        'MEL BRANDON': 'https://inara.cz/galaxy-engineer/22/',
        'PETRA OLMANOVA': 'https://inara.cz/galaxy-engineer/24/'
        }

    engineerSystemNames = {
        'COLONEL BRIS DEKKER': 'SOL' ,
        'MARCO QWENT': 'SIRIUS' ,
        'THE DWELLER': 'WYRD' ,
        'LORI JAMESON': 'SHINRARTA DEZHRA' ,
        'THE SARGE': 'BETA-3 TUCANI' ,
        'SELENE JEAN': 'KUK' ,
        'LIZ RYDER': 'EURYBIA' , 
        'BILL TURNER': 'ALIOTH' ,
        'TOD THE BLASTER MCQUINN': 'WOLF 397' , 
        'DIDI VATERMANN': 'LEESTI' , 
        'JURI ISHMAAK': 'GIRYAK' ,
        'LEI CHEUNG': 'LAKSAK' ,
        'FELICITY FARSEER': 'DECIAT' ,
        'TIANA FORTUNE': 'ACHENAR' ,
        'ZACARIAH NEMO': 'YORU' ,
        'RAM TAH': 'MEENE' ,
        'BROO TARQUIN': 'MUANG' ,
        'ELVIRA MARTUUK': 'KHUN' ,
        'HERA TANI': 'KUWEMAKI' ,
        'PROFESSOR PALIN': 'MAIA' ,
        'MARSHA HICKS': 'TIR' ,
        'ETIENNE DORN': 'LOS' ,
        'MEL BRANDON': 'LUCHTAINE' ,
        'PETRA OLMANOVA': 'ASURA'
        }
    engineerWhichRequireRareMatsList = {
        'ELVIRA MARTUUK' : 'Soontill Relics',
        'FELICITY FARSEER' : 'Meta Alloys',
        'ZACARIAH NEMO' : 'Xihe Companions',
        'HERA TANI' : 'Kamitra Cigars',
        'SELENE JEAN' : 'Painite',
        'MARCO QWENT' : 'Modular Terminals',
        'BROO TARQUIN' : 'Fujin Tea',
        'DIDI VATERMANN' : 'Lavian Brandy',
        'LORI JAMESON' : 'Kongga Ale',
        'BILL TURNER' : 'Bromellite'
        }


    return(data , distanceFromSol, engineerToLocation, coriolisNamingSystem, engineersInaraLinksDict , engineerSystemNames , engineerWhichRequireRareMatsList )
    #MEL BRANDON and ETIENNE DORN and PETRA OLMANOVA and MARSHA HICKS = Colonia Engineers <--- Kinda irelevant, but I thought it was important

#================================================================================================================================================================================================
#========================================================================================================================================================================================================
#=============================================================================================================================================================================================

def grabLog ( whichNum ) :                                                                                   #input the logFil you want, 0 for latest, 1 for the second latest, and so on
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               #Won't work for linux users(their .log files are in a different path)
    logFiles = glob.glob(location)
    logFilesNums = []
    for file in logFiles :
        nums = ''
        for charector in file :
            if charector.isdigit()==True :
                nums = nums + charector
        logFilesNums.append(nums)
    orderedNums = sorted(logFilesNums, key=int, reverse=True)
    specificNum = orderedNums[whichNum]

    for files in logFiles :
        nums = ''
        for charector in files :
            if charector.isdigit()==True :
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
    log = log.replace("\\'The Blaster\\'", "The Blaster")
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


#================================================================================================================================================
#========================================================================================================================================================
#=============================================================================================================================================================================================

def howManyLogFiles () :
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               
    logFiles = glob.glob(location)
    amountLogFiles = 0
    for i in logFiles :
        amountLogFiles = amountLogFiles + 1
    return(amountLogFiles)

def getCmdrName (whichFile) :
    try :
        logTransformer(grabLog(whichFile))
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
    return('No Other Cmdr Names Not Found - Program Closing' , False, 0)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def refineEngineers (bigEngineers) :
    unlockedEngineerList = []
    unlockedEngineerListFinal = []
    for engineer in bigEngineers :
        if engineer['Progress']=='Unlocked' :
            unlockedEngineerList.append(engineer['Engineer'])
    for string in unlockedEngineerList :
        unlockedEngineerListFinal.append(string.upper())
    return(unlockedEngineerListFinal)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def getCoriolisJson () :
    print('Name your build in Coriolis and click save, then click the export button and copy that. That is your Coriolis output!')
    nothing = input('Get coriolis output on your clipboard (copy it) and press enter - ')
    stringCoriolis = clipboard.paste()      #Imports your clipboard

    if len(stringCoriolis) == 0 :
        stringCoriolis = pyperclip.paste()
        if len( stringCoriolis ) == 0 : 
            print('Either you didnt copy the export or my clipoard importer failed.')
            print('Trying again!')
            print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
            getCoriolisJson()

    try :
        jsonCoriolis = json.loads(stringCoriolis)
        print('Import Sucessful!')
        return(jsonCoriolis)
    except Exception :
        print('Error Converting Input: A. You didnt copy the build to clipboard B. My code doesnt work(unlikely, but possible)')
        print('Trying again!')
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        getCoriolisJson()

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def findModules (allCoriolis) :
    allModules = []
    #Core ints below            WHEN CORIOLISBUG IS FIXED ALL ONE FOR BULKHEADS
    #Coriolis may change their naming system causing some of this to not work....
    try :
        powerPlant = [ 'Power Plant' , allCoriolis['components']['standard']['powerPlant']['blueprint']['grade']  ]
        allModules.append(powerPlant)
    except (KeyError,IndexError,TypeError ) :
        pass

    try :
        thrusters = [ 'Thrusters' , allCoriolis['components']['standard']['thrusters']['blueprint']['grade']  ]
        allModules.append(thrusters)
    except (KeyError,IndexError,TypeError ) :
        pass

    try :
        Fsd = [ 'Frame Shift Drive' , allCoriolis['components']['standard']['frameShiftDrive']['blueprint']['grade']  ]
        allModules.append(Fsd)
    except (KeyError,IndexError,TypeError ) :
        pass
    
    try :
        lifeSup = [ 'Life Support' , allCoriolis['components']['standard']['lifeSupport']['blueprint']['grade']  ]
        allModules.append(lifeSup)
    except (KeyError,IndexError,TypeError ):
        pass

    try :
        powerDis = [ 'Power Distributor' , allCoriolis['components']['standard']['powerDistributor']['blueprint']['grade']  ]
        allModules.append(powerDis)
    except (KeyError,IndexError,TypeError ) :
        pass

    try :
        sensors = [ 'Sensors' , allCoriolis['components']['standard']['sensors']['blueprint']['grade']  ]
        allModules.append(sensors)
    except (KeyError,IndexError,TypeError ) :
        pass
    #hardpoints
    for num in range(17) :
        try :
            gun = [ allCoriolis['components']['hardpoints'][num]['group']  ,  allCoriolis['components']['hardpoints'][num]['blueprint']['grade']   ]
            allModules.append(gun)
        except (KeyError,IndexError,TypeError) :
            pass
    #Utility mounts
    for num in range(17) :
        try :
            util = [ allCoriolis['components']['utility'][num]['group']  ,  allCoriolis['components']['utility'][num]['blueprint']['grade']   ]
            allModules.append(util)
        except (KeyError,IndexError,TypeError) :
            pass
    #Opt ints
    for num in range(17) :
        try :
            inter = [ allCoriolis['components']['internal'][num]['group']  ,   allCoriolis['components']['internal'][num]['blueprint']['grade']   ]
            allModules.append(inter)
        except (KeyError,IndexError,TypeError ) :
            pass

    return(allModules)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def checkModuleData ( currentModuleData ) :
    isRunningLoop = True
    isCorrectInput = input('Is All the data correct?(y/n) - ')
    while isRunningLoop==True :
        if isCorrectInput=='n' or isCorrectInput=='N' or isCorrectInput=='no' or isCorrectInput=='No' :                                     #if user answers no
            whatModuleAdd = input('Enter module name (Coriolis naming system(Same as inara excpet Core Ints) - ')      #Coriolis naming system: inara engineer blueprints for all except core ints. 
            whatGradeAdd = input('Enter module engineering grade (number 1 through 5) - ')

            whatModuleAdd = checkInputModuleName ( whatModuleAdd , 'Enter module name again, list of valid names above - ' )
            whatGradeAdd = checkInputVarNum( whatGradeAdd , 'Enter module engineering grade (number 1 through 5) - ' )                      #Check if it's a valid number

            currentModuleData.append( [ str(whatModuleAdd) , int(whatGradeAdd)  ]  )
            isCorrectInput = input('Is All the data correct?(y/n) - ')
        else :
            isRunningLoop = False
            return ( currentModuleData )

def checkInputVarNum ( potentiallyNum , text ) :
    try :
        x = int(potentiallyNum)
        if x <= 5 and x >= 1 :
            return(x)
        else :
            plz = int('plz work')      #causes an error (hopefully)
    except :
        print('Your grade input is either not an Integer or the integer wasnt betwwen 1 and 5, try again: ')
        thingInput = input(text)
        checkInputVarNum( thingInput , text )

def checkInputModuleName (potentiallyVariable , text ) :
    engineerDict , engineerDistanceOrderList , engineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    correct = False
    for subList in coriolisNamingSystem :
        for item in subList :
            if item==potentiallyVariable :
                correct = True
    if correct==False :
        print(str(coriolisNamingSystem))
        thingInput = input('The Module Name you put in isnt valid, please try again based on the module list above - ')
        checkInputModuleName( thingInput , text )
    else :
        return(potentiallyVariable)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def orderEngineers ( engineers ) :
    engineerDict , engineerDistanceOrderList , engineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    engineersInOrder = []
    for engineer in engineerDistanceOrderList :
        if engineer in engineers :
            engineersInOrder.append( engineer )
    return(engineersInOrder)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def claculateWhichEngineers ( unlockedEngineersInOrder , bigModuleData ) :      
    fullEngineerDict , fullEngineerDistanceOrderList , fullEngineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    unlockedEngineersNecessaryBig = []
    modulesAlreadyFound = []
    for smallModuleData in bigModuleData :
        actualModule = smallModuleData[0]
        actualGrade = smallModuleData[1]
        hasModuleBeenFound = False
        for engineerKey in fullEngineerDistanceOrderList :
            engineersUsageList = fullEngineerDict[engineerKey]
            for smallEngineerData in engineersUsageList :
                engineerModule = smallEngineerData[0]
                engineerGrade = smallEngineerData[1]
                if engineerModule.upper()==actualModule.upper() :
                    if engineerGrade >= actualGrade :
                        if engineerKey in unlockedEngineersInOrder :                                   
                            unlockedEngineersNecessaryBig.append(engineerKey)
                            modulesAlreadyFound.append(smallModuleData)
                            hasModuleBeenFound = True
                            break
            if hasModuleBeenFound==True :
                break
    unlockedEngineersNecessaryRefined = removeDuplicatesInList( unlockedEngineersNecessaryBig )
    modulesNotAlreadyFound = findWhichModules( unlockedEngineersNecessaryRefined , bigModuleData )
    if len(modulesNotAlreadyFound)==0 :
        isComplete = True
        needToUnlockRefined = []
        return( unlockedEngineersNecessaryRefined , isComplete , needToUnlockRefined )
    else :
        isComplete = False
        needToUnlock = []
        needToUnlockVeryRefined = []
        for smallModuleData in modulesNotAlreadyFound :
            actualModule = smallModuleData[0]
            actualGrade = smallModuleData[1]
            hasModuleBeenFound = False
            for engineerKey in fullEngineerDistanceOrderList :
                engineersUsageList = fullEngineerDict[engineerKey]
                for smallEngineerData in engineersUsageList :
                    engineerModule = smallEngineerData[0]
                    engineerGrade = smallEngineerData[1]
                    if engineerModule.upper()==actualModule.upper() :
                        if engineerGrade >= actualGrade :                               
                            needToUnlock.append(engineerKey)
                            modulesAlreadyFound.append(smallModuleData)
                            hasModuleBeenFound = True
                            break
                if hasModuleBeenFound==True :
                    break
        needToUnlockRefined = removeDuplicatesInList( needToUnlock )
        for thing in needToUnlockRefined :
            if thing not in unlockedEngineersNecessaryRefined :
                needToUnlockVeryRefined.append( thing )
        return( unlockedEngineersNecessaryRefined , isComplete , needToUnlockVeryRefined )

def removeDuplicatesInList ( initialList ) :
    cleanList = []
    for value in initialList :
        if value not in cleanList :
            cleanList.append(value)
    return(cleanList)

def findWhichModules ( moduleAlreadyFound , allModules ) :   #Subtract these lists
    modulesNotAlreadyFound = []
    for module in allModules :
        if module not in moduleAlreadyFound :
            modulesNotAlreadyFound.append( module )
    return(modulesNotAlreadyFound)

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def printFinalData ( engineers , isComplete , needToUnlock , engineerSystemList , engineerInaraLinkList , callEicQuestionMark ) :
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('This line is all engineers you need to visit:  ' + str(engineers))
    print()
    print('This line is all the systems these engineers reside in(copy paste into ED Pathfinder):  ' + str(engineerSystemList) )
    print()
    if isComplete==False :
        print('In order to make this build you need more engineers, unlock the following:  ' + str(needToUnlock) )
        print()
        print('Here are Inara links to the above engineers so you can find unlock requirements:  ' + str( engineerInaraLinkList ) )
        print()
        if callEicQuestionMark==True :
            print('One or more of the engineers above require rare materiels. If you want to trade for the mats and save time, check out East India Company at: https://eicgaming.com/trading-post/#pricing ')
            print()

def getEngineerSystemNames ( engineerList ) :
    fullEngineerDict , fullEngineerDistanceOrderList , fullEngineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    systemList = []
    for engineer in engineerList :
        system = engineerSystemNames[engineer]
        systemList.append( system )
    return(systemList)

def getInaraLink ( engineerList ) :
    fullEngineerDict , fullEngineerDistanceOrderList , fullEngineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    linkList = []
    for engineer in engineerList :
        linkList.append( engineersInaraLinkDict[engineer] )
    return(linkList)

def doesEicNeedCalling ( engineerList ) :
    fullEngineerDict , fullEngineerDistanceOrderList , fullEngineerDistanceValueFromSolDict , coriolisNamingSystem , engineersInaraLinkDict, engineerSystemNames , engineerWhichRequireRareMatsList = getEngineerData()
    needCall = False
    for engineer in engineerList :
        if engineer in engineerWhichRequireRareMatsList :
            needCall = True
    return( needCall )

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#=========================MAIN CODE FLOW, CALLS FUNCTIONS, PRINTS INFO=============================================================================================================================================================================================================================================================================================================================================================================================
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def main () :
    print('\n' + '\n' + 'Program Initialized' + '\n' + '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    amountLogFiles = howManyLogFiles()
    cmdrName , isCmdrNameFound, logNumber = getCorrectFinalCmdrName(amountLogFiles)
    if isCmdrNameFound==False :
        print(cmdrName)
        sys.exit()
    logTransformer(grabLog(logNumber))
    currentLogFile = convLog
    for line in reversed(currentLogFile) :
        if line["event"]=='EngineerProgress' :
            bigEngineers = line["Engineers"]
            break
    unlockedEngineerList = refineEngineers(bigEngineers)
    CoriolisAll = getCoriolisJson ()                                #Sometimes this fails and doesn't get anything, not sure why, just run it again and it should work. 1 in 50 times it fails, why, Idk
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    allBuildModuleData = findModules(CoriolisAll)
    print( str(allBuildModuleData) )
    allBuildModuleData = checkModuleData ( allBuildModuleData )
    unlockedEngineerListInOrder = orderEngineers( unlockedEngineerList )    
    #print( str(allBuildModuleData) )                                                                                     
    engineers , isComplete , needToUnlock = claculateWhichEngineers ( unlockedEngineerListInOrder , allBuildModuleData  )   #Where the magic happens
    engineerSystemList = getEngineerSystemNames ( engineers )
    engineerInaraLinkList = getInaraLink ( needToUnlock )
    callEicQuestionMark = doesEicNeedCalling ( needToUnlock )
    printFinalData ( engineers , isComplete , needToUnlock , engineerSystemList , engineerInaraLinkList , callEicQuestionMark ) #Print out data
    nothing = input( '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=' + '\n' +'Script Complete!' + '\n' + 'Press enter to close window!')
    
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================
#=========================STARTUP PORTION==========================================================================================================================================================================================================================================================================================================================================================================================================================
#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================

def start () :
    try :
        main ()
    except Exception as error :
        nothing = input('ERROR: ' + '\n \n' + str(error) + '\n' + str(error.args) + '\n \n' + 'Report this issue to GitHub to help me resolve this!' + '\n' + 'Thank You, press Enter to close!' + '\n')                               

start()             #Uncomment for normal operation
#main()             #Uncomment for finding exact error messages in testing: obtain log and build before testing

#==================================================================================================================================================================================================================================================================================================================================================================================================================================================================


#claculateWhichEngineers function split into multiple parts to make it easier to fix
#Split data function into multiple functions
#Clipboard import is still unstable - not sure why