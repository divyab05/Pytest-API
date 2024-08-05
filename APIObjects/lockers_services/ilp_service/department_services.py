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


class DepartmentLockerAPI:
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

    def verify_reserve_locker_dept_api(self, locker_bank, locker_size, TrkgID, departmentMail, departmentID, token_type, resource_type, token=None):
        """
        ReserveLocker	/api/v1/lockerBank/{id}/lockers/reserve
        This function validates reservation of locker for department
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'body_path_dept_reserve'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['departmentMail'] = bool(departmentMail)

        self.json_data['size'] = locker_size
        self.json_data['assetsReserved']['departmentCode'] = departmentID

        self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID

        if TrkgID.startswith("SSTO"):
            self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"__SSTO"

        if TrkgID.startswith("Fireball"):
            self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID+"_fireball"

        get_locker_reserve_for_dept_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserve"
        get_locker_reserve_for_dept_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/reserve/" + self.invalid_path

        if token is not None:
            self.access_token = token
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_for_dept_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_reserve_for_dept_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_Deposit_locker_department_api(self, context, locker_bank, token_type, resource_type, token=None):
        """
        UpdateDeposit	/api/v1/lockerBank/{id}/lockers/{lockerID}/deposit
        This function validates if a deposit is successful or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'body_path_Deposit'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['parcels'][0]['primaryTrackingID'] = context['Res_trackID_dept']

        if context['Res_trackID_dept'].startswith("SSTO"):
            self.json_data['parcels'][0]['secondaryTrackingID'] = context['Res_trackID_dept']+"__SSTO"

        if context['Res_trackID_dept'].startswith("Fireball"):
            self.json_data['parcels'][0]['secondaryTrackingID'] = context['Res_trackID_dept']+"_fireball"

        get_locker_deposit_for_dept_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + context['manufacturerLockerID_dept'] + "/deposit"
        get_locker_deposit_for_dept_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + context['manufacturerLockerID_dept'] + "/deposit/" + self.invalid_path

        if token is not None:
            self.access_token = token
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_deposit_for_dept_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_deposit_for_dept_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_Pickup_locker_department_api(self, context, locker_bank, departmentMail, departmentID,
                                            departmentpickcode, token_type, resource_type, staleMailPickup, token=None):
        """
        MultiplePickup	/api/v1/lockerBank/{id}/lockers/multiPickup
        This function validates the pickup for department is success or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'body_path_dept_pickup'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['departmentMail'] = bool(departmentMail)

        now = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.json_data['pickupDate'] = current_time
        self.json_data['pickupRequests'][0]['manufacturerLockerID'] = context['manufacturerLockerID_dept']
        self.json_data['pickupRequests'][0]['accesscode'] = departmentpickcode
        self.json_data['pickupRequests'][0]['departmentCode'] = departmentID
        self.json_data['staleMailPickup'] = bool(staleMailPickup)

        get_locker_pickup_for_dept_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/multiPickup"

        get_locker_pickup_for_dept_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/multiPickup/" + self.invalid_path

        if token is not None:
            self.access_token = token
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_for_dept_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=get_locker_pickup_for_dept_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_PersonalID_for_department(self, tenantID, siteID, departmentID, token_type, resource_type, kioskToken=None):
        """
        GetPersonalIDAddressBook	/api/v1/tenant/{tID}/sites/{sID}/departments/{depCode}/personalID
         This function validates the list of personalID associated with department
        :return: this function returns response and status code
        """
        get_personalID_for_department_endpoint = self.endpoint + "/api/v1/tenant/" + tenantID + "/sites/" + siteID + "/departments/" + departmentID + "/personalID"
        get_personalID_for_department_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + tenantID + "/sites/" + siteID + "/departments/" + departmentID + "/personalID/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_personalID_for_department_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_personalID_for_department_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_All_Department_at_site(self, tenantID, SiteID, token_type, resource_type, kioskToken=None):
        """
        ListDepartmentAtSite	/api/v1/tenant/{tID}/sites/{sID}/departments
        This function is validates the updated status of the department
        """
        Get_department_at_site = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/sites/" + str(SiteID) + "/departments"
        Get_department_at_site_invalid = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/sites/" + str(SiteID) + "/departments/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=Get_department_at_site, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=Get_department_at_site_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_department_reference(self, tenantID, departmentCode, token_type, resource_type):
        """
        CheckDepartmentReference	/api/v1/tenant/{tID}/department/reference
        This function validates the department reference
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'check_dept_reference'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data["departments"][0]["departmentCode"] = departmentCode

        get_department_reference_endpoint = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/department/reference"
        get_department_reference_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/department/reference/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_recipient_reference(self, tenantID, recipientID, token_type, resource_type):
        """
        CheckRecipientReference	/api/v1/tenant/{tID}/recipient/reference
        This function validates the department reference
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'check_recipient_reference'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data["recipients"][0]["recipientID"] = recipientID

        get_department_reference_endpoint = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/recipient/reference"
        get_department_reference_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/department/reference/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_location_reference(self, tenantID, locationID, token_type, resource_type):
        """
        CheckLocationReference	/api/v1/tenant/{tID}/location/reference
        This function validates the department reference
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow',
                                                                                      'check_location_reference'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data["locations"][0]["locationID"] = locationID

        get_department_reference_endpoint = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/location/reference"
        get_department_reference_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + str(
            tenantID) + "/location/reference/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.post_api_response(
                endpoint=get_department_reference_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_Update_Department_PersonalID(self, PID, tenantID, SiteID, departmentID, token_type, resource_type):
        """
        UpdatePersonalIDAddressBook	/api/v1/tenant/{tID}/sites/{sID}/departments/{depCode}/personalID
        This function validates the department reference
        :return: this will help to update the personalID of department
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'update_personalID'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data["personalID"] = PID

        get_department_reference_endpoint = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/sites/" + str(SiteID) + "/departments/" + departmentID + "/personalID"
        get_department_reference_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + str(tenantID) + "/" + str(SiteID) + "/departments/" + departmentID + "/personalID" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=get_department_reference_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code
        else:
            res = self.api.patch_api_response(
                endpoint=get_department_reference_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_reservation_based_on_unit_for_dept(self, locker_bank, locker_unit, size, TrkgID, departmentMail, departmentID, token_type, resource_type):
        """
        ReserveLockerBasedOnID	/api/v1/lockerBank/{id}/lockers/{lockerID}/reserve
        This function validates the reservation of a particular unit
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Department_Flow', 'body_path_dept_reserve'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['size'] = size

        if TrkgID.startswith("Tracking"):
            self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID

        if TrkgID.startswith("SSTO"):
            self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID + "__SSTO"

        if TrkgID.startswith("Fireball"):
            self.json_data['assetsReserved']['assets'][0]['primaryTrackingID'] = TrkgID
            self.json_data['assetsReserved']['assets'][0]['secondaryTrackingID'] = TrkgID + "_fireball"

        self.json_data['departmentMail'] = bool(departmentMail)

        self.json_data['assetsReserved']['departmentCode'] = departmentID

        get_locker_reserve_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserve"
        get_locker_reserve_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/lockers/" + locker_unit + "/reserve/" + self.invalid_path

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
