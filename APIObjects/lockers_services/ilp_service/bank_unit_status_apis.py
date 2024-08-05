"""This module is used for main page objects."""
import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class StatusAPIs:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.access_token = "Bearer " + access_token

    def verify_update_locker_bank_status(self, locker_bank, delivery, token_type, resource_type,
                                         kioskToken=None):
        """
        UpdateBankStatus	/api/v1/lockerBank/{id}/status
        This function validates the updation of locker bank status
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Locker_Bank',
                                                                                      'body_path_update_bank_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['userID'] = "pravin.bankar"

        self.json_data['deliveryEnabled'] = bool(delivery)

        update_locker_bank_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/status"
        update_locker_bank_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/status/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=update_locker_bank_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=update_locker_bank_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_locker_bank_status(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetBankStatus	/api/v1/lockerBank/{id}/status
        This function validates if a locker bank status is successfully fetch or not
        :return: this function returns response and status code
        """
        get_locker_bank_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/status"
        get_locker_bank_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/status/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_bank_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_bank_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_locker_unit_status(self, locker_bank, locker_unit, enabled, token_type, resource_type,
                                         kioskToken=None):
        """
        UpdateLockerStatus	/api/v1/lockerBank/{id}/lockers/{lockerID}/status
        This function validates the updation of locker unit status
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Locker_Bank',
                                                                                      'body_path_update_unit_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['userID'] = "pravin.bankar"
        self.json_data['enabled'] = bool(enabled)

        update_locker_unit_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/status"
        update_locker_unit_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/status/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=update_locker_unit_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=update_locker_unit_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_locker_unit_status(self, locker_bank, locker_unit, token_type, resource_type):
        """
        GetLockerStatus	/api/v1/lockerBank/{id}/lockers/{lockerID}/status
        This function validates if a locker unit status is successfully fetch or not
        :return: this function returns response and status code
        """
        get_locker_unit_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/status"
        get_locker_unit_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_unit_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_unit_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_list_of_lockers(self, locker_bank, enabled, unit_one, unit_two, token_type, resource_type):
        """
        UpdateLockersStatus	/api/v1/lockerBank/{id}/lockers/status
        This function validates the updation of list of locker units
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Locker_Bank',
                                                                                      'body_path_update_listOfLocker_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['userID'] = "pravin.bankar"
        self.json_data["lockers"][0]["manufacturerLockerID"] = unit_one
        self.json_data["lockers"][1]["manufacturerLockerID"] = unit_two
        self.json_data['enabled'] = bool(enabled)

        update_listOfLocker_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/status"
        update_listOfLocker_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=update_listOfLocker_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=update_listOfLocker_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
