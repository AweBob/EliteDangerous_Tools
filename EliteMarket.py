
nothing = input("Welcome to EliteMarket, press enter to commence")

from EliteExtraJsonParser import CargoJsonParser #for reading Cargo.json
import requests #For pinging inara
from bs4 import BeautifulSoup #for sorting inara

print("Imports sucessful")

json_Cargo = CargoJsonParser() 

tonsAboard = json_Cargo["Count"]
for item in json_Cargo["Inventory"] :
    if ( item["Name_Localised"] == "Limpet" ) :
        tonsAboard = tonsAboard - item["Count"]

print("You have " + str(tonsAboard) + " tons aboard.")

url='https://inara.cz/ajaxaction.php?act=goodsdata&refname=sellmax&refid=144&refid2=0' #get this link from inara inspect element
params ={}
response=requests.post(url, data=params)
#print(response.status_code) #200 is good

print("Communication with inara sucessful")

soup = BeautifulSoup(response.text, 'html5lib')

html = list(soup.children)[0] #In the html tag
body = list(html.children)[1] #In the body tag
table = list(body.children)[1] #In the table tag
tbody = list(table.children)[1] #In the tbody tag

trsOnPage = 40 #This is the number of items that are in the table (rows), or in the thml the number of tr headers

stationList = [] #str
systemList = [] #Str
largePadList = []  #If large pad true, if medium pad false - Bool
distanceList = [] #Str
quantityList = [] #Int
priceList = [] #Int
timeList = [] #Str
payoutOfHundredPercentList = [] #float
actualPriceList = [] #float

for i in range(0,trsOnPage) :
    tr =  list(tbody.children)[i]
    tdName = list(tr.children)[0]
    span = list(tdName.children)[0]
    a = list(span.children)[1]
    station = list(a.children)[0].get_text()
    system = list(a.children)[2].get_text()
    pad = list(tr.children)[1].get_text()
    scDist = list(tr.children)[2].get_text()
    dist = list(tr.children)[3].get_text()
    quantity = list(tr.children)[4].get_text()
    price = list(tr.children)[5].get_text()
    time = list(tr.children)[6].get_text()
    stationList.append(station)
    systemList.append(system)
    largePadList.append(pad == "L") #If pad is large append True, if it isn't as in medium "M" 
    distanceList.append(dist) #string for printing later
    quantityList.append( int(quantity.replace(",","")) ) #Remove the commas then convert to integer
    priceList.append(int( price.replace(",","")[:-3] )) #remove commas, remove last three characters " Cr" and convert to int
    timeList.append(time)  
    
#=================================================================================================================================
#==================CREDIT TO: https://github.com/neotron aka CMDR Neotron for the aproximation algorithm below====================
#=================================================================================================================================
estimatedPricePerTonList = []
estimatedPriceTotalList = []
perton = 0.00215 #0.215% per ton
maxratio = 27.77777777777777
#tonsAboard set above
for i in range(0, trsOnPage) :
    demand = quantityList[i] 
    cost = priceList[i] 
    perton = perton / ( demand / 504 )
    reduction = 0
    for i in range(0, tonsAboard) :
        ratio = demand / (tonsAboard - i)
        if (ratio <= maxratio) :
            reduction = reduction + perton
    reduction = min(0.7674, reduction)
    estimatedPricePerTonList.append( cost*(1-reduction) )
    estimatedPriceTotalList.append( ( cost*(1-reduction) ) * tonsAboard )
#=================================================================================================================================
#=================================================================================================================================
#=================================================================================================================================

firstVal = max(estimatedPriceTotalList)
firstIndex = estimatedPriceTotalList.index( firstVal ) 
estimatedPriceTotalList[firstIndex] = -1 #so it won't get chosen for the next bigest val
secondVal = max(estimatedPriceTotalList)
secondIndex = estimatedPriceTotalList.index(secondVal)
estimatedPriceTotalList[secondIndex] = -1
thirdVal = max(estimatedPriceTotalList)
thirdIndex = estimatedPriceTotalList.index(thirdVal)
estimatedPriceTotalList[thirdIndex] = -1

print("Algorithm sucessful: rank. system | station distance Large Pad: size estimated price per ton time since update")
print("1. " + systemList[firstIndex] + " | " + stationList[firstIndex] + " " + distanceList[firstIndex] + " Large Pad: " + str(largePadList[firstIndex]) + " " + str(estimatedPricePerTonList[firstIndex])[:-3] + "k " + timeList[firstIndex] )
print("2. " + systemList[secondIndex] + " | " + stationList[secondIndex] + " " + distanceList[secondIndex] + " Large Pad: " + str(largePadList[secondIndex]) + " " + str(estimatedPricePerTonList[secondIndex])[:-3] + "k " + timeList[secondIndex] )
print("3. " + systemList[thirdIndex] + " | " + stationList[thirdIndex] + " " + distanceList[thirdIndex] + " Large Pad:" + str(largePadList[thirdIndex]) + " " + str(estimatedPricePerTonList[thirdIndex])[:-3] + "k " + timeList[thirdIndex] )

nothing = input("Press enter to close.")
