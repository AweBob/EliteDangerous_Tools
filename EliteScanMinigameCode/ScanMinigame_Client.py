import asyncio
import time
from os import * #this might be unused
import os
from glob import *
import glob
import json
import win32com.client as wincl
import collections
import ast

#This is client code for advanced vessel scanner and station data uploader, when distributing change the below capslocked variables to the actual thing so users don't have to enter it manually
#===========================================================================================================================================================================================

tts = wincl.Dispatch("SAPI.SpVoice") #Will crash here for nonwindows users - if your playing on mac, im sorry, but get a real computer :p <--- just a joke
compare = lambda x, y: collections.Counter(x) == collections.Counter(y) #setup comparing function - should prolly do this elsewhere, but it looks really nice here as it's a 1 liners

print('Imported libraries Sucessfully')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 19.374.922.82) - ') #must be a string
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
READING_SETTING = input('Do you want to be read to everytime you die or get a kill? (y/n) - ')
RUNNING_MODE = input('Safe startup or normal startup? (s/n) - ') #Safe is really only for testing for errors, but I'll leave the option in there for now!

#===========================================================================================================================================================================================

def pingServer( ToSend ) : #ToSend should be a list - MUST be a list
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)
        startTimer = time.time()
        writer.write( json.dumps( ToSend ).encode() )
        data = await reader.read(1000) 
        recievedStuff = ast.literal_eval( str( data.decode() ) )
        endTimer = time.time()
        writer.close()
        ping = str( int(( endTimer - startTimer ) * 1000) ) 
        return( recievedStuff , ping )

    loop = asyncio.get_event_loop()
    recievedStuff , ping = loop.run_until_complete(tcp_echo_client(ToSend, loop))
    return( recievedStuff , ping )

#===========================================================================================================================================================================================

