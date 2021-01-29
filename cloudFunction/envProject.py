import os

class EnviromentException(Exception):
  pass

def findEnv(data, context):
    print('Checking if project id is automatically set')


    PROJECT_ID = os.getenv('GCP_PROJECT')
    if PROJECT_ID is None:
        raise EnvironmentException('No project specified in environment variable GCP_PROJECT')

    print(f'Project ID found: {PROJECT_ID}')
