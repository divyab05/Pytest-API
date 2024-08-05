"""This module is used for articles api."""
import json
import logging

import requests

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_user_okta_token_utils import UserOktaUtilily

class ArticlesAPI:
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        endpoint = self.prop.get('SELFSERVICEPORTAL', 'base_api')
        self.endpoint = endpoint.replace("temp", str(self.app_config.env_cfg['env']).lower())
        self.headers = {"Host": self.endpoint[8:]}

        self.okta_token = "Bearer {}".format(
            UserOktaUtilily.get_user_okta_token(self, env= self.app_config.env_cfg['env'], user_name=self.app_config.env_cfg['CLIENTUSERNAME'], pwd=self.app_config.env_cfg['client_pwd']))
        self.email=self.app_config.env_cfg['CLIENTUSERNAME']

    def verify_res_schema(self, res, expected_schema):
        """
        Verifies the response matches with the schema definition
        """
        isValid = self.api.schema_validation(response_schema=res, expected_schema=expected_schema)

        return isValid

    def getArticleList(self,test_data):
        """
        Get the article list from the api
        """
        get_articleList_endpoint = self.endpoint + "/api/v1/articles_by_prod?product_name="+test_data['product_name']+"&locale="+test_data['locale']+""
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_user_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.log.info(self.json_data)
        self.log.info(get_articleList_endpoint)

        res = self.api.get_api_response(get_articleList_endpoint, headers=self.headers)

        status_code = res.status_code

        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code

    def getArticleListWithMeter(self,test_data):
        """
        Get the article list from the api
        """
        get_articleList_endpoint = self.endpoint + "/api/v1/articles_by_prod?product_name="+test_data['product_name']+"&locale="+test_data['locale']+"&sub_product_names="+test_data['sub_product_name']+""
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_meter_user_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.log.info(self.json_data)
        self.log.info(get_articleList_endpoint)

        res = self.api.get_api_response(get_articleList_endpoint, headers=self.headers)

        status_code = res.status_code

        #self.log.info(res)
        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code


    def getArticleById(self, articleNumber, locale):
        """
        Get the article content for a given article number from the api
        """
        get_articleList_endpoint = self.endpoint + "/api/v1/article/"+articleNumber+"?locale="+locale+""
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'article_id_user_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.log.info(self.json_data)
        self.log.info(get_articleList_endpoint)

        res = self.api.get_api_response(get_articleList_endpoint, headers=self.headers)

        status_code = res.status_code

        #self.log.info(res)
        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code

    def getCoveoSearchResult(self, test_data):
        """
        Get the coveo search results from the api
        """
        get_coveoSearch_endpoint = self.endpoint + "/api/v1/coveo_search?email="+self.email
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'coveo_search_request_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['cq'] = test_data['product_name']
        self.json_data['lq'] = test_data['search_string']
        self.json_data['context']['siteCountry'] = test_data['context_siteCountry']
        self.json_data['context']['siteLanguage'] = test_data['context_siteLanguage']
        self.json_data['context']['InputDescription'] = test_data['search_string']

        self.log.info(self.json_data)
        self.log.info(get_coveoSearch_endpoint)

        res = self.api.post_api_response(get_coveoSearch_endpoint, headers=self.headers,body=json.dumps(self.json_data))

        status_code = res.status_code

        #self.log.info(res)
        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code

    def getSuggestedArticleList(self,test_data):
        """
        Get the suggested article list from the api for a given plan
        """
        get_articleList_endpoint = self.endpoint + "/api/v1/support/articles?plan="+test_data['plan']+"&locale="+test_data['locale']+""
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_user_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.log.info(self.json_data)
        self.log.info(get_articleList_endpoint)

        res = self.api.get_api_response(get_articleList_endpoint, headers=self.headers)

        status_code = res.status_code

        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code

    def getSuggestedArticleListWithDevice(self,test_data):
        """
        Get the suggested article list from the api for a given plan and device type
        """
        get_articleList_endpoint = self.endpoint + "/api/v1/support/articles?plan="+test_data['plan']+"&device="+test_data['device']+"&locale="+test_data['locale']+""
        self.headers['Authorization'] = self.okta_token

        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_user_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.log.info(self.json_data)
        self.log.info(get_articleList_endpoint)

        res = self.api.get_api_response(get_articleList_endpoint, headers=self.headers)

        status_code = res.status_code

        self.log.info(status_code)

        if res is not None:
            res = res.json()
            #self.log.info(res)
            result = True
        return res, status_code

