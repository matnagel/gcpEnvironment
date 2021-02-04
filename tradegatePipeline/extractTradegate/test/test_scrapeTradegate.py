from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

import sys
sys.modules['google.cloud.storage'] = MagicMock()

from scrapeTradegate import pubsubEntryPoint

@patch('builtins.print', Mock())
class testScrape(TestCase):
    def testMockRun(self):
        sqlSourcePatch = patch('scrapeTradegate.StdSource', MagicMock())
        with sqlSourcePatch:
            pubsubEntryPoint(None, None)

