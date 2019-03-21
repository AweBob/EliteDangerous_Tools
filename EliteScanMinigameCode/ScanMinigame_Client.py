import asyncio
import time      #Going to be used to ensure how long loops have been goin for #Currently unused

#===========================================================================================================================================================================================

print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 19.374.922.82) - ')
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')

#===========================================================================================================================================================================================

def pingServer( ToSend ) :
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)

        writer.write(message.encode())

        data = await reader.read(100)
        recievedString = data.decode()

        writer.close()
        return( recievedString )

    message = str(ToSend)
    loop = asyncio.get_event_loop()
    recievedString = loop.run_until_complete(tcp_echo_client(message, loop))
    return( recievedString )

#===========================================================================================================================================================================================

print( pingServer( input('What do you want to send? - ') ) )

#REST OF CODE GOES HERE, few functions which will call the above stuff