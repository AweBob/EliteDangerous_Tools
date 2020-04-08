
from EliteExtraJsonParser import CargoJsonParser #for reading Cargo.json
import requests #For pinging inara
from bs4 import BeautifulSoup #for sorting inara

#=================================================================================================================================

def main() :
    print()
    inputVal = input("") #Blank input (it's implied hitting enter reloads it)

    try :
        if (len(inputVal) == 0) :
            json_Cargo = CargoJsonParser() 
            tonsAboard = 0
            for item in json_Cargo["Inventory"] :
                if ( item["Name_Localised"] == "Low Temperature Diamonds" ) :
                    tonsAboard = item["Count"]
            try :
                singleValue(tonsAboard)
            except :
                print("Error in calculation...")
        else :
            inputVals = inputVal.split(" ") #split it into a list of values at the space
            testVal = list(map(int,inputVals)) #Convert all things into an integer, this confirms someone didn't just type in a few words and isn't used later
            valAmounts = len(inputVals)
            if (valAmounts == 1) :
                try :
                    singleValue(int(inputVals[0])) 
                except :
                    print("Error in calculation...")
            elif (valAmounts <= 4) :
                try :
                    groupValue(inputVals)
                except :
                    print("Error in calculation...")
            else :
                raise Exception  
    except :
        print("Error in handling input...")
    main() #If it gets to this point there must've been an error so just run it again

#=================================================================================================================================

def groupValue( tonsList ) : #prints results for a maximum of 4 users, displays payout for each person and trade divdens for each person, if group is 2 or 3 people it will shows 1 person selling non getting trade divs
    
    averageTonsAboard = 0
    stringTonsList = ""
    for i in range(0,len(tonsList)) :
        averageTonsAboard = averageTonsAboard + int(tonsList[i])
        if ( i ==  len(tonsList) - 2 ) :
            stringTonsList = stringTonsList + str(tonsList[i]) + ", and "
        elif ( i ==  len(tonsList) - 1 ) :
            stringTonsList = stringTonsList + str(tonsList[i]) 
        else :
            stringTonsList = stringTonsList + str(tonsList[i]) + ", "
    averageTonsAboard = int(averageTonsAboard / len(tonsList))

    print("Computing for " + str(averageTonsAboard) + " tons of LTDs which is the average of " + str(stringTonsList) + "." )



    main()

#=================================================================================================================================

def singleValue( tonsAboard ) : #prints results for one user - print trade dividens results for 1 other person

    print("Computing for " + str(tonsAboard) + " tons of LTDs.")

    url='https://inara.cz/ajaxaction.php?act=goodsdata&refname=sellmax&refid=144&refid2=0' #get this link from inara inspect element - THIS IS THE LINK FOR LOW TEMPATURE DIAMONDS
    params ={}
    response=requests.post(url, data=params)
    #print(response.status_code) #200 is good

    soup = BeautifulSoup(response.text, 'html5lib')

    html = list(soup.children)[0] #In the html tag
    body = list(html.children)[1] #In the body tag
    table = list(body.children)[1] #In the table tag
    tbody = list(table.children)[1] #In the tbody tag

    trsOnPage = 40 #This is the number of items that are in the table (rows), or in the html the number of tr headers

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

    numValues = 5 #I want 5 results to show (including the header)

    bigestIndexes = [0]
    bigestValues = [0]
    for i in range(1,numValues + 1) :
        bigestVal = max(estimatedPriceTotalList)
        index = estimatedPriceTotalList.index( bigestVal ) 
        estimatedPriceTotalList[index] = -1 #so it won't get chosen for the next bigest val
        bigestIndexes.append(index)
        bigestValues.append(bigestVal)

    printoutInfo = [ ["Rank", "≈Price Per Ton", "≈Total Price", "System", "Station", "Pad", "Last Updated"] ] #initialize it with the header
    for i in range(1,numValues + 1) :
        printoutInfo.append( [ str(i) + ".", "{:,.0f}".format(estimatedPricePerTonList[bigestIndexes[i]]), "{:,.0f}".format(bigestValues[i]), systemList[bigestIndexes[i]], stationList[bigestIndexes[i]],  largePadList[bigestIndexes[i]], timeList[bigestIndexes[i]] ]  )

    maxColumnList = []
    for i in range(0,len(printoutInfo[0])) :
        columnList = []
        for j in range(0,numValues + 1) :
            columnList.append( printoutInfo[j][i] )
        maxColumnList.append( len(max( columnList , key=len)) + 2 )

    for rowIndex in range(0,len(printoutInfo)) :
        for columnIndex in range(0,len(printoutInfo[0])) : 
            spaces = " " * ( maxColumnList[columnIndex] - len(printoutInfo[rowIndex][columnIndex]) )
            print(printoutInfo[rowIndex][columnIndex] + spaces , end='')
        print() #new line

    main()

#=================================================================================================================================

if __name__ == "__main__":
    print("Imports sucessful. Running LtdMarket...")
    main()

#Allow singleValue to printout trade dividens for group members
#Develop groupValue function
