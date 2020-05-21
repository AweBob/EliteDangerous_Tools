
#from EliteExtraJsonParser import CargoJsonParser #for reading Cargo.json
import requests #For pinging inara
#from bs4 import BeautifulSoup #for sorting inara
#import json

#====================================================================================================================================
#================================Credit for this idea to CMDR Longman.P.J.===========================================================
#====================================================================================================================================

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
            systems.append( [system["name"], system["x"], system["y"], system["z"] ])
        if doStatusPrintout :
            print("\rCompleted " + str(count + 1) + "/" + str(systemsCount) + "                                                ",end="")
    print("") #get a newline
    return(systems)

#====================================================================================================================================

sysnames = ""
for systemList in systemsThatMatchActiveStates(True) :
    sysnames = sysnames + systemList[0] + ", "

print(sysnames)

#====================================================================================================================================
