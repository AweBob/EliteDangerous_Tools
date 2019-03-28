import asyncio
import time
import json
import ast #testin

SERVER_IP_ADRESS = '192.168.1.4'               #string   - Server public IP adress   #This is an example, not my actual ip, don't even try it :p
SERVER_PORT = 13723                            #must be the same as the Server   integer
SERVER_PASSWORD = ''                           #Unnecessary for test version

def pingServer( ToSend ) :
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)

        start = time.time()
        writer.write( json.dumps( ToSend ).encode() ) #encoded

        data = await reader.read(1000)
        end = time.time()
        recievedStuff = ast.literal_eval( str( data.decode() ) )

        writer.close()
        totalTime = str(  (end - start) * 100 )
        return( recievedStuff , totalTime ) 

    loop = asyncio.get_event_loop()
    recievedStuff , totalTime = loop.run_until_complete(tcp_echo_client( ToSend , loop))
    return( recievedStuff , totalTime )

while True :
    toSend = []
    numOfThangs = int(input( '\n' + 'How many items do ya wanna send? - '))
    for i in range( numOfThangs ) :
        toSend.append( input('What do you want to send? - ') )

    if len( toSend ) != 0 :                     #cuz if u send nothing it will crash server
        serverResponse , pingToServer = pingServer( toSend ) 

        print( 'Recieved: ' + str(serverResponse) + ' from server in ' + str(pingToServer) + ' ms.' + '\n' )
        #for i in serverResponse :  #proof that this works
            #print(i)
