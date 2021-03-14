import datetime as dt

from gcp.SqlSources import Stock, Price, StdSource

source = StdSource()
# newStock = Stock(isin=??, name=??)

print(f'Stock - Number of rows: {source.query(Stock).count()}')
query = source.query(Stock).limit(30)
for stock in query:
    print(stock)
