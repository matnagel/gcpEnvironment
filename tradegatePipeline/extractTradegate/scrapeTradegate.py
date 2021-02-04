import concurrent.futures
import requests as rq

from datetime import date
import time

from gcp.SqlSources import Stock, StdSource
from gcp.Storage import Bucket

class PageScrape:
    def __init__(self, isin, content):
        self.isin = isin
        self.content = content

def requestPageFromTradegate(isin):
    rawPage = rq.get('https://www.tradegate.de/orderbuch.php?isin=' + isin)
    return PageScrape(isin, rawPage.text)

def scrapeStocks(stocks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        scrapeList = executor.map(lambda s : requestPageFromTradegate(s.isin), stocks)
    return scrapeList

def verifyPreconditions(source):
    stocks = source.query(Stock)
    if len(list(stocks)) >= 25:
        raise ValueError('There are more than 25 stocks to update')

def pubsubEntryPoint(event, context):
    print("Scraping Tradegate")
    source = StdSource()
    verifyPreconditions(source)
    stocks = source.query(Stock)

    startTime = time.time()
    scrapeList = scrapeStocks(stocks)
    endTime = time.time()
    print(f'Scraped Tradegate {date.today()} in {endTime - startTime:.2f}')

    bucket = Bucket("tradegatescrapes")
    dateString = date.today().strftime("%y%m%d")
    folder = { f'{dateString}_{stock.isin}.html':stock.content for stock in scrapeList }
    bucket.saveDictToZipBlob(f'{dateString}Scrapes.zip', folder)
    print(f'Stored scrapings in lake')
