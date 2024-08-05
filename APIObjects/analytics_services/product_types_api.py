"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class ProductTypesAPI:
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
        self.headers = json.loads(self.prop.get('PRODUCT_TYPES_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)


    def verify_product_types_api_response(self, divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        :return: this function returns json response and status code
        """
        get_product_types_endpoint = self.endpoint + "/productTypes?country=US"
        file_path=self.prop.get('PRODUCT_TYPES_API_MGMT','body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)




        result = False


        self.json_data = divisionIds



        res = self.api.post_api_response(
            endpoint=get_product_types_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Product Types API response:")
            self.log.info(res)
            result = True
        return res,status_code



    def verify_product_types_api_authorisation(self,expired_token, divisionIds=""):

        """
                This function is validates if analytics account_balance api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_product_types_endpoint = self.endpoint + "/productTypes?country=US"
        file_path = self.prop.get('PRODUCT_TYPES_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data = divisionIds

        res = self.api.post_api_response(
            endpoint=get_product_types_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Product_Types API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_product_types_api_header(self,invalid_header, divisionIds=""):

        """
                This function is validates if analytics account_balance api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_product_types_endpoint = self.endpoint + "/productTypes?country=US"
        file_path = self.prop.get('PRODUCT_TYPES_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data = divisionIds


        res = self.api.post_api_response(
            endpoint=get_product_types_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Product_Types API response:")
            self.log.info(res)
            result = True
        return res, status_code