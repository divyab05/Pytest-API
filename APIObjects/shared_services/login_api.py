import json
import logging
import re
import pytest
import requests
from hamcrest import assert_that
from urllib3.exceptions import InsecureRequestWarning
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility


class LoginAPI:
    """This class defines the methods and element identifications for Login APIs."""

    def __init__(self, app_config):
        self.common = common_utils()
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.log = log_utils.custom_logger(logging.INFO)
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['login_api'])
        self.origin_url = str(self.app_config.env_cfg['login_origin_url'])
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }

    def user_account_claim(self, password, token):
        """
        This function posts a request to account claim login api for claiming the new user account.

        :param password: The password required to set for the first time.
        :param token: The token generated while inviting the new user account.

        :return: Response of user account claim login API.
        """

        account_claim_endpoint = self.endpoint + '/loginServices/v2/account/claim'
        self.headers['X-PB-Locale'] = 'en-us'
        self.headers['X-PB-TransactionId'] = '9978e071-2308-4c38-95d3-60b680def722-1649393216742'
        self.headers['origin'] = self.origin_url

        with open(self.prop.get('LOGIN_API', 'account_claim_body')) as f:
            self.json_data = json.load(f)
        self.json_data['password'] = password
        self.json_data['passwordConfirmation'] = password
        self.json_data['token'] = token
        payload = json.dumps(self.json_data)

        response = self.api.post_api_response(account_claim_endpoint, self.headers, payload)
        return response

    def login_to_foundation_user_credentials(self, username, password):
        """
        This function posts a request to login api for the given user credentials.

        :param username: The username or email of the user account.
        :param password: The password of the user account.

        :return: Response of user login API.
        """

        account_login_endpoint = self.endpoint + '/loginServices/v2/account/login'
        self.headers['Origin'] = self.origin_url

        with open(self.prop.get('LOGIN_API', 'account_login_body')) as f:
            self.json_data = json.load(f)
        self.json_data['username'] = username
        self.json_data['password'] = password
        payload = json.dumps(self.json_data)

        response = self.api.post_api_response(account_login_endpoint, self.headers, payload)
        return response

    def generate_session_token(self, username='', password='', sso_flag=False):
        if sso_flag:
            auth_url = self.app_config.logIn_cfg['idp_log_in_auth_url']
        else:
            auth_url = self.app_config.logIn_cfg['okta_log_in_auth_url']
        payload = '{"username":"' + username + '","password":"' + password + '"}'
        headers = {"Content-Type": "application/json"}

        response = self.api.post_api_response(endpoint=auth_url, headers=headers, body=payload)
        session_token = response.json()['sessionToken']
        return session_token

    def get_user_authentication(self, username='', password='', sso_flag=False, admin=True):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        session_token = self.generate_session_token(username=username, password=password, sso_flag=sso_flag)
        if admin:
            client_id = self.app_config.logIn_cfg['pbadm_client_id']
        else:
            client_id = self.app_config.logIn_cfg['client_id']

        auth_header = {"Authorization": "okta_client_credential"}
        authentication_url = self.app_config.logIn_cfg['okta_preview_auth_url']
        params = {'client_id': client_id,
                  'scope': self.app_config.logIn_cfg['scope'],
                  'response_type': self.app_config.logIn_cfg['response_type'],
                  'redirect_uri': self.app_config.logIn_cfg['redirect_uri'],
                  'nonce': self.app_config.logIn_cfg['nonce'],
                  'state': self.app_config.logIn_cfg['state'],
                  'response_mode': self.app_config.logIn_cfg['response_mode'],
                  'sessionToken': self.app_config.logIn_cfg['sessionToken'].replace('[tok]', session_token)}
        response = requests.get(authentication_url, headers=auth_header, params=params, verify=False)
        return response

    def get_access_token(self, admin=False):
        try:
            if admin:
                username = self.app_config.env_cfg['username']
            else:
                username = self.app_config.env_cfg['CLIENTUSERNAME']
            password = self.app_config.env_cfg['enc_pwd']

            auth_resp = self.get_user_authentication(username=username, password=password)
            html_data = auth_resp.content
            okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
            access_token = "Bearer {}".format(okta_token)
            return access_token

        except Exception as ex:
            self.log.error(f'Exception occurred while generating access token!\n{ex}')

    def get_access_token_for_user_credentials(self, username='', password='', sso_flag=False, admin=False):
        try:
            auth_resp = self.get_user_authentication(username=username, password=password, sso_flag=sso_flag, admin=admin)
            html_data = auth_resp.content
            okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
            access_token = "Bearer {}".format(okta_token)
            return access_token

        except Exception as ex:
            self.log.error(f'Exception occurred while generating access token!\n{ex}')

    def check_user_login_status(self, username='', password='', login_success=True, sso_flag=False, admin=False):
        """
        This method is to check whether user login is successful and any error post login.

        :param username: The username or email of the user account.
        :param password: The password of the user account.
        :param login_success: The flag to identify if the call expects the login should be successful or not.
        :param sso_flag: The flag to identify if the access token should be generated from idp-sso url.
        :param admin: The client_id differs for the admin user.

        :return: True or Failure based on the set flags.
        """

        self.login_to_foundation_user_credentials(username, password)

        auth_resp = self.get_user_authentication(username=username, password=password, sso_flag=sso_flag, admin=admin)
        html_data = auth_resp.content

        if re.findall('name="error" value="access_denied"', str(html_data)) and login_success:
            pytest.fail('Access Denied! User is not assigned to the client application.')
        elif re.findall('name="error" value="access_denied"', str(html_data)) and login_success == False:
            self.log.info(f"User {username} login is unsuccessful as expected!")
            return True
        else:
            self.log.info(f"User {username} login is successful!")
            return True

    def get_device_access_token(self, scope='spa'):
        okta_preview_host = self.app_config.logIn_cfg['okta_preview_host']
        id = self.app_config.logIn_cfg['id']
        query_param = '?scope=' + scope
        okta_preview_url = okta_preview_host + '/oauth2/' + id + '/v1/token' + query_param

        device_cli_id = str(self.app_config.env_cfg['device_cli_id'])
        device_cli_secret = str(self.app_config.env_cfg['device_cli_secret'])
        basic_auth = self.common.get_basic_auth(client_id=device_cli_id, client_secret=device_cli_secret)

        self.headers = {'Authorization': basic_auth,
                        'Content-Type': 'application/x-www-form-urlencoded'}

        payload = {'grant_type': 'client_credentials'}

        response = self.api.post_api_response(endpoint=okta_preview_url, headers=self.headers, body=payload)
        assert_that(self.common.validate_response_code(response, 200))

        device_token = response.json()['access_token']

        return device_token

