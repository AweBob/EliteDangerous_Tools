
import requests #For pinging inara
import numpy as np #for distance calculation 

#from bs4 import BeautifulSoup 
#import json
#from EliteExtraJsonParser import CargoJsonParser 

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

def stationsThatMatchEconomy(rawSystemList) : 
    systemEddbIds = []
    for rawSystem in rawSystemList :
        systemEddbIds.append(rawSystem[1]) 
    eddbUrl = "https://eddb.io/archive/v6/stations.json"
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    stations = []
    #stationsCount = len(eddbGrab)
    for station in eddbGrab :
        if station["system_id"] in systemEddbIds :
            economiesList = station["economies"]
            for economy in economiesList :
                if economy=="Industrial" or economy=="High Tech" or economy=="Tourism" :  #Industrial, High Tech, Refinery or Tourism station enconomies required
                    stations.append([ station["name"], getSystemName(station["system_id"]), station["id"], station["system_id"] ]) #running get system name every time is ineficient asf but whatever lol
                    break
    return(stations) #[[stationame,sysname,statioid,sysid], [], []]

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

def getSystemNames(systemIdList) :
    systemNames = []
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    for system in eddbGrab :
        for inputId in systemIdList :
            if inputId==system["id"] :
                systemNames.append(system["name"])
    return(systemNames)

def getSystemName(sysId) :
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab = response.json()
    for system in eddbGrab :
        if sysId==system["id"] :
            return(system["name"])
    print("System " + str(sysId) + " does not exist.")
    return("DNE")

#====================================================================================================================================

def printMatchesToEconomyAndState() :
    rawSystemsList, systemsCount = systemsThatMatchActiveStates(False) #rawSystemList =  [[sysname, sysid], [], []]
    rawStationsList = stationsThatMatchEconomy(rawSystemsList) #rawStationsList = [[stationame,sysname,statioid,sysid], [], []]

    print("After analyzing " + str(systemsCount) + " populated systems. The following are stations that match economy and active BGS states:")
    for i in range(0,len(rawStationsList)) :
        print(rawStationsList[i][0] + ", " + rawStationsList[i][1])

#====================================================================================================================================

if __name__ == "__main__":
    printMatchesToEconomyAndState()

#====================================================================================================================================
