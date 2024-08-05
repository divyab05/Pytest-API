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


class AssestDetailsAPI:
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
        self.headers = json.loads(self.prop.get('ASSEST_DETAILS_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        decoded_data = jwt.decode(jwt=self.access_token, algorithms=["RS256"], verify=False)
        self.entID = decoded_data['claim_spa']['entID']

        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_assest_detail_api_response(self, startdate , enddate, divisionIds="",api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type=="Overall_Summary":
            file_path=self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_overall_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type=="Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_assest_detail_api_authorisation(self,startdate , enddate,expired_token, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_assest_detail_api_header(self,startdate , enddate,invalid_header, divisionIds="",api_type="Overall_Summary"):

        """
                This function is validates if analytics assest api gets response or not
                with different header type.
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False
        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    def verify_assest_detail_api_response_with_orderby_value(self, startdate , enddate, orderByCriteria,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics assest api gets response or not
        with orderby value.
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['orderByCriteria'] = orderByCriteria

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_assest_detail_api_response_with_groupby_value(self, startdate , enddate, groupByCriteria,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics assest api gets response or not
        with group by value.
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['groupByCriteria'] = groupByCriteria

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    def verify_assest_detail_api_response_without_response_type(self, startdate , enddate,divisionIds="",api_type="Overall_Spend_Summary"):
        """
        This function is validates if analytics assest api gets response or not
        without_response_type value.
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['responseType'] = ""

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        '''if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True'''
        return res, status_code


    def verify_assest_details_api_response_with_subfilter_value(self, startdate, enddate, subfilter,type, divisionIds="",
                                                     api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not
        with with_subfilter_value.
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['subFilter'][type] = subfilter


        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Assest response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_assest_detail_api_response_with_payload(self, startdate , enddate, payload,divisionIds="",api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not with_payload
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type=="Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', payload).replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open( file_path) as f:
                self.json_data = json.load(f)
        elif api_type=="Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', payload).replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        if self.json_data!={}:
            self.json_data['filter']['startdate'] = startdate
            self.json_data['filter']['endDate'] = enddate
            self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:

            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_assest_detail_api_response_with_source_value(self, startdate , enddate, source,divisionIds="",api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not with_source_value
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['source'] = source



        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_assest_detail_api_response_with_queryType_value(self, startdate , enddate, query,divisionIds="",api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not with_queryType_value(
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds
        self.json_data['queryType'] = query



        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_assest_details_api_response_with_filter_value(self, filterValue, api_type="Summary"):
        """
        This function is validates if analytics resets api gets response or not with_filter_value
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails?useExtendedRepository=true"
        if api_type == "Overall_Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_overall_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)
        elif api_type == "Summary":
            file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_summary').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)

        result = False

        self.json_data['filter']=filterValue

        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Assest details API response:")
            self.log.info(res)
            result = True
        return res, status_code



    def verify_assest_detail_paginated_api_response(self, startdate , enddate, divisionIds="",api_type="Overall_Summary"):
        """
        This function is validates if analytics assest api gets response or not for pagination
        :return: this function returns boolean status of element located
        """
        get_assest_details_endpoint = self.endpoint + "/recv/assestDetails/paginated?pageNumber=1&pageSize=1&useExtendedRepository=true"

        if api_type=="Overall_Summary":
            file_path=self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_overall_summary').replace("temp", str(self.app_config.env_cfg['env']).lower())
            with open(file_path) as f:
                self.json_data = json.load(f)


        result = False

        self.json_data['filter']['startdate'] = startdate
        self.json_data['filter']['endDate'] = enddate
        self.json_data['filter']['divisionIds'] = divisionIds



        res = self.api.post_api_response(
            endpoint=get_assest_details_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Assest API response:")
            #self.log.info(res)
            result = True
        return res,status_code




    #For Export API

    def verify_assest_detail_export_api_response(self, startdate, enddate, divisionIds=""):
        """
        This function is validates if analytics assest api gets response or not
        :return: this function returns boolean status of element located
        """
        get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        file_path=self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['recvProductsApiRequest']['filter']['startdate'] = startdate
        self.json_data['recvProductsApiRequest']['filter']['endDate'] = enddate
        self.json_data['recvProductsApiRequest']['filter']['divisionIds'] = divisionIds

        report_type=['CSV','XLSX']
        response_array=[]
        for report in report_type:
            get_assest_details_export_endpoint=str(get_assest_details_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_assest_details_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)


        return response_array[0],response_array[1]





    def verify_assest_detail_export_api_authorisation(self,startdate , enddate,expired_token, divisionIds=""):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))

        get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE"

        file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['recvProductsApiRequest']['filter']['startdate'] = startdate
        self.json_data['recvProductsApiRequest']['filter']['endDate'] = enddate
        self.json_data['recvProductsApiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_assest_details_export_endpoint=str(get_assest_details_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_assest_details_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_assest_detail_export_api_header(self,startdate , enddate,invalid_header, divisionIds=""):

        """
                This function is validates if analytics assest api gets response or not
                with different header type.
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE"
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/custom/export?locale=en_US&fileFormat=report_Type&exportType=CUSTOM_REPORT"

        file_path = self.prop.get('ASSEST_DETAILS_API_MGMT', 'body_path_export').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['recvProductsApiRequest']['filter']['startdate'] = startdate
        self.json_data['recvProductsApiRequest']['filter']['endDate'] = enddate
        self.json_data['recvProductsApiRequest']['filter']['divisionIds'] = divisionIds

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_assest_details_export_endpoint=str(get_assest_details_export_endpoint.replace('report_Type',report))
            res = self.api.post_api_response(
                endpoint=get_assest_details_export_endpoint, headers=header1, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]



    def verify_assest_detail_export_api_response_with_key_and_value(self, startdate , enddate, key,value,divisionIds=""):
        """
        This function is validates if analytics assest api gets response or not with key and value,
        key can be any key in payload and value will be updated value of that key.
        :return: this function returns response and status code
        """
        get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        file_path=self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False

        self.json_data['recvProductsApiRequest']['filter']['startdate'] = startdate
        self.json_data['recvProductsApiRequest']['filter']['endDate'] = enddate
        self.json_data['recvProductsApiRequest']['filter']['divisionIds'] = divisionIds
        if key=='reportColumns':
            self.json_data[key] = value
        else:
            self.json_data['recvProductsApiRequest'][key] = value

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_assest_details_export_endpoint=str(get_assest_details_export_endpoint.replace('report_Type',report))
            #print(get_assest_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_assest_details_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]


    def verify_assest_detail_export_api_response_by_deleting_key_in_payload(self, startdate , enddate, key,divisionIds=""):
        """
        This function is validates if analytics assest api gets response or not by_deleting_key_in_payload,
        key can be any key which we have to delete.
        :return: this function returns response and status code
        """
        get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            get_assest_details_export_endpoint = self.endpoint + "/recv/assestDetails/export?locale=en_US&fileFormat=report_Type&exportType=RECEIVING_PRODUCTS_USAGE&enterpriseId="+self.entID+"&userId="+self.app_config.logIn_cfg['client_id']

        file_path=self.prop.get('ASSEST_DETAILS_API_MGMT','body_path_export').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)


        result = False


        self.json_data['recvProductsApiRequest']['filter']['startdate'] = startdate
        self.json_data['recvProductsApiRequest']['filter']['endDate'] = enddate
        self.json_data['recvProductsApiRequest']['filter']['divisionIds'] = divisionIds

        if key == 'reportColumns':
            del self.json_data[key]
        else:
            del self.json_data['recvProductsApiRequest'][key]

        report_type = ['CSV', 'XLSX']
        response_array = []
        for report in report_type:
            get_assest_details_export_endpoint=str(get_assest_details_export_endpoint.replace('report_Type',report))
            #print(get_assest_details_export_endpoint)
            res = self.api.post_api_response(
                endpoint=get_assest_details_export_endpoint, headers=self.headers, body=json.dumps(self.json_data))
            status_code = res.status_code
            response_array.append(status_code)

        return response_array[0], response_array[1]

