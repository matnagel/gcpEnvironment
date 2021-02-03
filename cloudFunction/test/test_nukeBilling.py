import unittest
from unittest.mock import patch, Mock
import mockgoogleapi
from nukeBilling import checkBilling, EnvironmentException


enoughBudget = patch('nukeBilling.readBillingInformation', return_value = {'costAmount':50, 'budgetAmount':100})
overBudget = patch('nukeBilling.readBillingInformation', return_value = {'costAmount':5, 'budgetAmount':1})
alertBudget = patch('nukeBilling.readBillingInformation', return_value = {'costAmount':50, 'budgetAmount':100, 'alertThresholdExceeded': 0.7})
fcBudget = patch('nukeBilling.readBillingInformation', return_value = {'costAmount':50, 'budgetAmount':100, 'forecastThresholdExceeded': 0.7})

envVar = patch('nukeBilling.PROJECT_ID', 'project-8939583')
suppressPrint = patch('builtins.print', Mock())
json = patch('json.dumps', return_value =  None)

class BillingDisabled:
    def execute(self):
        return {'billingEnabled':False}

class BillingEnabled:
    def execute(self):
        return {'billingEnabled':True}

class BillingException:
    def execute(self):
        raise Exception('Could not get billing information')

class testNuke(unittest.TestCase):
    def discoveryWith(self, Projects):
        billing = Mock()
        projects = billing.projects.return_value
        projects.getBillingInfo.return_value = Projects()
        self.projects = projects
        return patch('nukeBilling.discovery.build', return_value = billing)
    def test_MissingEnvironment(self):
        with enoughBudget, self.discoveryWith(BillingEnabled), suppressPrint:
            self.assertRaises(EnvironmentException, checkBilling, ['data'], None)
    def test_BillingException(self):
        with envVar, overBudget, self.discoveryWith(BillingException), suppressPrint:
            self.assertRaises(RuntimeError, checkBilling, ['data'], None)
            self.projects.updateBillingInfo.assert_called()
    def test_EnoughBudget(self):
        with envVar, enoughBudget, self.discoveryWith(BillingEnabled), suppressPrint:
            checkBilling(['data'], None)
            self.projects.updateBillingInfo.assert_not_called()
    def test_OverBudget(self):
        with envVar, overBudget, self.discoveryWith(BillingEnabled), suppressPrint, json:
            checkBilling(['data'], None)
            self.projects.updateBillingInfo.assert_called()
    def test_OverBudgetBillDis(self):
        with envVar, overBudget, self.discoveryWith(BillingDisabled), suppressPrint, json:
            checkBilling(['data'], None)
            self.projects.updateBillingInfo.assert_not_called()
    def test_Alert(self):
        with envVar, alertBudget, self.discoveryWith(BillingEnabled), suppressPrint, json:
            checkBilling(['data'], None)
            self.projects.updateBillingInfo.assert_called()
    def test_ForecastAlert(self):
        with envVar, fcBudget, self.discoveryWith(BillingEnabled), suppressPrint, json:
            checkBilling(['data'], None)
            self.projects.updateBillingInfo.assert_called()
