import asyncio #for server communications
import time #for knowing when event is over and printing error timestamps
import json #for converting text into lists for transfering lists through server

#===========================================================================================================================================================================================

#Server code for advanced scanners! Please run in a folder as some .txt files will be created durig the process of runnin this

print('Imported libraries Sucessfully:') #prints this line tto show that asyncio, time, and json have sucessfully imported.
SERVER_IP_ADRESS = input ('Type the external IP of hosting server(i.e. 99.374.922.82) - ')      
SERVER_PORT = int(input('Type port of Server(i.e. 13723) - '))
SERVER_PASSWORD = input('Type in server password(i.e. pLzWoRk123) - ') #this has to be the same between each client and the server, other than that doesn't matter
EVENT_START_TIME = int(input('What time will the event start? - '))               #Must be in unix time, if your unsure google it, it's seconds since 1 of January 1970
LENGTH_EVENT = int(input('How long do you want the game to last in seconds - '))   #in seconds
SCANS_TO_WIN = int(input('How many scans till the attackers win - '))        #number of scans people with scanners have to grab and drop off to win
PLAYER_TO_SCAN = input('What is the name of the CMDR people are trying to scan - ')  #Not case sensitive, do not use CMDR in there ie Luvarien , the person the clients are trying to scan

written = False #This is wether or not the final .txt file has been written to with final data
eventOverDueToScoreTime = 0 #if the event ends due to score, this is set to the time the event ended
startTime = time.time() #Time the code starts in unix time.

#===========================================================================================================================================================================================

def calculateResponse ( listRecieved ) : #function to find a response to the client and log the clients data
    try : #it could get to this point and be an empty list, so the exception is thrown
        if listRecieved[0] == SERVER_PASSWORD : #if password correct
            listToSend = [SERVER_PASSWORD ] #list to send will begin with the password
            if listRecieved[1] == 'testConnection' : #if ping type is a testConnection
                listToSend.extend([ 'connectionSucessful' , PLAYER_TO_SCAN , LENGTH_EVENT , EVENT_START_TIME , SCANS_TO_WIN ]) #add a bunch of basic data
            elif eventTimeStatus() == 0 : #event is on, this is everythin!
                try : #try cuz if lists are empty, big crash might happen
                    dataJunkReceived = listRecieved[2:] #remove password and type - leaves everythin else for the for loop below
                    for category in dataJunkReceived : #for each section of the information received
                        if category[0] == 'uploadData' : #if the categorys header is uploadedData
                            for index in range( int(category[1]) ) : #loop this the number of scans acheived, which is a number stored here
                                pointsScored.addData( category[2] ) #add the cmdr name for each time they've scored 
                        elif category[0] == 'deathData' : #if category header is deathData
                            del category[0] #remove the header
                            for deathDataBunch in category : #for each list of someone killed someone 
                                deathsData.addData( deathDataBunch  ) # in format; [killername , victim] #add it to the data
                        elif category[0] == 'killData' : #if category header is killData
                            del category[0] #remove header
                            for killDataBunch in category : #for list in the category 
                                killsData.addData( killDataBunch ) #in format #store the list
                        else : #shouldn't happen, except with modded clients 
                            print('Received wierd ping from a client: ' + str( time.time() )) #prints an error, but will continue calculating response
                    try : #in case the server recieves a ping that crashes it, it can be restarted
                        writeTempData() #Write to the temp file, purpose is so just in case the server crashes half way through, then all the data isn't lost
                    except :
                        print('Error in writing to temp. This is a rare one! (if its repeating tell error causing clients to restart as they are sending data in sync)') #this shouldn't happen
                        pass
                except :
                    pass 
                listToSend.extend([ 'dataLogged' , str(len(pointsScored.getData())) ]) #second variable is how many points have been scored    #adds a sucessful run message and send number of points scored so far
            elif eventTimeStatus() == 1 : #event hasn't started , don't log anything
                listToSend.extend([ 'eventHasntStarted' , EVENT_START_TIME , LENGTH_EVENT ]) #send back info about when event is starting and how long it will last
            elif eventTimeStatus() == 2 or eventTimeStatus() == 2.1 : #event is over, dont log anything
                listToSend.append('eventIsOver') #add that the event is over
                if eventTimeStatus() == 2 : #if it's over due to time
                    listToSend.append('dueToTime') #add that the event is over due to time (people with scanners have lost)
                elif eventTimeStatus() == 2.1 : #if it's over due to score
                    listToSend.append('dueToScore') #add over due to score  (people with scanners have won)
                    if eventOverDueToScoreTime == 0 : #if this variable hasn't been set
                        eventOverDueToScoreTime = int( time.time() ) #set time the event ended due to score to the current time
                listToSend.extend([ PLAYER_TO_SCAN , str(LENGTH_EVENT) , str(EVENT_START_TIME) , str(len(pointsScored.getData())) ]) #add a bunch of data about the event
                if written == False : #if the final file hasn't been written to
                    written = True #ensure this happens first so that other threads running this won't even start writing
                    try :
                        writeTempData() #write final data
                        print('\n' + 'Event over. Output file written.')
                    except :
                        written = False
                        print('\n' + 'Event is over. Error in writing to output file.')
                if ((time.time() / 60) - 10) > ((EVENT_START_TIME + LENGTH_EVENT) / 60 ) or ( eventOverDueToScoreTime > ( int( time.time() ) - 600 )  ) : #if event has been over for more than 10 minutes
                    print('Game has been over for more than 10 minutes. Closing Server.')
                    raise SystemExit    #close server
            else : #this is impossible unless you have a modded client - but just in case someone figures it out
                listToSend = ['thisIsImpossible'] #if they have the right password, but an invalid ping type, respond with this
        else : #if password is incorrect
            listToSend = ['.' , 'incorrectPassword'] #add this, with a . in the password spot
        return( listToSend ) #send back the list
    except : #if there is an error somewhere throughout the server processingg
        print('CALCULATION_ERROR: A ping was received and processed, however, it wasnt logged correctly. A basic response will be sent. Message received:   ' + str( listRecieved )) #print an error
        return(['.' , 'serverError']) #return a standard error message to the client

