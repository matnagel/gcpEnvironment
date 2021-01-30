import os
import sqlalchemy

class MyGCPEngine():
    def __init__(self):
        self._getConfiguration()
        self._constructEngine()
    def _getConfiguration(self):
        self.db_user = os.environ["DB_USER"]
        self.db_pass = os.environ["DB_PASS"]
        self.db_name = os.environ["DB_NAME"]
        self.db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudproxy")
        self.cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
        self.socketPath = f'{self.db_socket_dir}/{self.cloud_sql_connection_name}'
    def _constructEngine(self):
        engineDef = sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=self.db_user,  # e.g. "my-database-user"
            password=self.db_pass,  # e.g. "my-database-password"
            database=self.db_name,  # e.g. "my-database-name"
            query={ "unix_socket": self.socketPath })
        self.engine = sqlalchemy.create_engine(engineDef, echo=False)
    def getEngine(self):
        return self.engine
    def __str__():
        return f'Engine({self.socketPath})'

myGCPEngine = MyGCPEngine()
