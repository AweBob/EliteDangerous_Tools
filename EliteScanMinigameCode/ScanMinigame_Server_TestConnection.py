import asyncio
import string     #only for random words func
import random     #only for rand word fu
import json

#port forward this info with TCP format
SERVER_IP_ADRESS = '192.168.1.4'                 #string - internal ip adress of your wifi network (use this ip in port forwarding)   YOUR LOCALHOST IP
SERVER_PORT = 13723                              #13722 13723 13780 13781 13784 13750 13760 13745        <---- example ports you can use, just pick a random one   integer (port forward and copy to client)
SERVER_PASSWORD = ''                             #Random string, as long as both server and client have this same thing isn't fine #Unnecessary for test version

async def handle_echo(reader, writer):
    try :
        data = await reader.read(1000)
        message = json.loads( data ) #no decode
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % ( str(message) , addr))
        #for i in message : #proof this works
            #print(i)

        lis = randomList()
        
        print('Sending: %r' % str(lis) )
        writer.write( json.dumps( lis ).encode() ) #encode
        await writer.drain()

        writer.close()
    except :
        print('Recieved incorectly formatted ping or failed to send message: ' + str( time.time() ) )

def randomList () :
    listThang = []
    for x in range( random.randint(2,5) ) :
        strin = ''
        for i in range(0,10) :
            strin = strin + random.choice(string.ascii_letters)
        listThang.append( strin )
    return( listThang )

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

