import asyncio
import time

SERVER_IP_ADRESS = '11.111.111.11'               #string   - Server public IP adress   #This is an example, not my actual ip, don't even try it :p
SERVER_PORT = 13723                            #must be the same as the Server   integer
SERVER_PASSWORD = ''                           #Unnecessary for test version

def pingServer( ToSend ) :
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)

        #print('Sending: %r' % message)
        start = time.time()
        writer.write(message.encode())

        data = await reader.read(100)
        end = time.time()
        recievedString = data.decode()
        #print('Received: %r' % data.decode())

        writer.close()
        totalTime = str(end - start)
        return( recievedString , totalTime )

    message = str(ToSend)
    loop = asyncio.get_event_loop()
    recievedString , totalTime = loop.run_until_complete(tcp_echo_client(message, loop))
    return( recievedString , totalTime )

while True :
    toSend = input('What do you want to send? - ')    
    if len( toSend ) == 0 :                     #cuz if u send nothing it will crash server
        toSend = '.'
    serverResponse , pingToServer = pingServer( toSend ) 
    print( 'Recieved: ' + serverResponse + ' from server in ' + pingToServer + ' seconds.' + '\n' )
