import asyncio
import time

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

outputFile = open("ServerOutput.txt","w+")   #Use outputFile.write('text' + '\n') to write a new line to it
written = False
#===========================================================================================================================================================================================
#Takes in: kd nothing points or both
#Sends: event time stats, how many points scored
#stores: kills deaths and points scored

def calculateResponse ( stringRecieved ) : 
    listRecieved = stringRecieved.split()   #0 = password ||| 1 = Message Type ||| 3 = data of message ||| 4 = extra data  
    if listRecieved[0] == SERVER_PASSWORD :
        if listRecieved[1] == 'testConnection' :
            stringToSend = SERVER_PASSWORD + ' connectionSucessful ' + PLAYER_TO_SCAN + ' ' + str(LENGTH_EVENT) + ' ' + str(EVENT_START_TIME)
        elif eventTimeStatus() == 0 : #if event is live
            if listRecieved[1] == 'normalClientPing' : #No new data sent, but requesting new data
                y = 69
            elif listRecieved[1] == 'oneUpdate' : 
                y = 69
            elif listRecieved[1] == 'twoUpdate' : 
                y = 69
            elif listRecieved[1] == 'threeUpdate' : 
                y = 69
            elif listRecieved[1] == 'fourUpdate' : 
                y = 69
        elif eventTimeStatus() == 1 : #event hasn't started
            stringToSend = SERVER_PASSWORD + ' eventHasntStarted ' + PLAYER_TO_SCAN + ' ' + str(LENGTH_EVENT) + ' ' + str(EVENT_START_TIME)
        elif eventTimeStatus() == 2 : #event is over
            stringToSend = SERVER_PASSWORD + ' eventIsOver ' + PLAYER_TO_SCAN + ' ' + str(LENGTH_EVENT) + ' ' + str(EVENT_START_TIME)
            if written == False :
                #outputFile.write('text' + '\n')            #Here write kills deaths and points scored and by who
                print('\n' + 'Event over. Output file written.')
                written = True
    else :
        stringToSend = '. incorrectPassword . .'   #Response password = '.'  type = 'incorpass' data = '.'   #software assumes period as nothing
    return( stringToSend )

def eventTimeStatus () :
    #timeLeft = ( EVENT_START_TIME + LENGTH_EVENT ) - time.time()
    if time.time() >= EVENT_START_TIME and time.time() <= ( EVENT_START_TIME + LENGTH_EVENT ) :
        stat = 0 #event is on
    elif time.time() < EVENT_START_TIME :
        stat = 1 #event hasn't started
    else :
        stat = 2 #event is over
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

#===========================================================================================================================================================================================

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    #print("Received %r from %r" % (message, addr))

    stringToSend = calculateResponse( message )

    #print('Sending: %r' % stringToSend )
    writer.write( stringToSend.encode() )
    await writer.drain()

    writer.close()
    print('Received: ' + message + '   Sending: ' + stringToSend + '  Time: ' + str( time.time() ) )

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

#===========================================================================================================================================================================================
