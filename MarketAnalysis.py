
#====================================================================================================================================

import requests #For apis
import numpy as np #for distance calculation 
import time #For timing how long all this junk takes

#If you get errors on the above 2 things run: 
# py -m pip install requests
# py -m pip install numpy

#====================================================================================================================================
#================================Credit for this idea to CMDR Longman.P.J.===========================================================
#====================================================================================================================================

def marketAnalysis() :
    input("Market Analysis 5 - By: AweBob#6221 & Pete#1168 - Press enter to begin - ")
    
    print("Downloading EDDB Stations & Populated Systems")
    startTime = time.time()
    rawEddbStations = requests.get( "https://eddb.io/archive/v6/stations.json" ).json()
    rawEddbPopulatedSystems = requests.get( "https://eddb.io/archive/v6/systems_populated.json" ).json()
    print(f"Download Took {round(time.time() - startTime, 2)} Seconds")

    print(f"Filtering {len(rawEddbStations)} Stations By State & Economy")
    startTime = time.time()
    outputStations = [[],[],[],[]]
    pointSol = np.array([0,0,0])
    for rawEddbStation in rawEddbStations :
        economies = rawEddbStation["economies"] #economy=="Industrial" or economy=="High Tech" or economy=="Tourism"
        ind = False #industrial
        hte = False#high tech
        tou = False #tourism
        ref = False #refinery
        ext = False #Extraction
        for economy in economies :
            if economy=="Industrial" :
                ind = True
            elif economy=="High Tech" :
                hte = True
            elif economy=="Tourism" :
                tou = True
            elif economy=="Refinery" :
                ref = True
            elif economy=="Extraction" :
                ext = True
        states = rawEddbStation["states"] 
        cleanStates = []
        inv = False #investement
        bom = False #boom
        cle = False #civil liberty
        phe = False #public holiday (idk why i put an e in this lmao)
        ee = False #expansion
        pae = False #pirate attack
        for stateGroup in states :
            state = stateGroup["name"] #Just grab the name of the state
            if state != "None" :
                cleanStates.append( state )
            if (state=="Boom"):
                bom = True
            elif (state=="Investment") :
                inv = True
            elif (state=="Civil Liberty"):
                cle = True
            elif (state=="Public Holiday"):
                phe = True
            elif (state=="Pirate Attack") :
                pae = True
            elif (state=="Expansion"):
                ee = True
        if (ind or hte or tou or ref) and (not ext) : #It's an acceptable economy
            if (inv and cle and phe) or (inv and cle and pae) or (bom and cle and phe) or (bom and cle and pae) : #if its an acceptable state
                sysName = "?" #gets overriden with the actual if it is found
                distanceToSol = "?" #^
                for system in rawEddbPopulatedSystems :
                    if rawEddbStation["system_id"]==system["id"] :
                        sysName = system["name"]
                        pointSys = np.array([system["x"], system["y"], system["z"]])
                        squared_dist = np.sum((pointSol-pointSys)**2, axis=0)
                        distanceToSol = str(round(np.sqrt(squared_dist), 2))
                        break #No need to keep searching
                if inv and cle and phe :
                    outputStations[0].append([str(rawEddbStation["name"]), sysName, rawEddbStation["max_landing_pad_size"], str(rawEddbStation["distance_to_star"]), distanceToSol ])
                elif inv and cle and pae :
                    outputStations[1].append([str(rawEddbStation["name"]), sysName, rawEddbStation["max_landing_pad_size"], str(rawEddbStation["distance_to_star"]), distanceToSol ])
                elif bom and cle and phe :
                    outputStations[2].append([str(rawEddbStation["name"]), sysName, rawEddbStation["max_landing_pad_size"], str(rawEddbStation["distance_to_star"]), distanceToSol ])
                elif bom and cle and pae :
                    outputStations[3].append([str(rawEddbStation["name"]), sysName, rawEddbStation["max_landing_pad_size"], str(rawEddbStation["distance_to_star"]), distanceToSol ])
    print(f"Filtering Took {round(time.time() - startTime, 2)} Seconds")

    print(f"Printing Final Results\n")
    for index, stationQualityLevel in enumerate(outputStations) :
        for outputStation in stationQualityLevel :
            print(str(index + 1) + ". " + outputStation[0] + "; " + outputStation[1] + "; " + outputStation[2] + " pad; " + outputStation[3] + " ls; " + outputStation[4] + " lys" )
    print() #newline

#====================================================================================================================================

if __name__ == "__main__":
    marketAnalysis()

#====================================================================================================================================
