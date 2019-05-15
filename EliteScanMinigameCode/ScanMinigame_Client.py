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

tts = wincl.Dispatch("SAPI.SpVoice") #Will crash here for nonwindows users - if your playing on mac, im sorry, but get a real computer :p <--- just a joke    #assign reading class to object
compare = lambda x, y: collections.Counter(x) == collections.Counter(y) #setup comparing function - should prolly do this elsewhere, but it looks really nice here as it's a 1 liners

print('Imported libraries Sucessfully') #If the above is passed, do a readout, if this isn't printed it's prolly an issue with pyinstaller loading in the above imports, this won't show up on linux builds
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 19.374.922.82) - ') #must be a string 
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
READING_SETTING = input('Do you want to be read to everytime you die or get a kill? (y/n) - ')
RUNNING_MODE = input('Safe startup or normal startup? (s/n) - ') #Safe is really only for testing for errors, but I'll leave the option in there for now! #In the end, set to 'n'

#===========================================================================================================================================================================================

def pingServer( ToSend ) : #ToSend should be a list - MUST be a list   #function to send the server a message and receive a message, will produce error if server cannot be found
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
    return( recievedStuff , ping ) #ping is in milliseconds, if it's above 5000 then this will produce an error, as it should

#===========================================================================================================================================================================================

