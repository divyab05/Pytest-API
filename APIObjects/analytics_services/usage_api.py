"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily

import json
import random

from context import Context


class UsageAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self,app_config, access_token):
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint=(self.app_config.env_cfg['base_api'])
        #endpoint = self.prop.get('USAGE_API_MGMT', 'base_api')
        #self.endpoint = endpoint.replace("temp", str(self.app_config.env_cfg['env']).lower())
        self.headers = json.loads(self.prop.get('USAGE_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_usage_api_response(self, startdate , enddate, divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gets response or not
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type=="Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT','body_path_overall_spent_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        elif api_type=="Summary":
            file_path = self.prop.get('USAGE_API_MGMT','body_path_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        elif api_type=="Details":

            file_path = self.prop.get('USAGE_API_MGMT','body_path_details').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds


        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            print("TESTING")
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_usage_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Spend_Summary"):

        """
                This function is validates if analytics usage api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_usage_api_header(self,startdate , enddate,invalid_header, divisionIds="",api_type="Overall_Spend_Summary"):

        """
                This function is validates if analytics usage api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code


        return res, status_code



    def verify_usage_api_response_with_orderby_value(self, startdate , enddate, orderByCriteria,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gets response or not
        with orderby value.
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'] = orderByCriteria

        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code




    def verify_usage_api_response_with_groupby_value(self, startdate , enddate, groupByCriteria,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gets response or not
        with group by value.
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'] = groupByCriteria



        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code

    def verify_usage_api_response_with_subfilter_value(self, startdate, enddate, subfilter,type, divisionIds="",
                                                     api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gets response or not
        with subfilter value.
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][type] = subfilter


        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_usage_api_response_without_response_type(self, startdate , enddate, divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gives error or not
        without response type.
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = ""


        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code

    def verify_usage_api_response_with_selectQueryColumnsList(self, startdate , enddate, selectQueryColumnsList,divisionIds="",api_type="Overall_Spend_Summary"):
        """
                This function is validates if analytics usage api gets response or not
                with select query column list.
                :return: this function returns json response and status code
                """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['selectQueryColumnsList'] = selectQueryColumnsList

        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_usage_api_response_with_subfilter_type_and_value(self, startdate , enddate, subFilterType,val,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics usage api gets response or not with_subfilter_type_and_value in json payload
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type == "Overall_Spend_Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_overall_spent_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Details":
            file_path = self.prop.get('USAGE_API_MGMT', 'body_path_details').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][subFilterType] = val

        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            print("TESING")
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_usage_paginated_api_response(self, startdate , enddate, divisionIds="",api_type="Details"):
        """
        This function is validates if analytics usage api working for pagination with not
        by passing pagesize=1
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage/paginated?locale=en_US&pageNumber=1&pageSize=1"
        if api_type=="Details":
            file_path = self.prop.get('USAGE_API_MGMT','body_path_details').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds


        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code


    #Export API

    def verify_usage_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics usage api gets response or not
        :return: this function returns json response and status code
        """
        get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        if self.app_config.env_cfg['product_name']=='fedramp':
            get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        file_path=self.prop.get('USAGE_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['apiRequest']['filter']['startdate'] = startdate
        self.json_data['apiRequest']['filter']['endDate'] = enddate
        self.json_data['apiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_usage_export_endpoint=str(get_usage_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_usage_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]




    def verify_usage_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics usage api is well authorized or not
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        if self.app_config.env_cfg['product_name']=='fedramp':
            get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        file_path = self.prop.get('USAGE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_usage_export_endpoint = str(get_usage_export_endpoint.replace('report_Type', report))
            res = self.api.post_api_response(
                endpoint=get_usage_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]






    def verify_usage_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics usage api gets response or not
                with different header type.
                :return: this function returns json response and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        if self.app_config.env_cfg['product_name']=='fedramp':
            get_usage_export_endpoint = self.endpoint + "/usage/custom/export?locale=en_US&fileFormat=report_Type&exportType=CUSTOM_REPORT"
        file_path = self.prop.get('USAGE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_usage_export_endpoint=str(get_usage_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_usage_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_usage_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics usage api gets response or not
        with_key_and_value in json payload.
        :return: this function returns json response and status code
        """
        get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        if self.app_config.env_cfg['product_name']=='fedramp':
            get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        file_path = self.prop.get('USAGE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_usage_export_endpoint=str(get_usage_export_endpoint.replace('report_Type',report))
            #print(get_usage_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_usage_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_usage_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics usage api gets response or not
        by_deleting_key in json payload.
        :return: this function returns json response and status code
        """
        get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        if self.app_config.env_cfg['product_name']=='fedramp':
            get_usage_export_endpoint = self.endpoint + "/usage/export?locale=en_US&fileFormat=report_Type&exportType=SPEND_BY_LOCATION"
        
        file_path = self.prop.get('USAGE_API_MGMT', 'body_path_export').replace("temp", str(
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
            get_usage_export_endpoint=str(get_usage_export_endpoint.replace('report_Type',report))
            #print(get_usage_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_usage_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]




    def verify_usage_api_reports_response(self, startdate , enddate, divisionIds="",api_type="Summary"):
        """
        This function is validates if analytics usage api gets response or not
        :return: this function returns json response and status code
        """
        get_usage_endpoint = self.endpoint + "/usage?isShippingUsageRequired=false&locale=en-US"
        if api_type=="Summary":
            file_path = self.prop.get('USAGE_API_MGMT','body_path_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        elif api_type=="Details":
            get_usage_endpoint = self.endpoint +"/usage/paginated?locale=en_US&pageNumber=1&pageSize=1001"
            file_path = self.prop.get('USAGE_API_MGMT','body_path_details').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds


        res = self.api.post_api_response(
            endpoint=get_usage_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            print("TESTING")
            res = res.json()
            self.log.info("Usage API response:")
            self.log.info(res)
            result = True
        return res,status_code

