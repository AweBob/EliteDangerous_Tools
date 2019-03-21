import asyncio

#===========================================================================================================================================================================================

#For info on what to put in here, see testing files.
print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')

#===========================================================================================================================================================================================

def calculateResponse ( stringRecieved ) : #Use global variables
    listRecieved = stringRecieved.split()   #0 = password 1 = type 2 = data
    if listRecieved[0] == SERVER_PASSWORD :
        #In here this needs more development, issue is idk what kinda data this should transfer
        stringToSend = '. MESSAGERECEIVED .'
    else :
        stringToSend = '. INCORRECTPASSWORD .'   #Response password = '.'  type = 'incorpass' data = '.'   #software assumes period as nothing
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