def mainCode () :
    loopRotations = 0 #loop rotations for main while loop.
    beforeEventRotations = 0 #number of times this thing has looped before the event has started
    afterEventRotations = 0 #times looped after event has ended
    duringEventRotations = 0 #times looped during event
    duringEventOverDueToTime = 0 #times event has been over due to score
    objectiveName , eventLength , eventStartTime , numberScansToWin = testConnection() #all time is unix time because it's easy - no timezoes, simple mathematic computable formula  #Send the server a first ping and gather data about the game
    dc_currentLogFileName = detectChange( grabLog(0) ) 
    eventOverride = False #Event is good to continue by defaultt, could change eventually

    while True :
        startClock = time.time() #The time the loop is starting at
        readingInfoClass = readInformation()   #clear/define the class for reading out information
        if eventOverride == True : #if event is over due to score
            if duringEventOverDueToTime >= 600 : #if event has been over due to score for more than 10 minutes
                nothing = input('Event has been over for ten minutes, press enter to close - ') #print a quick error message
                raise SystemExit #close the code
            duringEventOverDueToTime = duringEventOverDueToTime + 1 #Each time the event has been over due to score add a number to this
        elif time.time() >= int(eventStartTime) and time.time() <= ( int(eventLength) + int(eventStartTime) ) : #if event is live 

            logFile_Path = grabLog(0) #get the name of the path of the log file
            c_trueFalseChangeLogFile , d_changeLogFile = dc_currentLogFileName.check( logFile_Path ) #check if the name of the log file has changed
            logTransformer( logFile_Path )  #refresh variable convLog to contain acurate information of what's in the latest.log file

            deathsList , killsList = getKillsDeaths() #calculate kills and deaths of the curent .log file
            possesion , uploaded = doYaHaveScanData( objectiveName ) #figure out if you currently have scan data aboard and how many scans you have uploaded

            if loopRotations == 0 or c_trueFalseChangeLogFile == True :  #code had just started or a new .log file has apeared(elite has been restarted) - then - reset detect change classes that gather data from .log files
                dc_posessingScan = detectChange(False)  #bool  #Does CMDR have scna data aboard, True or false  #reinitialize class for detecting change
                dc_uploadedScan = detectChange(uploaded) #int  #reinitialize class for detecting change
                dc_killLog = detectChange(killsList)    #list     #records everyone you've killed   #reinitialize class for detecting change
                dc_deathLog = detectChange(deathsList) #list  #reinitialize class for detecting change

            c_possesingScan , possesion = dc_posessingScan.check( possesion ) #t/f #check if this has changed
            c_uploadedScan , uploaded = dc_uploadedScan.check( uploaded  )    #int  #check if this has changed
            C_killLog , killsList = dc_killLog.check( killsList )             #list  #check if this has changed
            c_deathLog , deathsList = dc_deathLog.check( deathsList )         #list   #check if this has changed

            listToSend = [ SERVER_PASSWORD ] #introduce the list which will be sent to server, so far iot onjly contains the password

            listToSend = addToSendingList( listToSend , c_uploadedScan , c_deathLog , C_killLog , uploaded , deathsList , killsList ) #Call function to add necessary info to list to send
            if len( listToSend ) != 0 : #checks that list has any content - theoretically impossible, but will prevent causing server errors(not server crashes) in modded clients
                try : 
                    recievedList , ping = pingServer( listToSend ) #ping in milliseconds, ms  #Attempt to ping the server
                except : #If there is an error
                    print('Error in the process of pinging the server ' + str( time.time() ) + ' in your local time that is ' + str( convertedTime() ) ) #print to console this error, will not exit app
                    recievedList = ['.' , 'serverError'] #set the received list to server error
                    ping = 0 #set ping to zero as to not cause errors down the line
            else: #theoretically impossible without modded clients
                print('Error in server pinging ' + str( convertedTime() ))
                recievedList , ping = mockPing()

            try : #attempt to process data from server (this is needed incase the server responds incorrectly, or your connected to the wrong server)
                if recievedList[0] == SERVER_PASSWORD : #first confirm the servere sent back the password
                    if recievedList[1] == 'dataLogged' : #if server responds with the basic reply 
                        numPointsAcheived = recievedList[2] #save the response contents, which should be an integer which is the number of scans your group has acheived
                    elif recievedList[1] == 'eventIsOver' : #if event is over ping is sent
                        if recievedList[2] == 'dueToTime' :  #if it's due to time, (very rare, cuz client keeps track of time as well)
                            readingInfoClass.add('Event is over due to time.') #add readout
                        elif recievedList[2] == 'dueToScore' : #if it's duetoscore (this one is not only possible, but likely)
                            readingInfoClass.add('Event is over due to all scans being sucessfully uploaded.') #add readout
                            eventOverride = True #Set it so event is over due to score - this will affect the main loop and will override the main loop
                        else : #if it's something else, another theoretically impossible one
                            readingInfoClass.add('Event is over for an unforseen issue.') #add readout
                    else : #if it's an unkown event, another theoretically impossible boyo
                        print('Error: Received unforseen event from server') #don't readout, just print this
                elif recievedList[0] == '.' : #if received list starts with this instead of nothing
                    if recievedList[1] == 'incorrectPassword' : #if password is wrong
                        readingInfoClass.add('Error, I.P. and port correct, but incorrect password.') #readout
                        nothing = input('Press enter to close - ') #quick pause
                        raise SystemExit #close code
                    elif recievedList[1]=='serverError' : #if it's a server error, do a printout and nothing else
                        print('Server error ' + str( convertedTime() ))
                    else :
                        print('Server error: password received is wrong and no reason why: ' + str( convertedTime() ))
                else :
                    print('Server error: First item in list is empty: ' + str( convertedTime() ))
            except :
                print('ERROR: In received data from server')

            if int(ping) > 3000 : #ping warning, remeber, ping is in string format  #if ping is big!
                readingInfoClass.add('Your ping is above three thousand.') #if ur ping is more than 5 thousand the client will stop
            if c_possesingScan == True : #if this variable has changed
                if possesion == True : #if you just got data
                    readingInfoClass.add('Data aboard.') #add to readout
                else : #if you lost the data
                    readingInfoClass.add('Data no longer aboard.') #add readoutt
            if c_uploadedScan == True : #if number of scans has changed
                try : #attempt
                    numScansLeft = int(numberScansToWin) - int(numPointsAcheived) #if numPointsAcheived doesn't exsist because of error in recieving data
                except : #if numPointsAcheived hasn't been defined because of a server error
                    numScansLeft = 'an unkown amount'
                readingInfoClass.add('You have uploaded ' + str(uploaded) + ' scans. You have ' + str(numScansLeft) + ' left to win.') #add readout
            if duringEventRotations == 0 : #if this is the first time during the major while loop that the event is active
                readingInfoClass.add('Event has started!') #add readout
            if READING_SETTING == 'y' or READING_SETTING == 'Y' or READING_SETTING == 'yes' or READING_SETTING == 'Yes' : #if additional readout is enabled
                if c_deathLog == True : #if change in the users deathlist is detected
                    deathsString = " and ".join( deathsList ) #split this list into a string split by the word and with some spaces
                    readingInfoClass.add('You have died to ' + str( deathsString )  ) #add to readout
                if C_killLog == True : #if change in killlog
                    if len( killsList ) >= 1 : #if ytou've got at least 1 kill
                        stringOfKillsDataForReading = '' #initialize string
                        for index , item in enumerate( killsList ) : #for each item inside killsList
                            stringOfKillsDataForReading = stringOfKillsDataForReading + item  #add the item to the string
                            if (int(index) + 1) <= len( killsList ) : #if the item isn't the last one in the list
                                stringOfKillsDataForReading = stringOfKillsDataForReading + ' and ' #add the word and to it
                        readingInfoClass.add('You have killed ' + stringOfKillsDataForReading ) #add readout
            
            duringEventRotations = duringEventRotations + 1 #add a round to the number of rotations while the event is online
        elif time.time() <= eventStartTime : #if event hasn't started 
            minutesTillStart = int( ( int(eventStartTime) - int(time.time()) ) / 60 ) #minutes until the game starts
            if beforeEventRotations == 0 or ( minutesTillStart < 10 and  beforeEventRotations == 1 ) or ( minutesTillStart < 1 and  beforeEventRotations == 2 ) : #ensure it hasn't been read for too much
                readingInfoClass.add('Event hasnt started yet. It will begin in ' + str(minutesTillStart) + ' minutes.') #readout
                beforeEventRotations = beforeEventRotations + 1 #increase number of times it's been read
        elif time.time() >= ( int(eventLength) + int(eventStartTime) ) : #if event is over due to time
            minutesSinceEnd = int( ( time.time() - (int(eventStartTime) + int(eventLength)) ) / 60 ) #minutes since the game has ended
            if (minutesSinceEnd == 0 and afterEventRotations == 0) or (minutesSinceEnd == 4 and afterEventRotations == 1) :
                readingInfoClass.add('Event is over, feel free to close the software.')
                afterEventRotations = afterEventRotations + 1
            elif minutesSinceEnd == 5 :
                readingInfoClass.add('Software closing. Event has been over for more than five minutes.')
                raise SystemExit
        else : #if event time status isn't valid, theoretically impossible
            print('Error in main loop, time: ' + str( time.time() ) + ' in your local time that is ' + str( convertedTime() )  ) #print error, no readout
        readingInfoClass.read() #read out all information added to readout information
        endClock = time.time() #end the time
        loopRotations = loopRotations + 1 #increase the number of times this while loop has rotated by one
        time.sleep( timeToSleep(startClock , endClock) ) #sleep however much time to ensure this entire loop took 10 seconds. This function takes 0.05 secs and therefore causes a slight bit of error, its fine tho

