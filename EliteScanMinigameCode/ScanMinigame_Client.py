import asyncio

#ROLE_IN_MINIGAME = 'Attacker'    # 'Attacker', 'Defender' , or 'ScannedGuy'

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
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