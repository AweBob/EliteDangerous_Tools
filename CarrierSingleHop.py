
import requests
import csv
import time
import numpy as np
import json

LISTINGS_URL = "https://eddb.io/archive/v6/listings.csv"
LISTINGS_NAME = "listings.csv"

def downloadListingsCsv() : #Non functional as of now
    response = requests.get(LISTINGS_URL)  
    #decode = response.content.decode('utf-8')
    decoded = csv.reader(response)
    return(decoded)

def getCsvFromCurrentDirectory() :
    return list(csv.reader(open(LISTINGS_NAME)))

def main() :
    response = requests.get('https://eddb.io/archive/v6/commodities.json')
    commodityList = json.loads(response.text)
    
    bestCommodityName = 'none'
    bestCommodityDifference = 0
    for commodityDict in commodityList :
        if (
            commodityDict["max_sell_price"] != None and commodityDict["max_buy_price"] != None and commodityDict["is_rare"] == 0 and 
            commodityDict["name"] !="Meta-Alloys" and #too rare to buy
            commodityDict["name"] !="CMM Composite" and #not enough buying quantity
            commodityDict["name"] !="Insulating Membrane" ): #not enough buying quantity
            commodityDifference =  commodityDict["max_sell_price"] - commodityDict["max_buy_price"] #sell - buy means lowest selling price and highest selling price
            if (commodityDifference > bestCommodityDifference) :
                bestCommodityDifference = commodityDifference
                bestCommodityName = commodityDict["name"]

    print(bestCommodityName + "  " + "{:,.0f}".format( bestCommodityDifference ))


main()

#Conclusion:
#Idk if this means anything, I've determined the best commodity to trade with assuming you're only interacting with stations is "Ceramic Composites",
#they can be bought for 80-90 credits at a lot of stations (most of which are over 25k quantity) and can be sold at stations for 10k credits per ton at stations with a million quantity demand.
#almost 10k profit per ton and you can transport 25k at a time which if u sold it all urself would pay 250mil.
#this prolly isn't worth it tho because of the time ti takes to bring the commodities to and from ur carrier.