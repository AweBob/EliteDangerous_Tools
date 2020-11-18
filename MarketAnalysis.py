
import requests #For apis
import numpy as np #for distance calculation 
import time #For timing how long all this junk takes

#If you get errors on the above 2 things run: 
# py -m pip install requests
# py -m pip install numpy

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#================================Credit for this idea to CMDR Longman.P.J.===========================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

#This works for sure and is quick, but not very clean code

def systemsThatMatchActiveStates (doStatusPrintout, eddbGrab) :
    systems = []
    systemsCount = len(eddbGrab)
    if doStatusPrintout :
        print("Ping of " + str(systemsCount) + " systems sucessful.        ",end="")
    for count, system in enumerate(eddbGrab) : 
        ibe = False #investement/boom
        cle = False #civil liberty
        phe = False #public holiday
        ee = False #expansion
        pae = False #pirate attack
        for state in system["states"] :
            if (state["name"]=="Boom" or state["name"]=="Investment"):
                ibe = True
            elif (state["name"]=="Civil Liberty"):
                cle = True
            elif (state["name"]=="Public Holiday"):
                phe = True
            elif (state["name"]=="Pirate Attack") :
                pae = True
            elif (state["name"]=="Expansion"):
                ee = True
        if (ibe and cle and ee and phe):
            systems.append( [system["name"], system["id"] ])
        if doStatusPrintout :
            print("\rCompleted " + str(count + 1) + "/" + str(systemsCount) + "                                                ",end="")
    if doStatusPrintout :
        print("") #get a newline
    return(systems, systemsCount)  #systems is [[sysname, sysid], [], []]  sysCount is the number of systems downloaded from eddb and analyzed for these checks

def stationsThatMatchEconomy (rawSystemList, eddbGrab, eddbGrabSys) : 
    systemEddbIds = []
    for rawSystem in rawSystemList :
        systemEddbIds.append(rawSystem[1]) 
    stations = []
    for station in eddbGrab :
        if station["system_id"] in systemEddbIds :
            economiesList = station["economies"]
            for economy in economiesList :
                if economy=="Industrial" or economy=="High Tech" or economy=="Tourism" :  #Industrial, High Tech, Refinery or Tourism station enconomies required
                    stations.append([ station["name"], getSystemName(station["system_id"], eddbGrabSys), station["id"], station["system_id"] ]) #running get system name every time is ineficient asf but whatever lol
                    break
    return(stations) #[[stationame,sysname,statioid,sysid], [], []]

def getSystemName(sysId, eddbGrab) : 
    for system in eddbGrab :
        if sysId==system["id"] :
            return(system["name"])
    print("System " + str(sysId) + " does not exist.")
    return("DNE")

def doEddbPings() :
    eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
    response = requests.get(eddbUrl)  
    eddbGrab1 = response.json()
    eddbUrl = "https://eddb.io/archive/v6/stations.json"
    response = requests.get(eddbUrl)  
    eddbGrab2 = response.json()
    return(eddbGrab1, eddbGrab2)

def marketAnalysis1 () :
    eddbSystems, eddbStations = doEddbPings()
    rawSystemsList, systemsCount = systemsThatMatchActiveStates(False, eddbSystems) #rawSystemList =  [[sysname, sysid], [], []]
    rawStationsList = stationsThatMatchEconomy(rawSystemsList, eddbStations, eddbSystems) #rawStationsList = [[stationame,sysname,statioid,sysid], [], []]
    print("\nAnalyzed " + str(systemsCount) + " systems. States: public holiday, civil liverty, expansion, boom or investment  Economy: Industrial High Tech Tourism")
    if len(rawStationsList)==0:
        print("not a single system meets the requirements F")
    for i in range(0,len(rawStationsList)) :
        print(rawStationsList[i][0] + ", " + rawStationsList[i][1])

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

#Market Analysis 2: This one takes an extremely longass time

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

def marketAnalysis2 () :
    input("Market Analysis 2 - By: AweBob#6221 - Press enter to begin - ")

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
    startTime = int(time.time())
    for index, eddbSystem in enumerate(eddbSystems) :
        if eddbSystem.hasFourLuckyStates() :
            for station in eddbSystem.getStationsWithLuckyEconomy() :
                print(f"\n{station.getSys()} - {station.getStat()} - {int(eddbSystem.getDistanceFromSol())}lys\n")

        """
        #Used this to get my time estimate for how long this would take
        try :
            print(f"Processed {index} out of {len(eddbSystems)} in {int(time.time()) - startTime} secs projecting finished in {int(((int(time.time()) - startTime) /  index ) * len(eddbSystems))} secs")
        except ZeroDivisionError:
            print(f"Processed {index} out of {len(eddbSystems)} in {int(time.time()) - startTime} secs projecting finished in ? secs")
        """

    print(f"\nDone in {int(time.time()) - startTime} secs")

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

#This will work the same way market analysis1 does but its going to be a lot cleaner once I'm done with it

