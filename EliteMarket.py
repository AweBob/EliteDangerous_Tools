
from EliteExtraJsonParser import ExtraJsonParserMain #for reading Cargo.json
import requests #For pinging inara
from bs4 import BeautifulSoup #for sorting inara

json_Cargo , json_Market , json_ModulesInfo , json_Outfitting , json_Shipyard , json_Status = ExtraJsonParserMain() #Get all the 

amountInHold = json_Cargo["Count"]
for item in json_Cargo["Inventory"] :
    if ( item["Name_Localised"] == "Limpet" ) :
        amountInHold = amountInHold - item["Count"]

url='https://inara.cz/ajaxaction.php?act=goodsdata&refname=sellmax&refid=144&refid2=0' #get this link from inara inspect element
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
    
#Implement neotron's estimation algorithm
#Printout top 3 systems to sell at as some may be in Colonia