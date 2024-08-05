"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class ReserveWithPin:
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

    def verify_reserve_with_pin_locker_api(self, locker_bank, size, reservation_type, accessible, refrigeration,
                                           climate_type, TrackingID, receiver, depositor, departmentMail, flagRecipient,
                                           flagDepositor, token_type, resource_type, kioskToken=None):
        """
        ReserveLockerWithPin	/api/v1/lockerBank/{id}/lockers/reserveWithPin
        This function validates if a reservation has happened or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_ReserveWithPin_Flow', 'body_path_reserve_with_pin'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size
        self.json_data['reservationType'] = reservation_type
        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrackingID
        self.json_data['accessible'] = bool(accessible)
        self.json_data['refrigerated'] = bool(refrigeration)
        self.json_data['lockerType'] = climate_type

        if flagRecipient == 'personal':
            self.json_data['assetsReserved']['recipient']['recipientID'] = receiver
        elif flagRecipient == 'department':
            if departmentMail:
                self.json_data["departmentMail"] = bool(departmentMail)
                self.json_data['assetsReserved']['departmentCode'] = receiver
            else:
                self.json_data["departmentMail"] = bool("")
                self.json_data['assetsReserved']['departmentCode'] = receiver

        if flagDepositor == 'personal':
            self.json_data['assetsReserved']['depositor']['recipientID'] = depositor
            self.json_data['assetsReserved']['depositor']['departmentMail'] = bool("")
        elif flagDepositor == 'department':
            if departmentMail:
                self.json_data['assetsReserved']['depositor']['departmentMail'] = bool(departmentMail)
                self.json_data['assetsReserved']['depositor']['departmentCode'] = depositor
            else:
                self.json_data['assetsReserved']['depositor']['departmentMail'] = bool("")

        # if reservation_type == 'storageFlexible':
        #     self.json_data['reservationType'] = 'storage'
        #     now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        #     current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        #     self.json_data['expireReservedDate'] = current_time
        # elif reservation_type == 'storageFlexibleEndReservationError':
        #     self.json_data['reservationType'] = 'storage'
        #     self.json_data['expireReservedDate'] = '2000-01-01T12:12:12Z'

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

    def verify_reserve_with_pin_based_on_unit(self, locker_bank, locker_unit, size, reservation_type, accessible, refrigeration,
                                              climate_type, TrackingID, receiver, depositor, departmentMail, flagRecipient,
                                              flagDepositor, token_type, resource_type, kioskToken=None):
        """
        ReserveLockerWithPinBasedOnID	/api/v1/lockerBank/{id}/lockers/{lockerID}/reserveWithPin
        This function validates the reservation of a particular unit
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_ReserveWithPin_Flow', 'body_path_reserve_with_pin'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size
        self.json_data['reservationType'] = reservation_type
        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrackingID
        self.json_data['accessible'] = bool(accessible)
        self.json_data['refrigerated'] = bool(refrigeration)
        self.json_data['lockerType'] = climate_type

        if flagRecipient == 'personal':
            self.json_data['assetsReserved']['recipient']['recipientID'] = receiver
        elif flagRecipient == 'department':
            if departmentMail:
                self.json_data["departmentMail"] = bool(departmentMail)
                self.json_data['assetsReserved']['departmentCode'] = receiver
            else:
                self.json_data["departmentMail"] = bool("")
                self.json_data['assetsReserved']['departmentCode'] = receiver

        if flagDepositor == 'personal':
            self.json_data['assetsReserved']['depositor']['recipientID'] = depositor
            self.json_data['assetsReserved']['depositor']['departmentMail'] = bool("")
        elif flagDepositor == 'department':
            if departmentMail:
                self.json_data['assetsReserved']['depositor']['departmentMail'] = bool(departmentMail)
                self.json_data['assetsReserved']['depositor']['departmentCode'] = depositor
            else:
                self.json_data['assetsReserved']['depositor']['departmentMail'] = bool("")

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserveWithPin"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserveWithPin/" + self.invalid_path

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
