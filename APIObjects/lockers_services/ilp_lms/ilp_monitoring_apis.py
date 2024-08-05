import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class ilpLMS:
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, client_token, admin_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['ilp_lms'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.client_access_token = "Bearer " + client_token
        self.admin_token = "Bearer " + admin_token

    def get_live_status(self, token_type, resource_type, token=None, sendToken=None):
        """
        GetAllLockerBanksHealthStatus	/api/v1/lms/lockerBanks/status/live
        This function gets status of locker banks
        :return: this function returns response and status code
        """

        get_live_status_endpoint = self.endpoint + '/api/v1/lms/lockerBanks/status/live'
        get_live_status_endpoint_invalid = self.endpoint + '/api/v1/lms/lockerBanks/status/live' + self.invalid_path

        if token == 'admin':
            self.access_token = self.admin_token
        elif token == 'device':
            self.access_token = sendToken
        else:
            self.access_token = self.client_access_token

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_live_status_endpoint, headers=headers_update)
            status_code = res.status_code
        else:
            res = self.api.get_api_response(
                endpoint=get_live_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        # self.log.info(res)
        return res, status_code
