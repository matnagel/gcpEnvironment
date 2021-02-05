import pandas as pd
import datetime as dt

from gcp.SqlSources import Stock, Price, StdSource

source = StdSource()

print(f'Tables: {source.getTableNames()}\n')

print(f'Price - Number of rows: {source.query(Price).count()}')
query = source.query(Price).order_by(Price.date.desc()).limit(20)
for priceInfo in query:
    print(priceInfo)
print('\n')

print(f'Stock - Number of rows: {source.query(Stock).count()}')
query = source.query(Stock).limit(5)
for stock in query:
    print(stock)
