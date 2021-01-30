import os

import pandas as pd
import datetime as dt

from SqlDataSources import Stock, Price, myGCPDataSource

from pathlib import Path

seedPath = Path(os.environ["GCP_DATA_PATH"]) / 'seedData'


source = myGCPDataSource
session = myGCPDataSource.getSession()
if session.query(Stock).count() == 0:
    isins = pd.read_csv(seedPath / 'isin.csv', index_col='isin')
    rows = []
    for index, row in isins.iterrows():
        r = Stock(isin = index, name=row['name'])
        rows.append(r)
    source.addRows(rows)
    source.commit()

if session.query(Price).count() == 0:
    history = pd.read_csv(seedPath / 'history.csv', parse_dates=['date'], index_col=['date', 'isin'])
    history = history.groupby([pd.Grouper(level='date', freq='D'), pd.Grouper(level='isin')]).last()
    rows = []
    for index, row in history.iterrows():
        r = Price(isin = index[1], date=index[0], last=row['last'], low=row['low'], high=row['high'])
        rows.append(r)
    source.addRows(rows)
    source.commit()
