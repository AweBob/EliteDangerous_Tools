
from EliteExtraJsonParser import CargoJsonParser #for reading Cargo.json
import requests #For pinging inara
from bs4 import BeautifulSoup #for sorting inara

def main(  ) :
    print()
    json_Cargo = CargoJsonParser() 

    tonsAboard = 0
    for item in json_Cargo["Inventory"] :
        if ( item["Name_Localised"] == "Low Temperature Diamonds" ) :
            tonsAboard = item["Count"]

    print("You have " + str(tonsAboard) + " tons of LTDs aboard.")

    url='https://inara.cz/ajaxaction.php?act=goodsdata&refname=sellmax&refid=144&refid2=0' #get this link from inara inspect element - THIS IS THE LINK FOR LOW TEMPATURE DIAMONDS
    params ={}
    response=requests.post(url, data=params)
    #print(response.status_code) #200 is good

    soup = BeautifulSoup(response.text, 'html5lib')

    html = list(soup.children)[0] #In the html tag
    body = list(html.children)[1] #In the body tag
    table = list(body.children)[1] #In the table tag
    tbody = list(table.children)[1] #In the tbody tag

    trsOnPage = 40 #This is the number of items that are in the table (rows), or in the thml the number of tr headers

    stationList = [] #str
    systemList = [] #Str
    largePadList = []  #str
    distanceList = [] #Str
    quantityList = [] #Int
    priceList = [] #Int
    timeList = [] #Str

    for i in range(0,trsOnPage) :
        tr =  list(tbody.children)[i]
        tdName = list(tr.children)[0]
        span = list(tdName.children)[0]
        a = list(span.children)[1]
        station = list(a.children)[0].get_text()
        system = list(a.children)[2].get_text()
        pad = list(tr.children)[1].get_text()
        #scDist = list(tr.children)[2].get_text()
        dist = list(tr.children)[3].get_text()
        quantity = list(tr.children)[4].get_text()
        price = list(tr.children)[5].get_text()
        time = list(tr.children)[6].get_text()
        if (float(dist[:-3]) <  10000) : #exclude colonia ones or ones more than 10,000 lys out 
            stationList.append(station)
            systemList.append(system)
            largePadList.append(pad) #str
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
    for i in range(0, len(systemList)) :
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

    fourthVal = max(estimatedPriceTotalList)
    fourthIndex = estimatedPriceTotalList.index(fourthVal)
    estimatedPriceTotalList[fourthIndex] = -1

    fifthVal = max(estimatedPriceTotalList)
    fifthIndex = estimatedPriceTotalList.index(fifthVal)
    estimatedPriceTotalList[fifthIndex] = -1

    printoutInfo =  [  
        ["Rank", "Estimated Price Per Ton", "System", "Station", "Distance", "Pad Size", "Last Updated"],
        ["1.", "{:,.0f}".format(estimatedPricePerTonList[firstIndex]), systemList[firstIndex], stationList[firstIndex], distanceList[firstIndex], largePadList[firstIndex], timeList[firstIndex] ],
        ["2.", "{:,.0f}".format(estimatedPricePerTonList[secondIndex]), systemList[secondIndex], stationList[secondIndex], distanceList[secondIndex], largePadList[secondIndex], timeList[secondIndex] ],
        ["3.", "{:,.0f}".format(estimatedPricePerTonList[thirdIndex]), systemList[thirdIndex], stationList[thirdIndex], distanceList[thirdIndex], largePadList[thirdIndex], timeList[thirdIndex] ],
        ["4.", "{:,.0f}".format(estimatedPricePerTonList[fourthIndex]), systemList[fourthIndex], stationList[fourthIndex], distanceList[fourthIndex], largePadList[fourthIndex], timeList[fourthIndex] ],
        ["5.", "{:,.0f}".format(estimatedPricePerTonList[fifthIndex]), systemList[fifthIndex], stationList[fifthIndex], distanceList[fifthIndex], largePadList[fifthIndex], timeList[fifthIndex] ]
    ]

    maxColumnList = [
        len(max([printoutInfo[0][0],printoutInfo[1][0], printoutInfo[2][0], printoutInfo[3][0], printoutInfo[4][0], printoutInfo[5][0] ], key=len)) + 2,
        len(max([printoutInfo[0][1],printoutInfo[1][1], printoutInfo[2][1], printoutInfo[3][1], printoutInfo[4][1], printoutInfo[5][1] ], key=len)) + 2,
        len(max([printoutInfo[0][2],printoutInfo[1][2], printoutInfo[2][2], printoutInfo[3][2], printoutInfo[4][2], printoutInfo[5][2] ], key=len)) + 2,
        len(max([printoutInfo[0][3],printoutInfo[1][3], printoutInfo[2][3], printoutInfo[3][3], printoutInfo[4][3], printoutInfo[5][3] ], key=len)) + 2,
        len(max([printoutInfo[0][4],printoutInfo[1][4], printoutInfo[2][4], printoutInfo[3][4], printoutInfo[4][4], printoutInfo[5][4] ], key=len)) + 2,
        len(max([printoutInfo[0][5],printoutInfo[1][5], printoutInfo[2][5], printoutInfo[3][5], printoutInfo[4][5], printoutInfo[5][5] ], key=len)) + 2,
        len(max([printoutInfo[0][6],printoutInfo[1][6], printoutInfo[2][6], printoutInfo[3][6], printoutInfo[4][6], printoutInfo[5][6] ], key=len)) + 2
    ]

    for rowIndex in range(0,len(printoutInfo)) :
        for columnIndex in range(0,len(printoutInfo[0])) : 
            spaces = " " * ( maxColumnList[columnIndex] - len(printoutInfo[rowIndex][columnIndex]) )
            print(printoutInfo[rowIndex][columnIndex] + spaces , end='')
        print() #new line

    nothing = input("") #Blank input (it's implied hitting enter reloads it)
    main()

if __name__ == "__main__":
    print("Imports sucessful. Running EliteMarket")
    main( )
