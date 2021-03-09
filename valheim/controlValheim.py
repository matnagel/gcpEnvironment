from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

import base64

def readEventInformation(data):
    info = base64.b64decode(data['data']).decode('utf-8')
    return info

def pubsubEntryPoint(event, context):

    if not 'data' in event:
        raise RuntimeError('Called without message data in event.')

    message = readEventInformation(event)
    print(f"Valheim control: {message}")

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = os.getenv('GCP_PROJECT')
    # The name of the zone for this request.
    zone = os.getenv('GCP_ZONE')
    # Name of the instance resource to stop.
    instance = os.getenv('INSTANCE_NAME')

    if message == 'start':
        print("Starting Valheim instance")
        request = service.instances().start(project=project, zone=zone, instance=instance)
        response = request.execute()
        print(response)
    if message == 'stop':
        print("Stopping Valheim instance")
        request = service.instances().stop(project=project, zone=zone, instance=instance)
        response = request.execute()
        print(response)


