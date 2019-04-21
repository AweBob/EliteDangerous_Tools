import pyautogui
from os import *
import os
from glob import *
import glob
import xml.etree.ElementTree as ET
import keyboard
import pyperclip 
import time
import win32gui

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
            GALAXYMAP = None
            for i in binds['GalaxyMapOpen'] : 
                dirtySimplfied = i[0] 
                cutBind = dirtySimplfied.split('_')
                if cutBind[0] == 'Key' :
                    actualBind = cutBind[1].lower()
                    GALAXYMAP = str(actualBind)
                    break
            if GALAXYMAP == None :
                nothing = input('It apears that the bind for open galaxy map isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
        except :
            nothing = input('Binds file found, but it apears open Galaxy Map isnt bound to anything. Press enter to close - ')
            raise SystemExit

        try :
            UISELECT = None
            for i in binds['UI_Select'] : 
                dirtySimplfied = i[0] 
                cutBind = dirtySimplfied.split('_')
                if cutBind[0] == 'Key' :
                    actualBind = cutBind[1].lower()
                    UISELECT = str(actualBind)
                    break
            if UISELECT == None :
                nothing = input('It apears that the bind for ui select isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
        except :
            nothing = input('Binds file found, but it apears ui select isnt bound to anything. Press enter to close - ')
            raise SystemExit 

        try :
            NEXTPANELTAB = None
            for i in binds['CycleNextPanel'] :
                dirtySimplfied = i[0] 
                cutBind = dirtySimplfied.split('_')
                if cutBind[0] == 'Key' :
                    actualBind = cutBind[1].lower()
                    NEXTPANELTAB = str(actualBind)
                    break
            if NEXTPANELTAB == None :
                nothing = input('It apears that the bind for next panel tab isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
        except :
            nothing = input('Binds file found, but it apears next panel tab isnt bound to anything. Press enter to close - ')
            raise SystemExit 

        try :
            UIRIGHT = None
            for i in binds['UI_Right'] :
                dirtySimplfied = i[0] 
                cutBind = dirtySimplfied.split('_')
                if cutBind[0] == 'Key' :
                    actualBind = cutBind[1].lower()
                    UIRIGHT = str(actualBind)
                    break
            if UIRIGHT == None :
                nothing = input('It apears that the bind for ui right isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
        except :
            nothing = input('Binds file found, but it apears ui right isnt bound to anything. Press enter to close - ')
            raise SystemExit 

        try :
            UIBACK = None
            for i in binds['UI_Back'] :
                dirtySimplfied = i[0] 
                cutBind = dirtySimplfied.split('_')
                if cutBind[0] == 'Key' :
                    actualBind = cutBind[1].lower()
                    UIBACK = str(actualBind)
                    break
            if UIBACK == None :
                nothing = input('It apears that the bind for ui back isnt bound to a keyboard key. Press enter to close - ')
                raise SystemExit
        except :
            nothing = input('Binds file found, but it apears ui back isnt bound to anything. Press enter to close - ')
            raise SystemExit 

        return(GALAXYMAP , UISELECT , NEXTPANELTAB , UIRIGHT , UIBACK)

    except :
        nothing = input('Cannot find binds file. Press enter to close - ')
        raise SystemExit

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def findImageAndClick ( imageToClick , loopAmount , ifClick ) :
    if type(imageToClick) is str : #Confirm file name isn't some other format
        for i in range( int(loopAmount) ) :
            startTime = time.time()
            amount = 0
            for tupleThing in pyautogui.locateAllOnScreen( imageToClick )  : #OSError if image isn't in the directory --- if no matches are found it will skip the for loop, no errors
                amount = amount + 1
            if amount == 1 :
                if ifClick == True :
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
        
def pressKey ( key , length ) : 
    for i in range(length) : #1/2 a second = .01 x 50
        try :
            keyboard.press(key)
        except :
            nothing = input('Your thing bound to ' + str(key) + ' isnt accepted by this, please change it and try again - ')
            raise SystemExit
        time.sleep(0.01)
    keyboard.release(key)

def waitTillFound ( imageName , secsTillQuit ) :
    done = False
    start = time.time()
    timeToQuit = start + secsTillQuit
    while done == False :
        status , details = findImageAndClick(imageName , 1 , False)
        if status == True :
            done = True
        if time.time() > timeToQuit :
            done = True
    #when this finishes it'll go back to main

def pasteClipboard() : #USELESS - for some reason elite dangerous blocks this, why, idk
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')

def convertedTime () :
    try :
        current = time.strftime("%H:%M:%S",time.localtime(int(time.time())))
    except :
        current = str(time.time())
    return(current)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ensure that  nothing else is overlapping "NEXTPANELTAB" in the galaxy map
def main () :
    GALAXYMAP , UISELECT , NEXTPANELTAB , UIRIGHT , UIBACK = checkBinds()
    ACTIVATION_HOTKEY = str(input('Enter hotkey to plot route -  '))
    while True :
        try :
            if keyboard.is_pressed( ACTIVATION_HOTKEY ) == True :
                #print(str(win32gui.GetWindowText (win32gui.GetForegroundWindow())))
                if win32gui.GetWindowText (win32gui.GetForegroundWindow()) == 'Elite - Dangerous (CLIENT)' :
                    GALAXYMAP , UISELECT , NEXTPANELTAB , UIRIGHT , UIBACK = checkBinds()
                    clipboard = pyperclip.paste() #MUST run as admin or this won't work
                    if len( clipboard ) != 0 :
                        pressKey( GALAXYMAP , 50 ) #opens the galaxy map
                        waitTillFound('menuBar.png' , 20 )
                        pressKey( NEXTPANELTAB , 50 )
                        time.sleep(0.1)
                        keyboard.press(UISELECT)
                        time.sleep(0.1)
                        keyboard.release(UISELECT)
                        pyautogui.typewrite(pyperclip.paste().lower())
                        time.sleep(0.03)
                        keyboard.press('enter')
                        time.sleep(0.25)
                        keyboard.release('enter')
                        waitTillFound('routePloterAboveSystemUI.png' , 20) 
                        pressKey(UIRIGHT , 25)
                        time.sleep(0.1)
                        pressKey(UISELECT , 100)
                        time.sleep(0.1)
                        pressKey(UIBACK , 25) #test if this closes galmap
                        print('Sucessful run at ' + convertedTime() + ' with system ' + str(pyperclip.paste()) )
                    else :
                        print('Next system not in clipboard or you didnt run as admin at time ' + convertedTime() )
                else :
                    print('Hotkey was pressed, but elite isnt the active window at ' + convertedTime() )
                time.sleep(0.75) #prevent hotkey spamming accidentally
        except :
            pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

main()
