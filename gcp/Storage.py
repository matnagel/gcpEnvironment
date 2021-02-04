from google.cloud.storage import Client, Blob
from io import BytesIO, StringIO

from zipfile import ZipFile

def createZip(folder):
    zipMemory = BytesIO()
    zhandle = ZipFile(zipMemory, 'w')
    for fname, cont in folder.items():
        zhandle.writestr(fname, cont)
    zipMemory.seek(0)
    return zipMemory

class Bucket:
    def __init__(self, name):
        client = Client()
        self.bucket = client.get_bucket(name)
    def saveDictToZipBlob(self, blobname, folder):
        blob = Blob(blobname, self.bucket)
        zipfile = createZip(folder)
        blob.upload_from_file(zipfile)
    def saveStringToBlob(self, blobname, string):
        blob = Blob(blobname, self.bucket)
        content = StringIO(string)
        blob.upload_from_file(content)
