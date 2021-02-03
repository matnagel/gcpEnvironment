import base64
import json
import os
from googleapiclient import discovery

class EnvironmentException(Exception):
  pass

PROJECT_ID = os.getenv('GCP_PROJECT')

def readBillingInformation(data):
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    info = json.loads(pubsub_data)
    return info

def checkBilling(data, context):
    print('Check billing notification')

    if not 'data' in data:
        raise RuntimeError('Called without billing notification data.')

    info = readBillingInformation(data)
    cost_amount = info['costAmount']
    budget_amount = info['budgetAmount']

    billing = discovery.build(
        'cloudbilling',
        'v1',
        cache_discovery=False
    )
    projects = billing.projects()
    projectName = f'projects/{PROJECT_ID}'

    if PROJECT_ID is None:
        raise EnvironmentException('No project specified in environment variable GCP_PROJECT')

    print(f'Considering project: {PROJECT_ID}')

    if cost_amount > budget_amount:
        print(f'Current costs: {cost_amount} are larger than budget {budget_amount}')
        disableBilling(projectName, projects)
        return

    if 'alertThresholdExceeded' in info:
        print(f"Alert threshold {info['alertThresholdExceeded']} with costs {cost_amount} exceeded")
        disableBilling(projectName, projects)
        return

    if 'forecastThresholdExceeded' in info:
        print(f"Forecast threshold {info['forecastThresholdExceeded']} exceeded")
        disableBilling(projectName, projects)
        return

    billingStatus = isBillingEnabled(projectName, projects)
    print(f'No action necessary. Current cost: {cost_amount} and billingEnabled: {billingStatus}')

def disableBilling(projectName, projects):
    try:
        billingEnabled = isBillingEnabled(projectName, projects)
    except Exception:
        print(f'Unable to determine if billing is enabled on project {projectName}. Trying to disabling anyways.')
        disableBillingForProject(projectName, projects)
        raise RuntimeError('Could not determine whether billing is enabled, while trying to disable billing')

    if billingEnabled:
        disableBillingForProject(projectName, projects)
    else:
        print('Billing already disabled')

def isBillingEnabled(projectName, projects):
    """
    Determine whether billing is enabled for a project
    @param {string} projectName Name of project to check if billing is enabled
    @return {bool} Whether project has billing enabled or not
    """

    res = projects.getBillingInfo(name=projectName).execute()
    if 'billingEnabled' in res:
        return res['billingEnabled']
    else:
        # If billingEnabled isn't part of the return, billing is not enabled
        return False

def disableBillingForProject(projectName, projects):
    """
    Disable billing for a project by removing its billing account
    @param {string} projectName Name of project disable billing on
    """

    body = {'billingAccountName': ''}  # Disable billing
    try:
        res = projects.updateBillingInfo(name=projectName, body=body).execute()
        print(f'Billing disabled: {json.dumps(res)}')
    except Exception:
        raise RuntimeError('Failed to disable billing, possibly check permissions')
