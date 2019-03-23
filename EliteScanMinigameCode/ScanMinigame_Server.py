import asyncio
import time

#===========================================================================================================================================================================================

#For info on what to put in here, see testing files. or @ me on discord
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
EVENT_START_TIME = int(input('What time will the event start? - '))               #Must be in unix time, if your unsure google it, it's seconds since 1 of January 1970
LENGTH_EVENT = int(input('How long do you want the game to last in seconds - '))
SCANS_TO_WIN = int(input('How many scans till the attackers win - '))        
PLAYER_TO_SCAN = input('What is the name of the CMDR people are trying to scan - ')  #Include CMDR in it; i.e. CMDR Luvarien 

outputFile = open("ServerOutput.txt","w+")   #Use outputFile.write('text' + '\n') to write a new line to it

#===========================================================================================================================================================================================
#Takes in: User inf(cmdr name; isEliteRunning; spaceType(docked,supercruise,normal); possesion of scan), role, deaths and to who(only within the time limits tho)
#Sends/Stores: Points scored(who scored em); kill tracker; time left/time till start; 

def calculateResponse ( stringRecieved ) : 
    listRecieved = stringRecieved.split()   #0 = password ||| 1 = Message Type ||| 3 = data of message ||| 4 = extra data  
    if listRecieved[0] == SERVER_PASSWORD :
        if listRecieved[1] == 'testConnection' :
            stringToSend = SERVER_PASSWORD + ' connectionSucessful None 0' 
        elif listRecieved[1] == 'normalClientPing' :
            stringToSend = 69 #PLACEHOLDER
    else :
        stringToSend = '. incorrectPassword . .'   #Response password = '.'  type = 'incorpass' data = '.'   #software assumes period as nothing
    return( stringToSend )


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
    print("Received %r from %r" % (message, addr))

    stringToSend = calculateResponse( message )

    print('Sending: %r' % stringToSend )
    writer.write( stringToSend.encode() )
    await writer.drain()

    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

#===========================================================================================================================================================================================
