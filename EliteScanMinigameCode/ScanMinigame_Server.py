import asyncio
import time

#===========================================================================================================================================================================================

#For info on what to put in here, see testing files.
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')
SERVER_MODE = int(input('What mode is the server starting in - '))       # 0= pregame      Anything else is time in seconds till game starts in seconds
LENGTH_EVENT = int(input('How long do you want the game to last in seconds - '))
SCANS_TO_WIN = int(input('How many scans till the attackers win - '))

if SERVER_MODE != 0 :
    TIME_AT_START = time.time() + SERVER_MODE

playerList = []
#===========================================================================================================================================================================================

def calculateResponse ( stringRecieved ) : #Use global variables
    listRecieved = stringRecieved.split()   #0 = password ||| 1 = Message Type ||| 3 = data of message ||| 4 = extra data  
    if listRecieved[0] == SERVER_PASSWORD :
        if listRecieved[1] == 'testConnection' :
            stringToSend = SERVER_PASSWORD + ' connectionSucessful None 0' 
        elif listRecieved[1] == 'whenStart' :
            stringToSend = SERVER_PASSWORD + ' serverStartTime ' + TIME_AT_START + ' 0'
        elif listRecieved[1] == 'initSpectator' :
            playerList.append(listRecieved[2])
            stringToSend = SERVER_PASSWORD + ' loggedIn'
    else :
        stringToSend = '. incorrectPassword . .'   #Response password = '.'  type = 'incorpass' data = '.'   #software assumes period as nothing
    return( stringToSend )

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
