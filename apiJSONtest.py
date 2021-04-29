#!/usr/bin/env python3
#BWG 030321 Test to see how fetching JSON from a stock API would work
#Using the financial modeling prep API

import json
import sys
import os
import urllib
from urllib import request

#API Key stored locally and read on startup for security.

API_URL = 'https://financialmodelingprep.com/api/v3/'
API_STOCK_DIV = 'historical-price-full/stock_dividend/'
API_KEY_FILL = '&apikey='

#Reading the arguments from the command-line for the user
if len(sys.argv) > 1:
    with open(sys.argv[1],"r") as f:
        API_KEY = f.read()
    fileOutput = sys.argv[2]

#These are just for development purposes- So that I can run it from vscode quick with some default params.
else:
    fileOutput = 'testFile.txt'
    with open("stockAPIKey.txt","r") as f:
        API_KEY = f.read()

def dividendSceener(minDividend=.10,minAPR=.08,maxAPR=.15,maxPrice=50):
    """MinDividend taken is is the minimum annual return of the stock given current valuation and last annual dividend.
       MaxPrice is the maximum current market value for a stock at the moment."""
       #File contains a JSON Object collected from a list of historical dividends 
    
    #Strings to concatenate to make into a URL, along with the arguments provided in the function.
    API_PRICE_LOWER = '&priceLowerThan='
    API_DIVIDEND_MORE = '&dividendMoreThan='
    API_STOCK_SCREEN = 'stock-screener?'

    #Will complete the request to the API with a link that is made via the variables that the user provided
    with urllib.request.urlopen(API_URL + API_STOCK_SCREEN + API_PRICE_LOWER + str(maxPrice) + API_DIVIDEND_MORE + str(minDividend) + '&exchange=NYSE,NASDAQ' + API_KEY_FILL + API_KEY ) as url:
        data = json.loads(url.read().decode())
        tempList = [] #List to store all of the matching stocks in
        for i in data:
            try:  #Using a try block here because if we divide by a price that's 0 for any reason, obvious error.
                if((maxAPR > (i['lastAnnualDividend']/i['price']) > minAPR) and i['isActivelyTrading']): # Filtering out stocks here that don't match the return rate or aren't active
                    percentageReturn = i['lastAnnualDividend']/i['price'] #Calculating the yearly percentage of dividend return
                    tempList.append([i["symbol"],percentageReturn,i["price"],i["lastAnnualDividend"]]) #Putting them into the return list, in the format of:
                    #[Symbol, prcntReturn, currentPrice, lastAnnualDividend]     
            except:
                continue
        tempList.sort(key = lambda testList: -testList[1]) #On exit of the loop, will sort it from highest dividend to lowest dividend.
        return tempList

def main():
    tempList = dividendSceener()
    printArgs(tempList)
    f = open(fileOutput,'a')
    for i in tempList:
        f.write(str(i)+ '\n')

#TODO 
#041921 Using the dividend calendar feature, grab all of the stocks that are paying dividends in the next 3 months or so and then parse them to see if 
#They are already in a hash from the above stock screener, so that I can get a complete picture of the dividend, price, payment date, returnPercentage, and stock
#from only 2 api pulls and then can work on sorting it inside of the code here or something like that.



if __name__ == "__main__":
    main()