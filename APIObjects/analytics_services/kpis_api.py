"""This module is used for main page objects."""

import logging



from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily
from FrameworkUtilities.request_utils import send_request_based_on_http_method

import json
import random

from context import Context


class KpisAPI:
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
        self.headers = json.loads(self.prop.get('KPIS_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"] = common_utils.get_x_user_id_from_okta(self.access_token)
        # self.log = log_utils.custom_logger(logging.INFO)



    def verify_kpis_api_status_code(self):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns json response and status code
        """
        get_verify_kpis_api_endpoint = self.endpoint + "/kpis"


        res = send_request_based_on_http_method(
            request_url=get_verify_kpis_api_endpoint,params="", headers=self.headers,body='', method_type='get', others=1)
        status_code = res['response_code']


        if res is not None:
            self.log.info("KPIS API response:")


        return res['response_body'],status_code




    def verify_kpis_api_response_authorisation(self,expired_token,with_context=""):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns json response and status code
        """
        get_verify_kpis_api_endpoint = self.endpoint + "/kpis"


        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))

        res = self.api.get_api_response(
            endpoint=get_verify_kpis_api_endpoint, headers=header1)
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("KPIS API response:")


        return res,status_code