class readInformation : #readout class
    def __init__ (self) : #init creates a clean list
        self.fullList = []
    def add ( self , message ) : #adds message to list
        self.fullList.append( message )
    def read ( self ) : #reads out each item in list, with delay.
        for index , item in enumerate(self.fullList) :
            tts.speak( str(item) )
            print('SAY: ' + str(item) + ' at ' + str(convertedTime()) )
            if (index + 1) != len(self.fullList) :
                time.sleep(0.65)

def addToSendingList ( listToSend , c_upload , c_death , c_kill , upload , death , kill) : #if there is a change in c_ variables, add the other variable into list to send, then send it back
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

def mockPing () : #returns info of an error ping
    list1 = [SERVER_PASSWORD , 'None']
    return( list1 , 1 )

def getKillsDeaths ( ) : #calculates if you've died or killed anyone, returns the info. ensure convlog is updated first
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

def timeToSleep ( startTime , endTime ) : #takes in start and end time and does math in roder to make loop last 10 secs exactly
    timeElapsed = endTime - startTime
    time = 10 - timeElapsed
    if time >= 0 :
        return( time )
    else :
        return( 0 )

class detectChange : #detects change in variables
    def __init__ (self , default) : #defines an initial values and logs the type of that variable
        self.oldVar = default
        self.dataType = type(default).__name__
    def check ( self , newVar ) : #takes in a variable sees if its changed form the last value. if it has send back the change in it and wether or not it has changed. Then sets variable to newly sent one.
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

def testConnection () : #Example Call Output: objectiveName , eventLength , eventStartTime , numberScansToWin   #Initial ping to server, grabs basic info about the active event and ensures server is online
    listToSend = [ SERVER_PASSWORD , 'testConnection']
    try :
        recievedList , ping = pingServer( listToSend )
    except :
        recievedList = [SERVER_PASSWORD , 'incorrectIpOrPort']
    if recievedList[1] == 'connectionSucessful' :
        print('Initialization ping to server is sucessful, your ping is ' + ping )
        return( recievedList[2] , int(recievedList[3]) , int(recievedList[4]) , int(recievedList[5]) ) #This is the objective name
    elif recievedList[1] == 'incorrectPassword' :
        nothing = input('The password you entered is incorrect, but IP and port are correct were correct. Please retry.')
        raise SystemExit #closes code
    else :
        nothing = input('Ping to server was unsucessful. Incorrect IP or port. Press enter to close code. Please try again!')
        raise SystemExit #closes code

def getCMDRName () : #get the CMDR name of the latest .log file
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('None') #Will only happen if game is just starting up

def stateOfSpace ( line ) : #returns what state of space you are in based on the event in a line from convLog
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

def doYaHaveScanData ( objectiveVessel ) : #see if u are possesiong the scn data and how many scans you have dropped off
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