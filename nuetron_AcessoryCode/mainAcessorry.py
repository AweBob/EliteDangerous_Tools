import pyautogui
from os import *
import os
from glob import *
import glob
import xml.etree.ElementTree as ET
import keyboard
import pyperclip 
import time
import mouse

pyautogui.FAILSAFE = False # disables the fail-safe

print('If you run shaders or a non 1920x1080 monitor for elite your gonna have to retake the screenshots. Future Update will fix this.')
print('Libaries sucessfully imported. Script starting. Time is  ' + str(time.time()) )
print('This is recommended for use with ED:Pathinder and neutron on Windows and maybe Mac and has been developed by: CMDR AweBob' + '\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def grabBind () :
    location = os.path.expanduser('~\AppData\Local\\frontier developments\elite dangerous\options\\bindings\*.binds')         #File path different for linux
    bindFilePath = glob.glob(location)
    if len(bindFilePath) == 0 :
        nothing = input('Bind file not found. Press enter to close - ')
        raise SystemExit

    bindFileName = str(bindFilePath[0])
    bindText = openBind( bindFileName )   #tree = 

    root = ET.fromstring( bindText )  #root = 
    bindsDictionary = { }
    for child in root :
        for grandChild in child :
            try :
                if grandChild.attrib['Key'] != '' :
                    if child.tag not in bindsDictionary.keys() :
                        bindsDictionary[child.tag] = [ [ grandChild.attrib['Key'] , grandChild.tag ] ]
                    else :
                        oldValue = bindsDictionary[child.tag]
                        oldValue.append( [ grandChild.attrib['Key'] , grandChild.tag ] )
                        bindsDictionary[child.tag] = oldValue
            except :
                pass

    return( bindsDictionary )

def openBind ( bindFileName ) :
    openText = open(bindFileName , O_RDONLY)
    importedBindText = read(openText , 9999999)
    close(openText)
    return( importedBindText )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def checkBinds () :
    try :
        binds = grabBind ()
        try :
            test = binds['GalaxyMapOpen'] #Errors here if no binds file found
            dirtySimplfied = binds['GalaxyMapOpen'][0][0]
            cutBind = dirtySimplfied.split('_')
            if cutBind[0] != 'Key' :
                nothing = input('It apears that the bind for open galaxy map isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
            else :
                actualBind = cutBind[1].lower()
                return(str(actualBind))
        except :
            nothing = input('Binds file found, but it apears open Galaxy Map isnt bound to anything. Press enter to close - ')
            raise SystemExit
    except :
        nothing = input('Cannot find binds file. Press enter to close - ')
        raise SystemExit

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def findImageAndClick ( imageToClick , loopAmount ) :
    if type(imageToClick) is str : #Confirm file name isn't some other format
        for i in range( int(loopAmount) ) :
            startTime = time.time()
            amount = 0
            for tupleThing in pyautogui.locateAllOnScreen( imageToClick )  : #OSError if image isn't in the directory --- if no matches are found it will skip the for loop, no errors
                amount = amount + 1
            if amount == 1 :
                pyautogui.moveTo( pyautogui.center( tupleThing ) ) #move to the correct tab
                pyautogui.click()
                return(True , 'Sucess')
            elif amount > 1 :
                return(False , 'Multiple found')
            #if it's less than one image wasn't found and it'll loop again, no need to do anything
            endTime = time.time()
            time.sleep( calcTimeToSleep(1 , startTime , endTime) )
    return(False , 'None found or Incorrect image file')

def calcTimeToSleep ( timeInSec , start , end ) :
    timeToSleep = int(timeInSec) - ( int(start) + int(end) )
    if timeToSleep > 0 :
        return(timeToSleep)
    elif timeToSleep <= 0 :
        return(0)
    else : #this is theoretically impossible, but ya never know
        return(0)
        
def pressKey ( key ) :
    for i in range(50) : #1/2 a second = .01 x 50
        keyboard.press(key)
        time.sleep(0.01)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main () :
    bindOfGalaxyMap = checkBinds()
    ACTIVATION_HOTKEY = str(input('Enter hotkey to plot route -  '))
    while True :
        try :
            if keyboard.is_pressed( ACTIVATION_HOTKEY ) == True :
                bindOfGalaxyMap = checkBinds()
                clipboard = pyperclip.paste() #Must run as admin for this to work, MUST, for some reason your clipboard is an admin only thing
                if len( clipboard ) != 0 :
                    pressKey( bindOfGalaxyMap ) #opens the galaxy map
                    time.sleep(0.25) #cuz game takes a quick sec to load here
                    status , additional = findImageAndClick('menuBar.png' , 5) 
                    if status != False :
                        time.sleep(0.1)
                        status , additional = findImageAndClick('searchBar.png' , 3)
                        if status == False : #if the first one can't be found, try to find this one
                            status , additional = findImageAndClick('searchBar2.png' , 3)
                        if status != False :
                            time.sleep(0.5)
                            keyboard.press('space') #focus in on the searchbar
                            time.sleep(0.5)
                            pyautogui.typewrite( clipboard , interval=0.03 ) #type clipboard with a tiny wait between each charector
                            #WORKS UNTIL HERE <><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><<><><><><><
                            pressKey('enter') #Do the search
                            #pyautogui.press('enter')
                            #keyboard.press('enter')
                            time.sleep(1) #Pre wait, even tho find image has a build in wait function
                            status , additional = findImageAndClick('selectSystem.png' , 45) 
                            if status != False :
                                status , additional = findImageAndClick('exitButton.png' , 5)
                                print('Sucessful run  ' + str(time.time()) + '  ' + clipboard )
                            else :
                                print('System not found or Route button not found  ' + str(time.time()) + '  ' + clipboard )
                                status , additional = findImageAndClick('exitButton.png' , 5)
                        else :
                            print('Search bar cannot be found  ' +  str(time.time()) + '  ' + clipboard )
                            status , additional = findImageAndClick('exitButton.png' , 5)
                    else :
                        print('Menu bar cannot be found  ' +  str(time.time()) + '  ' + clipboard + '  ' + str(bindOfGalaxyMap) )
                        status , additional = findImageAndClick('exitButton.png' , 5)    
                else :
                    print('Next system not in clipboard  ' + str(time.time()) )
                time.sleep(0.75)
        except :
            pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main()
