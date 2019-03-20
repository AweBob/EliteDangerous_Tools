import asyncio
import time

#===========================================================================================================================================================================================

print('Imported libraries Sucessfully:')
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ')

#===========================================================================================================================================================================================

def pingServer( ToSend ) :
    recievedString = ''
    async def tcp_echo_client(message, loop):
        reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                    loop=loop)

        #print('Sending: %r' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        global recievedString
        recievedString = data.decode()
        #print('Received: %r' % data.decode())

        writer.close()

    message = str(ToSend)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()
    return( recievedString )

#===========================================================================================================================================================================================

def main () :
    programRunning = True
    while programRunning == True :
        startTime = time.time()

        stringToSend = getInfoToSend(  )
        recievedString = pingServer ( stringToSend )
        updateUI ( recievedString )

        endTime = time.time()
        totalTime = endTime - startTime
        time.sleep( abs( 10 - totalTime )  )

#===========================================================================================================================================================================================

def getInfoToSend () :
    #ADD STUFF HERE
    stringToSend = ''
    return ( stringToSend )

#===========================================================================================================================================================================================

def updateUI ( receivedText ) :
    y = 69 #placeholder
    #update the user interface here

#===========================================================================================================================================================================================

main()

