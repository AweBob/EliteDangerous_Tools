import asyncio
import string     #only for random words func
import random     #only for rand word fu

#LENGTH_OF_MINIGAME = 120    #In seconds ( or put a 60 times then minutes)

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
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()

#figure out how ot make this work over the internet