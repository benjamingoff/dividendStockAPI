#!/usr/bin/env python3
#BWG 030321 Test to see how fetching JSON from a stock API would work
#Using the financial modeling prep API

import json
import sys
import os
import urllib
from urllib import request

API_KEY = '0adf89572710cccad0e9dfc118574b82'
API_URL = 'https://financialmodelingprep.com/api/v3/'
API_STOCK_DIV = 'historical-price-full/stock_dividend/'
API_STOCK_SCREEN = 'stock-screener?'
API_KEY_FILL = '&apikey='

if len(sys.argv) > 1:
    fileOutput = sys.argv[1]

else:
    fileOutput = 'testFile.txt'
def dividendSceener(minDividend=.10,minAPR=.08,maxAPR=.15,maxPrice=50):
    """MinDividend taken is is the minimum annual return of the stock given current valuation and last annual dividend.
       MaxPrice is the maximum current market value for a stock at the moment."""
       #File contains a JSON Object collected from a list of historical dividends 
       
    API_PRICE_LOWER = '&priceLowerThan='
    API_DIVIDEND_MORE = '&dividendMoreThan='

    with urllib.request.urlopen(API_URL + API_STOCK_SCREEN + API_PRICE_LOWER + str(maxPrice) + API_DIVIDEND_MORE + str(minDividend) + '&exchange=NYSE,NASDAQ' + API_KEY_FILL + API_KEY ) as url:
        data = json.loads(url.read().decode())
        tempList = []
        for i in data:
            try:
                if((.15 > (i['lastAnnualDividend']/i['price']) > minAPR) and i['isActivelyTrading']):
                    percentageReturn = i['lastAnnualDividend']/i['price']
                    tempList.append([i["symbol"],percentageReturn,i["price"],i["lastAnnualDividend"]])
                tempList.sort(key = lambda testList: -testList[1])     
            except:
                continue
        return tempList

def main():
    tempList = dividendSceener()
    print(tempList)
    f = open(fileOutput,'a')
    for i in tempList:
        f.write(str(i)+ '\n')

if __name__ == "__main__":
    main()