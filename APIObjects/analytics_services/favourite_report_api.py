"""This module is used for main page objects."""

import logging

from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.get_okta_token_utils import OktaUtilily
from FrameworkUtilities.get_user_okta_token_utils import UserOktaUtilily
import json
import random

from context import Context


class FavouriteReportAPI:
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
        self.headers = json.loads(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"]=common_utils.get_x_user_id_from_okta(self.access_token)
        # self.log = log_utils.custom_logger(logging.INFO)




#-------------------------------------------Get all favourite reports---------------------------------------------------
    def verify_favourite_report_get_api_response(self):
        """
        This function is validates if analytics favourite report get api gets response or not

        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint + '/favourite/report/templates'


        res = self.api.get_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Favourite Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_favourite_report_get_api_response_with_header(self,headerType,val):
        """
        This function is validates if analytics favourite report get api gets response or not
        with response header
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint + '/favourite/report/templates'
        h1 = self.headers.copy()
        #print(self.headers["X-UserId"])
        h1[headerType] = val

        res = self.api.get_api_response(
            endpoint=get_favourite_report_endpoint, headers=h1)
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_favourite_report_get_api_authorization(self,token):
        """
        This function is validates if analytics favourite report get api gets response or not
        with okta token is passed.
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint + '/favourite/report/templates'
        h1=self.headers.copy()
        h1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))

        res = self.api.get_api_response(
            endpoint=get_favourite_report_endpoint, headers=h1)
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res, status_code



# -------------------------------------------Creation of new favourite reports---------------------------------------------------
    def verify_favourite_report_creation_api_response(self,name):
        """
        This function is validates if analytics favourite report create api gets response or not
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_favourite_report_creation_api_response_with_templateinfo_and_val(self,name,val):
        """
        This function is validates if analytics favourite report create api gets response or not
        with templateinfo keys and values
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        self.json_data['templateInfo'] = val
        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_favourite_report_creation_api_response_with_property_and_val(self,name,prop,val):
        """
        This function is validates if analytics favourite report create api gets response or not
        with any key and value pair
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        self.json_data['templateInfo']['prop'] = val
        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code







#-------------------------------------------Get details of perticular favourite reports---------------------------------------------------

    def verify_favourite_report_getdetails_api_response(self,name):
        """
        This function is validates if analytics favourite report getdetails api gets response or not
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/getDetails'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_getdetails_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code


    def verify_favourite_report_getdetails_api_response_with_deleting_keys(self,name,val):
        """
        This function is validates if analytics favourite report getdetails api gets response or not
        by deleting keys from json data
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/delete'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_getdetails_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        data=self.json_data.copy()
        del data[val]

        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code



#-------------------------------------------Update last run of favourite reports---------------------------------------------------

    def verify_favourite_report_update_last_run_api_response(self,name):
        """
        This function is validates if analytics favourite report updateLastRun api gets response or not

        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/updateLastRunDate'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_updateLastRun_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        res = self.api.put_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code




    def verify_favourite_report_update_last_run_api_response_with_deleting_keys(self,name,val):
        """
        This function is validates if analytics favourite report updateLastRun api gets response or not
        by deleting keys in json data
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/updateLastRunDate'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_getdetails_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        data=self.json_data.copy()
        del data[val]

        res = self.api.put_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code


#-------------------------------------------Delete favourite reports---------------------------------------------------

    def verify_favourite_report_delete_api_response(self,name):
        """
        This function is validates if analytics favourite report delete api gets response or not
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/delete'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_delete_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            #self.log.info(res)
            result = True
        return res,status_code




    def verify_favourite_report_delete_api_response_with_deleting_keys(self,name,val):
        """
        This function is validates if analytics favourite report delete api gets response or not
        by deleting keys in payload
        :return: this function return response and status code
        """
        get_favourite_report_endpoint = self.endpoint+'/favourite/report/template/delete'




        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_delete_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        self.json_data['name'] = name
        data=self.json_data.copy()
        del data[val]

        res = self.api.post_api_response(
            endpoint=get_favourite_report_endpoint, headers=self.headers, body=json.dumps(data))
        status_code = res.status_code

        if res is not None:
            # res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res,status_code




#----------------------------------------------Favourite Report update Api------------------------------------------

    def verify_favourite_report_update_api_response_with_key_and_value(self,key,val,report):
        """
        This function is validates if analytics favourite report get api gets response or not

        :return: this function return response and status code
        """
        get_favourite_report_update_endpoint = self.endpoint + '/favourite/report/template/report'

        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        report['templateInfo'][key]['field1'] = val


        res = self.api.put_api_response(
            endpoint=get_favourite_report_update_endpoint, headers=self.headers, body=json.dumps(report))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res, status_code


    def verify_favourite_report_update_api_response_with_header(self,key,val,report,contentType):
        """
        This function is validates if analytics favourite report get api gets response or not
        with response header
        :return: this function return response and status code
        """
        get_favourite_report_update_endpoint = self.endpoint + '/favourite/report/template/report'
        h1 = self.headers.copy()
        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(
                self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        report['templateInfo'][key]['field1'] = val
        h1['Content-Type'] = contentType

        res = self.api.put_api_response(
            endpoint=get_favourite_report_update_endpoint, headers=h1, body=json.dumps(report))
        status_code = res.status_code

        if res is not None:
            #res = res.json()
            self.log.info("Favourite Report API response:")
            self.log.info(res)
            result = True
        return res, status_code

    def verify_favourite_report_update_api_authorization(self,key,val,report,expired_token):
        """
        This function is validates if analytics favourite report get api gets response or not
        with okta token is passed.
        :return: this function return response and status code
        """
        get_favourite_report_update_endpoint = self.endpoint + '/favourite/report/template/report'
        h1=self.headers.copy()
        if expired_token == 'yes':
            h1['Authorization'] = "Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))

        with open(self.prop.get('FAVOURITE_REPORT_API_MGMT', 'body_path').replace("temp", str(
                self.app_config.env_cfg['env']).lower())) as f:
            self.json_data = json.load(f)

        self.json_data['userId'] = self.headers['X-UserId']
        report['templateInfo'][key]['field1'] = val


        res = self.api.put_api_response(
            endpoint=get_favourite_report_update_endpoint, headers=h1, body=json.dumps(report))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Favourite Report API response:")
            #self.log.info(res)
            result = True
        return res, status_code


