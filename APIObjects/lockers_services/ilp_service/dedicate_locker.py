"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class DedicateLocker:
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

    def verify_add_dedicated_locker(self, locker_bank, recipientFlag, recipientID, token_type, resource_type, Locker_unit):
        """
        AddDedicatedLockers	/api/v1/lockerBank/{id}/dedicatedLockers/{dedicatedID}
        This function validates adding of dedicated locker
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Dedicated_Locker', 'body_path_dedicated_locker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['units'][0]['manufacturerLockerID'] = str(Locker_unit)
        self.json_data["recipientEnabled"] = bool(recipientFlag)

        get_dedicated_locker_assigned_to_recipient_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID
        get_dedicated_locker_assigned_to_recipient_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_dedicated_locker_assigned_to_recipient_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_dedicated_locker_assigned_to_recipient_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_dedicated_locker_unit(self, locker_bank, recipientID, token_type, resource_type):
        """
        GetDedicatedLockerStatus	/api/v1/lockerBank/{id}/dedicatedLocker/status
        This function validates the assignment of dedicated locker
        :return: this function returns response and status code
        """
        get_dedicated_locker_unit_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID
        get_dedicated_locker_unit_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_dedicated_locker_unit_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_dedicated_locker_unit_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_dedicate_locker(self, locker_bank, recipientFlag, recipientID, token_type, resource_type, Locker_unit):
        """
        UpdateDedicatedLockers	/api/v1/lockerBank/{id}/dedicatedLockers/{dedicatedID}
        This function validates the updation of dedicated locker
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Dedicated_Locker', 'update_dedicated_locker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['units'][0]['manufacturerLockerID'] = str(Locker_unit)
        self.json_data["recipientEnabled"] = bool(recipientFlag)

        get_update_dedicated_locker_to_recipient_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID
        get_update_dedicated_locker_to_recipient_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_update_dedicated_locker_to_recipient_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_update_dedicated_locker_to_recipient_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_remove_dedicate_locker(self, context, locker_bank, recipientID, token_type, resource_type):
        """
        FreeDedicatedLockers	/api/v1/lockerBank/{id}/dedicatedLockers/{dedicatedID}
        This function is validates the removal of dedicated locker
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Dedicated_Locker', 'remove_dedicated_locker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['units'][0]['manufacturerLockerID'] = context['manufacturerLockerID1']
        self.json_data['units'][1]['manufacturerLockerID'] = context['manufacturerLockerID2']

        get_removal_of_dedicated_locker_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID
        get_removal_of_dedicated_locker_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLockers/" + recipientID + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.put_api_response(
                endpoint=get_removal_of_dedicated_locker_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.put_api_response(
                endpoint=get_removal_of_dedicated_locker_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_dedicated_locker_status(self, locker_bank, status, token_type, resource_type):
        """
        UpdateDedicatedLockerStatus	/api/v1/lockerBank/{id}/dedicatedLocker/status
        This function is validates the status of dedicated locker in bank
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Dedicated_Locker', 'update_dedicated_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['status'] = bool(status)

        get_update_dedicated_locker_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLocker/status"
        get_update_dedicated_locker_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLocker/status" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_update_dedicated_locker_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_update_dedicated_locker_status_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_dedicated_locker_status(self, locker_bank, token_type, resource_type):
        """
        GetDedicatedLockerStatus	/api/v1/lockerBank/{id}/dedicatedLocker/status
        This function validates the status of dedicated locker in bank
        :return: this function returns response and status code
        """
        get_dedicated_locker_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLocker/status"
        get_dedicated_locker_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/dedicatedLocker/status" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_dedicated_locker_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_dedicated_locker_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
