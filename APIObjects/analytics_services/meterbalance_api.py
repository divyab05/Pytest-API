"""This module is used for main page objects."""

import logging
import jwt



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily
from FrameworkUtilities.get_user_okta_token_utils import UserOktaUtilily

import json
import random

from context import Context


class MeterbalanceAPI:
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
        self.headers = json.loads(self.prop.get('METERBALANCE_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"]=common_utils.get_x_user_id_from_okta(self.access_token)
        decoded_data = jwt.decode(jwt=self.access_token, algorithms=["RS256"], verify=False)
        self.entID = decoded_data['claim_spa']['entID']
        # self.log = log_utils.custom_logger(logging.INFO)


    def verify_meterbalance_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_meterbalance_api_authorisation(self,startdate , enddate,expired_token, divisionIds=""):

        """
                This function is validates if analytics meterbalance api is well authorized or not
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res, status_code



    def verify_meterbalance_api_header(self,startdate , enddate,headerType,invalid_header, divisionIds=""):

        """
                This function is validates if analytics meterbalance api gets response or not
                with different header type.
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        header1[headerType]=invalid_header
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_meterbalance_api_response_without_response_type(self, startdate , enddate,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        without response type valur .
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = ""

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        '''if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True'''
        return res, status_code


    def verify_meterbalance_api_response_with_groupby_value(self, startdate , enddate, groupByCriteria,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        with group by value.
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'] = groupByCriteria

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_meterbalance_api_response_with_orderby_value(self, startdate , enddate, orderByCriteria,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        with orderby value.
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'] = orderByCriteria

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("meterbalance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_meterbalance_api_response_with_subfilter_value(self, startdate, enddate, subfilter,type, divisionIds=""):
         """
            This function is validates if analytics meterbalance api gets response or not
            with subfilter value.
            :return: this function returns response body and status code
            """
         get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
         with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
             self.json_data = json.load(f)

         result = False

         self.json_data['filter']['startdate'] = startdate
         self.json_data['filter']['endDate'] = enddate
         self.json_data['filter']['divisionIds'] = divisionIds
         self.json_data['subFilter'][type] = subfilter

         res = self.api.post_api_response(
             endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
         status_code = res.status_code

         if res is not None:
             res = res.json()
             self.log.info("Meterbalance API response:")
             self.log.info(res)
             result = True
         return res, status_code



    def verify_meterbalance_api_response_with_filtergroup_value(self, startdate , enddate, filtersGroup,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        with filter group value.
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filtersGroup'] = filtersGroup

        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_meterbalance_api_response_with_whole_filter_value(self,filter):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']=filter


        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_meterbalance_api_response_with_filter_value(self, startdate , enddate, attr,val,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter'][attr] = val





        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_meterbalance_api_response_with_selectquerycolumnlist_value(self, startdate , enddate, val,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=100"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['selectQueryColumnsList'] = val



        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Meterbalance API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_meterbalance_paginated_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_endpoint = self.endpoint + "/meterbalance/paginated?locale=en_US&pageNumber=1&pageSize=1"
        with open(self.prop.get('METERBALANCE_API_MGMT', 'body_path').replace("temp", str(
                self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_meterbalance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("meterbalance API response:")
            #self.log.info(res)
            result = True
        return res,status_code

    
    
    
    #Export Api
    
    def verify_meterbalance_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        :return: this function returns response body and status code
        """
        get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/export?locale=en-US&useExtendedRepository=true&getLatestBalanceReport=false&fileFormat=report_Type&exportType=METER_BALANCE_TYPE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/custom/export?locale=en_US&useExtendedRepository=true&getLatestBalanceReport=true&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path=self.prop.get('METERBALANCE_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_meterbalance_export_endpoint=str(get_meterbalance_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_meterbalance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]




    def verify_meterbalance_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics meterbalance api is well authorized or not
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        header1['Authorization']="Bearer {}".format(expired_token)
        get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/export?locale=en_US&query=locale%3Den_US%26useExtendedRepository%3Dtrue%26getLatestBalanceReport%3Dtrue%26fileFormat%3DXLSX%26exportType%3DCUSTOM_REPORT&fileFormat=report_Type&exportType=CUSTOM_REPORT&useExtendedRepository=true&getLatestBalanceReport=true"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/custom/export?locale=en_US&useExtendedRepository=true&getLatestBalanceReport=true&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path = self.prop.get('METERBALANCE_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_meterbalance_export_endpoint = str(get_meterbalance_export_endpoint.replace('report_Type', report))
            res = self.api.post_api_response(
                endpoint=get_meterbalance_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]






    def verify_meterbalance_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics meterbalance api gets response or not
                with different header type.
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/export?locale=en_US&query=locale%3Den_US%26useExtendedRepository%3Dtrue%26getLatestBalanceReport%3Dtrue%26fileFormat%3DXLSX%26exportType%3DCUSTOM_REPORT&fileFormat=report_Type&exportType=CUSTOM_REPORT&useExtendedRepository=true&getLatestBalanceReport=true"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/custom/export?locale=en_US&useExtendedRepository=true&getLatestBalanceReport=true&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path = self.prop.get('METERBALANCE_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_meterbalance_export_endpoint=str(get_meterbalance_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_meterbalance_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_meterbalance_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        with replacing value of the key from payload.
        :return: this function returns response body and status code
        """
        get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/export?locale=en-US&useExtendedRepository=true&getLatestBalanceReport=false&fileFormat=report_Type&exportType=METER_BALANCE_TYPE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/custom/export?locale=en_US&useExtendedRepository=true&getLatestBalanceReport=true&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path = self.prop.get('METERBALANCE_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds
        if key=='reportColumns':
            self.json_data[key] = value
        else:
            self.json_data['apiRequest'][key] = value

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_meterbalance_export_endpoint=str(get_meterbalance_export_endpoint.replace('report_Type',report))
            #print(get_meterbalance_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_meterbalance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_meterbalance_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics meterbalance api gets response or not
        by deleting keys from payload.
        :return: this function returns response body and status code
        """
        get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/export?locale=en-US&useExtendedRepository=true&getLatestBalanceReport=false&fileFormat=report_Type&exportType=METER_BALANCE_TYPE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_meterbalance_export_endpoint = self.endpoint + "/meterbalance/custom/export?locale=en_US&useExtendedRepository=true&getLatestBalanceReport=true&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path = self.prop.get('METERBALANCE_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        if key == 'reportColumns':
            del self.json_data[key]
        else:
            del self.json_data['apiRequest'][key]

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_meterbalance_export_endpoint=str(get_meterbalance_export_endpoint.replace('report_Type',report))
            #print(get_meterbalance_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_meterbalance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



