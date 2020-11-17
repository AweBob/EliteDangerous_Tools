
#====================================================================================================================================

#Credit for this idea to CMDR Longman.P.J.
#All code by CMDR AweBob

#====================================================================================================================================

import requests #For grabbin from eddb and from elitebgs
import numpy as np #for distance calculation 

#====================================================================================================================================

class EddbSystem :
    def __init__(self, eddbSystemDictionary) :
        self.id = eddbSystemDictionary["id"]
        self.name = eddbSystemDictionary["name"]
        self.x = eddbSystemDictionary["x"]
        self.y = eddbSystemDictionary["y"]
        self.z = eddbSystemDictionary["z"]

    def getId(self) :
        return(self.id)
    def getName(self) :
        return(self.name)
    def getX(self) :
        return(self.x)
    def getY(self) :
        return(self.y)
    def getZ(self) :
        return(self.z)
    
    def getDistance(self, targetSystem) : 
        p1 = np.array([float(self.x), float(self.y), float(self.z)])
        p2 = np.array([float(targetSystem.getX()), float(targetSystem.getY()), float(targetSystem.getZ())])
        squared_dist = np.sum((p1-p2)**2, axis=0)
        dist = np.sqrt(squared_dist)
        return(dist)

    def getDistanceFromSol(self) :
        p1 = np.array([float(self.x), float(self.y), float(self.z)])
        p2 = np.array([0,0,0])
        squared_dist = np.sum((p1-p2)**2, axis=0)
        dist = np.sqrt(squared_dist)
        return(dist)

    def hasFourLuckyStates(self) :
        states = []
        systemInfo = requests.get( f"https://elitebgs.app/api/ebgs/v4/systems?name={self.name}"  ).json()["docs"]
        for bgsState in systemInfo :
            states.append( bgsState["name"] )
        ibe = False #investement/boom
        cle = False #civil liberty
        phe = False #public holiday
        ee = False #expansion
        pae = False #pirate attack #not used currently but if you wanted to experiment
        for state in states :
            if (state=="Boom" or state=="Investment"):
                ibe = True
            elif (state=="Civil Liberty"):
                cle = True
            elif (state=="Public Holiday"):
                phe = True
            elif (state=="Pirate Attack") :
                pae = True
            elif (state=="Expansion"):
                ee = True
        return(ibe and cle and ee and phe)

    def getStationsWithLuckyEconomy(self) :
        returningStations = []
        stationsList = requests.get( f"https://elitebgs.app/api/ebgs/v4/stations?eddbid={self.id}"  ).json()["docs"]
        for stationDict in stationsList :
            if stationDict["economy"]=="$economy_refinery;" or stationDict["economy"]=="$economy_hightech;" or stationDict["economy"]=="$economy_industrial;" or stationDict["economy"]=="$economy_tourism;" :  #Industrial, High Tech, Refinery or Tourism station enconomies required
                returningStations.append(BasicStation(self.name, stationDict["name"]))
        return(returningStations)

#====================================================================================================================================

class BasicStation :
    def __init__(self, sysName, statName) :
        self.sysName = sysName
        self.statName = statName
    def getSys(self) :
        return(self.sysName)
    def getStat(self) :
        return(self.getStat)

#====================================================================================================================================

def main() :
    input("Market Analysis - By: AweBob#6221 - Press enter to begin - ")

    print("Downloading eddb populated systems")
    rawEddbPopulatedSystems = requests.get( "https://eddb.io/archive/v6/systems_populated.json" ).json()
    
    print("Parsing Data")
    eddbSystems = []
    for rawEddbSystemDictionary in rawEddbPopulatedSystems :
        eddbSystems.append( EddbSystem(rawEddbSystemDictionary) )

    """
    print("Filtering Colonia Systems") #Not Tested
    for eddbSystem in eddbSystems :
        if eddbSystem.getDistanceFromSol() > 10000 :
            eddbSystems.pop(eddbSystem)
    """

    print("Processing Individual Systems\n")
    for eddbSystem in eddbSystems :
        if eddbSystem.hasFourLuckyStates() :
            for station in eddbSystem.getStationsWithLuckyEconomy() :
                print(f"{station.getSys()} - {station.getStat()} - {int(eddbSystem.getDistanceFromSol())}lys")

    print("\nDone")

#====================================================================================================================================

if __name__ == "__main__":
    main()

#====================================================================================================================================
