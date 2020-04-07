
amountInHold = int(input("How much do you have in your hold?: "))

import requests
from bs4 import BeautifulSoup

url='https://inara.cz/ajaxaction.php?act=goodsdata&refname=sellmax&refid=144&refid2=0' #get this link from inara inspect element
params ={}
response=requests.post(url, data=params)
#print(response.status_code) #200 is good

soup = BeautifulSoup(response.text, 'html5lib')

html = list(soup.children)[0] #In the html tag
body = list(html.children)[1] #In the body tag
table = list(body.children)[1] #In the table tag
tbody = list(table.children)[1] #In the tbody tag

trsOnPage = 40 #This is the number of items that r in the table (rows), or in the thml the number of tr headers

stationList = [] #str
systemList = [] #Str
largePadList = []  #If large pad true, if medium pad false - Bool
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
    quantityList.append( int(quantity.replace(",","")) ) #Remove the commas then convert to integer
    priceList.append(int( price.replace(",","")[:-3] )) #remove commas, remove last three characters " Cr" and convert to int
    timeList.append(time)  
    
    if ( int(quantity.replace(",","")) > amountInHold * 27.7777 ) :
        payoutOfHundredPercentTemp = 100
    else :
        payoutOfHundredPercentTemp = (2.8527 * (int(quantity.replace(",","")) / int(amountInHold) ) ) + 46.8285
        if ( payoutOfHundredPercentTemp > 100 ) :
            payoutOfHundredPercentTemp = 100

    payoutOfHundredPercentList.append( payoutOfHundredPercentTemp ) #payout of 100% = 2.8527 * (Demand/Units) + 46.8285
    actualPriceList.append( payoutOfHundredPercentTemp * int( price.replace(",","")[:-3] ) )

bigestVal = 0
bigestValIndex = 0
for i in range(0,trsOnPage) :
    if ( actualPriceList[i] > bigestVal) :
        bigestVal = actualPriceList[i]
        bigestValIndex = i

print("The best system to sell at's estimated price is " + str(actualPriceList[bigestValIndex]) + " with a payout of 100 percent of " + str(payoutOfHundredPercentList[bigestValIndex]))
print(str(i) + ". " + station + " | " + system + " | " + pad + " | " + scDist + " " + dist + " | " + quantity + " | " + price + " | " + time)
