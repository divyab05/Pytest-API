"""This module is used for main page objects."""
import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.db_utils import DbUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class vendorapitool:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = "Bearer " + access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.env = self.app_config.env_cfg['env'].lower()

    def verify_getlocker_onboring_status(self, manufacturerHardwareID, token_type, resource_type, kioskToken=None):
        """
        Get onbording status /api/v1/lockerBank/ManufactuerhardwareID/onBoardingStatus
        This function validates if get locker bank onording status fetched successfully
        :return: this function returns response and status code
        """

        get_locker_plan_endpoint = self.endpoint + "/api/v1/lockerBank/" + manufacturerHardwareID + "/onBoardingStatus"
        get_locker_plan_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + manufacturerHardwareID + "/" + self.invalid_path

        if kioskToken is not None:
            device_token = kioskToken['basic_device_token']
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, device_token)
        else:
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_plan_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_plan_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code