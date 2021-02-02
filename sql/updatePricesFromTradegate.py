import requests as rq

from bs4 import BeautifulSoup
from datetime import date
from src.SqlDataSources import myGCPDataSource, Price, Stock

def extractId(soup, css):
    #setlocale(LC_NUMERIC, 'de_DE.UTF-8')
    html = soup.select(css)[0]
    txt = html.text.replace(' ', '')
    txt = txt.replace(',', '.')
    return float(txt)
    #return atof(txt)

def getStockInformation(stocks):
    dataList = []
    for stock in stocks:
        isin = stock.isin
        rawPage = rq.get('https://www.tradegate.de/orderbuch.php?isin=' + isin)
        soupPage = BeautifulSoup(rawPage.text, 'html.parser')
        try:
            last = extractId(soupPage, '#last')
            high = extractId(soupPage, '#high')
            low = extractId(soupPage, '#low')
            dataList.append(Price(isin=isin, date=date.today(), last=last, high=high, low=low))
        except ValueError:
            print(f"Could not extract price for {isin}")
    return dataList

def verifyPreconditions(source):
    stocks = source.query(Stock)
    if len(list(stocks)) >= 25:
        raise ValueError('There are more than 25 stocks to update')
    lastUpdate = source.query(Price.date).order_by(Price.date.desc()).first()
    today = date.today()
    if lastUpdate.date >= today:
        raise RuntimeError(f'Already have entries with date {lastUpdate.date}, which is today {today} or later. Only updates once a day.')

def pubsubEntry(event, context):
    print("Update Tradegate triggered")
    source = myGCPDataSource
    verifyPreconditions(source)
    print('Preconditions meet')

    stocks = source.query(Stock)
    newPrices = getStockInformation(stocks)
    print(f'Received stock prices of {date.today()}')

    source.addRows(newPrices)
    source.commit()
    print('Successfully added new prices to table')
