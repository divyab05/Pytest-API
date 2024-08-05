"""This module is used for main page objects."""

import datetime
import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class LockerAPI:

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

    def verify_Lockerbank_details(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetBank	/api/v1/lockerBank/{id}
        This function validates if a locker bank details are fetched successfully
        :return: this function returns response and status code
        """

        get_locker_plan_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank
        get_locker_plan_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
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

    def verify_reserve_locker_api(self, locker_bank, size, accessible, refrigeration, climate_type,
                                  TrkgID, EmailID, recipientID, token_type, resource_type, kioskToken=None, token=None):
        """
        ReserveLocker	/api/v1/lockerBank/{id}/lockers/reserve
        This function validates if a reservation has happened or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow', 'body_path_reserve'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size

        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID

        if TrkgID.startswith("SSTO"):
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"__SSTO"

        if TrkgID.startswith("Fireball"):
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"_fireball"

        self.json_data['accessible'] = bool(accessible)
        self.json_data['refrigerated'] = bool(refrigeration)
        self.json_data['lockerType'] = climate_type

        if EmailID != "":
            self.json_data['assetsReserved']['recipient']['email'] = EmailID

        if recipientID != "":
            self.json_data['assetsReserved']['recipient']['recipientID'] = recipientID

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserve"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserve/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        elif token is not None:
            self.access_token = token
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

    def verify_get_reserved_locker_based_on_trackingID(self, trackingID, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetReservedLocker	/api/v1/lockerBank/{id}/lockers/reserved/{reservationID}
        This function validates the reservation based on trackingID
        :return: this function returns response and status code
        """
        get_reserved_locker_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserved/" + trackingID
        get_reserved_locker_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserved/" + trackingID + "/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_reserved_locker_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_reserved_locker_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_reserved_V2(self, locker_bank, recipientID, token_type, resource_type, kioskToken=None):
        """
        GetReservedLockers	/api/v1/lockerBank/{id}/lockers/reservedV2/{reservationID}
        This function validates the reserved unit assigned to recipient
        :return: this function returns response and status code
        """
        get_sites_based_on_tenantID_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reservedV2/" + recipientID
        get_sites_based_on_tenantID_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reservedV2/" + recipientID + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_sites_based_on_tenantID_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_sites_based_on_tenantID_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_deposit_locker_api(self, trackingID, locker_unit, locker_bank, token_type, resource_type, kioskToken=None, token=None):
        """
        UpdateDeposit	/api/v1/lockerBank/{id}/lockers/{lockerID}/deposit
        This function validates if a deposit has happened or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow', 'body_path_Deposit'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['parcels'][0]['primaryTrackingID'] = trackingID

        if trackingID.startswith("SSTO"):
            self.json_data['parcels'][0]['secondaryTrackingID'] = trackingID + "__SSTO"

        if trackingID.startswith("Fireball"):
            self.json_data['parcels'][0]['secondaryTrackingID'] = trackingID + "_fireball"

        get_locker_deposit_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/deposit"
        get_locker_deposit_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/deposit/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        elif token is not None:
            self.access_token = token
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_locker_deposit_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=get_locker_deposit_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_authenticate_Pickup_api(self, access_code, locker_bank, token_type, resource_type, kioskToken=None):
        """
        AuthenticatePickupBasedOnCode	/api/v1/lockerBank/{id}/lockers/pickup/authenticateCode or authenticateV2
        This function validates the authentication for pickup is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow', 'body_path_authenticate'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['accessCode'] = access_code

        get_locker_authenticate_pickup_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/pickup/authenticateCode"
        get_locker_authenticate_pickup_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/pickup/authenticateCode/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_pickup_locker_api(self, access_code, locker_unit, locker_bank, token_type, resource_type, staleMailPickup, kioskToken=None, token=None):
        """
        MultiplePickup	/api/v1/lockerBank/{id}/lockers/multiPickup
        This function validates the pickup from a locker is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow', 'body_path_pickup'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        now = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.json_data['pickupDate'] = current_time
        self.json_data['staleMailPickup'] = bool(staleMailPickup)
        self.json_data['pickupRequests'][0]['manufacturerLockerID'] = locker_unit
        self.json_data['pickupRequests'][0]['accesscode'] = access_code

        get_locker_pickup_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/multiPickup"
        get_locker_pickup_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/multiPickup/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        elif token is not None:
            self.access_token = token
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_reservation_based_on_unit(self, locker_bank, locker_unit, size, accessible, refrigeration, climate_type,
                                         TrkgID, EmailID, recipientID, token_type, resource_type, kioskToken=None):
        """
        ReserveLockerBasedOnID	/api/v1/lockerBank/{id}/lockers/{lockerID}/reserve
        This function validates the reservation of a particular unit
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow',
                                                                                      'body_path_reserve'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size

        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID

        if TrkgID.startswith("SSTO"):
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"__SSTO"

        if TrkgID.startswith("Fireball"):
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"_fireball"

        self.json_data['accessible'] = bool(accessible)
        self.json_data['refrigerated'] = bool(refrigeration)
        self.json_data['lockerType'] = climate_type

        if EmailID != "":
            self.json_data['assetsReserved']['recipient']['email'] = EmailID

        if recipientID != "":
            self.json_data['assetsReserved']['recipient']['recipientID'] = recipientID

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserve"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserve/" + self.invalid_path

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

    def verify_get_unique_tracking_id(self, locker_bank, tracking_id, token_type, resource_type):
        """
        GetUniqueReservationStatusAtBank	/api/v1/lockerBank/{id}/lockers/unique/{reservationID}
        This function will validate if the tracking id is unique or not
        :return: this function returns response and status code
        """

        get_unique_trackingID_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/unique/" + tracking_id
        get_unique_trackingID_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/unique/" + tracking_id + "/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_unique_trackingID_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_unique_trackingID_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_authenticate_Pickup_api_v1(self, access_code, locker_bank, token_type, resource_type):
        """
        AuthenticatePickup	/api/v1/lockerBank/{id}/lockers/pickup/authenticate
        This function validates the authentication for pickup is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow',
                                                                                      'body_path_authenticate'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['accessCode'] = access_code

        get_locker_authenticate_pickup_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/pickup/authenticate"
        get_locker_authenticate_pickup_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/pickup/authenticate/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_normal_pickup_locker_api(self, access_code, locker_unit, locker_bank, token_type, resource_type,
                                        staleMailPickup):
        """
        Pickup	/api/v1/lockerBank/{id}/lockers/{lockerID}/pickup
        This function validates the pickup from a locker is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow',
                                                                                      'body_path_normal_pickup'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        now = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.json_data['pickupDate'] = current_time
        self.json_data['staleMailPickup'] = bool(staleMailPickup)
        self.json_data['accesscode'] = access_code

        get_locker_pickup_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/pickup"
        get_locker_pickup_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/pickup" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_auth_v2_api(self, access_code, search_in_otherbank, locker_bank, token_type, resource_type, kioskToken=None):
        """
        AuthenticatePickupBasedOnCodeV2	/api/v2/lockerBank/{id}/lockers/pickup/authenticateCode
        This function validates the authentication for pickup is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Personal_Flow', 'body_auth_v2'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['accessCode'] = access_code
        self.json_data['searchInOtherBank'] = search_in_otherbank

        get_locker_authenticate_pickup_endpoint = self.endpoint + "/api/v2/lockerBank/" + locker_bank + "/lockers/pickup/authenticateCode"
        get_locker_authenticate_pickup_endpoint_invalid = self.endpoint + "/api/v2/lockerBank/" + locker_bank + "/lockers/pickup/authenticateCode/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_authenticate_pickup_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
