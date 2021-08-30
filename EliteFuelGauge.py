
#===========================================================================================================================================================================================================
#
# Python 3.8.6 (Although doesn't use any of the latest syntax so should work in most versions of Python 3)
# By: AweBob#6221 aka CMDR AweBob
# Log Parser is Only tested on windows (I am almost positive log files are handled differently on different systems)
#
# Intended to gauge feul during timelapses or other long durations in which you cannot simply look at your normal gauge in Elite
# Inspiration for this is that I almost ran out of feul during one of my timelapses in Elite that I did for my yt channel and wanted to prevent this from happening in the future
#
# Currently a non functional work in progress, once working command line I'll add tkinter support to it 
#
#===========================================================================================================================================================================================================

from EliteLogParserRewrite import getLogJson as getEliteLog
from time import time
from time import sleep 
from math import pow 
#import tkinter
#import logging

#===========================================================================================================================================================================================================

REFRESH_RATE_SECONDS = 60  #How often you want the gauge to refresh, 60 seconds is a solid baseline, for long timelapses longer is fine, I wouldn't go anything quicker then a few seconds as fuel drains relatively slowly in elite

#===========================================================================================================================================================================================================

def getFuelTankSize ( logJson ) :
    fuel = 0
    for logLine in reversed(logJson) :
        if logLine["event"] == 'LoadGame' :
            return(logLine["FuelCapacity"], True)
        elif logLine["event"]=='Loadout' :
            for module in logLine["Modules"] :
                if (module["Slot"]=='FuelTank') or ( ('Slot' in module["Slot"]) and ('Int_FuelTank' in module['Item']) )   : #If main fuel tank or an additional feul tank 
                    #module['Item'] #<- need to get tier number out of this and then use pow to get the actual feul amount 
                    pass

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getCurrentFuel ( logJson, fuelTankCapacity ) :                          
    for logLine in reversed(logJson) :
        if logLine["event"]=="ReservoirReplenished" :
            return(float(logLine["FuelMain"]) + float(logLine["FuelReservoir"]), True)
        elif logLine["event"]=="FSDJump" :
            return(float(logLine["FuelLevel"]), True) #Assuming resevoir is empty, maybe incorrect idk 
        elif logLine["event"]=="FuelScoop" :
            return(float(logLine["Total"]), True) #Assuming resevoir is empty, maybe incorrect idk 
        elif logLine["event"]=='LoadGame' :
            return(float(logLine["FuelLevel"]), True) #Assuming resevoir is empty, maybe incorrect idk 
        elif logLine["event"]=='RefuelAll' :
            return(float(fuelTankCapacity), True)
    return(0, False)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main () :
    #startTime = int(time())
    while True : #Continue until ended by error or python closing
        log = getEliteLog()
        capacity, found1 = getFuelTankSize(log)
        current, found2 = getCurrentFuel(log, capacity)
        if found1 and found2 : #If both worked ok 
            print(f"f{current}/{capacity}")
        else :
            print("error")
        sleep(REFRESH_RATE_SECONDS) 

#===========================================================================================================================================================================================================

if __name__ == "__main__" :
    main()

#===========================================================================================================================================================================================================

#Refrence code from EliteExplorationTool.py in this repo 

"""
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
"""

"""
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
"""

"""
def timelapse_infoCall () :
    maxFuel = fuelTankSize()
    currentFuel = get_currentFuel(maxFuel)
    try :
        percentFuelTank = (str(( currentFuel / maxFuel ) * 100) + '%')
    except :
        percentFuelTank = '100%'
    info_fuelList = [maxFuel, currentFuel, percentFuelTank]
    return(info_fuelList)
"""

#===========================================================================================================================================================================================================
