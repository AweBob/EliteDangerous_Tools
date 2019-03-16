from os import *
import os
from glob import *
import glob
import xml.etree.ElementTree as ET

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def grabBind () :
    location = os.path.expanduser('~\AppData\Local\\frontier developments\elite dangerous\options\\bindings\*.binds')         #File path different for linux
    bindFilePath = glob.glob(location)
    if len(bindFilePath) == 0 :
        nothing = input('No binds found!')

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def openBind ( bindFileName ) :
    openText = open(bindFileName , O_RDONLY)
    importedBindText = read(openText , 9999999)
    close(openText)
    return( importedBindText )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#EXAMPLES

#binds = grabBind ()                                       #Grabs dictionary
#print(binds)
#print(binds['SAAThirdPersonYawAxisRaw'])                   #prints list in a list of info for bind called that
#print(binds['ExplorationFSSRadioTuningX_Increase'][0])     #prints list of info for bind
#print(binds['CommanderCreator_Undo'][0][0])                #prints the bind key for that bind
#print(binds['ExplorationFSSZoomIn'])

#The only issue with this code is that it won't pickup "Modifier"s which are keybinds as well, this seems very difficult to figure out
