"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class RecommendationsAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self,app_config, access_token):
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        #endpoint=(self.app_config.env_cfg['base_api'])
        #self.endpoint = endpoint.replace("temp", str(self.app_config.env_cfg['env']).lower())
        self.headers = json.loads(self.prop.get('RECOMMENDATIONS_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)


    def verify_recommendations_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        :return: this function returns boolean status of element located
        """
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path=self.prop.get('RECOMMENDATIONS_API_MGMT','body_path_recommendations').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)




        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_recommendations_api_authorisation(self,startdate , enddate,expired_token, divisionIds=""):

        """
                This function is validates if analytics account_balance api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_recommendations_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics account_balance api gets response or not
                with different header type.
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code




    def verify_recommendations_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns boolean status of element located
        """
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data[key] = value

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_recommendations_api_response_with_deleting_keys_in_payload(self, startdate , enddate, keyTobeDelete,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with group by value.
        :return: this function returns boolean status of element located
        """
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data[keyTobeDelete]

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_recommendations_api_response_with_key_and_value_in_subfilter(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns boolean status of element located
        """
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][key] = value

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_recommendations_api_response_with_deleting_key_in_subfilter(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns boolean status of element located
        """
        get_recommendations_endpoint = self.endpoint + "/recommendations?locale=en_US"
        file_path = self.prop.get('RECOMMENDATIONS_API_MGMT', 'body_path_recommendations').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data['subFilter'][key]

        res = self.api.post_api_response(
            endpoint=get_recommendations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Recommendations API response:")
            self.log.info(res)
            result = True
        return res, status_code