"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class LockerBankAPI:
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

    def verify_Lockerbank_sizes(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetLockerSizes	/api/v1/lockerBank/{id}/lockers/sizes
        This function validates if a locker bank sizes is successfully fetch or not
        :return: this function returns response and status code
        """
        get_locker_sizes_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/sizes"
        get_locker_sizes_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/sizes/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_sizes_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_sizes_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_lockerbank_Dimensions(self, locker_bank, token_type, resource_type):
        """
        GetLockerDimensions	/api/v1/lockerBank/{id}/lockers/dimensions
        This function validates the locker bank dimension details
        :return: this function returns response and status code
        """
        get_locker_bank_dimensions_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/dimensions"
        get_locker_bank_dimensions_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/dimensions/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_bank_dimensions_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_bank_dimensions_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_locker_refrigerated_locker_types(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetRefrigeratedLockerTypes	/api/v1/lockerBank/{id}/lockers/types
        This function validates the refrigeration types in the locker bank
        :return: this function returns response and status code
        """
        get_locker_refrigerated_type_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/types"
        get_locker_refrigerated_type_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/types/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_locker_refrigerated_type_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(endpoint=get_locker_refrigerated_type_endpoint_invalid,
                                            headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_locker_timezone(self, locker_bank, token_type, resource_type):
        """
        GetLockerBankTimeZone	/api/v1/lockerBank/{id}/timezone
        This function validates the locker bank timezone
        :return: this function returns response and status code
        """
        get_lockerbank_timezone_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/timezone"
        get_lockerbank_timezone_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/timezone/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_lockerbank_timezone_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(endpoint=get_lockerbank_timezone_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_stale_packages_at_lockerBank(self, locker_bank, token_type, resource_type):
        """
        GetStaleLockers	/api/v1/lockerBank/{id}/lockers/stale
        This function will validate the stale package count at the locker bank
        :return: this function returns response and status code
        """
        get_locker_bank_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/stale"
        get_locker_bank_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/stale/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_bank_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_bank_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_qr_code_api(self, locker_bank, token_type, resource_type):
        """
        GetQRCode	/api/v1/lockerBank/{id}/info/qrcode
        This function validates the get qr code api
        :return: this function returns response and status code
        """
        get_qr_code_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/info/qrcode"
        get_qr_code_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/info/qrcode/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_qr_code_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_qr_code_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_config_pair_api(self, locker_bank, qr_code, hardwareID, token_type, resource_type, kioskToken=None):
        """
        GetConfiguration	/api/v1/lockerBank/{id}/pair/{code}/config
        This function validates the get qr code api
        :return: this function returns response and status code
        """
        get_config_pair_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pair/" + qr_code + "/config"
        get_config_pair_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pair/" + qr_code + "/config/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)
        headers_update['X-PB-Locker-HWID'] = hardwareID

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_config_pair_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_config_pair_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_decode_api(self, encodedString, token_type, resource_type, kioskToken=None):
        """
        Decode	/api/v1/decode
        This function validates the get decode api response
        :return: this function returns response and status code
        """
        get_decode_endpoint = self.endpoint + "/api/v1/decode?id=" + encodedString + "&encodedURL=true"
        get_decode_endpoint_invalid = self.endpoint + "/api/v1/decodee?id=" + encodedString + "&encodedURL=true"

        if kioskToken is not None:
            device_token = kioskToken['basic_device_token']
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, device_token)
        else:
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_decode_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_decode_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_decodeV2_api(self, locker_bank, trackingID, encodedFlag, token_type, resource_type, token=None,
                            kioskToken=None):
        """
        DecodeV2	/api/v1/lockerBank/{id}decode
        This function validates the get decode api response
        :return: this function returns response and status code
        """
        get_decodeV2_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/decode"
        get_decodeV2_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/decode"

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Locker_Bank',
                                                                                      'body_path_decodeV2'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['trackingNumber'][0] = trackingID
        self.json_data['encoded'] = bool(encodedFlag)

        if kioskToken is None:
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)
        elif token is not None:
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, token)
        else:
            device_token = kioskToken['basic_device_token']
            headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, device_token)

        if resource_type == "validResource":
            response = self.api.post_api_response(
                endpoint=get_decodeV2_endpoint, headers=headers_update, body=json.dumps(self.json_data))
        else:
            response = self.api.post_api_response(
                endpoint=get_decodeV2_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))

        self.log.info(response)
        return response

    def verify_post_locker_activity_event(self, locker_bank, locker_unit, token_type, resource_type, kioskToken=None):
        """
        LockerActivity	/api/v1/lockerBank/{id}/lockers/activity
        This function validates the post locker activity event
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Locker_Bank', 'body_path_post_activity_event_api'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['units'][0]['manufacturerLockerID'] = locker_unit

        post_locker_activity_event_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/activity"
        post_locker_activity_event_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/activity/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=post_locker_activity_event_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=post_locker_activity_event_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_pair_code_by_MHID_api(self, MHID, token_type, resource_type, kioskToken=None):
        """
        GetPairCode	/api/v1/lockerBank/{id}/pair/code
        This function validates the get qr code api
        :return: this function returns response and status code
        """
        get_get_pair_code_endpoint = self.endpoint + "/api/v1/lockerBank/" + MHID + "/pair/code?mHID=true"
        get_get_pair_code_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + MHID + "/pair/code/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_get_pair_code_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_get_pair_code_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code