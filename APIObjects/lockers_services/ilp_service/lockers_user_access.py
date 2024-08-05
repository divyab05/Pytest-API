"""This module is used for main page objects."""

import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class LockerUserAccessLevel:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))

    def get_locker_banks_tenant_api(self, tenantID='', token=''):
        get_lockerbanks_tenant_url = self.endpoint + '/api/v1/lockerBanks?tenantID=' + str(tenantID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_lockerbanks_tenant_url, headers=self.headers)
        return response

    def get_locker_banks_tenant_and_site_api(self, tenantID='', siteID='', token=''):
        get_lockerbanks_site_url = self.endpoint + '/api/v1/lockerBanks?tenantID=' + str(tenantID) + "&siteID=" + str(
            siteID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_lockerbanks_site_url, headers=self.headers)
        return response

    def get_locker_bank_api(self, token=''):
        get_lockerbank_site_url = self.endpoint + '/api/v1/lockerBank'
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_lockerbank_site_url, headers=self.headers)
        return response

    def get_locker_bank_by_id(self, MID='', token=''):
        get_lockerbank_site_url = self.endpoint + '/api/v1/lockerBank/' + MID
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_lockerbank_site_url, headers=self.headers)
        return response

    def get_locker_bank_with_site_api(self, siteID='', token=''):
        get_lockerbank_url = self.endpoint + '/api/v1/lockerBank?siteID=' + siteID
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_lockerbank_url, headers=self.headers)
        return response

    def get_sites_api(self, tenantID='', token=''):
        get_sites_url = self.endpoint + '/api/v1/tenant/' + str(tenantID) + "/sites"
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_sites_url, headers=self.headers)
        return response

    def get_reserved_units_across_tenant_api(self, tenantID='', recipientID='', token=''):
        get_reserved_units_url = self.endpoint + '/api/v1/tenant/' + str(tenantID) + '/lockers/reserved/' + str(
            recipientID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_reserved_units_url, headers=self.headers)
        return response

    def get_locker_activity_v2(self, tenantID='', token=''):
        get_locker_activity_v2_url = self.endpoint + '/api/v2/lockeractivity?tenantID={arg}&limit=25&skip=0&sortBy=activityDate:desc'.format(
            arg=tenantID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_activity_v2_url, headers=self.headers)
        return response

    def get_locker_activity_v1(self, tenantID='', token=''):
        get_locker_activity_v1_url = self.endpoint + '/api/v1/lockeractivity?tenantID={arg}&limit=25&skip=0&sortBy=activityDate:desc'.format(
            arg=tenantID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_activity_v1_url, headers=self.headers)
        return response

    def get_locker_activity_count(self, tenantID='', token=''):
        get_locker_activity_count_url = self.endpoint + '/api/v1/lockeractivity/count?tenantID=' + str(tenantID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_activity_count_url, headers=self.headers)
        return response

    def get_locker_banks_v2_tenantID(self, tenantID='', token=''):
        get_locker_banks_v2_tenant = self.endpoint + '/api/v1/lockerBanksV2?tenantID=' + str(tenantID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_banks_v2_tenant, headers=self.headers)
        return response

    def get_locker_banks_v2_siteID(self, tenantID='', siteID='', token=''):
        get_locker_banks_v2_tenant = self.endpoint + '/api/v1/lockerBanksV2?tenantID=' + str(
            tenantID) + "&siteID=" + str(siteID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_banks_v2_tenant, headers=self.headers)
        return response

    def get_locker_banks_v2_MID(self, tenantID='', MID='', token=''):
        get_locker_banks_v2_tenant = self.endpoint + '/api/v1/lockerBanksV2?tenantID=' + str(
            tenantID) + "&manufacturerID=" + str(MID)
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_locker_banks_v2_tenant, headers=self.headers)
        return response

    # add export, MID in remaining
