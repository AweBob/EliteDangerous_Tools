
#THIS DOESN'T WORK SADLY
print( '\n' + 'IN ITS CURRENT STATE THIS DOESNT WORK, PROCEED WITH CAUTION' + '\n')

import pyautogui
from os import *
import os
from glob import *
import glob
import xml.etree.ElementTree as ET
import keyboard
import pyperclip 
import time

pyautogui.FAILSAFE = False # disables the fail-safe

print('If you run shaders that affect your galaxy map and/or galaxy map menu system this may not work. To fix this, retake the screenshots. This will only work on Windows as well.')
print('Libaries sucessfully imported. Script starting. Time is  ' + str(time.time()) )
print('This is recommended for use with ED:Pathinder and neutron and has been developed by: CMDR AweBob' + '\n')

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

def closeGalaxyMap () :
    for index in range(500) :
        time.sleep(0.01)
        exitButtonLocation = pyautogui.locateCenterOnScreen('exitButton.png') 
        if exitButtonLocation != None :
            break
    if exitButtonLocation != None :
        pyautogui.moveTo( exitButtonLocation )
        pyautogui.click() 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main () :
    bindOfGalaxyMap = checkBinds()
    ACTIVATION_HOTKEY = str(input('Enter hotkey to plot route -  '))
    while True :
        try :
            selectButtonFound = False
            if keyboard.is_pressed( ACTIVATION_HOTKEY ) == True :
                buttonLocation = None
                bindOfGalaxyMap = checkBinds()
                clipboard = pyperclip.paste()
                if len( clipboard ) != 0 :
                    pyautogui.press( bindOfGalaxyMap )
                    for index in range(500) :
                        time.sleep(0.01)
                        try :
                            print('w')
                            buttonLocation = pyautogui.locateCenterOnScreen('menuBar.png') 
                            break
                        except :
                            print('l')
                            pass
                    if buttonLocation != None :
                        pyautogui.moveTo( buttonLocation ) #move to the correct tab
                        pyautogui.click()
                    for index in range(500) :
                        time.sleep(0.01)
                        searchBarLocation = pyautogui.locateCenterOnScreen('searchBar.png') 
                        if searchBarLocation != None :
                            break
                    if searchBarLocation != None :
                        pyautogui.moveTo( searchBarLocation ) #select search bar
                        pyautogui.click()
                        pyautogui.typewrite( clipboard , interval=0.03 ) #type clipboard with a tiny wait between each charector
                        pyautogui.press('enter') #Do the search
                        for index in range(500) : #Will try and find it for slightly more than 5 seconds
                            time.sleep(0.01) #this allows the above to work
                            selectButton = pyautogui.locateCenterOnScreen('selectSystem.png') 
                            if selectButton != None :
                                selectButtonFound = True
                                break
                        if selectButtonFound == True :
                            pyautogui.moveTo( selectButton ) #select button
                            pyautogui.click() #click button
                            time.sleep(0.25)
                            closeGalaxyMap()
                            print('Sucessful run  ' + str(time.time()))
                        else :
                            print('System not found  ' + str(time.time()) )
                            closeGalaxyMap()
                    else :
                        print('Search bar cannot be found  ' +  str(time.time()) )
                        closeGalaxyMap()                        
                else :
                    print('Next system not in clipboard  ' + str(time.time()) )
                time.sleep(0.75)
        except :
            pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main()
