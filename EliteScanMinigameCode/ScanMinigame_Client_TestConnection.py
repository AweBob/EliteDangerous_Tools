import asyncio

SERVER_IP_ADRESS = '192.168.1.4'               #string   - Server external IP adress
SERVER_PORT = 13723                            #must be the same as the Server   integer

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection(SERVER_IP_ADRESS, SERVER_PORT,
                                                   loop=loop)

    print('Sending: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    writer.close()

while True :
    message = input('\n' + 'What do you want to send - ')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()

#Add way to detect if server is offline as oppose to crashing script if it's offline
