"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class SuppliesAPI:
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
        self.headers = json.loads(self.prop.get('SUPPLIES_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)


#------------------------------------Supplies Api------------------------------------------


    def verify_supplies_api_response(self, startdate , enddate, divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT','body_path_supplies').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds


        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res,status_code




    def verify_supplies_api_authorization(self, startdate , enddate, token,divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with authorization token
        :return: this function returns json response and status code
        """

        h1=self.headers.copy()
        h1['Authorization']=token


        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=h1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_supplies_api_response_with_header(self, startdate , enddate, contentVal,divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with header
        :return: this function returns json response and status code
        """

        h1=self.headers.copy()
        h1['Content-Type']=contentVal

        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=h1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_supplies_api_response_with_groupByCriteria(self, startdate , enddate,type,val ,divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with groupby criteria value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'][type]= val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_supplies_api_response_with_orderByCriteria(self, startdate , enddate,type,val ,divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with order by criteria
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'][type]= val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res,status_code

    def verify_supplies_api_response_with_subFilter(self, startdate, enddate, type, val, divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with subfilter value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint + "/supplies?locale=en_US"
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][type] = val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_supplies_api_response_with_Filter(self, startdate, enddate, type, val, divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with filter value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filter'][type] = val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_supplies_api_response_with_Filtergroup_value(self, startdate, enddate, val , divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with filtergroup value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['filtersGroup'] = val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_supplies_api_response_with_selectQueryColumnsList_value(self, startdate, enddate, val , divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with select query values
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['selectQueryColumnsList'] = val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_supplies_api_response_with_responseType_value(self, startdate, enddate, val , divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with response type value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies?locale=en-US'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = val

        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_supplies_paginated_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if supplies api gets response or not
        with response type value
        :return: this function returns json response and status code
        """
        get_supplies_endpoint = self.endpoint +'/supplies/paginated?locale=en-US&pageNumber=1&pageSize=1'
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_supplies').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds


        res = self.api.post_api_response(
            endpoint=get_supplies_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Supplies API response:")
            self.log.info(res)
            result = True
        return res, status_code



    #Export
    def verify_supplies_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics supplies api gets response or not
        :return: this function returns json response and status code
        """
        
        get_supplies_export_endpoint = self.endpoint + "/supplies/export?locale=en_US&query=locale%3Den-US%26exportType%3DSUPPLY_BY_LOCATION%26fileFormat%3DXLSX%26query%3DLAS&fileFormat=report_Type&exportType=SUPPLY_BY_LOCATION"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_supplies_export_endpoint = self.endpoint + "/supplies/custom/export?locale=en-US&exportType=SUPPLY_BY_LOCATION&fileFormat=report_Type&query=LAS"

        file_path=self.prop.get('SUPPLIES_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_supplies_export_endpoint=str(get_supplies_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_supplies_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]




    def verify_supplies_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics supplies api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        
        
        get_supplies_export_endpoint = self.endpoint + "/supplies/export?locale=en_US&query=locale%3Den-US%26exportType%3DSUPPLY_BY_LOCATION%26fileFormat%3DXLSX%26query%3DLAS&fileFormat=report_Type&exportType=SUPPLY_BY_LOCATION"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_supplies_export_endpoint = self.endpoint + "/supplies/custom/export?locale=en-US&exportType=SUPPLY_BY_LOCATION&fileFormat=report_Type&query=LAS"

        
        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_supplies_export_endpoint = str(get_supplies_export_endpoint.replace('report_Type', report))
            res = self.api.post_api_response(
                endpoint=get_supplies_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]






    def verify_supplies_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics supplies api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        
        get_supplies_export_endpoint = self.endpoint + "/supplies/export?locale=en_US&query=locale%3Den-US%26exportType%3DSUPPLY_BY_LOCATION%26fileFormat%3DXLSX%26query%3DLAS&fileFormat=report_Type&exportType=SUPPLY_BY_LOCATION"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_supplies_export_endpoint = self.endpoint + "/supplies/custom/export?locale=en-US&exportType=SUPPLY_BY_LOCATION&fileFormat=report_Type&query=LAS"

        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_supplies_export_endpoint=str(get_supplies_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_supplies_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_supplies_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics supplies api gets response or not
        with perticular key and its value in json payload.
        :return: this function returns json response and status code
        """
        
        get_supplies_export_endpoint = self.endpoint + "/supplies/export?locale=en_US&query=locale%3Den-US%26exportType%3DSUPPLY_BY_LOCATION%26fileFormat%3DXLSX%26query%3DLAS&fileFormat=report_Type&exportType=SUPPLY_BY_LOCATION"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_supplies_export_endpoint = self.endpoint + "/supplies/custom/export?locale=en-US&exportType=SUPPLY_BY_LOCATION&fileFormat=report_Type&query=LAS"

        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_supplies_export_endpoint=str(get_supplies_export_endpoint.replace('report_Type',report))
            #print(get_supplies_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_supplies_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_supplies_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics supplies api gets response or not
        by deleting the key in json payload.
        :return: this function returns json response and status code
        """
        
        get_supplies_export_endpoint = self.endpoint + "/supplies/export?locale=en_US&query=locale%3Den-US%26exportType%3DSUPPLY_BY_LOCATION%26fileFormat%3DXLSX%26query%3DLAS&fileFormat=report_Type&exportType=SUPPLY_BY_LOCATION"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_supplies_export_endpoint = self.endpoint + "/supplies/custom/export?locale=en-US&exportType=SUPPLY_BY_LOCATION&fileFormat=report_Type&query=LAS"

        file_path = self.prop.get('SUPPLIES_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_supplies_export_endpoint=str(get_supplies_export_endpoint.replace('report_Type',report))
            #print(get_supplies_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_supplies_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]

