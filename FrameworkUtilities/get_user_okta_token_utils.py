"""
This module contains api utility functions.
"""

import logging
import requests, re
from traceback import print_stack
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
import FrameworkUtilities.logger_utility as log_utils


class UserOktaUtilily:
    """
    This class with give us function to fetch okta token.
    """

    # TO DO: Generating access token and related login activity is being handle by login_api.py class.
    # This class can be removed after refactoring its usages.

    def __init__(self, app_config):
        self.log = log_utils.custom_logger(logging.INFO)
        self.app_config = app_config

    def get_user_okta_token(self, env='', user_name='', pwd=''):
        """
        This method is used to return the api response
        :return: This method return the api response
        """
        try:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            res = requests.post(self.app_config.logIn_cfg['okta_log_in_auth_url'],
                                data='{"username":"'+user_name+'","password":"'+pwd+'"}',
                                headers={"Content-Type": "application/json"})

            json_data = res.json()
            session_token = json_data['sessionToken']

            headr = {"Authorization": "okta_client_credential"}
            updated_url = self.app_config.logIn_cfg['okta_preview_auth_url']
            params = {'client_id': self.app_config.logIn_cfg['client_id'],
                      'scope': self.app_config.logIn_cfg['scope'],
                      'response_type': self.app_config.logIn_cfg['response_type'],
                      'redirect_uri': self.app_config.logIn_cfg['redirect_uri'],
                      'nonce': self.app_config.logIn_cfg['nonce'],
                      'state': self.app_config.logIn_cfg['state'],
                      'response_mode': self.app_config.logIn_cfg['response_mode'],
                      'sessionToken': self.app_config.logIn_cfg['sessionToken'].replace('[tok]', session_token)}
            new_res = requests.get(updated_url, headers=headr, params=params, verify=False)
            html_data = new_res.content
            okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
            return okta_token

        except HTTPError as http_err:
            self.log.error(
                f'HTTP Error occurred while generating okta.please check for proper credentials.\n{http_err}')
            print_stack()

        except Exception as ex:
            self.log.error(
                f'Failed to get the response, other error occurred while generating okta.please check for proper credentials.\n{ex}')
            print_stack()

        # elif (env == "DEV") :
        #     try:
        #         res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
        #                              data='{"username":"'+user_name+'","password":"'+pwd+'"}',
        #                              headers={"Content-Type": "application/json"})
        #         # res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
        #         #                      data='{"username":"' + Context.USERNAME + '","password":"' + Context.PASSWORD + '"}',
        #         #                      headers={"Content-Type": "application/json"})
        #
        #         json_data = res.json()
        #         sessionToken = json_data['sessionToken']
        #
        #         url = "https://pitneybowes.oktapreview.com/oauth2/austlaq2lihWmiUEP0h7/v1/authorize?client_id=0oatl85b03pUUq2w70h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
        #             sessionToken)
        #
        #         headr = {"Authorization": "okta_client_credential"}
        #         new_res = requests.get(url, headers=headr)
        #         html_data = new_res.content
        #         okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
        #         #userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]
        #
        #
        #     except HTTPError as http_err:
        #         self.log.error(
        #             f'HTTP Error occurred while generating okta.please check for proper credentials.\n{http_err}')
        #         print_stack()
        #
        #     except Exception as ex:
        #         self.log.error(
        #             f'Failed to get the response, other error occurred while generating okta.please check for proper credentials.\n{ex}')
        #         print_stack()



    # def get_userid_token(self, env):
    #     """
    #     This method is used to return the api response
    #     :return: This method return the api response
    #     """
    #
    #     if Context.ENV == "DEV":
    #         try:
    #             # res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
    #             #                    data='{"username":"demouser@yopmail.com","password":"Aqswde@123"}',
    #             #                    headers={"Content-Type": "application/json"})
    #             res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
    #                                 data='{"username":"' + Context.USERNAME + '","password":"' + Context.PASSWORD + '"}',
    #                                 headers={"Content-Type": "application/json"})
    #
    #             json_data = res.json()
    #             sessionToken = json_data['sessionToken']
    #
    #             url = "https://pitneybowes.oktapreview.com/oauth2/austlaq2lihWmiUEP0h7/v1/authorize?client_id=0oatl85b03pUUq2w70h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
    #                 sessionToken)
    #
    #             headr = {"Authorization": "okta_client_credential"}
    #             new_res = requests.get(url, headers=headr)
    #             html_data = new_res.content
    #             # okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
    #             userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]
    #
    #
    #         except HTTPError as http_err:
    #             self.log.error(f'HTTP Error occurred.\n{http_err}')
    #             print_stack()
    #
    #         except Exception as ex:
    #             self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
    #             print_stack()
    #
    #     elif Context.ENV == "QA":
    #         try:
    #             res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
    #                                 data='{"username":"tanu@mailinator.com","password":"Aqswde@123"}',
    #                                 headers={"Content-Type": "application/json"})
    #             json_data = res.json()
    #             sessionToken = json_data['sessionToken']
    #
    #             url = "https://pitneybowes.oktapreview.com/oauth2/austlb7mc40Fgj6ik0h7/v1/authorize?client_id=0oatl86njpT7nJLEX0h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
    #                 sessionToken)
    #
    #             headr = {"Authorization": "okta_client_credential"}
    #             new_res = requests.get(url, headers=headr)
    #             html_data = new_res.content
    #             # okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
    #             userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]
    #
    #
    #         except HTTPError as http_err:
    #             self.log.error(f'HTTP Error occurred.\n{http_err}')
    #             print_stack()
    #
    #         except Exception as ex:
    #             self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
    #             print_stack()
    #
    #     return userId
