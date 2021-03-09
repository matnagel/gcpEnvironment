from datetime import date
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import os

def pubsubEntryPoint(event, context):
    print("Valheim control")

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = os.getenv('GCP_PROJECT')
    # The name of the zone for this request.
    zone = os.getenv('GCP_ZONE')
    # Name of the instance resource to stop.
    instance = os.getenv('INSTANCE_NAME')
    request = service.instances().stop(project=project, zone=zone, instance=instance)
    response = request.execute()
