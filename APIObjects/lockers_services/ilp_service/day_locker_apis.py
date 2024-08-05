"""This module is used for main page objects."""

import json
import logging
import platform
import datetime

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class DayLocker:
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

    def verify_reserve_day_locker(self, locker_bank, size, reservation_type, accessible, refrigeration,
                                  climate_type, TrackingID, receiver, personalID, expireReservedDate,
                                  token_type, resource_type, kioskToken=None):
        """
        ReserveLockerWithPin	/api/v1/lockerBank/{id}/lockers/reserveWithPin
        This function validates reservation for a day locker
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Day_Locker', 'reserve_daylocker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size
        self.json_data['reservationType'] = reservation_type
        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrackingID
        self.json_data['assetsReserved']['recipient']['recipientID'] = receiver
        self.json_data['assetsReserved']['recipient']['personalID'] = personalID
        self.json_data['expireReservedDate'] = expireReservedDate
        self.json_data['accessible'] = bool(accessible)
        self.json_data['refrigerated'] = bool(refrigeration)
        self.json_data['lockerType'] = climate_type

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserveWithPin"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserveWithPin/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def authenticate_day_locker(self, locker_bank, access_code, token_type, resource_type, kioskToken=None):
        """
        AuthDayLockerBasedOnCode	/api/v1/lockerBank/{id}/authDayLocker
        This function validates the authentication of a day locker using pid and access code
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Day_Locker', 'authenticate_daylocker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['accessCode'] = access_code

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/authDayLocker"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/authDayLocker" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def day_locker_pre_reservation(self, locker_bank, Name, EmailID, token_type, resource_type, kioskToken=None):
        """
        VerifyVisitor	/api/v1/lockerBank/{id}/pre/reservation
        This function validates the recipient is existing  record or new one and along with his reservation details
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Day_Locker', 'pre_reservation_daylocker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['name'] = str(Name)
        self.json_data['email'] = str(EmailID)

        pre_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pre/reservation"
        pre_reserve_endpoint_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pre/reservation" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=pre_reserve_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=pre_reserve_endpoint_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def get_locker_management_unit_allocation(self, locker_bank, token_type, resource_type):
        """
        GetLockersManagement	/api/v1/lockerBank/{id}/lockersManagement
        This function validates the get unit management api of a locker bank
        :returns: response and status code
        """
        get_locker_management_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockersManagement"
        get_locker_management_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockersManagement/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_locker_management_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_management_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def post_locker_management_unit_allocation(self,  locker_bank, body_json, requestedCount, token_type, resource_type):
        """
        AddLockersManagement	/api/v1/lockerBank/{id}/lockersManagement
        This function validates the post unit management api of a locker bank
        :returns: response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data = json.loads(json.dumps(body_json))
        self.json_data['deliveryUnits'][0]['count']['countRequested'] = requestedCount

        post_locker_management_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockersManagement"
        post_locker_management_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockersManagement/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(endpoint=post_locker_management_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(endpoint=post_locker_management_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
