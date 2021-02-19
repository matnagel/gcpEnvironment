import os
import sqlalchemy

class AlchemyEngine():
    def __init__(self, conf):
        self.db_user = conf["DB_USER"]
        self.db_pass = conf["DB_PASS"]
        self.db_name = conf["DB_NAME"]
        self.db_socket_dir = conf["DB_SOCKET_DIR"]
        self.cloud_sql_connection_name = conf["CLOUD_SQL_CONNECTION_NAME"]
        self.socketPath = f'{self.db_socket_dir}/{self.cloud_sql_connection_name}'
        self._constructEngine()
    def _constructEngine(self):
        engineDef = sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=self.db_user,  # e.g. "my-database-user"
            password=self.db_pass,  # e.g. "my-database-password"
            database=self.db_name,  # e.g. "my-database-name"
            query={ "unix_socket": self.socketPath })
        self.engine = sqlalchemy.create_engine(engineDef, echo=False)
    def getTableNames(self):
        return self.engine.table_names()
    def getEngine(self):
        return self.engine
    def __str__(self):
        return f'Engine({self.socketPath})'
    def getConfRequirements():
        return ['DB_USER', 'DB_PASS', 'DB_NAME', 'DB_SOCKET_DIR',\
                'CLOUD_SQL_CONNECTION_NAME']
    def getMissingConfRequirements(conf):
        missing = []
        for key in AlchemyEngine.getConfRequirements():
            if not key in conf:
                missing.append(key)
        return missing

