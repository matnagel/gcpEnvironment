import concurrent.futures
import requests as rq

from datetime import date
import time

from gcp.Storage import Bucket

import re

class PageScrape:
    def __init__(self, isin, content):
        self.isin = isin
        self.content = content


class Stock:
    isinPattern = re.compile('^[A-Z]{2}[A-Z0-9]{10}$')
    def __init__(self, isin):
        match = self.isinPattern.match(isin)
        if not match:
            raise ValueError(f"Wrong formated isin {isin}")
        self.isin = isin

def requestPageFromTradegate(isin):
    rawPage = rq.get('https://www.tradegate.de/orderbuch.php?isin=' + isin)
    return PageScrape(isin, rawPage.text)

def scrapeStocks(stocks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        scrapeList = executor.map(lambda s : requestPageFromTradegate(s.isin), stocks)
    return scrapeList

def loadListOfStocks(bucket):
    text = bucket.readFromBlob("stockList")
    ls = text.split()
    return list(map(Stock, ls))

def pubsubEntryPoint(event, context):
    print("Scraping Tradegate")
    bucket = Bucket("tradegatescrapes")

    stocks = loadListOfStocks(bucket)
    if len(list(stocks)) >= 25:
        raise ValueError('There are more than 25 stocks to update')

    startTime = time.time()
    scrapeList = scrapeStocks(stocks)
    endTime = time.time()
    print(f'Scraped Tradegate {date.today()} in {endTime - startTime:.2f}')

    dateString = date.today().strftime("%y%m%d")
    folder = { f'{dateString}_{stock.isin}.html':stock.content for stock in scrapeList }
    bucket.saveDictToZipBlob(f'{dateString}Scrapes.zip', folder)
    print(f'Stored scrapings in lake')
