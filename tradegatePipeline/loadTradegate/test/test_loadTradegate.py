from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from datetime import datetime

import sys
sys.modules['google.cloud'] = MagicMock()

from loadTradegate import filesToProcess, unzipFiles, \
        convertToWebpage, toPrice, saveToDB, laterThanCutOff, \
        loadTradegatePipeline
from apache_beam.testing.test_pipeline import TestPipeline
import apache_beam as beam

class testScrape(TestCase):
    def testBeam(self):
        cutOffDate = datetime.strptime('2021-02-14', "%Y-%m-%d")
        store = []
        mockStdSource = Mock()
        mockStdSource.addRow = lambda x: store.append(x)
        sqlPatch = patch('loadTradegate.StdSource', return_value=mockStdSource)
        bucketName = 'testBucket'
        with sqlPatch, TestPipeline() as p:
            pipe = p | loadTradegatePipeline(bucketName, cutOffDate)
        self.assertEqual(len(store), 2)
        fstore = list(filter(lambda price: price.isin == 'IE00B3RBWM25', store))
        self.assertEqual(len(fstore), 1)
