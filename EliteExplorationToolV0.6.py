from os import *
import os
from glob import *
import glob
import json
from time import *
import time
from pygame import *
import pygame as p
import pygame
from pypresence import Presence
import win32api
import win32con
import win32gui
import screeninfo
from ctypes import windll, Structure, c_long, byref       #windows only I think....

#=======================================================================================================================================================================================================================
#=======================================THIS GRABS LOG FILE AND CONVERTS IT TO A GLOBAL VARIABLE=============================================================================================================
#=======================================================================================================================================================================================================================

def grabLog ( whichNum ) :                                                                                   #input the logFil you want, 0 for latest, 1 for the second latest, and so on
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.log')               #Won't work for linux users
    logFiles = glob.glob(location)
    logFilesNums = []
    for file in logFiles :
        nums = ''
        for charector in file :
            if charector.isdigit()==True :
                nums = nums + charector
        logFilesNums.append(nums)
    orderedNums = sorted(logFilesNums, key=int, reverse=True)
    specificNum = orderedNums[whichNum]

    for files in logFiles :
        nums = ''
        for charector in files :
            if charector.isdigit()==True :
                nums = nums + charector
        if nums==specificNum :
            latestFile = files
    return(latestFile)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logTransformer ( logFile ) :
    openLog = open(logFile,O_RDONLY)
    importedLog = read(openLog,9999999)
    close(openLog)

    log = str(importedLog)
    log = log[1:]
    log = log[1:]
    log = log.replace('\\n',', ')
    log = log.replace("\\'The Blaster\\'", " The Blaster")
    log = log[:-3]
    log = "[" + log + "]"
    return(logConverter( log ))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logConverter ( cleanLogFile ) :
    try:
        global convLog
        convLog = json.loads(cleanLogFile)
    except ValueError as error:
        error = str(error)
        nums = ''
        for charector in error :
            if charector.isdigit()==True :
                nums = nums + charector
        errorChar = nums[1:]
        lengthError = int(-1 * (len(errorChar)/2))
        errorChar = errorChar[:lengthError]
        errorChar = int(errorChar)
        logCleaner( cleanLogFile , errorChar )

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def logCleaner ( dirtyLogFile , errorPos ) :
    beginningPos = int(errorPos) - 1
    endingPos = int(errorPos) + 0
    cleanLogFile = dirtyLogFile[:beginningPos] + dirtyLogFile[endingPos:]
    logConverter( cleanLogFile )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#logTransformer(grabLog(0))     #updates convLog variable with latest log file
#print(convLog)                 #prints out the entire latest log file, probably 1000 to 1000000 charactoers lol

#=======================================================================================================================================================================================================================
#======================================EXTRA UTILITIES FOR GRABBING EVENTS AND DATA=====================================================================================================================================
#=======================================================================================================================================================================================================================

#def pullEvents ( whichLog ) :                     #this function can ruin loop if used incorrectly, disabled for now
    #logTransformer(grabLog(whichLog))
    #events = []
    #for lineNum in range(1,(len(convLog))+1) :
        #events.append(convLog[(-1*lineNum)]["event"])
    #logTransformer(grabLog(whichLog))
    #return(events)                                                      #This gets returned as a list of all events in logFile, whichLog is which log file to use

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#function to output list of change in events: output the full dictionaries that are new
def reset_findNewLinesOfLog ( ) :
    global findNewLinesOfLog_latest 
    findNewLinesOfLog_latest = []

def normal_findNewLinesOfLog ( ) :
    newEvents = []
    global findNewLinesOfLog_latest 
    for log_lines in convLog :
        if log_lines not in findNewLinesOfLog_latest :
            newEvents.append(log_lines)
    findNewLinesOfLog_latest = findNewLinesOfLog_latest + newEvents
    return(newEvents)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def pullEvent ( listOfEvents ) : #Includes choice of log file
    events = []
    for lineNum in range(1,(len(listOfEvents))+1) :
        events.append(listOfEvents[(-1*lineNum)]["event"])
    return(events)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def whatSystem () :
    current_System = ''
    for eventLine in reversed(convLog) :
        if eventLine["event"]=="FSDJump" :
            current_System = eventLine["StarSystem"]
            return (current_System)
    for eventLine in convLog :
        if eventLine["event"]=="Location" :
            current_System = eventLine["StarSystem"]
            return(current_System)
    current_System = 'error'
    return(current_System)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#=======================================================================================================================================================================================================================
