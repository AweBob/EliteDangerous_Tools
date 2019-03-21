import asyncio
import string     #only for random words func
import random     #only for rand word fu

#port forward this info with TCP format
SERVER_IP_ADRESS = '192.168.1.4'                 #string - internal ip adress of your wifi network (use this ip in port forwarding)   YOUR LOCALHOST IP
SERVER_PORT = 13723                              #13722 13723 13780 13781 13784 13750 13760 13745        <---- example ports you can use, just pick a random one   integer (port forward and copy to client)
SERVER_PASSWORD = ''                             #Random string, as long as both server and client have this same thing isn't fine #Unnecessary for test version

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    word = randomWords()
    print('Sending: %r' % word )
    writer.write( word.encode() )
    await writer.drain()

    writer.close()

def randomWords () :
    strin = ''
    for i in range(0,10) :
        strin = strin + random.choice(string.ascii_letters)
    return( str(strin) )

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

