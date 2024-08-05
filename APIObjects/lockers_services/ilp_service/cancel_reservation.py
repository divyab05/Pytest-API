"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class CancelReservation:
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

    def cancel_reservation_basedon_lockerunitID(self, locker_unit, locker_bank, token_type, resource_type, kioskToken=None):
        """
        FreeLocker	/api/v1/lockerBank/{id}/lockers/{lockerID}/free
        This function is validates the cancellation of a reservation by providing the locker unit
        :return: this function returns response and status code
         """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Cancel_Reservation',
                                                                                      'cancel_reservation_by_ID'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        cancel_reservation_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/free"
        cancel_reservation_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/free/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=cancel_reservation_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=cancel_reservation_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def cancel_reservation_by_trackingID(self, trackingID, locker_unit, locker_bank, token_type, resource_type, kioskToken=None):
        """
        CancelReservationBasedOnTrackingID	/api/v1/lockerBank/{id}/lockers/{lockerID}/free/reservation
        This function is validates the cancellation of a reservation by providing the locker unit and tracking ID
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Cancel_Reservation', 'cancel_reservation_byTrackingID'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['assets'][0]['primaryTrackingID'] = trackingID

        cancel_reservation_by_trackingID_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/free/reservation"
        cancel_reservation_by_trackingID_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/free/reservation/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=cancel_reservation_by_trackingID_endpoint, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=cancel_reservation_by_trackingID_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def free_list_of_locker_units(self, unit_one, unit_two, locker_bank, token_type, resource_type):
        """
        FreeLockers	/api/v1/lockerBank/{id}/lockers/free
        This function is validates the cancellation of a reservations
        :return: this function returns response and status code
         """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Cancel_Reservation',
                                                                                      'free_list_of_locker_units'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data["lockers"][0]["manufacturerLockerID"] = unit_one
        self.json_data["lockers"][1]["manufacturerLockerID"] = unit_two

        cancel_reservation_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/free"
        cancel_reservation_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/free/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=cancel_reservation_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=cancel_reservation_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
