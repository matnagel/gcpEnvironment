import sqlalchemy

from sqlalchemy import Column, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from gcp.Engines import AlchemyEngine

import os

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

def constructConf(confKeys, defaults, env):
    result = dict()
    for key in confKeys:
        if key in env:
            result[key] = env[key]
        elif key in defaults:
            result[key] = defaults[key]
    return result

class StdSource:
    def __init__(self, conf=dict()):
        eConf = constructConf( \
                AlchemyEngine.getConfRequirements(), \
                {'DB_SOCKET_DIR': '/cloudsql'},
                os.environ)
        conf.update(eConf)
        missKeys = AlchemyEngine.getMissingConfRequirements(conf)
        if missKeys:
            raise Exception(f"Engine needs the keys: {missKeys}")

        self.engine = AlchemyEngine(conf)
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
    def addRow(self, row):
        self.session.add(row)
    def commit(self):
        self.session.commit()
    def tearDown(self):
        self.session.close()
