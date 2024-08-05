"""This module is used for main page objects."""

import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class AdminAPI:
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

    def verify_lookup_activity_admin(self, tenantID, token_type, resource_type):
        """
        LookupActivityAdmin	/api/v1/subscriptions/{tID}/lockeractivity
        This function validates the daily activity count based on tenantID
        :return: this function returns response and status code
        """
        get_lookup_activity_admin_endpoint = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity?limit=25&tenantID=" + tenantID
        get_lookup_activity_admin_endpoint_invalid = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_lookup_activity_count_admin(self, tenantID, token_type, resource_type):
        """
        LookupActivityCountAdmin	/api/v1/subscriptions/{tID}/lockeractivity/count
        This function validates the daily activity count based on tenantID
        :return: this function returns response and status code
        """
        get_lookup_activity_admin_endpoint = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity/count?tenantID=" + tenantID
        get_lookup_activity_admin_endpoint_invalid = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity/count" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_activity_export_admin(self, tenantID, token_type, resource_type):
        """
        ExportActivityAdmin	/api/v1/subscriptions/{tID}/lockeractivity/export/file
        This function validates the activity export based on tenantID
        :return: this function returns response and status code
        """
        get_lookup_activity_admin_endpoint = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity/export/file?limit=25&tenantID=" + tenantID
        get_lookup_activity_admin_endpoint_invalid = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/lockeractivity/export/file" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_sites_admin(self, tenantID, token_type, resource_type):
        """
        GetSitesAdmin	/api/v1/subscriptions/{tID}/sites
        This function validates the get sites via admin
        :return: this function returns response and status code
        """
        get_lookup_activity_admin_endpoint = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/sites"
        get_lookup_activity_admin_endpoint_invalid = self.endpoint + "/api/v1/subscriptions/" + tenantID + "/sites" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_lookup_activity_admin_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code