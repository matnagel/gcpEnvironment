"""Create Stock and Price tables

Revision ID: 5d4bf47b3ed0
Revises:
Create Date: 2021-01-30 12:56:15.754519

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Date, Float


import os
import pandas as pd
import datetime as dt
from pathlib import Path

Session = sessionmaker()
Base = declarative_base()

class Stock(Base):
    __tablename__ = 'tracked_stocks'
    isin = Column(String(12), primary_key = True)
    name = Column(String(20))
    def __str__(self):
        return f'{self.name}'

class Price(Base):
    __tablename__ = 'stock_prices'
    isin = Column(String(12), primary_key = True)
    date = Column(Date, primary_key = True)
    last = Column(Float)
    low = Column(Float)
    high = Column(Float)
    def __str__(self):
        return f'{self.isin} {self.date} - {self.last}'

seedPath = Path(os.environ["GCP_DATA_PATH"]) / 'seedData'

# revision identifiers, used by Alembic.
revision = '5d4bf47b3ed0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    engine = op.get_bind()
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    createStockTable(session)
    createPriceTable(session)
    session.commit()

def downgrade():
    engine = op.get_bind()
    Base.metadata.drop_all(bind=engine)
    pass

def createStockTable(session):
    assert session.query(Stock).count() == 0
    isins = pd.read_csv(seedPath / 'isin.csv', index_col='isin')
    rows = []
    for index, row in isins.iterrows():
        r = Stock(isin = index, name=row['name'])
        rows.append(r)
    session.add_all(rows)

def createPriceTable(session):
    assert session.query(Price).count() == 0
    history = pd.read_csv(seedPath / 'history.csv', parse_dates=['date'], index_col=['date', 'isin'])
    history = history.groupby([pd.Grouper(level='date', freq='D'), pd.Grouper(level='isin')]).last()
    rows = []
    for index, row in history.iterrows():
        r = Price(isin = index[1], date=index[0], last=row['last'], low=row['low'], high=row['high'])
        rows.append(r)
    session.add_all(rows)
