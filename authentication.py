import json

import requests
import urllib3
from requests.exceptions import ConnectionError

urllib3.disable_warnings()


def get_auth_token(ip, username, password):
    token = None
    try:
        url = f'https://{username}:{password}@{ip}/api/tokenservices'
        headers = {'Content-Type': "application/json"}
        payload = ""
        print(f'REST API Trying to get token {ip}')
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        if response:
            token = response.headers['x-auth-token']
            return {
                'X-Auth-Token': token,
                'Content-Type': "application/json"}
        elif response.status_code == 401:
            print(f'REST API Failed login status code {response.status_code} Unauthorized')
        else:
            print(f'REST API No data returned')
    except ConnectionError:
        print(f'REST API Failed to establish connection')
