import os
import sqlalchemy

class AlchemyEngineConfiguration:
    def __init__(self, configuration):
        configuration.update(
                AlchemyEngineConfiguration.getComplementaryConf(self.requiredKeys, self.defaultDict, os.environ))
        self.configuration = configuration
        missingKeys = self.getMissingKeys()
        if missingKeys:
            raise ValueError(f"Missing keys={missingKeys}")

    def getMissingKeys(self):
        missing = []
        for key in self.requiredKeys:
            if not key in self.configuration:
                missing.append(key)
        return missing

    def getComplementaryConf(confKeys, defaults, env):
        result = dict()
        for key in confKeys:
            if key in env:
                result[key] = env[key]
            elif key in defaults:
                result[key] = defaults[key]
        return result

    def __getitem__(self, key):
        return self.configuration[key]

    def fromDict(configuration):
        if 'HOST' in configuration:
            return TCPConfiguration(configuration)
        else:
            return SocketConfiguration(configuration)

class SocketConfiguration(AlchemyEngineConfiguration):
    requiredKeys = ['DB_USER', 'DB_PASS', 'DB_NAME', 'DB_SOCKET_DIR',\
                'CLOUD_SQL_CONNECTION_NAME']
    defaultDict = {'DB_SOCKET_DIR': '/cloudsql'}
    def getEngineDef(self):
        socketDir = self["DB_SOCKET_DIR"]
        cloudConnectionName = self["CLOUD_SQL_CONNECTION_NAME"]
        socketPath = f'{socketDir}/{cloudConnectionName}'
        engineDef = sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=self["DB_USER"],  # e.g. "my-database-user"
            password=self["DB_PASS"],  # e.g. "my-database-password"
            database=self["DB_NAME"],  # e.g. "my-database-name"
            query={ "unix_socket": socketPath })
        return engineDef

class TCPConfiguration(AlchemyEngineConfiguration):
    requiredKeys = ['DB_USER', 'DB_PASS', 'DB_NAME', 'HOST', 'PORT']
    defaultDict = {}
    def getEngineDef(self):
        engineDef = sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=self["DB_USER"],  # e.g. "my-database-user"
            password=self["DB_PASS"],  # e.g. "my-database-password"
            database=self["DB_NAME"],  # e.g. "my-database-name"
            host=self['HOST'],
            port=self['PORT'])
        return engineDef


class AlchemyEngine():
    def __init__(self, conf):
        self.conf = conf
        self._constructEngine()
    def _constructEngine(self):
        engineDef = self.conf.getEngineDef()
        self.engine = sqlalchemy.create_engine(engineDef, echo=False)
    def getTableNames(self):
        return self.engine.table_names()
    def getEngine(self):
        return self.engine
    def __str__(self):
        return f'Engine({self.socketPath})'
