from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from datetime import date, timedelta

import sys
sys.modules['google.cloud.storage'] = MagicMock()
sys.modules['requests'] = MagicMock()

from loadTradegate import pubsubEntryPoint

class Stock:
    def __init__(self, isin):
        self.isin = isin
        self.date = date.today() - timedelta(days=1)

class Query:
    def __init__(self, stockList):
        self.stockList = stockList
    def __iter__(self):
        return self.stockList.__iter__()
    def __next__(self):
        return self.stockList.__next__()
    def order_by(self, _):
        return self
    def first(self):
        return self.stockList[0]

class Page:
    def __init__(self):
        self.text = "Html content"

@patch('builtins.print', Mock())
class testScrape(TestCase):
    def testMockRun(self):
        source = Mock()
        source.query.return_value = Query([Stock('US3434'), Stock('DE78322')])
        sqlSourcePatch = patch('loadTradegate.StdSource', return_value=source)
        rqPatch = patch('loadTradegate.rq.get', return_value=Page())
        soupPatch = patch('loadTradegate.BeautifulSoup', MagicMock())
        with sqlSourcePatch, rqPatch, soupPatch:
            pubsubEntryPoint(None, None)

