"""This module is used for main page objects."""

import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class ActivityAPI:
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

    def verify_get_daily_activitycount_tenantID(self, tenantID, token_type, resource_type):
        """
        GetDailyActivityCountForTenant	/api/v1/tenant/{tID}/activity/count
        This function validates the daily activity count based on tenantID
        :return: this function returns response and status code
        """
        get_daily_activity_count_from_tenantID_endpoint = self.endpoint + "/api/v1/tenant/" + tenantID + "/activity/count"
        get_daily_activity_count_from_tenantID_endpoint_invalid = self.endpoint + "/api/v1/tenant/" + tenantID + "/activity/count/" + self.invalid_path

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

    def verify_get_daily_activitycount_siteID(self, siteID, token_type, resource_type):
        """
        GetDailyActivityCountAtSite	/api/v1/site/{sID}/activity/count
        This function validates the daily activity count based on siteID
        :return: this function returns response and status code
        """
        get_daily_activity_count_from_siteID_endpoint = self.endpoint + "/api/v1/site/" + siteID + "/activity/count"
        get_daily_activity_count_from_siteID_endpoint_invalid = self.endpoint + "/api/v1/site/" + siteID + "/activity/count/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_siteID_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_daily_activity_count_from_siteID_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_invalidate_integrator_cache(self, integrator, token_type, resource_type):
        """
        InvalidateIntegratorCache	/api/v1/lockeractivity/{integratorID}/cache
        This function invalidate the integrator cache
        :return: this function returns response and status code
        """
        get_invalidate_integrator_cache_endpoint = self.endpoint + "/api/v1/lockeractivity/" + integrator + "/cache"
        get_invalidate_integrator_cache_endpoint_invalid = self.endpoint + "/api/v1/lockeractivity/" + integrator + "/cache/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.delete_api_response(
                endpoint=get_invalidate_integrator_cache_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.delete_api_response(
                endpoint=get_invalidate_integrator_cache_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_invalidate_lockerbank_cache(self, locker_bank, token_type, resource_type):
        """
        InvalidateBankCache	/api/v1/lockerBank/{id}/cache
        This function invalidate the locker bank cache
        :return: this function returns response and status code
        """
        get_invalidate_locker_bank_cache_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/cache"
        get_invalidate_locker_bank_cache_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/cache/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.delete_api_response(
                endpoint=get_invalidate_locker_bank_cache_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.delete_api_response(
                endpoint=get_invalidate_locker_bank_cache_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_lockerbank_activity_count(self, tenantID, siteID, manufacturerID, activityCode, transactionType, recipientInfo,
                                   trackingID, manufacturerLockerID, startDate, token_type, resource_type):
        """
        LookupActivityCount	/api/v1/lockeractivity/count
        This function validates the lockerbank activity count
        :return: this function returns response and status code
        """
        get_lockerbank_activity_count_endpoint = self.endpoint + "/api/v1/lockeractivity/count"
        get_lockerbank_activity_count_invalid = self.endpoint + "/api/v1/lockeractivity/count/" + self.invalid_path

        default_endpoint = self.endpoint + "/api/v1/lockeractivity/count?"

        if tenantID != "":
            get_lockerbank_activity_count_endpoint = default_endpoint + "tenantID=" + tenantID
            if siteID != "":
                get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&siteID=" + siteID
                if manufacturerID != "":
                    get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&manufacturerID=" + manufacturerID
                    if activityCode != "" and transactionType != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&activityCode=" + activityCode + "&transactionType=" + transactionType
                    elif activityCode != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&activityCode=" + activityCode
                    elif transactionType != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&transactionType=" + transactionType
                    elif recipientInfo != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&recipientInfo=" + recipientInfo
                    elif trackingID != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&trackingID=" + trackingID
                    elif manufacturerLockerID != "":
                        get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&manufacturerLockerID=" + manufacturerLockerID
            elif startDate != "":
                get_lockerbank_activity_count_endpoint = get_lockerbank_activity_count_endpoint + "&startDate=" + startDate

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lockerbank_activity_count_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lockerbank_activity_count_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_locker_activity_api(self, tenantID, siteID, manufacturerID, activityCode, transactionType, recipientInfo,
                                   trackingID, manufacturerLockerID, startDate,  token_type, resource_type):
        """
        LookupActivity	/api/v1/lockeractivity
        This function validates the lockerbank activity api
        :return: this function returns response and status code
        """
        get_lockerbank_activity_endpoint = self.endpoint + "/api/v1/lockeractivity"
        get_lockerbank_activity_endpoint_invalid = self.endpoint + "/api/v1/lockeractivity/" + self.invalid_path

        default_endpoint = self.endpoint + "/api/v1/lockeractivity?limit=25&skip=0&sortBy=activityDate:desc"

        if tenantID != "":
            get_lockerbank_activity_endpoint = default_endpoint + "&tenantID=" + tenantID
            if siteID != "":
                get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&siteID=" + siteID
                if manufacturerID != "":
                    get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&manufacturerID=" + manufacturerID
                    if activityCode != "" and transactionType != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&activityCode=" + activityCode + "&transactionType=" + transactionType
                    elif activityCode != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&activityCode=" + activityCode
                    elif transactionType != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&transactionType=" + transactionType
                    elif recipientInfo != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&recipientInfo=" + recipientInfo
                    elif trackingID != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&trackingID=" + trackingID
                    elif manufacturerLockerID != "":
                        get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&manufacturerLockerID=" + manufacturerLockerID
            elif startDate != "":
                get_lockerbank_activity_endpoint = get_lockerbank_activity_endpoint + "&startDate=" + startDate

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lockerbank_activity_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lockerbank_activity_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_lockerbank_detail_at_site(self, siteID, token_type, resource_type):
        """
        GetLockerAvailabilityCountAtSite	/api/v1/site/{sID}/lockerBank/count
        This function validates the daily activity count based on siteID
        :return: this function returns response and status code
        """
        get_locker_bank_detail_at_site_endpoint = self.endpoint + "/api/v1/site/" + siteID + "/lockerBank/count"
        get_locker_bank_detail_at_site_endpoint_invalid = self.endpoint + "/api/v1/site/" + siteID + "/lockerBank/count/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_bank_detail_at_site_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_bank_detail_at_site_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_lockercount_available_at_lockerbank(self, siteID, locker_bank, token_type, resource_type):
        """
        GetLockerAvailabilityCountAtLocker	/api/v1/site/{sID}/lockerBank/{id}/count
        This function validates the lockerunit count available at particular lockerbank and lockerunit count at site
        :return: this function returns response and status code
        """
        get_locker_count_at_bank_endpoint = self.endpoint + "/api/v1/site/" + siteID + "/lockerBank/" + locker_bank + "/count"
        get_locker_count_at_bank_endpoint_invalid = self.endpoint + "/api/v1/site/" + siteID + "/lockerBank/" + locker_bank + "/count/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_locker_count_at_bank_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_locker_count_at_bank_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code