import os
import sqlalchemy

from sqlalchemy import Column, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Engines import myGCPEngine

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

class MyGCPDataSource:
    def __init__(self):
        self.engine = myGCPEngine
        Session = sessionmaker(bind=self.engine.getEngine())
        self.session = Session()
    def purgeDB(self):
        Base.metadata.drop_all(self.engine.getEngine())
    def constructDB(self):
        Base.metadata.create_all(self.engine.getEngine(), Base.metadata.tables.values(), checkfirst=True)
    def __str__(self):
        return f'{self.engine}'
    def addRows(self, rows):
        self.session.add_all(rows)
    def commit(self):
        self.session.commit()
    def getSession(self):
        return self.session

myGCPDataSource = MyGCPDataSource()
