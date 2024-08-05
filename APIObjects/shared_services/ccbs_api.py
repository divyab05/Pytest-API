import json
import logging
import re
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities import Crypt
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils


class CCBSApi:

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.login = LoginAPI(app_config)
        self.prop = self.config.load_properties_file()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.endpoint = str(self.app_config.env_cfg['ccbs_api'])
        self.headers = {"Accept": "*/*"}
        self.authorization_value = Crypt.decode("DBENCRYPTIONKEY",
                                                str(self.app_config.env_cfg['ccbs_authorization']))
        self.token = self.generate_ccbs_token()

    def generate_ccbs_token(self):
        token = None
        oauth_token_endpoint = f"{self.endpoint}/oauth/token"
        self.headers = {"Authorization": self.authorization_value, "Content-Type": "text/plain"}
        body = 'grant_type=client_credentials'

        response = self.api.post_api_response(endpoint=oauth_token_endpoint, headers=self.headers, body=body)
        if response.status_code == 200:
            token = response.json().get('access_token')
            return token
        else:
            self.log.error(f"CCBS Token is not generated!\n{response.json()}")
        return token

    def get_user_profile_information_using_email_api(self, email=None, token=None):

        user_info_endpoint = f"{self.endpoint}/saase2e/reserved/v3/userServices/idp/users/{email}"
        self.headers = {"Authorization": f"Bearer {token if token else self.token}", "Content-Type": "application/json"}

        response = self.api.get_api_response(endpoint=user_info_endpoint, headers=self.headers)
        return response

    def get_user_profile_information_using_userid_api(self, user_id=None, token=None):

        user_info_endpoint = f"{self.endpoint}/saase2e/v3/userServices/users/{user_id}/info"
        self.headers['Authorization'] = f"Bearer {token if token else self.token}"

        response = self.api.get_api_response(endpoint=user_info_endpoint, headers=self.headers)
        return response

    def patch_update_user_email_api(self, email=None, new_email=None, token=None):

        if not email or not new_email:
            return None

        with open(self.prop.get('CCBS_USER_DATA', 'patch_update_user_profile_req')) as f:
            payload = json.load(f)

        if new_email:
            payload['profile']['email'] = new_email
            payload['profile']['username'] = new_email
            payload['profile']['login'] = new_email

        update_user_email_endpoint = f"{self.endpoint}/saase2e/reserved/v3/userServices/idp/users/{email}"
        self.headers = {"Authorization": f"Bearer {token if token else self.token}", "Content-Type": "application/json"}

        response = self.api.post_api_response(endpoint=update_user_email_endpoint,
                                              headers=self.headers, body=json.dumps(payload))
        return response

    @staticmethod
    def replace_email_domain(email='', new_domain=''):
        username, old_domain = re.match(r"([^@]+)@(.+)", email).groups()
        new_email = f"{username}@{new_domain}"
        return new_email
