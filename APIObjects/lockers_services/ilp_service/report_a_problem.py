import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class ReportProblem:
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

    def verify_validate_api_for_report_problem(self, locker_bank, id, token_type, resource_type, kioskToken=None):
        """
        Validate	/api/v1/lockerBank/{id}/validate/{searchBy}
        This function will validate the user for being able to report a problem at locker bank
        return: this function returns response and status code
        """
        get_validate_api_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/validate/" + id
        get_validate_api_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/validate/" + id + "/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_validate_api_endpoint, headers=headers_update)
            status_code = res.status_code
        else:
            res = self.api.get_api_response(endpoint=get_validate_api_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_post_add_complaint_at_lockerbank(self, locker_bank, messageID, message, recipientEmail, operatorEmail, visitorEmail,
                                                details, lockerunit, accesscode, trackingid, token_type, resource_type, kioskToken=None):
        """
        AddComplaint	/api/v1/lockerBank/{id}/complaints/complaint
        This function validates the addition of complaints at a lockerbank is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Report_Problem', 'report_problem'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['messageID'] = messageID
        self.json_data['message'] = message
        self.json_data['Details'] = details

        if recipientEmail != "":
            self.json_data['recipient'] = recipientEmail
        if operatorEmail != "":
            self.json_data['operator'] = operatorEmail
        if visitorEmail != "":
            self.json_data['visitor'] = visitorEmail
        if lockerunit != "":
            self.json_data['authUnits'][0]['manufacturerLockerID'] = lockerunit
        if accesscode != "":
            self.json_data['authUnits'][0]['assetsDeposited']['accesscode'] = accesscode
        if trackingid != "":
            self.json_data['authUnits'][0]['assetsDeposited']['parcels'][0]['primaryTrackingID'] = trackingid

        get_add_complaints_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints/complaint"
        get_add_complaints_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints/complaint/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_add_complaints_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_add_complaints_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_complaints_at_lockerBank(self, locker_bank, token_type, resource_type):
        """
        AllComplaints	/api/v1/lockerBank/{id}/complaints
        This function will validate the complaints received at a locker bank
        :return: this function returns response and status code
        """
        get_complaints_at_locker_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints"
        get_complaints_at_locker_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_complaints_at_locker_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_complaints_at_locker_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_export_complaints_at_lockerBank(self, locker_bank, token_type, resource_type):
        """
        ExportComplaints	/api/v1/lockerBank/{id}/complaints/export
        This function will validate the export api
        :return: this function returns response and status code
        """
        get_export_at_locker_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints/export"
        get_export_at_locker_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/complaints/export/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_export_at_locker_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_export_at_locker_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
