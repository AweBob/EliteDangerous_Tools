import asyncio
import time
import json

#===========================================================================================================================================================================================

#Server code for advanced scanners! Please run in a folder as some .txt files will be created durig the process of runnin this

#For info on what to put in here, see testing files. or @ me on discord
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
EVENT_START_TIME = int(input('What time will the event start? - '))               #Must be in unix time, if your unsure google it, it's seconds since 1 of January 1970
LENGTH_EVENT = int(input('How long do you want the game to last in seconds - '))   #in seconds
SCANS_TO_WIN = int(input('How many scans till the attackers win - '))        
PLAYER_TO_SCAN = input('What is the name of the CMDR people are trying to scan - ')  #Not case sensitive, do not use CMDR in there ie Luvarien 

written = False 
eventOverDueToScoreTime = 0 
startTime = time.time()

#===========================================================================================================================================================================================

def calculateResponse ( listRecieved ) :
    try : #it could get to this point and be an empty list, so the exception is thrown
        if listRecieved[0] == SERVER_PASSWORD : #if password correct
            listToSend = [SERVER_PASSWORD ]
            if listRecieved[1] == 'testConnection' :
                listToSend.extend([ 'connectionSucessful' , PLAYER_TO_SCAN , LENGTH_EVENT , EVENT_START_TIME , SCANS_TO_WIN ])
            elif eventTimeStatus() == 0 : #event is on, this is everythin!
                try : #try cuz if lists are empty, big crash might happen
                    dataJunkReceived = listRecieved[2:] #remove password, type - leaves everythin else
                    for category in dataJunkReceived :
                        if category[0] == 'uploadData' :
                            for index in range( int(category[1]) ) : #this is the num of points the cmdr has added
                                pointsScored.addData( category[2] ) #add the cmdr name for each time they've scored
                        elif category[0] == 'deathData' :
                            del category[0]
                            for deathDataBunch in category :
                                deathsData.addData( deathDataBunch  ) # in format; [killername , victim]
                        elif category[0] == 'killData' :
                            del category[0]
                            for killDataBunch in category :
                                killsData.addData( killDataBunch ) #in format 
                        else : #shouldn't happen, except with modded clients
                            print('Received wierd ping from a client!')
                    try :
                        writeTempData() #in case the server recieves a ping that crashes it, it can be restarted
                    except :
                        print('Error in writing to temp. This is a rare one! (if its repeating tell error causing clients to restart as they are sending data in sync)')
                        pass
                except :
                    pass 
                listToSend.extend([ 'dataLogged' , str(len(pointsScored.getData())) ]) #second variable is how many points have been scored
            elif eventTimeStatus() == 1 : #event hasn't started , don't log anything
                listToSend.extend([ 'eventHasntStarted' , EVENT_START_TIME , LENGTH_EVENT ])
            elif eventTimeStatus() == 2 or eventTimeStatus() == 2.1 : #event is over, dont log anything
                listToSend.append('eventIsOver')
                if eventTimeStatus() == 2 :
                    listToSend.append('dueToTime')
                elif eventTimeStatus() == 2.1 :
                    listToSend.append('dueToScore')
                    if eventOverDueToScoreTime == 0 :
                        eventOverDueToScoreTime = int( time.time() )
                listToSend.extend([ PLAYER_TO_SCAN , str(LENGTH_EVENT) , str(EVENT_START_TIME) , str(len(pointsScored.getData())) ])
                if written == False :
                    written = True #ensure this happens first so that other threads running this won't even start writing
                    try :
                        writeFinalData()
                        print('\n' + 'Event over. Output file written.')
                    except :
                        written = False
                        print('\n' + 'Event is over. Error in writing to output file.')
                if ((time.time() / 60) - 10) > ((EVENT_START_TIME + LENGTH_EVENT) / 60 ) or ( eventOverDueToScoreTime > ( int( time.time() ) - 600 )  ) : #if event has been over for more than 10 minutes
                    print('Game has been over for more than 10 minutes. Closing Server.')
                    raise SystemExit
            else : #this is impossible - but just in case someone figures it out
                listToSend = [ SERVER_PASSWORD , 'thisIsImpossible']
        else :
            listToSend = ['.' , 'incorrectPassword']
        return( listToSend )
    except :
        print('CALCULATION_ERROR: A ping was received and processed, however, it wasnt logged correctly. A basic response will be sent. Message received:   ' + str( listRecieved ))
        return(['.' , 'serverError'])