def writeTempData () : #write to temp file
    fileName = 'ServerOutput' + str( startTime ) + '.txt' #the name of the file is this
    tempFile = open( fileName ,'w+') #this is incase the server crashs and ya don't wanna lose data   #if it doesn't exsist open a file to write to
    tempFile.write('OUTPUT FROM SERVER' + '\n' ) #first line is a header
    tempFile.write('Current time: ' + '\n' + str( time.time() ) + '\n' + str( eventTimeStatus() ) + '\n' + '\n' ) #unix time - int based on time status so I don't have to do math manually  #add time info and server status
    tempFile.write('Standards: ' + '\n' + str(PLAYER_TO_SCAN) + '\n' + str(LENGTH_EVENT) + '\n' + str(EVENT_START_TIME) + '\n' + str(SCANS_TO_WIN) + '\n' + str(SERVER_PASSWORD) + '\n' + str(SERVER_PORT) + '\n' + str(SERVER_IP_ADRESS) + '\n' + '\n'  ) #refer to here for what where   #add a bunch of data defined at the top, mostly constants
    tempFile.write( 'KILLS LIST' + '\n') #header for kills data
    for d in killsData.getData() : #for each list in killsData
        tempFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n' )   #killername then victim  #write each line with killer then victim name      
    tempFile.write('\n' + 'DEATHS LIST' + '\n'  ) #header for deaths list
    for d in deathsData.getData() : #for item in deathsList
        tempFile.write(str(d[0]) + ' , ' + str(d[1]) + '\n')   #personWho died then their killers name #write each line with victim then killers name
    tempFile.write('\n' + 'POINTS SCORED LIST' + '\n'  )  #header for who scored points
    for d in pointsScored.getData() : #for item in pointsScored
        tempFile.write( str(d) + '\n' )    #person who scored a scan  #write the name of each person who has scored a point
    tempFile.write('\n' + '\n' + 'Event Time status ' + '\n' + str( eventTimeStatus() ) + '\n')  #write the current time status (this is a number, see the function for specifics)
    tempFile.close() #close the temp file

