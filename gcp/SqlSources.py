import sqlalchemy

from sqlalchemy import Column, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from gcp.Engines import AlchemyEngine

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
    last = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    def __str__(self):
        return f'{self.isin} {self.date} - {self.last}'

class StdSource:
    def __init__(self):
        self.engine = AlchemyEngine()
        Session = sessionmaker(bind=self.engine.getEngine())
        self.session = Session()
    def dropAssociatedTables(self):
        Base.metadata.drop_all(self.engine.getEngine())
    def createAssociatedTables(self):
        Base.metadata.create_all(self.engine.getEngine(), Base.metadata.tables.values(), checkfirst=True)
    def getTableNames(self):
        return self.engine.getTableNames()
    def __str__(self):
        return f'SQLSource({self.engine})'
    def query(self, c):
        return self.session.query(c)
    def addRows(self, rows):
        self.session.add_all(rows)
    def commit(self):
        self.session.commit()
