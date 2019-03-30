import asyncio
import time
import json

#===========================================================================================================================================================================================

#For info on what to put in here, see testing files. or @ me on discord
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
EVENT_START_TIME = int(input('What time will the event start? - '))               #Must be in unix time, if your unsure google it, it's seconds since 1 of January 1970
LENGTH_EVENT = int(input('How long do you want the game to last in seconds - '))   #in seconds
SCANS_TO_WIN = int(input('How many scans till the attackers win - '))        
PLAYER_TO_SCAN = input('What is the name of the CMDR people are trying to scan - ')  #Not case sensitive, do not use CMDR in there ie Luvarien 

written = False #this could be an issue regarding variable not being global
#Open all class stuff here (below cuz it has to be, but should be with all this data)

#===========================================================================================================================================================================================
#Takes in: kd nothing points or both
#Sends: event time stats, how many points scored
#stores: kills deaths and points scored

def calculateResponse ( listRecieved ) :  #NEEDS A COMPLETE REWRITE - PROLLY GONNA COMPLETELY DELETE AND REWRITE THIS FOR NEXT COMMIT
    #0 = password ||| 1= testConnection or normalPing ||| 3= cmdr name
    
    if listRecieved[0] == SERVER_PASSWORD : #if password correct
        listToSend = [SERVER_PASSWORD ]
        if listRecieved[1] == 'testConnection' :
            listToSend.extend([ 'connectionSucessful' , PLAYER_TO_SCAN , LENGTH_EVENT , EVENT_START_TIME , SCANS_TO_WIN ])
        elif eventTimeStatus() == 0 : #event is on, this is everythin!
            try : #try cuz if lists are empty, big crash might happen
                dataJunkReceived = listRecieved[3:] #remove password, type and CMDR name - leaves everythin else
                for category in dataJunkReceived :
                    if category[0] == 'uploadData' :
                        foo = 'bar'
                    elif category[0] == '' :
                        foo = 'bar'
                    elif category[0] == '' :
                        foo = 'bar'
                writeTempData() #in case the server recieves a ping that crashes it, it can be restarted
            except :
                pass

            #HERE IS WHERE I PUT IN THE INFORMATION LOGGING
            #Return here number of scans completed here as well

        elif eventTimeStatus() == 1 : #event hasn't started , don't log anything
            listToSend.extend([ 'eventHasntStarted' , EVENT_START_TIME , LENGTH_EVENT ])
        elif eventTimeStatus() == 2 or eventTimeStatus() == 2.1 : #event is over, dont log anything
            listToSend.append('eventIsOver')
            if eventTimeStatus() == 2 :
                listToSend.append('dueToTime')
            elif eventTimeStatus() == 2.1 :
                listToSend.append('dueToScore')
            listToSend.extend([  PLAYER_TO_SCAN , str(LENGTH_EVENT) , str(EVENT_START_TIME) ])
            if written == False :
                writeFinalData()
                print('\n' + 'Event over. Output file written.')
                written = True
    else :
        listToSend = ['.' , 'incorrectPassword']
    return( listToSend )


def writeTempData () :
    tempFile = open('TempServerOutput.txt','w+') #this is incase the server crashs and ya don't wanna lose data
    tempFile.write('\n' + 'TEMP OUTPUT FROM SERVER' + '\n' )
    tempFile.write('Current time: ' + str(time.time()) + str(eventTimeStatus()) + '\n' + '\n' ) #unix time - int based on time status so I don't have to do math manually
    tempFile.write('Standards: ' + PLAYER_TO_SCAN + LENGTH_EVENT + EVENT_START_TIME + SCANS_TO_WIN + SERVER_PASSWORD + SERVER_PORT + SERVER_IP_ADRESS + '\n' + '\n' ) #refer to here for what where
    tempFile.write('\n' + '\n' + '\n' + '\n' + 'KILLS LIST' + '\n'  )
    for d in killsData.getData() :
        tempFile.write(d[0] + ' ' + d[1] + '\n' )   #killername then victim        
    tempFile.write('\n' + '\n' + '\n' + '\n' + 'DEATHS LIST' + '\n'  ) 
    for d in deathsData.getData() :
        tempFile.write(d[0] + ' ' + d[1] + '\n')   #personWho died then their killers name
    tempFile.write('\n' + '\n' + '\n' + '\n' + 'POINTS SCORED LIST' + '\n'  ) 
    for d in pointsScored.getData() :
        tempFile.write( d[0] + '\n' )    #person who scored a scan
    tempFile.close()


def writeFinalData () :
    outputFile = open("ServerOutput.txt","w+")   #Use outputFile.write('text' + '\n') to write a new line to it
    outputFile.write('\n' + '\n' + '\n' + '\n' + 'KILLS LIST' + '\n'  )
    for d in killsData.getData() :
        outputFile.write(d[0] + ' ' + d[1] + '\n' )   #killername then victim        
    outputFile.write('\n' + '\n' + '\n' + '\n' + 'DEATHS LIST' + '\n'  ) 
    for d in deathsData.getData() :
        outputFile.write(d[0] + ' ' + d[1] + '\n')   #personWho died then their killers name
    outputFile.write('\n' + '\n' + '\n' + '\n' + 'POINTS SCORED LIST' + '\n'  ) 
    for d in pointsScored.getData() :
        outputFile.write( d[0] + '\n')    #person who scored a scan
    tttt = eventTimeStatus()
    if tttt == 2.1 :
        outputFile.write('\n' + '\n' + '\n' + '\n' + 'EVENT ENDED DUE TO SCORE' + '\n' + 'SCANNING EQUIPPED VESSELS HAVE WON' + '\n' ) 
    else :
        outputFile.write('\n' + '\n' + '\n' + '\n' + 'EVENT ENDED DUE TO TIME' + '\n' + 'VESSELS DEFENDING DATA HAVE WON' + '\n' )
    outputFile.close()
    print('Sucessfully wrote data to .txt file in this current directoy. Reference it for developing a post match report.')


def eventTimeStatus () :
    #timeLeft = ( EVENT_START_TIME + LENGTH_EVENT ) - time.time()
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
    data = await reader.read(1000) 
    message = json.loads( data )     #no decode - yes this is necessary, i think lmao we'll find out
    addr = writer.get_extra_info('peername')
    #print("Received %r from %r" % (message, addr))

    listToSend = calculateResponse( message )

    #print('Sending: %r' % stringToSend )
    writer.write( json.dumps( listToSend ).encode() )
    await writer.drain()

    writer.close()
    print('Received: ' + str(message) + '   Sending: ' + str( listToSend ) + '  Time: ' + str( time.time() ) + '  From: ' + str( addr ) )

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

#===========================================================================================================================================================================================
