import logging
import json
import re
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities import Crypt
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility


class JitProvisioningAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.common = common_utils()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.endpoint = str(self.app_config.env_cfg['jit_service_api'])
        self.headers = {"Accept": "*/*"}
        self.jit_auth = Crypt.decode("DBENCRYPTIONKEY", str(self.app_config.env_cfg['jit_auth']))

    def post_update_user_details_via_jit_api(self, unique_id='', given_name='', family_name='', email='', user_id='',
                                             role='', location='', cost_center='', idp='', default_loc='true',
                                             user_status='EXTERNAL_PROVIDER', username=''):

        with open(self.prop.get('JIT_SERVICE', 'update_sso_user_details_via_jit_req_body')) as f:
            payload = json.load(f)

        if cost_center:
            cost_center = re.sub(r'\s+', ' ', cost_center)

        def set_payload_value(key, value):
            if value != '':
                payload[key] = value
            elif key in payload:  # Remove key if value is empty
                del payload[key]

        set_payload_value('custom:uniqueID', unique_id)
        set_payload_value('given_name', given_name)
        set_payload_value('family_name', family_name)
        set_payload_value('email', email)
        set_payload_value('custom:userId', user_id)
        set_payload_value('custom:role', role)
        set_payload_value('custom:location', location)
        set_payload_value('custom:costcenter', cost_center)
        set_payload_value('custom:identityProviderName', idp)
        set_payload_value('custom:defaultLoc', default_loc)
        set_payload_value('cognito:user_status', user_status)
        set_payload_value('username', username)

        update_sso_user_endpoint = f"{self.endpoint}/api/v1/federated/users"
        self.headers = {"Authorization": f"{self.jit_auth}",
                        "x-pb-source-idp": "COGNITO_SSO",
                        "Content-Type": "application/json"}

        response = self.api.post_api_response(endpoint=update_sso_user_endpoint,
                                              headers=self.headers, body=json.dumps(payload))
        return response
