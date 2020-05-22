
import requests 
import json

eddbUrl = "https://eddb.io/archive/v6/systems_populated.json" 
response = requests.get(eddbUrl)  
eddbJson = response.json()

output = []

for systemDict in eddbJson :
    output.append({
        "id":systemDict["id"],
        "name":systemDict["name"],
        "x":systemDict["x"],
        "y":systemDict["y"],
        "z":systemDict["z"]
        })

with open('simplified_systems_populated.json',"w+") as outputFile :
    json.dump(output, outputFile)