def eventTimeStatus () : #gets the status of event
    if len(pointsScored.getData()) >= SCANS_TO_WIN : #if event is over by score
        stat = 2.1 #event is over due to scored 
    else : #if event isn't over by score
        if time.time() >= EVENT_START_TIME and time.time() <= ( EVENT_START_TIME + LENGTH_EVENT ) : #if event is currently active
            stat = 0 #event is on
        elif time.time() < EVENT_START_TIME : #if event hasn't started
            stat = 1 #event hasn't started
        else :
            stat = 2 #event is over due to time
    return( stat ) #sends back the number representing the event status

class dataListStorage : #class for preserving data throughout the event
    def __init__ ( self ) : #on initial call
        self.data = [] #create an empty list
    def addData ( self , newData ) : #add data
        self.data.append( newData ) #adds data sent to self list
    def removeData ( self , toRemove ) : #remove an item
        try :
            self.data.remove( toRemove ) #try to remove it from the stored internal list
        except : #this happens if the one you wanna remove isn't in it
            pass #if it fails, do nothing
    def getData ( self ) : #getData
        return( self.data ) #sends back the internal list
    def getDataString ( self ) : #Unused - and is seemingly pointless, I'll remove this later, returns a string filled with each item in the list
        string = ''
        for item in self.data :
            string = string + ' ' + item 
        return( string )

killsData = dataListStorage() #Filled with lists like this [ killerName , victim ]
deathsData = dataListStorage() #Filled with lists like this [ cmdrWhoDied , personWhoKilledThem ]
pointsScored = dataListStorage() #This is one list filled with names of people who got points

#===========================================================================================================================================================================================

async def handle_echo(reader, writer): #Server function, this is openned everytime a client connects to the server
    try : #try, just incase the ping received is just a random scan across the internet and not something for the server to process
        data = await reader.read(1000) #grab the data sent, maxing out at 1000 digits, anything more will be cutoff. MY code will never send any more than that, so this will onyl save server power from random scans or ddos attempts
        message = json.loads( data )     #converts bytes format into a list: why/how this works idk, all I know is that it does
        addr = writer.get_extra_info('peername') #grabs the ip of client, might remove in final version as this is kind of a breach of privacy and I would feel bad
        listToSend = calculateResponse( message ) #run my calculate response function which will also log the data sent by the client
        writer.write( json.dumps( listToSend ).encode() ) #Sends off the response list that is converted to a string via json and then encoded to bytes
        await writer.drain() #Sends message in writer
        writer.close() #closes connection
        print('Received: ' + str(message) + '    Sending: ' + str( listToSend ) + '    Time: ' + str( time.time() ) + '    From: ' + str( addr ) ) #reads out data about the interaction
    except : #if the ping received isn't in list format this error is thrown and no response to the client will be issued
        print('PING_ERROR: A ping which failed to be read or failed to be converted to list format was received. No response will be issued. TimeStamp: ' + str(time.time())) #data about this error is printed

loop = asyncio.get_event_loop() #asyncio loop
coro = asyncio.start_server(handle_echo, SERVER_IP_ADRESS, SERVER_PORT, loop=loop) #asyncio start server
server = loop.run_until_complete(coro) #asyncio add server to loop
print('Serving on {}'.format(server.sockets[0].getsockname())) #print that it is running
loop.run_forever() #run the loop until manually shutdown.

#===========================================================================================================================================================================================
