"""This module is used for main page objects."""

import logging
import jwt


from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily
from FrameworkUtilities.get_user_okta_token_utils import UserOktaUtilily

import json
import random

from context import Context


class ContractAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self,app_config, access_token):
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        # endpoint = self.prop.get('CONTRACT_API_MGMT', 'base_api')
        # self.endpoint = endpoint.replace("temp", str(self.app_config.env_cfg['env']).lower())
        self.headers = json.loads(self.prop.get('CONTRACT_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        decoded_data = jwt.decode(jwt=self.access_token, algorithms=["RS256"], verify=False)
        self.entID = decoded_data['claim_spa']['entID']
        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_contract_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_authorisation(self, startdate, enddate, expired_token, divisionIds=""):

        """
                This function is validates if analytics contract api is well authorized or not
                :return: this function return response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_header(self, startdate, enddate, headerType, invalid_header, divisionIds=""):

        """
                This function is validates if analytics contract api gets response or not
                with different header type.
                :return: this function return response and status code
                """

        header1 = self.headers.copy()
        header1[headerType] = invalid_header
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_without_response_type(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        without response type valur by value.
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = ""

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        '''if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True'''
        return res, status_code

    def verify_contract_api_response_with_groupby_value(self, startdate, enddate, groupByCriteria, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        with group by value.
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'] = groupByCriteria

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_orderby_value(self, startdate, enddate, orderByCriteria, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        with orderby value.
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'] = orderByCriteria

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_contractSubFilter_value(self, startdate, enddate, subfilter, type,
                                                                  divisionIds=""):
        """
           This function is validates if analytics contract api gets response or not
           with contractSubfilter value.
           :return: this function return response and status code
           """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['contractSubFilter'][type] = subfilter

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_filtergroup_value(self, startdate, enddate, filtersGroup, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        with filter group value.
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filtersGroup'] = filtersGroup

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_whole_filter_value(self, filter):
        """
        This function is validates if analytics contract api gets response or not
        with whole filter value
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter'] = filter

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_filter_value(self, startdate, enddate, attr, val, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter'][attr] = val

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_api_response_with_selectquerycolumnlist_value(self, startdate, enddate, val, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?isShippingUsageRequired=false&locale=en_US&pageNumber=1&pageSize=1001"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['selectQueryColumnsList'] = val

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_contract_paginated_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        :return: this function return response and status code
        """
        get_contract_endpoint = self.endpoint + "/contract/paginated?locale=en_US&pageNumber=1&pageSize=1"
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_contract_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Contract API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    #Export

    def verify_contract_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not
        :return: this function return response and status code
        """
        get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en-US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en-US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path_export').replace("temp",
                                                                            str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['contractApiRequest']['filter']['startdate'] = startdate
        self.json_data['contractApiRequest']['filter']['endDate'] = enddate
        self.json_data['contractApiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_contract_export_endpoint=str(get_contract_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_contract_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]




    def verify_contract_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics contract api is well authorized or not
                :return: this function return response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))

        get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND"

        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path_export').replace("temp",
                                                                                   str(self.app_config.env_cfg[
                                                                                           'env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['contractApiRequest']['filter']['startdate'] = startdate
        self.json_data['contractApiRequest']['filter']['endDate'] = enddate
        self.json_data['contractApiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_contract_export_endpoint = str(get_contract_export_endpoint.replace('report_Type', report))
            res = self.api.post_api_response(
                endpoint=get_contract_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]






    def verify_contract_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics contract api gets response or not
                with different header type.
                :return: this function return response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header

        get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_contract_export_endpoint = self.endpoint + "/contract/custom/export?locale=en_US&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path_export').replace("temp",
                                                                                   str(self.app_config.env_cfg[
                                                                                           'env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['contractApiRequest']['filter']['startdate'] = startdate
        self.json_data['contractApiRequest']['filter']['endDate'] = enddate
        self.json_data['contractApiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_contract_export_endpoint=str(get_contract_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_contract_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_contract_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics contract api gets response by updating values of the keys in payload.
        :return: this function return response and status code
        """
        get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        

        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path_export').replace("temp",
                                                                                   str(self.app_config.env_cfg[
                                                                                           'env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['contractApiRequest']['filter']['startdate'] = startdate
        self.json_data['contractApiRequest']['filter']['endDate'] = enddate
        self.json_data['contractApiRequest']['filter']['divisionIds'] = divisionIds
        if key=='reportColumns':
            self.json_data[key] = value
        else:
            self.json_data['contractApiRequest'][key] = value

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_contract_export_endpoint=str(get_contract_export_endpoint.replace('report_Type',report))
            #print(get_contract_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_contract_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_contract_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics contract api gets response or not by deleting key in payload
        :return: this function return response and status code
        """
        get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_contract_export_endpoint = self.endpoint + "/contract/export?locale=en_US&fileFormat=report_Type&exportType=CONTRACT_SPEND&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        
        
        
        file_path = self.prop.get('CONTRACT_API_MGMT', 'body_path_export').replace("temp",
                                                                                   str(self.app_config.env_cfg[
                                                                                           'env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['contractApiRequest']['filter']['startdate'] = startdate
        self.json_data['contractApiRequest']['filter']['endDate'] = enddate
        self.json_data['contractApiRequest']['filter']['divisionIds'] = divisionIds

        if key == 'reportColumns':
            del self.json_data[key]
        else:
            del self.json_data['contractApiRequest'][key]

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_contract_export_endpoint=str(get_contract_export_endpoint.replace('report_Type',report))
            #print(get_contract_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_contract_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


