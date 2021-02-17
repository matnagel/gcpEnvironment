from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from datetime import date, timedelta

import sys
sys.modules['google.cloud'] = MagicMock()

from loadTradegate import filesToProcess, unzipFiles, \
        convertToWebpage, toPrice, saveToDB
from apache_beam.testing.test_pipeline import TestPipeline
import apache_beam as beam

class testScrape(TestCase):
    def testBeam(self):
        mockStdSource = Mock()
        sqlPatch = patch('loadTradegate.StdSource', return_value=mockStdSource)
        bucketName = 'testBucket'
        with sqlPatch, TestPipeline() as p:
            pipe = p | filesToProcess(bucketName) \
              | beam.FlatMap(unzipFiles) \
              | beam.Map(convertToWebpage) \
              | beam.Map(toPrice) \
              | beam.ParDo(saveToDB()) \
              | beam.Map(print)
        mockStdSource.addRow.assert_called()