def mainCode () :
    loopRotations = 0 #loop rotations for main while loop.
    beforeEventRotations = 0 #number of times this thing has looped before the event has started
    afterEventRotations = 0 #times looped after event has ended
    duringEventRotations = 0 #times looped during event
    duringEventOverDueToTime = 0 #times event has been over due to score
    objectiveName , eventLength , eventStartTime , numberScansToWin = testConnection() #all time is unix time because it's easy - no timezoes, simple mathematic computable formula
    dc_currentLogFileName = detectChange( grabLog(0) ) 
    eventOverride = False #Event is good to continue

    while True :
        startClock = time.time()
        readingInfoClass = readInformation()
        if eventOverride == True : #event is over due to score
            if duringEventOverDueToTime >= 600 : #it's been 10 minutes
                nothing = input('Event has been over for ten minutes, press enter to close - ')
                raise SystemExit
            duringEventOverDueToTime = duringEventOverDueToTime + 1
        elif time.time() >= int(eventStartTime) and time.time() <= ( int(eventLength) + int(eventStartTime) ) : #if event is live

            c_trueFalseChangeLogFile , d_changeLogFile = dc_currentLogFileName.check( grabLog(0) )
            logTransformer(grabLog(0))
            if loopRotations == 0 or c_trueFalseChangeLogFile == True :  #code had just started or elite has just started - then - reset detect change classes
                deathsList , killsList = getKillsDeaths()
                possesion , uploaded = doYaHaveScanData( objectiveName )
                dc_posessingScan = detectChange(False)  #bool  #Does CMDR have scna data aboard, True or false
                dc_uploadedScan = detectChange(uploaded) #int
                dc_killLog = detectChange(killsList)    #list     #records everyone you've killed 
                dc_deathLog = detectChange(deathsList) #list

            deathsList , killsList = getKillsDeaths()
            possesion , uploaded = doYaHaveScanData( objectiveName )  #Needs testing

            c_possesingScan , possesion = dc_posessingScan.check( possesion ) #t/f #say this, but don't send it to server, it doesn't care
            c_uploadedScan , uploaded = dc_uploadedScan.check( uploaded  )    #int
            C_killLog , killsList = dc_killLog.check( killsList )             #list
            c_deathLog , deathsList = dc_deathLog.check( deathsList )         #list

            listToSend = [ SERVER_PASSWORD ]

            listToSend = addToSendingList( listToSend , c_uploadedScan , c_deathLog , C_killLog , uploaded , deathsList , killsList )
            if len( listToSend ) != 0 : #checks that list has any content - going to make it so this won't crash the server here soon, thx Phelbore!
                try :
                    recievedList , ping = pingServer( listToSend ) #ping in milliseconds, ms
                except :
                    print('Error in the process of pinging the server ' + str( time.time() ) + ' in your local time that is ' + str( convertedTime() ) )
                    recievedList = ['.' , 'serverError']
                    ping = 0
            else:
                print('Error in server pinging')
                recievedList , ping = mockPing()

            try :
                if recievedList[0] == SERVER_PASSWORD :
                    if recievedList[1] == 'None' :
                        print('Error: Mock ping in main loop.')
                    elif recievedList[1] == 'dataLogged' :
                        numPointsAcheived = recievedList[2]
                    elif recievedList[1] == 'eventIsOver' :
                        if recievedList[2] == 'dueToTime' :
                            readingInfoClass.add('Event is over due to time.')
                        elif recievedList[2] == 'dueToScore' :
                            readingInfoClass.add('Event is over due to all scans being sucessfully uploaded.')
                            eventOverride = True #Set it so event is over due to score
                        else :
                            readingInfoClass.add('Event is over for an unforseen issue.')
                    else :
                        print('Error: Received unforseen event from server')
                elif recievedList[0] == '.' :
                    if recievedList[1] == 'incorrectPassword' :
                        readingInfoClass.add('Error, I.P. and port correct, but incorrect password.')
                        nothing = input('Press enter to close - ')
                    elif recievedList[1]=='serverError' :
                        print('Server error ' + str(time.time()) )
            except :
                print('ERROR: In received data from server')

            if int(ping) > 3000 : #ping warning, remeber, ping is in string format
                readingInfoClass.add('Your ping is above three thousand.') #if ur ping is more than 5 thousand the client will stop
            if c_possesingScan == True : 
                if possesion == True :
                    readingInfoClass.add('Data aboard.')
                else :
                    readingInfoClass.add('Data no longer aboard.')
            if c_uploadedScan == True :
                try :
                    numScansLeft = int(numberScansToWin) - int(numPointsAcheived) #if numPointsAcheived doesn't exsist because of error in recieving data
                except :
                    numScansLeft = 'an unkown amount'
                readingInfoClass.add('You have uploaded ' + str(uploaded) + ' scans. You have ' + str(numScansLeft) + ' left to win.')
            if duringEventRotations == 0 :
                readingInfoClass.add('Event has started!')
            if READING_SETTING == 'y' or READING_SETTING == 'Y' or READING_SETTING == 'yes' or READING_SETTING == 'Yes' :
                if c_deathLog == True :
                    if len( deathsList ) == 1 :
                        readingInfoClass.add('You have died to ' + str( deathsList[0] ) )
                    else :
                        readingInfoClass.add('You have died multiple or zero times in the last few seconds.') #theoretically impossible, ya never know tho
                if C_killLog == True :
                    if len( killsList ) >= 1 :
                        stringOfKillsDataForReading = ''
                        for index , item in enumerate( killsList ) :
                            stringOfKillsDataForReading = stringOfKillsDataForReading + item 
                            if (int(index) + 1) <= len( killsList ) :
                                stringOfKillsDataForReading = stringOfKillsDataForReading + ' and '
                        readingInfoClass.add('You have killed ' + stringOfKillsDataForReading )
            
            duringEventRotations = duringEventRotations + 1
        elif time.time() <= eventStartTime : #if event hasn't started 
            minutesTillStart = int( ( int(eventStartTime) - int(time.time()) ) / 60 )
            if beforeEventRotations == 0 or ( minutesTillStart < 10 and  beforeEventRotations == 1 ) or ( minutesTillStart < 1 and  beforeEventRotations == 2 ) :
                readingInfoClass.add('Event hasnt started yet. It will begin in ' + str(minutesTillStart) + ' minutes.')
                beforeEventRotations = beforeEventRotations + 1
        elif time.time() >= ( int(eventLength) + int(eventStartTime) ) : #event is over due to time
            minutesSinceEnd = int( ( time.time() - (int(eventStartTime) + int(eventLength)) ) / 60 )
            if (minutesSinceEnd == 0 and afterEventRotations == 0) or (minutesSinceEnd == 4 and afterEventRotations == 1) :
                readingInfoClass.add('Event is over, feel free to close the software.')
                afterEventRotations = afterEventRotations + 1
            elif minutesSinceEnd == 5 :
                readingInfoClass.add('Software closing. Event has been over for more than five minutes.')
                raise SystemExit
        else :
            print('Error in main loop, time: ' + str( time.time() ) + ' in your local time that is ' + str( convertedTime() )  )
        readingInfoClass.read()
        endClock = time.time()
        loopRotations = loopRotations + 1
        time.sleep( timeToSleep(startClock , endClock) )