class AdvancedEddbSystem :
    def __init__(self, eddbSystemDictionary) :
        self.id = eddbSystemDictionary["id"]
        self.name = eddbSystemDictionary["name"]
        self.x = eddbSystemDictionary["x"]
        self.y = eddbSystemDictionary["y"]
        self.z = eddbSystemDictionary["z"]
        self.stations = [] #These are added via self.addStation()
        self.states = []
        for state in eddbSystemDictionary["states"] :
            self.states.append(state["name"])

    def addStation(self, station) :
        self.stations.append([ station["name"], station["economies"] ])

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
        ibe = False #investement/boom
        cle = False #civil liberty
        phe = False #public holiday
        ee = False #expansion
        pae = False #pirate attack
        for state in self.states :
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
        returningStations = [] #list of station names
        for station in self.stations :
            for economy in station[1] :
                if economy=="Industrial" or economy=="High Tech" or economy=="Tourism" :  #Industrial, High Tech, Refinery or Tourism station enconomies required
                    returningStations.append(station[0]) #add the station name
                    break #onto next station
        return(returningStations)

def marketAnalysis3() :
    input("Market Analysis 3 - By: AweBob#6221 - Press enter to begin - ")

    print("Downloading eddb")
    startTime = int(time.time())
    rawEddbPopulatedSystems = requests.get( "https://eddb.io/archive/v6/systems_populated.json" ).json()
    rawEddbStations = requests.get( "https://eddb.io/archive/v6/stations.json" ).json()
    
    print("Parsing Data")
    eddbSystems = []
    for rawEddbSystemDictionary in rawEddbPopulatedSystems :
        eddbSystems.append( AdvancedEddbSystem(rawEddbSystemDictionary) )
    for rawEddbStationDictionary in rawEddbStations :
        for eddbSystem in eddbSystems :
            if rawEddbStationDictionary["system_id"] == eddbSystem.getId() :
                eddbSystem.addStation(rawEddbStationDictionary)
                break #onto next station

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
                print(f"\n{station} - {eddbSystem.getName()} - {int(eddbSystem.getDistanceFromSol())}lys\n")

    print(f"\nDone in {int(time.time()) - startTime} secs")

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

#Attempt #4 - Using ELite BGS, but filtering out shitty economies first


def marketAnalysis4() :
    input("Market Analysis 4 - By: AweBob#6221 - Press enter to begin - ")

    print("Downloading eddb")
    startTime = int(time.time())
    rawEddbStations = requests.get( "https://eddb.io/archive/v6/stations.json" ).json()
    rawEddbPopulatedSystems = requests.get( "https://eddb.io/archive/v6/systems_populated.json" ).json()

    print(f"Filtering {len(rawEddbStations)} stations by economy")
    economyMatches = []
    for rawEddbStation in rawEddbStations :
        for economy in station["economies"] :
            if economy=="Industrial" or economy=="High Tech" or economy=="Tourism" :  #Industrial, High Tech, Refinery or Tourism station enconomies required
                sysName = "?"
                for system in rawEddbPopulatedSystems :
                    if station["system_id"]==system["id"] :
                        sysName = system["name"]
                        break #No need to keep searching
                economyMatches.append([ station["name"], sysName, station["id"], station["system_id"] ])
                break #onto next station

    print(f"Calculating number of different systems from {len(economyMatches)} stations")
    systemsForAnalysis = []
    for stationInfo in economyMatches :
        if stationInfo[3] not in systemsForAnalysis : #If the system id isn't on the list
            systemsForAnalysis.append( stationInfo[3] ) #add the system id

    print(f"Filtering {len(economyMatches)} stations over {len(systemsForAnalysis)} systems by system state")
    cachedSystemInfo = {}
    economyStateMatches = [] #Matches Economy and State! (economy checked above, state checked below)
    for stationList in economyMatches :
        try :
            systemInfo = cachedSystemInfo[str(stationList[3])] #try and grabbed the cached data
        except KeyError : #if it's not cached
            systemInfo = requests.get( f"https://elitebgs.app/api/ebgs/v4/systems?name={stationList[1]}"  ).json()["docs"] #THIS API IS RLLY DIFFICULT TO GET THE INFO I WANT OUT OF, I WANT ALL STATES OF SYSTEM
            cachedSystemInfo[str(stationList[3])] = systemInfo #cache it
        finally :
            #DETERMINE IF THE STATION IS IN A SYSTEM THAT MEETS THE REQUIREMENTS
            #ADD IT TO economyStateMatches
            print("placeholder")
                    
    print("Completed system state checking, printing results")
    if len(economyStateMatches) == 0 :
        print("lol jk no systems meet the requirements")
    else :
        for stationList in economyStateMatches :
            print(f"{stationList[0]} - {stationList[1]}")
    
    print(f"Total this took {int(time.time()) - startTime} seconds.")

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

if __name__ == "__main__":
    #marketAnalysis1() #Ugly code but it works 100%
    #marketAnalysis2() #Uses latest information, but takes forever to run
    #marketAnalysis3() #Cleaner code, needs more testing to be confirmed functional
    marketAnalysis4() #Uses latest information, based on the asumption station economies are constant, faster then market analysis 2, but still uses elitebgs
