from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

import sys
sys.modules['google.cloud'] = MagicMock()
sys.modules['flask'] = MagicMock()

from main import checkValheimPreconditions

class testScrape(TestCase):
    def testMockRun(self):
        #source = Mock()
        #source.query.return_value = [Stock('US3434'), Stock('DE78322')]
        #sqlSourcePatch = patch('scrapeTradegate.StdSource', return_value=source)
        #rqPatch = patch('scrapeTradegate.rq.get', return_value=Page())
        ##source.query().limit().return_value = ['US3434', 'DE78322']
        envPatch = patch('os.getenv', return_value = 'testSecret')
        with envPatch:
            test = checkValheimPreconditions('testSecret')
