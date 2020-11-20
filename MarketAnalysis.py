
#====================================================================================================================================
#====================================================================================================================================
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
    
    print("Downloading EDDB Stations")
    startTime = int(time.time())
    rawEddbStations = requests.get( "https://eddb.io/archive/v6/stations.json" ).json()
    rawEddbPopulatedSystems = requests.get( "https://eddb.io/archive/v6/systems_populated.json" ).json()

    print(f"Filtering {len(rawEddbStations)} stations - {int(time.time()) - startTime}  seconds elapsed so far")
    outputStations = [[],[],[],[]]
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
                for system in rawEddbPopulatedSystems :
                    if rawEddbStation["system_id"]==system["id"] :
                        sysName = system["name"]
                        break #No need to keep searching
                if inv and cle and phe :
                    outputStations[0].append([str(rawEddbStation["name"]), sysName, str( time.strftime( "%H:%M:%S" , time.gmtime(startTime - int(rawEddbStation["updated_at"]) ))), cleanStates, economies ])
                elif inv and cle and pae :
                    outputStations[1].append([str(rawEddbStation["name"]), sysName, str( time.strftime( "%H:%M:%S" , time.gmtime(startTime - int(rawEddbStation["updated_at"]) ))), cleanStates, economies ])
                elif bom and cle and phe :
                    outputStations[2].append([str(rawEddbStation["name"]), sysName, str( time.strftime( "%H:%M:%S" , time.gmtime(startTime - int(rawEddbStation["updated_at"]) ))), cleanStates, economies ])
                elif bom and cle and pae :
                    outputStations[3].append([str(rawEddbStation["name"]), sysName, str( time.strftime( "%H:%M:%S" , time.gmtime(startTime - int(rawEddbStation["updated_at"]) ))), cleanStates, economies ])

    print(f"Printing final results - {int(time.time()) - startTime}  seconds elapsed so far\n")
    for index, stationQualityLevel in enumerate(outputStations) :
        for outputStation in stationQualityLevel :
            economyStr = ", ".join(outputStation[4])
            statesStr = ", ".join(outputStation[3])
            print(str(index + 1) + ". " + outputStation[0] + " - " + outputStation[1] + " - " + economyStr + " - " + statesStr ) #Add the time stuff later, that would be a nice feature
        
    print(f"\nProcess took {int(time.time()) - startTime} seconds")

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================

if __name__ == "__main__":
    marketAnalysis()

#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================