#======================================Valuable Body Calculation Functions=====================================================================================================================================
#=======================================================================================================================================================================================================================

def get_eliteValueBody () :

    alreadyScannedPlanetsList = []
    body_earthLikeWorlds = []
    body_ammonia = []
    body_waterWorld = []
    body_terraformables = []

    system_now = whatSystem()
    newLines = convLog
    if len(newLines)>=1 :
        for lines in newLines :
            if lines["event"]=='Scan' :
                if lines["ScanType"]=="Detailed" or lines["ScanType"]=="AutoScan" :
                    if system_now in lines["BodyName"] :
                        if "PlanetClass" in lines :
                            if lines["PlanetClass"]=="Earthlike body" :
                                body_earthLikeWorlds.append(lines["BodyName"])
                            elif lines["PlanetClass"]=="Ammonia world" :
                                body_ammonia.append(lines["BodyName"])
                            elif lines["PlanetClass"]=="Water world" :
                                body_waterWorld.append(lines["BodyName"])
                            elif "TerraformState" in lines :
                                if lines["TerraformState"]!='' :
                                    body_terraformables.append(lines["BodyName"])

            elif lines["event"]=='SAAScanComplete' :
                bodyName = lines["BodyName"]
                alreadyScannedPlanetsList.append(bodyName)
    
    body_earthLikeWorlds = remove_previouslyMapped(alreadyScannedPlanetsList , body_earthLikeWorlds )
    body_ammonia = remove_previouslyMapped(alreadyScannedPlanetsList , body_ammonia )
    body_waterWorld = remove_previouslyMapped(alreadyScannedPlanetsList , body_waterWorld )
    body_terraformables = remove_previouslyMapped(alreadyScannedPlanetsList , body_terraformables )
    
    planet_earthLikeWorlds = remove_systemFromPlanet(system_now , body_earthLikeWorlds )
    planet_ammonia = remove_systemFromPlanet(system_now , body_ammonia )
    planet_waterWorld = remove_systemFromPlanet(system_now , body_waterWorld )
    planet_terraformables = remove_systemFromPlanet(system_now , body_terraformables )
    
    valuablePlanetDictionary = { "earthLikeWorlds": planet_earthLikeWorlds , "ammoniaWorlds": planet_ammonia , "waterWorlds": planet_waterWorld , "terraWorlds": planet_terraformables }
    return(valuablePlanetDictionary)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def remove_previouslyMapped (alreadyScanned , valuablePlanets) :
    noDupValuablePlanets = []
    for planet in valuablePlanets :
        if planet not in noDupValuablePlanets :
            noDupValuablePlanets.append(planet)
    
    for planet in noDupValuablePlanets :
        if planet in alreadyScanned :
            noDupValuablePlanets.remove(planet)
    return(noDupValuablePlanets)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def remove_systemFromPlanet (current_system , planetsList) :
    completePlanetsList = []
    for planet in planetsList :
        cleanPlanet = planet.replace(current_system , '')
        completePlanetsList.append(cleanPlanet)
    return(completePlanetsList)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#=======================================================================================================================================================================================================================
#======================================Timelapse mode functions=====================================================================================================================================
#=======================================================================================================================================================================================================================

