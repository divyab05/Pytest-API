"""This module is used for main page objects."""

import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class LookUPAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = "Bearer " + access_token
        print(self.access_token)
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))

    def verify_list_banks(self, tenantID, siteID, token_type, resource_type):
        """
        ListBanks	/api/v1/lockerBank
        This function validates the daily activity count based on tenantID
        :return: this function returns response and status code
        """
        get_daily_activity_count_from_tenantID_endpoint = self.endpoint + "/api/v1/lockerBank?tenantID=" + str(tenantID) + "&siteID=" + str(siteID)
        get_daily_activity_count_from_tenantID_endpoint_invalid = self.endpoint + "/api/v1/llockerBank/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_tenantID_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_tenantID_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_lookUp_bank(self, tenantID, token_type, resource_type):
        """
        LookupBanks	/api/v1/lockerBanks
        This function validates the daily activity count based on tenantID
        :return: this function returns response and status code
        """
        get_daily_activity_count_from_tenantID_endpoint = self.endpoint + "/api/v1/lockerBanks?tenantID=" + tenantID
        get_daily_activity_count_from_tenantID_endpoint_invalid = self.endpoint + "/api/v1/lockerBanks/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_tenantID_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_tenantID_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_sites_basedon_tenantID(self, tenantID, token_type, resource_type):
        """
        GetSites	/api/v1/tenant/{tID}/sites
        This function validates the sites based on tenantID at selected locker bank
        :return: this function returns response and status code
        """
        get_sites_based_on_tenantID_endpoint = self.endpoint + "/api/v1/tenant/" + tenantID + "/sites"
        get_sites_based_on_tenantID_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + tenantID + "/sites/" + self.invalid_path

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

    def verify_list_banks_for_site(self, siteID, token_type, resource_type):
        """
        ListBanksForSite	/api/v1/sites/{sID}/lockerBank
        This function validates the list of banks on site
        :return: this function returns response and status code
        """
        get_list_banks_for_site_endpoint = self.endpoint + "/api/v1/sites/" + siteID + "/lockerBank"
        get_list_banks_for_site_endpoint_invalid = self.endpoint + "/api/v1/sites/" + siteID + "/lockerBank/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_list_banks_for_site_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_list_banks_for_site_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_lockers(self, lockerID, token_type, resource_type):
        """
        GetLockers	/api/v1/lockerBank/{id}/lockers
        This function validates the get lockers
        :return: this function returns response and status code
        """
        get_lockers_endpoint = self.endpoint + "/api/v1/lockerBank/" + lockerID + "/lockers"
        get_lockers_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + lockerID + "/lockers/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lockers_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lockers_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_locker_unit(self, lockerID, locker_unit, token_type, resource_type):
        """
        GetLocker	/api/v1/lockerBank/{id}/lockers/{lockerID}
        This function validates the get locker_unit
        :return: this function returns response and status code
        """
        get_locker_unit_endpoint = self.endpoint + "/api/v1/lockerBank/" + lockerID + "/lockers/" + locker_unit
        get_locker_unit_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + lockerID + "/lockers/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_unit_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_unit_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
