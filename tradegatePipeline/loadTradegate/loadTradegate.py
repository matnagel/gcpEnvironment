import concurrent.futures
import requests as rq

from datetime import date
import time

from bs4 import BeautifulSoup

from gcp.SqlSources import Stock, Price, StdSource

def extractId(soup, css):
    #setlocale(LC_NUMERIC, 'de_DE.UTF-8')
    html = soup.select(css)[0]
    txt = html.text.replace(' ', '')
    txt = txt.replace(',', '.')
    return float(txt)
    #return atof(txt)

def requestTradegate(isin):
    rawPage = rq.get('https://www.tradegate.de/orderbuch.php?isin=' + isin)
    soupPage = BeautifulSoup(rawPage.text, 'html.parser')
    try:
        last = extractId(soupPage, '#last')
        high = extractId(soupPage, '#high')
        low = extractId(soupPage, '#low')
    except ValueError:
        print(f"Malformed page returned for {isin}")
    return Price(isin=isin, date=date.today(), last=last, high=high, low=low)

def getStockInformation(stocks):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        newPrices = executor.map(lambda stock : requestTradegate(stock.isin), stocks)
    return list(newPrices)

def verifyPreconditions(source):
    stocks = source.query(Stock)
    if len(list(stocks)) >= 25:
        raise ValueError('There are more than 25 stocks to update')
    lastUpdate = source.query(Price.date).order_by(Price.date.desc()).first()
    today = date.today()
    if lastUpdate.date >= today:
        raise RuntimeError(f'Already have entries with date {lastUpdate.date}, which is today {today} or later. Only updates once a day.')

def pubsubEntryPoint(event, context):

    print("Update Tradegate triggered")
    source = StdSource()
    verifyPreconditions(source)
    print('Preconditions meet')

    stocks = source.query(Stock)
    startTime = time.time()
    newPrices = getStockInformation(stocks)
    endTime = time.time()
    print(f'Received stock prices of {date.today()} in {endTime - startTime:.2f}')

    source.addRows(newPrices)
    source.commit()
    print('Successfully added new prices to table')
