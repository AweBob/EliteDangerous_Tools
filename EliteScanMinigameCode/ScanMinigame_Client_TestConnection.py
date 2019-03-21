import asyncio

SERVER_IP_ADRESS = '11.111.111.11'               #string   - Server public IP adress   #This is an example, not my actual ip, don't even try it :p
SERVER_PORT = 13723                            #must be the same as the Server   integer
SERVER_PASSWORD = ''                           #Unnecessary for test version

def pingServer( ToSend ) :
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)

        #print('Sending: %r' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        recievedString = data.decode()
        #print('Received: %r' % data.decode())

        writer.close()
        return( recievedString )

    message = str(ToSend)
    loop = asyncio.get_event_loop()
    recievedString = loop.run_until_complete(tcp_echo_client(message, loop))
    return( recievedString )

while True :
    toSend = input('What do you want to send? - ')
    serverResponse = pingServer( toSend ) 
    print( serverResponse )
