"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class ShipmentTransactionsAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self,app_config, access_token):
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        # endpoint=(self.app_config.env_cfg['base_api'])
        # self.endpoint = endpoint.replace("temp", str(self.app_config.env_cfg['env']).lower())
        self.headers = json.loads(self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_shipment_transaction_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT','body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open( file_path) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_shipment_transaction_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics shipment_transaction api is well authorized or not
                :return: return test status, response body
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint =self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_shipment_transaction_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics shipment_transaction api gets response or not
                with different header type.
                :return: return test status, response body
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_shipment_transactions_api_response_without_response_type(self, startdate , enddate,divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        without response type valur by value.
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT','body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open( file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = ""

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        '''if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True'''
        return res, status_code


    def verify_shipment_transactions_api_response_with_groupby_value(self, startdate , enddate, groupByCriteria,divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        with group by value.
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'] = groupByCriteria

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_shipments_transactions_api_response_with_orderby_value(self, startdate , enddate, orderByCriteria,divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        with orderby value.
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'] = orderByCriteria

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_shipment_transactions_api_response_with_subfilter_value(self, startdate, enddate, subfilter,type, divisionIds=""):
         """
            This function is validates if analytics shipment_transaction api gets response or not
            with subfilter value.
            :return: return test status, response body
            """
         get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
         if self.app_config.env_cfg['product_name'] == 'sp360commercial':
             get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
         file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
             self.app_config.env_cfg['env']).lower())
         with open(file_path) as f:
             self.json_data = json.load(f)

         result = False

         self.json_data['filter']['startdate'] = startdate
         self.json_data['filter']['endDate'] = enddate
         self.json_data['filter']['divisionIds'] = divisionIds
         self.json_data['subFilter'][type] = subfilter

         res = self.api.post_api_response(
             endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
         status_code = res.status_code

         if res is not None:
             res = res.json()
             self.log.info("Shipment_Transaction API response:")
             self.log.info(res)
             result = True
         return res, status_code


    def verify_shipments_transactions_api_response_with_filtergroup_value(self, startdate , enddate, filtersGroup,divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        with filter group value.
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filtersGroup'] = filtersGroup

        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_shipment_transaction_api_response_without_country_value(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api gets response or not
        without_country_value
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        if self.app_config.env_cfg['product_name'] == 'sp360commercial':
            get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter']['country'] = ""



        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_shipment_transaction_paginated_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics shipment_transaction api working for pagination with not
        by passing pagesize=1
        :return: return test status, response body
        """
        get_shipment_transaction_endpoint = self.endpoint + "/shipmentTransactions/paginated?locale=en_US&pageNumber=1&pageSize=1"
        file_path = self.prop.get('SHIPMENT_TRANSACTIONS_API_MGMT','body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open( file_path) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_shipment_transaction_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Shipment_Transaction API response:")
            self.log.info(res)
            result = True
        return res,status_code
