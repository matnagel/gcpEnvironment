from google.cloud.storage import Client, Blob
from io import BytesIO, StringIO

from zipfile import ZipFile, ZIP_DEFLATED

def createZip(folder):
    zipMemory = BytesIO()
    with ZipFile(zipMemory, 'w', ZIP_DEFLATED) as zhandle:
        for fname, cont in folder.items():
            zhandle.writestr(fname, cont)
    #zhandle.close()
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
    def readFromBlob(self, blobname):
        blob = self.bucket.get_blob(blobname)
        if not blob:
            raise ValueError(f"Could not get blob for {blobname}")
        with blob.open("rt") as f:
            text = f.read()
        return text
