from unittest.mock import Mock
import sys
import types

module_name = 'googleapiclient'
bogus_module = types.ModuleType(module_name)
sys.modules[module_name] = bogus_module
bogus_module.discovery = Mock(name=module_name+'.discovery')
bogus_module.discovery.build = Mock(return_value='test')
