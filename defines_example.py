import requests
import json

def getCreds():
    creds = dict()
    creds['access_token'] = ''
    creds['client_id'] = ''
    creds['client_secret'] = ''
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v8.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['debug'] = False
    creds['page_id'] = ''
    creds['instagram_account_id'] = ''
    
    return creds


def makeApiCall(url, endpointParams=None, debug=False):
    if endpointParams == None:
        data = requests.get(url)
    else:
        data = requests.get(url, endpointParams)
    
    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)
    
    if debug:
        displayApiCallData(response)
    
    return response

def displayApiCallData(response):
    print("\nURL: ")
    print(response['url'])
    print("\nEndpoint Params: ")
    print(response['endpoint_params_pretty'])
    print("\nResponse: ")
    print(response['json_data_pretty'])
    