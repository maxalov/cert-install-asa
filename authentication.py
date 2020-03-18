import json

import requests
import urllib3

urllib3.disable_warnings()


def get_auth_token(ip, username, password):
    token = None
    url = f'https://{username}:{password}@{ip}/api/tokenservices'
    headers = {'Content-Type': "application/json"}
    payload = ""
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    if not response:
        print("No Data returned")
    else:
        token = response.headers['x-auth-token']
    return {
        'X-Auth-Token': token,
        'Content-Type': "application/json"}
