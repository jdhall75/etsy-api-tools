import requests
import json

CK_BASE_URL = 'https://api.convertkit.com/v3'
HEADERS = {
    'user-agent': 'pyRequests 0.1.0',
    'Content-Type': 'application/json; charset=utf-8'
}
# functions to add subscribers via the forms api in convertkit


def add_subscriber(form_id, api_key=None, sub_data=None):
    # method post
    uri = f'/forms/{form_id}/subscribe'

    if api_key:
        sub_data['api_key'] = api_key

    if isinstance(dict, sub_data):


    resp = requests.post(CK_BASE_URL + uri, data=sub_data)