class readInformation :
    def __init__ (self) :
        self.fullList = []
    def add ( self , message ) :
        self.fullList.append( message )
    def read ( self ) :
        for index , item in enumerate(self.fullList) :
            tts.speak( str(item) )
            print('SAY: ' + str(item) + ' at ' + str(convertedTime()) )
            if (index + 1) != len(self.fullList) :
                time.sleep(0.65)

def addToSendingList ( listToSend , c_upload , c_death , c_kill , upload , death , kill) :
    clientCmdrName = getCMDRName()
    listToSend.append('normalPing')
    if c_upload == True :
        uploadList = ['uploadData' , upload , clientCmdrName ] #var upload is an integer
        listToSend.append( uploadList )
    if c_death == True :
        deathList = ['deathData']
        for killer in death : #list
            deathList.append( [ killer , clientCmdrName ] ) #killername  then  victim
        listToSend.append( deathList )
    if c_kill == True :
        killList = ['killData']
        for killedPerson in kill : #list
            killList.append( [ killedPerson , clientCmdrName ] ) #killed person then killer
        listToSend.append( killList )
    return(listToSend)

def mockPing () :
    list1 = [SERVER_PASSWORD , 'None']
    return( list1 , 1 )

def getKillsDeaths ( ) :
    deathsList = []
    killsList = []
    for line in reversed(convLog) :
        if line['event']=='Died' :
            try :
                deathsList.append( line['KillerName'] )   #Output of this example: "Cmdr Luvarien" #THIS MIGHT NOT WORK IF U GET KILLED MY MULTIPLE PEOPLE
            except : #if you kill yourself in game, not real life, positivity....
                deathsList.append( getCMDRName() )
        if line['event']=='PVPKill' :
            killsList.append( line['Victim'] )     #no CMDR or anything in front of it
    return( deathsList , killsList )

def timeToSleep ( startTime , endTime ) :
    timeElapsed = endTime - startTime
    time = 10 - timeElapsed
    if time >= 0 :
        return( time )
    else :
        return( 0 )

class detectChange :
    def __init__ (self , default) :
        self.oldVar = default
        self.dataType = type(default).__name__
    def check ( self , newVar ) :
        if self.dataType == 'int' or self.dataType == 'float'  :
            if newVar == self.oldVar :
                return( False , newVar )
            else :
                returnVar = newVar - self.oldVar
                self.oldVar = newVar
                return(True , returnVar)
        elif self.dataType == 'list' : 
            comRes = compare( self.oldVar , newVar )
            if comRes == True :
                return( False , newVar )
            else :
                returnVar = []
                for item in newVar :
                    returnVar.append(item)
                for item in self.oldVar:
                    try:
                        returnVar.remove(item)
                    except ValueError:
                        pass
                self.oldVar = newVar
                return( True , returnVar )
        elif self.dataType == 'bool' : #t/f
            if self.oldVar == newVar :
                return( False , newVar )
            else :
                self.oldVar = newVar
                returnVar = newVar
                return( True , returnVar )
        elif self.dataType == 'dict' :
            print('Error, if you get this one I really messed up')
        elif self.dataType == 'str' : #TEST THIS
            if self.oldVar == newVar :
                return(False , newVar)
            else :
                returnVar = ''
                for index , letter in enumerate(self.oldVar) :
                    try :
                        if letter == newVar[index] :
                            returnVar.append( letter )
                    except :
                        pass
                self.oldVar = newVar
                return( True , returnVar )
        else :
            print('Error in detect change class')
            return( False , newVar )

def testConnection () : #Example Call Output: objectiveName , eventLength , eventStartTime , numberScansToWin 
    listToSend = [ SERVER_PASSWORD , 'testConnection']
    try :
        recievedList , ping = pingServer( listToSend )
    except :
        recievedList = [SERVER_PASSWORD , 'incorrectIpOrPort']
    if recievedList[1] == 'connectionSucessful' :
        print('Test ping to server is sucessful; your ping is ' + ping )
        return( recievedList[2] , int(recievedList[3]) , int(recievedList[4]) , int(recievedList[5]) ) #This is the objective name
    elif recievedList[1] == 'incorrectPassword' :
        nothing = input('The password you entered is incorrect, but IP and port are correct were correct. Please retry.')
        raise SystemExit #closes code
    else :
        nothing = input('Ping to server was unsucessful. Incorrect IP or port. Press enter to close code. Please try again!')
        raise SystemExit #closes code

