"""This module is used for main page objects."""

import logging


from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class ProductsAPI:
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
        self.headers = json.loads(self.prop.get('PRODUCTS_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"] = common_utils.get_x_user_id_from_okta(self.access_token)
        # self.log = log_utils.custom_logger(logging.INFO)


    def verify_products_api_response(self,entpriseID, divisionIds=""):
        """
        This function is validates if analytics products api gets response or not
        :return: this function returns json response and status code
        """

        file_path=self.prop.get('PRODUCTS_API_MGMT','body_path_products').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID',str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            #self.log.info(res)
            result = True
        return res,status_code






    def verify_products_api_authorisation(self,entpriseID,expired_token, divisionIds=""):

        """
                This function is validates if analytics products api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code


    def verify_products_api_header(self,entpriseID,invalid_header, divisionIds=""):

        """
                This function is validates if analytics products api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code




    def verify_products_api_response_with_key_and_value(self,entpriseID , key,value,divisionIds=""):
        """
        This function is validates if analytics products api gets response or not
        with_key_and_value in json payload.
        :return: this function returns json response and status code
        """
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data[key] = value
        print(self.json_data)

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code


    def verify_products_api_response_with_deleting_keys_in_payload(self, entpriseID, keyTobeDelete,divisionIds=""):
        """
        This function is validates if analytics products api gets response or not
        with_deleting_keys_in json payload.
        :return: this function returns json response and status code
        """
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data[keyTobeDelete]

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code


    def verify_products_api_response_with_key_and_value_in_subfilter(self, entpriseID, key,value,divisionIds=""):
        """
        This function is validates if analytics products api gets response or not
        with_key_and_value_in_subfilter in json payload.
        :return: this function returns json response and status code
        """
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][key] = value

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code


    def verify_products_api_response_with_deleting_key_in_subfilter(self, entpriseID, key,divisionIds=""):
        """
        This function is validates if analytics products api gets response or not
        with_deleting_key_in_subfilter in json  payload.
        :return: this function returns json response and status code
        """
        file_path = self.prop.get('PRODUCTS_API_MGMT', 'body_path_products').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        get_products_endpoint = self.endpoint + "/enterprise/Ent_ID/products?useFedrampRepository=true"
        get_products_endpoint = str(get_products_endpoint).replace('Ent_ID', str(entpriseID))

        result = False

        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data['subFilter'][key]

        res = self.api.post_api_response(
            endpoint=get_products_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Products API response:")
            # self.log.info(res)
            result = True
        return res, status_code