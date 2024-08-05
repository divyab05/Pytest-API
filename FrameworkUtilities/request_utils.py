import json
import requests.packages
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

'''
This method is used to send http requests using requests package and except below arguments
request_url: The End point/Base Url provided
params: parameters in dictionary provided for requests
headers: Headers provided for the api
body: request post body provided for post requests
method_type: Method type provided which can be post/put/get/delete/patch
others: Any other parameter required
'''


def send_request_based_on_http_method(request_url, params, headers, body, method_type, others):
    response = None
    response_data = {}
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    if method_type == "get":
        try:
            response = requests.get(request_url, headers=headers, params=params, timeout=15,
                                    verify=False)
        except requests.exceptions.Timeout as e:
            print("Requests Time out after 15 seconds")
            raise e.response
    elif method_type == "post":
        try:
            response = requests.post(url=request_url, json=json.loads(body), headers=headers, timeout=15, verify=False)
        except requests.exceptions.Timeout as e:
            print("Requests Time out after 15 seconds")
            raise e.response
    elif method_type == "put":
        try:
            response = requests.put(url=request_url, json=json.loads(body), headers=headers, timeout=15, verify=False)
        except requests.exceptions.Timeout as e:
            print("Requests Time out after 15 seconds")
            raise e.response
    elif method_type == "delete":
        try:
            response = requests.delete(request_url, headers=headers, params=params, timeout=15, verify=False)
        except requests.exceptions.Timeout as e:
            print("Requests Time out after 15 seconds")
            raise e.response

    response_data['response_code'] = response.status_code
    response_data['response_time'] = response.elapsed.total_seconds()
    if type(others) == str:
        response_data['response_body'] = response.text
    else:
        response_data['response_body'] = json.loads(response.text)
    return response_data


def device_token_generation(kioskToken):
    response = None
    response_data = {}
    try:
        response = requests.post(kioskToken['url'], auth=HTTPBasicAuth(kioskToken['clientID'], kioskToken['clientSecret']), data=kioskToken['body'])
    except requests.exceptions.Timeout as e:
        print("Requests Time out after 15 seconds")
        raise e.response

    response_data['response_code'] = response.status_code
    response_data['response_body'] = json.loads(response.text)

    return response_data


def generate_token_for_hbc_flows(hbc_authorization_key):
    payload = {}
    response_data = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{arg1}{arg2}'.format(arg1="Basic ", arg2=hbc_authorization_key['authorization_header'])
    }
    try:
        response = requests.request("POST", hbc_authorization_key['token_url'], headers=headers, data=payload)
    except requests.exceptions.Timeout as e:
        print("Requests Time out after 15 seconds")
        raise e.response

    response_data['response_code'] = response.status_code
    response_data['response_body'] = json.loads(response.text)

    return response_data