def timelapse_infoCall () :
    maxFuel = fuelTankSize()
    currentFuel = get_currentFuel(maxFuel)
    try :
        percentFuelTank = (str(( currentFuel / maxFuel ) * 100) + '%')
    except :
        percentFuelTank = '100%'
    info_fuelList = [maxFuel, currentFuel, percentFuelTank]
    return(info_fuelList)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fuelTankSize () :
    for line in reversed(convLog) :
        if line["event"]=='LoadGame' :
            totalTons = line["FuelCapacity"]
            return(totalTons)
        elif line["event"]=='Loadout' :
            fueladdition = []
            OptionalInernal = 'Slot'
            OptIntFuelTank = 'Int_FuelTank'
            fuelTankSpecsDictionary = { '1':2, '2':4, '3':8, '4':16, '5':32, '6':64, '7':128 }
            totalTonsList = []
            totalTons = 0
            digitslist = []
            for module in line["Modules"] :
                if module["Slot"]=='FuelTank' :
                    fueladdition.append(module['Item'])
                elif OptionalInernal in module["Slot"] :
                    if OptIntFuelTank in module['Item'] :
                        fueladdition.append(module['Item'])
            for longindividualmodule in fueladdition :
                longindividualmodule = longindividualmodule[:-1]
                for digits in longindividualmodule :
                    if digits=='1' or digits=='2' or digits=='3'  or digits=='4'  or digits=='5'  or digits=='6' or digits=='7' :
                        digitslist.append(digits)
            for value in digitslist :
                totalTonsList.append(fuelTankSpecsDictionary[value])
            for value in totalTonsList :
                totalTons = totalTons + value
            return(totalTons)
    return(1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_currentFuel (fuelTankFull) :                          
    for line in reversed(convLog) :
        if line["event"]=="ReservoirReplenished" :
            fuelMain = line["FuelMain"]
            fuelReso = line["FuelReservoir"]
            totalFuel = int(fuelMain) + int(fuelReso)
            return(totalFuel)
        elif line["event"]=="FSDJump" :
            fuelMain = line["FuelLevel"]
            fuelReso = 0
            totalFuel = int(fuelMain) + int(fuelReso)
            return(totalFuel)
        elif line["event"]=="FuelScoop" :
            fuelMain = line["Total"]
            fuelReso = 0
            totalFuel = int(fuelMain) + int(fuelReso)
            return(totalFuel)
        elif line["event"]=='LoadGame' :
            fuelMain = line["FuelLevel"]
            fuelReso = 0
            totalFuel = int(fuelMain) + int(fuelReso)
            return(totalFuel)
        elif line["event"]=='RefuelAll' :
            totalFuel = fuelTankFull
            return(totalFuel)
    return(0)


#=======================================================================================================================================================================================================================
#====================================USER INTERFACE FUNCTIONS========================================================================================================================================
#=======================================================================================================================================================================================================================

def interface_run () :
    reset_findNewLinesOfLog()                                     #Reset global variable for 
    init()                                                        #initialize pygame
    statusLoop = True
    white = (255,255,255)
    black = (0,0,0)      
    screen = display.set_mode([400, 500])                          #build window
    p.display.set_caption('ED Exploration Tool - AweBob')
    discordOnline = False
    RPC = 'None'

    while statusLoop==True :
        screen.fill(black)                                         #Set screen background
        logTransformer(grabLog(0))                                 #Update variable convLog
        for event in p.event.get() :                               #check events
            if event.type==p.QUIT :                                #if X button is clicked
                statusLoop = False
            elif event.type == p.MOUSEBUTTONUP :                     #if a mouse button is clicked
                interface_mouseClick ( p.mouse.get_pos() )         #Call function to process clicks

        interface_drawText('ED Exploration Tool', 200 , 20 , screen, 30, (66, 244, 235))         #Title

        fuelList = timelapse_infoCall()
        fuelPercent = fuelList[2]
        interface_drawText(fuelPercent , 200 , 75 , screen, 20, (204, 115, 53))                 #Fuel percent

        yourSolarSystem = whatSystem()
        interface_drawText(yourSolarSystem , 200 , 125 , screen, 20, (66, 206, 87))             #Curent system
        
        lastEvents = calculateLastEvents ()
        interface_drawText(lastEvents[0] , 200 , 175 , screen, 20, (183, 45, 59))             #last log
        interface_drawText(lastEvents[1] , 200 , 200 , screen, 20, (183, 45, 59))             #second last log
        interface_drawText(lastEvents[2] , 200 , 225 , screen, 20, (183, 45, 59))             #third last log

        pilotName = getCMDRName()
        pilotNameRefined = 'CMDR ' + pilotName
        interface_drawText( pilotNameRefined , 200 , 50 , screen , 13 , (191, 42, 211) )      #Cmdr name

        valueableBodies = get_eliteValueBody ()
        #print(str(valueableBodies))                                                                                 #HERE FOR TESTING PURPOSES
        formattedInfo_allPlanets = bodyFormatter(200, 265, valueableBodies)                                         
        for planet in formattedInfo_allPlanets :
            interface_drawText(planet[0], planet[2], planet[1], screen, 18, planet[3])          #Valuable planets

        pygame.draw.rect(screen, (50, 193, 162) , (350 , 475 , 45 , 20 ), 0 )                       
        interface_drawText ('Overlay' , 372 , 485 , screen, 10 , (0, 0, 0) )                         #overlay button

        shipName = getShipName()
        discordOnline , RPC = discordUpdate ( discordOnline , yourSolarSystem , shipName , RPC )

        p.display.update()                                       #Updates pygame

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def overlayWindow (  ) :   #Show valuable bodies exclusively in overlay, update discord rpc as well 
    pygame.quit()
    RPC = 'None'
    discordOnline = False
    pygame.init()
    overlayLoop = True
    black = (0, 0, 0)

    Xsize , Ysize = getMainMonitorRez()                                        #get monitor resolution and create window below
    windowXsize , windowYsize , Xlocation , Ylocation = calcWindowSize( Xsize , Ysize )     
    overlay = pygame.display.set_mode( ( ( int(windowXsize) - 1) , (int(windowYsize) - 1)  ), pygame.NOFRAME )

    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (Xlocation , Ylocation )      #Move display to location below
    overlay = pygame.display.set_mode( (int(windowXsize) , int(windowYsize)) , pygame.NOFRAME)                    

    invis = (255, 0, 128)  # Transparency color is this RGB code              #Set window transparency color below
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*invis), 0, win32con.LWA_COLORKEY)

    onTop(pygame.display.get_wm_info()['window'])    #Make it stay on top

    while overlayLoop==True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:        #Event handler, this is necessary
                overlayLoop = False

        overlay.fill(invis)                              # Transparent background
        logTransformer(grabLog(0))                       #Update variable convLog

        yourSolarSystem = whatSystem()
        shipName = getShipName()
        valueableBodies = get_eliteValueBody ()
        formattedValueBodies = formatOverlayBodies ( valueableBodies , windowXsize , windowYsize )                                 #THIS SIN'T DONE - might be done, needs more testing
        #print( str( formattedValueBodies ) )                                                                                      #HERE FOR TESTING
        for planetList in formattedValueBodies :                                                                                   #This for loop is used to print info from formattedValueBodies
            interface_drawText( planetList[0] , planetList[1] , planetList[2] , overlay, planetList[3], planetList[4] )            

        discordOnline , RPC = discordUpdate ( discordOnline , yourSolarSystem , shipName , RPC )
        p.display.update()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def formatOverlayBodies ( bodiesDictionary , windowX , windowY ) :   #THIS SIN'T DONE 
    planetsBigList = []
    fontSize = int((windowX * windowY) / 6000) 
    
    #Goal of this is to start top left (row1,column1) then go down and then left to right with that top to bottom pattern
    rowCounter = 0
    columnCounter = 1
    row1 = int((windowY / 3) * 1)
    row2 = int((windowY / 3) * 2)
    column1 = int((windowX / 24 ) * 1)
    column2 = int((windowX / 24 ) * 2)
    column3 = int((windowX / 24 ) * 3)
    column4 = int((windowX / 24 ) * 4)
    column5 = int((windowX / 24 ) * 5)

    for planets in bodiesDictionary['earthLikeWorlds'] :
        color = (7, 150, 100)
        if rowCounter % 2 == 0 : #if even
            yCord = row1
        elif rowCounter % 2 ==1 :   #if odd
            yCord = row2
            columnCounter = columnCounter + 1
        if columnCounter == 1 :
            xCord = column1
        elif columnCounter == 2 :
            xCord = column2
        elif columnCounter == 3 :
            xCord = column3
        elif columnCounter == 4 :
            xCord = column4
        elif columnCounter == 5 :
            xCord = column5
        rowCounter = rowCounter + 1
        planetList = [planets,xCord,yCord,fontSize,color]
        planetsBigList.append(planetList)
        
    for planets in bodiesDictionary['ammoniaWorlds'] :
        color = (229, 229, 16)
        if rowCounter % 2 == 0 : #if even
            yCord = row1
        elif rowCounter % 2 ==1 :   #if odd
            yCord = row2
            columnCounter = columnCounter + 1
        if columnCounter == 1 :
            xCord = column1
        elif columnCounter == 2 :
            xCord = column2
        elif columnCounter == 3 :
            xCord = column3
        elif columnCounter == 4 :
            xCord = column4
        elif columnCounter == 5 :
            xCord = column5
        rowCounter = rowCounter + 1
        planetList = [planets,xCord,yCord,fontSize,color]
        planetsBigList.append(planetList)

    for planets in bodiesDictionary['waterWorlds'] :
        color = (16, 72, 229)
        if rowCounter % 2 == 0 : #if even
            yCord = row1
        elif rowCounter % 2 ==1 :   #if odd
            yCord = row2
            columnCounter = columnCounter + 1
        if columnCounter == 1 :
            xCord = column1
        elif columnCounter == 2 :
            xCord = column2
        elif columnCounter == 3 :
            xCord = column3
        elif columnCounter == 4 :
            xCord = column4
        elif columnCounter == 5 :
            xCord = column5
        rowCounter = rowCounter + 1
        planetList = [planets,xCord,yCord,fontSize,color]
        planetsBigList.append(planetList)

    for planets in bodiesDictionary['terraWorlds'] :
        color = (173, 26, 10) 
        if rowCounter % 2 == 0 : #if even
            yCord = row1
        elif rowCounter % 2 ==1 :   #if odd
            yCord = row2
            columnCounter = columnCounter + 1
        if columnCounter == 1 :
            xCord = column1
        elif columnCounter == 2 :
            xCord = column2
        elif columnCounter == 3 :
            xCord = column3
        elif columnCounter == 4 :
            xCord = column4
        elif columnCounter == 5 :
            xCord = column5
        rowCounter = rowCounter + 1
        planetList = [planets,xCord,yCord,fontSize,color]
        planetsBigList.append(planetList)

    return ( planetsBigList )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def calcWindowSize ( monitorXsize , monitorYsize ) :                          
    windowXsize = int(monitorXsize) / 2
    windowYsize = int(monitorYsize) / 9
    Xlocation = int(monitorXsize) / 4
    Ylocation = 0                                            #location is based on from top left of screen, being +x +y for os.environ formula
    return( windowXsize , windowYsize , Xlocation , Ylocation )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getMainMonitorRez () :
    mon = screeninfo.get_monitors()[0]
    numsAndInfo = ''
    for character in str(mon) :
        if character=='x' or character=='+' or character=='-' or character.isdigit()==True :
            numsAndInfo = numsAndInfo + character
    Dirty_head , Useless_sep , Useless_tail = numsAndInfo.partition('+')    
    Xcord , Useless_sep , Ycord = Dirty_head.partition('x')
    return ( Xcord , Ycord )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def discordUpdate( discordOnline , yourSolarSystem , shipName , RPC ) :
    if discordOnline==True :
        try :
            RPC.update( details= yourSolarSystem , state= shipName )    #Attempts to update
        except :
            discordOnline = False      #If update errors, send back, discord online false
    else :
        try :
            discord_clientID = '554387312486907918'   #discord id - this is constant for this application (says client id, but it's really application id)
            RPC = Presence(discord_clientID)  # Initialize the Presence class for discord
            RPC.connect()                     # Start the handshake loop
            discordOnline = True              #If the above works it sets discordOnline to true
        except :
            discordOnline = False              #If it fails return it failed
    return( discordOnline , RPC )                #sends back RPC data and if discord sucessfully updated or not

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def interface_mouseClick ( mousePos ) :                      
    mouseX = mousePos[0]
    mouseY = mousePos[1]
    #Overlay button tuple (350 , 475 , 45 , 20 ) = ( x , y , width , height ) stats from top left, +x and +y is screen
    if mouseX >= 350 and mouseX <= 395 :
        if mouseY >= 475 and mouseY <= 495 :
            print('Overlay button clicked. Openning Overlay.' + '\n' + 'To close program, close this terminal.')
            overlayWindow ()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def interface_drawText (importedText , locationX , locationY , screen, size, color ) :          #screen is for "window", its the thing initialzed at the top - used in core loop multiple times
    font = p.font.SysFont("freesans", size)
    text = font.render(importedText, True, color)
    screen.blit(text, (locationX - text.get_width() // 2, locationY - text.get_height() // 2))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def bodyFormatter (centralX, startY, bodiesDictionary) :
    yCurrent = startY
    xCurrent = centralX
    planetsBigList = []
    for planet in bodiesDictionary['earthLikeWorlds'] :
        color = (7, 150, 100)
        yCord = yCurrent
        xCord = xCurrent
        yCurrent = yCurrent + 25
        planetList = [planet,yCord,xCord,color]
        planetsBigList.append(planetList)
    for planet in bodiesDictionary['ammoniaWorlds'] :
        color = (229, 229, 16)
        yCord = yCurrent
        xCord = xCurrent
        yCurrent = yCurrent + 25
        planetList = [planet,yCord,xCord,color]
        planetsBigList.append(planetList)
    for planet in bodiesDictionary['waterWorlds'] :
        color = (16, 72, 229)
        yCord = yCurrent
        xCord = xCurrent
        yCurrent = yCurrent + 25
        planetList = [planet,yCord,xCord,color]
        planetsBigList.append(planetList)
    for planet in bodiesDictionary['terraWorlds'] :
        color = (173, 26, 10)
        yCord = yCurrent
        xCord = xCurrent
        yCurrent = yCurrent + 25
        planetList = [planet,yCord,xCord,color]
        planetsBigList.append(planetList)

    return(planetsBigList)        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def calculateLastEvents () :
    allEvents = pullEvent( convLog )
    lastEvents = allEvents[:3]
    return(lastEvents)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getShipName () :
    for line in reversed(convLog) :
        try :
            shipName = line['ShipName'] 
            return( shipName )
        except :
            pass
    return('Loading...')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getCMDRName () :
    for line in convLog :
        if line['event']=='Commander' :
            cmdrName = line['Name']
            return(cmdrName)
    return('Loading...')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RECT(Structure):       #Class to assist function below
    _fields_ = [
    ('left',    c_long),
    ('top',     c_long),
    ('right',   c_long),
    ('bottom',  c_long),
    ]
    def width(self):  return self.right  - self.left
    def height(self): return self.bottom - self.top


def onTop(window):                                        #Moves sent window to "always on top" mode
    SetWindowPos = windll.user32.SetWindowPos
    GetWindowRect = windll.user32.GetWindowRect
    rc = RECT()
    GetWindowRect(window, byref(rc))
    SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def isEliteRunningQuestionMark () :             #Checks if the game is running. Might not work if game crashed on last shutdown
    if convLog[-1]['event']=='Shutdown' :
        return(False)
    else :
        return(True)

#=======================================================================================================================================================================================================================
#====================================STUFF FOR RUNNING AND TESTING ABOVE FUNCIONS========================================================================================================================================
#=======================================================================================================================================================================================================================

def start () :
    try :
        print('Libaries Imported' + '\n' + 'Opening UI' + '\n' + 'To close overlay while its running close this terminal window' + '\n' + 'Any bugs please report on github, Thank You!')
        interface_run()
    except Exception as error :
        nothing = input('ERROR: ' + '\n \n' + str(error) + '\n' + str(error.args) + '\n \n' + 'Report this issue to GitHub to help me resolve this!' + '\n' + 'Thank You, press Enter to close!' + '\n')

#logTransformer(grabLog(0))
#reset_findNewLinesOfLog()
#interface_run()
start () 



#Notes to myself(aka things to work on):
    #Check if overlay is working, and check for other computers

    #ISSUE: Exploration thing doesn't clear thing after surface scan sometimes, rarely tho
    #ISSUE: program closes when starting (aka starting a new log file) This might have been fixed, test it
    #SUGESTION: Add discord rpc ability to track how long you've been flying (look at latest log file, get startup timestamp, use that number) see my bookmarks for more info
    #SUGESTION: Make discord rpc information toggleable in case people don't want foes to see their location
    