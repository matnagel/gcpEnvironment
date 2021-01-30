import pandas as pd
import datetime as dt

from SqlDataSources import Stock, Price, myGCPDataSource

source = myGCPDataSource
session = source.getSession()
print(f'Price - Number of rows: {session.query(Price).count()}')
query = session.query(Price).order_by(Price.date.desc()).limit(5)
for priceInfo in query:
    print(priceInfo)

print(f'Stock - Number of rows: {session.query(Stock).count()}')
query = session.query(Stock).limit(5)
for stock in query:
    print(stock)

