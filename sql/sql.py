import os
import sqlalchemy

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'tracked_stocks'
    isin = Column(String, primary_key = True)
    name = Column(String)

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "sqlproxy")
cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]


socketPath = f'{db_socket_dir}/{cloud_sql_connection_name}'
print(f'Connecting using socket {socketPath}')

engineDef = sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={ "unix_socket": socketPath })

engine = sqlalchemy.create_engine(engineDef, echo=True)
Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
