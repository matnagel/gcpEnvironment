from google.cloud.storage import Client, Blob
from io import StringIO


class Bucket:
    def __init__(self, name):
        client = Client()
        self.bucket = client.get_bucket(name)
    def saveStringToBlob(self, blobname, string):
        blob = Blob(blobname, bucket)
        content = StringIO(string)
        blob.upload_from_file(content)
