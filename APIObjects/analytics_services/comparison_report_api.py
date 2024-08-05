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


class ComparisonReportAPI:
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
        self.headers = json.loads(self.prop.get('COMPARISON_REPORT_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"] = common_utils.get_x_user_id_from_okta(self.access_token)

        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_comparison_report_api_response(self):
        """
        This function is validates if analytics comparison api gets response or not
        :return: this function returns boolean status of element located
        """
        get_comparison_report_endpoint = self.endpoint + "/usage/custom/comparisonReportExport?locale=en-US&fileFormat=XLSX&exportType=SPEND_BY_LOCATION&useExtendedRepository=true"
        file_path=self.prop.get('COMPARISON_REPORT_API_MGMT','body_path_comparison_report').replace("temp", str(self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)




        result = False



        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.text
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_comparison_report_api_authorisation(self,expired_token):

        """
                This function is validates if analytics comparison api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_comparison_report_endpoint = self.endpoint + "/usage/custom/comparisonReportExport?locale=en_US&query=locale%3Den_US%26fileFormat%3DXLSX%26exportType%3DCUSTOM_REPORT&fileFormat=XLSX&exportType=SPEND_BY_LOCATION"
        file_path = self.prop.get('COMPARISON_REPORT_API_MGMT', 'body_path_comparison_report').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_comparison_report_api_header(self, invalid_header):

        """
                This function is validates if analytics comparison api gets response or not
                with different header type.
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_comparison_report_endpoint = self.endpoint + "/usage/custom/comparisonReportExport?locale=en_US&query=locale%3Den_US%26fileFormat%3DXLSX%26exportType%3DCUSTOM_REPORT&fileFormat=XLSX&exportType=SPEND_BY_LOCATION"
        file_path = self.prop.get('COMPARISON_REPORT_API_MGMT', 'body_path_comparison_report').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    #Comparison Report getStatus API

    def verify_comparison_report_getStatus_api_response(self,reportID):
        """
        This function is validates if analytics comparison api gets response or not
        :return: this function returns boolean status of element located
        """
        get_comparison_report_endpoint = self.endpoint + "/ComparisonReport/getStatus?Report_Id="+ reportID

        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            res = res.text
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_comparison_report_getStatus_api_authorisation(self,expired_token,reportID):

        """
                This function is validates if analytics comparison api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_comparison_report_endpoint = self.endpoint + "/ComparisonReport/getStatus?Report_Id=" + reportID

        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=header1)
        status_code = res.status_code

        if res is not None:
            res = res.text
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    #Comparison Report  generatePresignedUrl API

    def verify_comparison_report_generatePresignedUrl_api_response(self,reportID):
        """
        This function is validates if analytics comparison api gets response or not
        :return: this function returns boolean status of element located
        """
        get_comparison_report_endpoint = self.endpoint + "/ComparisonReport/generatePresignedUrl?Report_Id={arg1}&fileFormat=XLSX"
        get_comparison_report_endpoint=str(get_comparison_report_endpoint).format(arg1=reportID)

        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.text
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_comparison_report_generatePresignedUrl_api_authorisation(self,expired_token,reportID):

        """
                This function is validates if analytics comparison api is well authorized or not
                :return: this function returns boolean status of element located
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_comparison_report_endpoint = self.endpoint + "/ComparisonReport/generatePresignedUrl?Report_Id={arg1}&fileFormat=XLSX"
        get_comparison_report_endpoint = str(get_comparison_report_endpoint).format(arg1=reportID)
        result = False

        res = self.api.post_api_response(
            endpoint=get_comparison_report_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.text
            self.log.info("Comparison Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code


