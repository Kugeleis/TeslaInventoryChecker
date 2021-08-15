import http.client
import json
from types import SimpleNamespace

def get_token():
    conn = http.client.HTTPSConnection("www.tesla.com")
    payload = {
        "resource": "geocodesvc",
        "csrf_name": "",
        "csrf_value": ""
    }
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/inventory/api/v1/refresh_token", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    auth = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return auth.token

def decode_zip(token, zip_code, country_code):
    conn = http.client.HTTPSConnection("www.tesla.com")
    payload = {
        "token": token,
        "postal_code": zip_code,
        "country_code": country_code,
        "csrf_name": "",
        "csrf_value": ""
    }
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/inventory/api/v1/address", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    geo_result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    # Example Data:
    # {
    #     "city": "Montreal",
    #     "stateProvince": "Quebec",
    #     "postalCode": "H1K 3T2",
    #     "countryCode": "CA",
    #     "countryName": "Canada",
    #     "longitude": -73.5614205,
    #     "latitude": 45.60802700000001,
    #     "county": "Montreal",
    #     "stateCode": "QC"
    # }

    return geo_result.data