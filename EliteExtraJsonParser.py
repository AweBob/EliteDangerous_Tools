from os import *
import os
from glob import *
import glob
import json

EXTRA_JSON_FILE_NAMES = [ 'Cargo' , 'Market' , 'ModulesInfo' , 'Outfitting' , 'Shipyard' , 'Status' ]        #Not necessary, but good for reference

def ExtraJsonParserMain (  ) :
    location = os.path.expanduser('~\Saved Games\Frontier Developments\Elite Dangerous\*.json')               #Won't work for linux users - their thing is in a different file path
    jsonFiles = glob.glob(location)                                                                           #finds all files in that location, make into a list
    for eachFilePath in jsonFiles :
        fileTypeCharacters = eachFilePath[-7:][:-5]               #last 2 characters of name, enough to determine which file it is
        fileString = openFile( eachFilePath )
        jsonOutput = jsonCleanerAndConverter( fileString )
        if fileTypeCharacters=='go' :
            Cargo = jsonOutput
        elif fileTypeCharacters=='et' :
            Market = jsonOutput
        elif fileTypeCharacters=='fo' :
            ModulesInfo = jsonOutput
        elif fileTypeCharacters=='ng' :
            Outfitting = jsonOutput
        elif fileTypeCharacters=='rd' :
            Shipyard = jsonOutput
        elif fileTypeCharacters=='us' :
            Status = jsonOutput
    return( Cargo , Market , ModulesInfo , Outfitting , Shipyard , Status )


def openFile ( fileLocationAndName ) :
    openText = open(fileLocationAndName , O_RDONLY)
    importedFileText = read(openText , 9999999)
    close(openText)
    return( importedFileText )

def jsonCleanerAndConverter ( fileString ) :             
    continueLoop = True
    fileString3 = fileString
    while continueLoop==True :
        try :
            fileConverted = json.loads( fileString3 )
            continueLoop = False
            return( fileConverted )
        except ValueError as error :
            error = str(error)
            print(error)
            nums = ''
            for charector in error :
                if charector.isdigit()==True :
                    nums = nums + charector
            errorChar = nums[1:]
            lengthError = int(-1 * (len(errorChar)/2))
            errorChar = errorChar[:lengthError]
            errorChar = int(errorChar)
            fileString3 = fileCleaner( fileString3 , errorChar )

def fileCleaner ( dirtyText , errorPos ) :
    beginningPos = int(errorPos) - 1
    endingPos = int(errorPos) + 0
    cleanString = dirtyText[:beginningPos] + dirtyText[endingPos:]
    return( cleanString )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#EXAMPLES
#json_Cargo , json_Market , json_ModulesInfo , json_Outfitting , json_Shipyard , json_Status = ExtraJsonParserMain()      #this func outputs lists of events in each of these files, it is always in this order
#print(json_Cargo)                                           #prints entire Cargo file
#print(json_Cargo['Inventory'])                              #prints whats in the invenotry tag in the dictionary
#print(json_Cargo['Inventory'][0]['Name'])                   #prints name of first item in inventory in Cargo
#print(json_Outfitting)                                      #prints Outfitting file in its entirety
#print(json_Outfitting['StationName'])                       #prints value for station name key in outfitting file dictionary
#print(json_Outfitting['Items'][2]['Name'])                  #prints name of the second item in items in outfitting file

