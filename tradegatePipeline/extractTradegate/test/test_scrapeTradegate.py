from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

import sys
sys.modules['google.cloud.storage'] = MagicMock()
sys.modules['requests'] = MagicMock()

from gcp.Storage import Bucket
from scrapeTradegate import pubsubEntryPoint, loadListOfStocks

class Stock:
    def __init__(self, isin):
        self.isin = isin

class Page:
    def __init__(self):
        self.text = "Html content"

@patch('builtins.print', Mock())
class testScrape(TestCase):
    def testMockRun(self):
        source = Mock()
        source.query.return_value = [Stock('US3434'), Stock('DE78322')]
        rqPatch = patch('scrapeTradegate.rq.get', return_value=Page())
        #source.query().limit().return_value = ['US3434', 'DE78322']
        strIO = patch('gcp.Storage.StringIO', Mock)
        stockListPatch = patch('gcp.Storage.Bucket.readFromBlob', return_value="US02079K3059\nDE0005190003")
        with strIO, stockListPatch, rqPatch:
            pubsubEntryPoint(None, None)

    def testSplitText(self):
        stockListPatch = patch('gcp.Storage.Bucket.readFromBlob', return_value="US02079K3059\nDE0005190003")
        with stockListPatch:
            bucket = Bucket("tradegatescrapes")
            ls = loadListOfStocks(bucket)
            self.assertEqual(len(ls), 2) 

    def testNoISINStartsWithNumber(self):
        stockListPatch = patch('gcp.Storage.Bucket.readFromBlob', return_value="5US3434\n\nDE7832")
        with stockListPatch, self.assertRaises(ValueError):
            bucket = Bucket("tradegatescrapes")
            ls = loadListOfStocks(bucket)