def writeTempData () :
    fileName = 'TempServerOutput' + str( startTime ) + '.txt'
    tempFile = open( fileName ,'w+') #this is incase the server crashs and ya don't wanna lose data
    tempFile.write('TEMP OUTPUT FROM SERVER' + '\n' )
    tempFile.write('Current time: ' + '\n' + str( time.time() ) + '\n' + str( eventTimeStatus() ) + '\n' + '\n' ) #unix time - int based on time status so I don't have to do math manually
    tempFile.write('Standards: ' + '\n' + str(PLAYER_TO_SCAN) + '\n' + str(LENGTH_EVENT) + '\n' + str(EVENT_START_TIME) + '\n' + str(SCANS_TO_WIN) + '\n' + str(SERVER_PASSWORD) + '\n' + str(SERVER_PORT) + '\n' + str(SERVER_IP_ADRESS) + '\n' + '\n'  ) #refer to here for what where
    tempFile.write( 'KILLS LIST' + '\n')
    for d in killsData.getData() :
        tempFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n' )   #killername then victim        
    tempFile.write('\n' + 'DEATHS LIST' + '\n'  ) 
    for d in deathsData.getData() :
        tempFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n')   #personWho died then their killers name
    tempFile.write('\n' + 'POINTS SCORED LIST' + '\n'  ) 
    for d in pointsScored.getData() :
        tempFile.write( str(d) + '\n' )    #person who scored a scan
    tempFile.close()

def writeFinalData () :
    fileName = 'ServerOutput' + str(startTime) + '.txt'
    outputFile = open( fileName ,"w+")   #Use outputFile.write('text' + '\n') to write a new line to it
    outputFile.write('KILLS LIST' + '\n'  )
    for d in killsData.getData() :
        outputFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n' )   #killername then victim        
    outputFile.write('\n' + 'DEATHS LIST' + '\n'  ) 
    for d in deathsData.getData() :
        outputFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n')   #personWho died then their killers name
    outputFile.write('\n' + 'POINTS SCORED LIST' + '\n'  ) 
    for d in pointsScored.getData() :
        outputFile.write( str(d) + '\n')    #person who scored a scan
    tttt = eventTimeStatus()
    if tttt == 2.1 :
        outputFile.write('\n' + '\n' + '\n' + '\n' + 'EVENT ENDED DUE TO SCORE' + '\n' + 'SCANNING EQUIPPED VESSELS HAVE WON' + '\n' ) 
    else :
        outputFile.write('\n' + '\n' + '\n' + '\n' + 'EVENT ENDED DUE TO TIME' + '\n' + 'VESSELS DEFENDING DATA HAVE WON' + '\n' )
    outputFile.close()
    print('Sucessfully wrote data to .txt file in this current directoy. Reference it for developing a post match report.')

def eventTimeStatus () :
    if len(pointsScored.getData()) >= SCANS_TO_WIN : #if event is over by score
        stat = 2.1 #event is over due to scored
    else : #if event isn't over by score
        if time.time() >= EVENT_START_TIME and time.time() <= ( EVENT_START_TIME + LENGTH_EVENT ) :
            stat = 0 #event is on
        elif time.time() < EVENT_START_TIME :
            stat = 1 #event hasn't started
        else :
            stat = 2 #event is over due to time
    return( stat )

class dataListStorage :
    def __init__ ( self ) :
        self.data = []
    def addData ( self , newData ) :
        self.data.append( newData )
    def removeData ( self , toRemove ) :
        try :
            self.data.remove( toRemove )
        except :                           #this happens if the one you wanna remove isn't in it
            pass
    def getData ( self ) :
        return( self.data )
    def getDataString ( self ) :
        string = ''
        for item in self.data :
            string = string + ' ' + item 
        return( string )

killsData = dataListStorage() #Filled with lists like this [ killerName , victim ]
deathsData = dataListStorage() #Filled with lists like this [ cmdrWhoDied , personWhoKilledThem ]
pointsScored = dataListStorage() #This is one list filled with names of people who got points

#===========================================================================================================================================================================================

async def handle_echo(reader, writer):
    try :
        data = await reader.read(1000) 
        message = json.loads( data )     #no decode - yes this is necessary, i think lmao we'll find out
        addr = writer.get_extra_info('peername')
        listToSend = calculateResponse( message )
        writer.write( json.dumps( listToSend ).encode() )
        await writer.drain()
        writer.close()
        print('Received: ' + str(message) + '    Sending: ' + str( listToSend ) + '    Time: ' + str( time.time() ) + '    From: ' + str( addr ) )
    except :
        print('PING_ERROR: A ping which failed to be read or failed to be converted to list format was received. No response will be issued. TimeStamp: ' + str(time.time()))
        pass #if thing recieved is empty or not in list format, don't respond or do anything

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)
print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

#===========================================================================================================================================================================================
