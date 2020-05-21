
import requests #For pinging inara
import numpy as np

#from bs4 import BeautifulSoup #for sorting inara
#import json
#from EliteExtraJsonParser import CargoJsonParser #for reading Cargo.json

#================================Credit for this idea to CMDR Longman.P.J.===========================================================

def systemsThatMatchActiveStates (doStatusPrintout) : 
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    systems = []
    systemsCount = len(eddbGrab)
    if doStatusPrintout :
        print("Ping of " + str(systemsCount) + " systems sucessful.        ",end="")
    for count, system in enumerate(eddbGrab) : 
        ibe = False #investement/boom
        cle = False #civil liberty
        phe = False #public holiday
        ee = False #expansion
        minorFacts = system["minor_faction_presences"]
        for minorFact in minorFacts :
            activeStatesList = minorFact["active_states"]
            for state in activeStatesList :
                if (state["name"]=="Boom" or state["name"]=="Investment"):
                    ibe = True
                elif (state["name"]=="Civil Liberty"):
                    cle = True
                elif (state["name"]=="Public Holiday"):
                    phe = True
                elif (state["name"]=="Expansion"):
                    ee = True
        if (ibe and cle and phe and ee):
            systems.append( [system["name"], system["id"] ])
        if doStatusPrintout :
            print("\rCompleted " + str(count + 1) + "/" + str(systemsCount) + "                                                ",end="")
    if doStatusPrintout :
        print("") #get a newline
    return(systems, systemsCount)  #systems is [[sysname, sysid], [], []]  sysCount is the number of systems downloaded from eddb and analyzed for these checks

#====================================================================================================================================

def stationsThatMatchEconomy(systemEddbIds, doStatusPrintout) : #Industrial, High Tech, Refinery or Tourism station enconomies required
    
    return("placeholder") #return [systemName, stationName, systemId, stationId]

#====================================================================================================================================

def hasBeenUpdated(stationEddbIds) :

    return("placeholder") 

#====================================================================================================================================

def getSystemCordinatesFromId(systemEddbId) :
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    for systemDict in eddbGrab :
        if systemDict["id"]==systemEddbId :
            return (True, [systemDict["x"], systemDict["y"], systemDict["z"]])
    return (False,[]) 

def getSystemCordinatesFromName(systemName) :
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    for systemDict in eddbGrab :
        if systemDict["name"]==systemName :
            return (True, [systemDict["x"], systemDict["y"], systemDict["z"]])
    return (False,[]) 

def getSystemDistance(sys1CordinateList, sys2CordinateList) : #cordinate list looks like [xCord, yCord, zCord] all in integer form
    p1 = np.array(sys1CordinateList)
    p2 = np.array(sys2CordinateList)
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return(dist)

#====================================================================================================================================

def printMatchesToEconomyAndState() :
    rawSystemsList, systemsCount = systemsThatMatchActiveStates(False)
    systemEddbIds = []
    for rawSystem in rawSystemsList :
        systemEddbIds.append(rawSystem[1]) 
    rawStationsList = stationsThatMatchEconomy(systemEddbIds, False)
    print("After analyzing " + str(systemsCount) + " systems. The following are stations that match economy and active BGS states:")
    for rawStation in rawStationsList :
        print(str(rawStation)) 

#====================================================================================================================================

if __name__ == "__main__":
    #foo = "bar" #placeholder
    printMatchesToEconomyAndState()

#====================================================================================================================================
