import asyncio
import time
from os import *
import os
from glob import *
import glob
import json
import win32com.client as wincl

#This is client code for advanced vessel scanner and station data uploader, when distributing change the below capslocked variables to the actual thing so users don't have to enter it

#===========================================================================================================================================================================================

tts = wincl.Dispatch("SAPI.SpVoice") #Will crash here for nonwindows users - if your playing on mac, im sorry
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 19.374.922.82) - ')
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')

#===========================================================================================================================================================================================

def pingServer( ToSend ) :
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)
        startTimer = time.time()
        writer.write(message.encode())
        data = await reader.read(100)
        recievedString = data.decode()
        endTimer = time.time()
        writer.close()
        ping = str( int(( endTimer - startTimer ) * 100) )
        return( recievedString , ping )

    message = str(ToSend)
    loop = asyncio.get_event_loop()
    recievedString , ping = loop.run_until_complete(tcp_echo_client(message, loop))
    return( recievedString , ping )

#===========================================================================================================================================================================================
#recievedString , ping = pingServer( input('What do you want to send? - ') )
#tts.speak('test')

def mainCode () :
    testConnection()
    dc_spaceTtype = detectChange('')       #Space position(normal, supercruise, docked), string
    dc_posessingScan = detectChange('')    #Does CMDR have scna data aboard, True or false
    dc_killDeathLog = detectChange('')         #records everyone you've killed and everyone who has killed you
    while True :
        startClock = time.time()
        logTransformer(grabLog(0))  #update .log import variable is convLog
        #Ping server every 10 seconds requesting all info, based on role only display some of it; unless something changes in which case nofity server, which will always respond with the same thing
        spaceType = stateOfSpace()
        clientName = getCMDRName()
        deathsList , killsList = getKillsDeaths()
        possesion , uploaded = scanCalc() #NOT COMPLEETED
        #recievedString , ping = pingServer( input('What do you want to send? - ') )
        endClock = time.time()
        time.sleep( timeToSleep(startClock , endClock) )


def scanCalc () :           #NOT EVEN CLOSE TO DONE, this is the major function of this script
    inPossesion = False
    uploaded = 0
    opisoteConvLog = reversed(convLog)
    lineNumber = 0
    for line in opisoteConvLog :
        if line['event']=='Died' :
            break
        lineNumber = lineNumber + 1
    relevantLogLines = opisoteConvLog[:lineNumber]   #it doesn't like this, why, g-d knows
    for line in relevantLogLines :
        y = 69 #placeholder
    


def getKillsDeaths ( ) :  #eventondeath: https://prnt.sc/n1y0ex DELETE LATER
    deathsList = []
    killsList = []
    for line in reversed(convLog) :
        if line['event']=='Died' :
            deathsList.append( line['KillerName'] )   #Output of this example: "Cmdr Luvarien"
        if line['event']=='PVPKill' :
            killsList.append( line['Victim'] )     #UNSURE ABOUT THIS, AWAITTING EXAMPLE
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
    def check ( self , newVar ) :
        if self.oldVar == newVar :
            return( False )
        else :
            self.oldVar = newVar 
            return( True )

def testConnection () :
    listToSend = [ SERVER_PASSWORD , 'testConnection' , 'None' , '0' ]
    stringToSend = ' '.join( listToSend )
    recievedString , ping = pingServer( stringToSend )
    recievedList = recievedString.split()
    if recievedList[1] == 'connectionSucessful' :
        print('Test ping to server is sucessful; your ping is ' + ping )
    elif recievedList[1] == 'incorrectPassword' :
        nothing = input('The password you entered is incorrect, but IP and port are correct were correct. Restart code.')
    else :
        nothing = input('Ping to server was unsucessful. Incorrect IP or port. Restart the code.')

def getCMDRName () :
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('None') #Will only happen if game is just starting up

def stateOfSpace () :
    for line in reversed(convLog) :
        if line['event']=='Died' :
            state = 'dead'
            return(state)
        elif line['event']=='Docked' :
            state = 'atStation'
            return(state)
        elif line['event']=='FSDJump' or line['event']=='SupercruiseEntry' :
            state = 'supercruise' 
            return(state)
        elif line['event']=='SupercruiseExit' :
            state = 'normal'
            return(state)
    state = 'startingGame'
    return(state)

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

mainCode()
