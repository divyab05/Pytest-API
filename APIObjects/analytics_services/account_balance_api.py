"""This module is used for main page objects."""

import logging
import jwt



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class AccountBalanceAPI:
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
        self.headers = json.loads(self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        decoded_data = jwt.decode(jwt=self.access_token, algorithms=["RS256"], verify=False)
        self.entID= decoded_data['claim_spa']['entID']

        # self.log = log_utils.custom_logger(logging.INFO)


    def verify_account_balance_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        :return: this function returns json response and status code
        """

        #get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=100"
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=en-US&pageNumber=1&pageSize=300"
        file_path=self.prop.get('ACCOUNT_BALANCE_API_MGMT','body_path_account_balance').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)




        result = False

        self.json_data['filter']['startdate'] = str(startdate)
        self.json_data['filter']['endDate'] = str(enddate)
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res,status_code



    def verify_account_balance_api_authorisation(self,startdate , enddate,expired_token, divisionIds=""):

        """
                This function is validates if analytics account_balance api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=en-US&pageNumber=1&pageSize=300"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_account_balance_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics account_balance api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=100"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code





    def verify_account_balance_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns json response and status code
        """
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=en-US&pageNumber=1&pageSize=300"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data[key] = value



        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_account_balance_api_response_with_deleting_keys_in_payload(self, startdate , enddate, keyTobeDelete,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with group by value.
        :return: this function returns json response and status code
        """
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=100"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data[keyTobeDelete]

        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code




    def verify_account_balance_api_response_with_key_and_value_in_subfilter(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns json response and status code
        """
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=100"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][key] = value

        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_account_balance_api_response_with_deleting_key_in_subfilter(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics account_balance api gets response or not
        with orderby value.
        :return: this function returns json response and status code
        """
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=100"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        del self.json_data['subFilter'][key]

        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Account Balance API response:")
            self.log.info(res)
            result = True
        return res, status_code
    
    def verify_account_balance_paginated_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if analytics  account_balance api gets response or not
        :return: this function returns json response and status code
        """
        get_account_balance_endpoint = self.endpoint + "/account_balance_details/paginated?locale=locale%3Den-US%26pageNumber%3D1%26pageSize%3D300&pageNumber=1&pageSize=1"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_account_balance').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_account_balance_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code

    #Export API
    
    def verify_account_balance_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics  account_balance export api gets response or not
        :return: this function returns json response and status code
        """
        get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        file_path=self.prop.get('ACCOUNT_BALANCE_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_account_balance_export_endpoint=str(get_account_balance_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_account_balance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]




    def verify_account_balance_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds=""):

        """
                This function is validates if analytics  account_balance export api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en_US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE_TYPE"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en_US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE_TYPE"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_account_balance_export_endpoint = str(get_account_balance_export_endpoint.replace('report_Type', report))
            res = self.api.post_api_response(
                endpoint=get_account_balance_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]






    def verify_account_balance_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics  account_balance export api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en_US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE_TYPE"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/custom/export?locale=en_US&fileFormat=report_Type&exportType=CUSTOM_REPORT"
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_account_balance_export_endpoint=str(get_account_balance_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_account_balance_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_account_balance_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics  account_balance export api gets response or not
        :return: this function returns json response and status code
        """
        get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_account_balance_export_endpoint=str(get_account_balance_export_endpoint.replace('report_Type',report))
            #print(get_assest_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_account_balance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_account_balance_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics  account_balance export api gets response or not
        :return: this function returns json response and status code
        """
        get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_account_balance_export_endpoint = self.endpoint + "/account_balance_details/export?locale=en-US&fileFormat=report_Type&exportType=ACCOUNT_BALANCE&customFieldRequired=true&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        file_path = self.prop.get('ACCOUNT_BALANCE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_account_balance_export_endpoint=str(get_account_balance_export_endpoint.replace('report_Type',report))
            #print(get_assest_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_account_balance_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]