def getCMDRName () :
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('None') #Will only happen if game is just starting up

def stateOfSpace ( line ) :
    if line['event']=='Docked' or line['event']=='Died' :
        state = 'atStation'
        return(state)
    elif line['event']=='FSDJump' or line['event']=='SupercruiseEntry' :
        state = 'supercruise' 
        return(state)
    elif line['event']=='SupercruiseExit' :
        state = 'normal'
        return(state)
    else :
        return('None')

def doYaHaveScanData ( objectiveVessel ) :
    opisoteConvLog = convLog[::-1]
    spaceForm = []
    for index, line in enumerate(opisoteConvLog) :
        if stateOfSpace( line ) != 'None' :
            spaceForm.append( [ stateOfSpace(line) , index ] )  #time in normal space is, time between normal and the supercruise before it
    
    indexOfNormalSpace = []
    opsioteSpaceForm = spaceForm[::-1]
    for index, listData in enumerate( opsioteSpaceForm ) :
        if listData[0]=='normal' or listData[0]=='atStation' :
            try :                                                      #if this function doesn't work, made some modifications here earlier
                indexOfNormalSpace.append( [ listData[1] , opsioteSpaceForm[ int(index) + 1 ][1] ] )
            except IndexError : #index error will happen on opisoteSpaceForm is normal or station was the last event in it's list
                indexOfNormalSpace.append( [ listData[1] , 0 ] ) #If last event is normal or docked then it will last toward the latest line

    linesWithinNormalSpace = [] #keep in mind this is backwards
    for index , line in enumerate( opisoteConvLog ) :
        for between in indexOfNormalSpace :
            if index <= between[0] and index >= between[1] :
                linesWithinNormalSpace.append( line )
    
    possesionIndex = []
    deathIndex = []
    dockIndex = []
    undockIndex = []
    for index , line in enumerate(linesWithinNormalSpace) :
        if line['event']=='ShipTargeted' :
            try :
                fullname = line['PilotName_Localised']
                namelist = fullname.split()
                if namelist[0]=='CMDR' or namelist[0]=='Cmdr' or namelist[0]=='cmdr' :
                    del namelist[0]
                    nameOfScanned = ' '.join( namelist )
                    if nameOfScanned.upper() == objectiveVessel.upper() :
                        possesionIndex.append( index )
            except :
                pass
        elif line['event']=='Docked' :
            dockIndex.append( index )
        elif line['event'] == 'Undocked' :
            undockIndex.append( index )
        elif line['event']=='Died' :
            deathIndex.append( index )
    
    stuffOrdered = []
    for orderIndex in range(len(linesWithinNormalSpace)) :
        for itemIndex in possesionIndex :
            if itemIndex==orderIndex :
                stuffOrdered.append('scannedTarget')
        for itemIndex in deathIndex :
            if itemIndex==orderIndex :
                stuffOrdered.append('died')
        for itemIndex in dockIndex :
            if itemIndex==orderIndex :
                stuffOrdered.append('dock')
        for itemIndex in undockIndex :
            if itemIndex==orderIndex :
                stuffOrdered.append('undock')
    
    if len(stuffOrdered) != 0 :
        if stuffOrdered[0] == 'scannedTarget' :
            possesion = True
        else :
            possesion = False
        pointsUploaded = 0
        for index , item in enumerate(stuffOrdered) :
            if item == 'scannedTarget' :
                try :
                    if index >= 1 :
                        itemAfter = stuffOrdered[ index - 1 ] 
                    else :
                        itemAfter = 'None'
                except :
                    itemAfter = 'None'
                if itemAfter == 'dock' :
                    pointsUploaded = pointsUploaded + 1
    else :
        possesion = False
        pointsUploaded = 0
    return( possesion , pointsUploaded )

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

def convertedTime () :
    try :
        current = time.strftime("%H:%M:%S",time.localtime(int(time.time())))
    except :
        current = str(time.time())
    return(current)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def start () :
    if RUNNING_MODE == 's' :
        try :
            mainCode()
        except Exception as error :
            nothing = input('Big error!!!   ' + str(error))
            raise SystemExit  
    else :
        mainCode()

start()