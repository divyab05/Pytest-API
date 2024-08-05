"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class UpdateFlow:
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

    def verify_update_reservation_based_on_unit(self, locker_bank, locker_unit, new_tracking_id, token_type, resource_type, kioskToken=None):
        """
        UpdateReservationBasedOnLockerID	/api/v1/lockerBank/{id}/lockers/{lockerID}/reservation/update
        This function validates the updation of reservation based unit.
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Update_Flow',
                                                                                      'body_path_update_reservation'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['assets'][0]['primaryTrackingID'] = new_tracking_id

        get_update_reservation_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reservation/update"
        get_update_reservation_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reservation/update/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_update_reservation_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_update_reservation_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_reservation_by_trackingID(self, locker_bank, old_trackingID, new_trackingID, token_type,
                                                resource_type):
        """
        UpdateReservation	/api/v1/lockerBank/{id}/lockers/reserved/{reservationID}
        This function validates the updation of locker unit by tracking id
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Update_Flow',
                                                                                      'body_path_update_reservation'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['assets'][0]['primaryTrackingID'] = new_trackingID

        get_update_reservation_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserved/" + old_trackingID
        get_update_reservation_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserved/" + old_trackingID + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_update_reservation_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_update_reservation_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_deposit_multiple_parcels(self, locker_bank, locker_unit, firstTracking, secondTracking, token_type,
                                        resource_type, kioskToken=None):
        """
        UpdateDeposit	/api/v1/lockerBank/{id}/lockers/{lockerID}/deposit
        This function validates the deposit of multiple parcels
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Update_Flow',
                                                                                      'body_path_multipleDeposit'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['parcels'][0]['primaryTrackingID'] = firstTracking
        self.json_data['parcels'][1]['primaryTrackingID'] = secondTracking

        get_multi_deposit_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/deposit"
        get_multi_deposit_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/deposit/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_multi_deposit_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_multi_deposit_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
