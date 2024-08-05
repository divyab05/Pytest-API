"""
This module contains api utility functions.
"""

import logging
import requests,re
from traceback import print_stack
from requests.exceptions import HTTPError
import FrameworkUtilities.logger_utility as log_utils
from context import Context


class OktaUtilily:
    """
    This class with give us function to fetch okta token.
    """

    def __init__(self):
        self.log = log_utils.custom_logger(logging.INFO)


    def get_okta_token(self, env):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        if Context.ENV=="DEV":
            try:
                #res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                #                    data='{"username":"demouser@yopmail.com","password":"Aqswde@123"}',
                #                    headers={"Content-Type": "application/json"})
                res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                                    data='{"username":"'+Context.USERNAME+'","password":"'+Context.PASSWORD+'"}',
                                    headers={"Content-Type": "application/json"})

                json_data = res.json()
                sessionToken = json_data['sessionToken']

                url = "https://pitneybowes.oktapreview.com/oauth2/austlaq2lihWmiUEP0h7/v1/authorize?client_id=0oatl85b03pUUq2w70h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
                    sessionToken)

                headr = {"Authorization": "okta_client_credential"}
                new_res = requests.get(url, headers=headr)
                html_data = new_res.content
                okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
                userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]


            except HTTPError as http_err:
                self.log.error(f'HTTP Error occurred.\n{http_err}')
                print_stack()

            except Exception as ex:
                self.log.error(f'Error occurred while generating okta.please check for proper credentials.\n{ex}')
                print_stack()

        elif Context.ENV == "QA":
            try:
                #res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                #                    data='{"username":"tanu@mailinator.com","password":"Aqswde@123"}',
                #                    headers={"Content-Type": "application/json"})
                res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                                    data='{"username":"' + Context.USERNAME + '","password":"' + Context.PASSWORD + '"}',
                                    headers={"Content-Type": "application/json"})

                json_data = res.json()
                sessionToken = json_data['sessionToken']

                url = "https://pitneybowes.oktapreview.com/oauth2/austlb7mc40Fgj6ik0h7/v1/authorize?client_id=0oatl86njpT7nJLEX0h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
                    sessionToken)

                headr = {"Authorization": "okta_client_credential"}
                new_res = requests.get(url, headers=headr)
                html_data = new_res.content
                okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
                userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]


            except HTTPError as http_err:
                self.log.error(f'HTTP Error occurred while generating okta.please check for proper credentials.\n{http_err}')
                print_stack()

            except Exception as ex:
                self.log.error(f'Failed to get the response, other error occurred while generating okta.please check for proper credentials.\n{ex}')
                print_stack()

        return okta_token

    def get_userid_token(self, env):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        if Context.ENV=="DEV":
            try:
                #res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                #                    data='{"username":"demouser@yopmail.com","password":"Aqswde@123"}',
                #                    headers={"Content-Type": "application/json"})
                res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                                    data='{"username":"'+Context.USERNAME+'","password":"'+Context.PASSWORD+'"}',
                                    headers={"Content-Type": "application/json"})

                json_data = res.json()
                sessionToken = json_data['sessionToken']

                url = "https://pitneybowes.oktapreview.com/oauth2/austlaq2lihWmiUEP0h7/v1/authorize?client_id=0oatl85b03pUUq2w70h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
                    sessionToken)

                headr = {"Authorization": "okta_client_credential"}
                new_res = requests.get(url, headers=headr)
                html_data = new_res.content
                #okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
                userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]


            except HTTPError as http_err:
                self.log.error(f'HTTP Error occurred.\n{http_err}')
                print_stack()

            except Exception as ex:
                self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
                print_stack()

        elif Context.ENV == "QA":
            try:
                res = requests.post("https://pitneybowes.oktapreview.com/api/v1/authn",
                                    data='{"username":"tanu@mailinator.com","password":"Aqswde@123"}',
                                    headers={"Content-Type": "application/json"})
                json_data = res.json()
                sessionToken = json_data['sessionToken']

                url = "https://pitneybowes.oktapreview.com/oauth2/austlb7mc40Fgj6ik0h7/v1/authorize?client_id=0oatl86njpT7nJLEX0h7&scope=openid%20profile%20email%20address%20phone%20offline_access%20spa%20anx%20adm%20pbadm&response_type=token%20id_token&redirect_uri=http://localhost:8081/auth&nonce=875234875&state=1324&response_mode=form_post&sessionToken={}".format(
                    sessionToken)

                headr = {"Authorization": "okta_client_credential"}
                new_res = requests.get(url, headers=headr)
                html_data = new_res.content
                #okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]
                userId = re.findall(r"userId: \\'[a-zA-Z0-9]*", str(html_data))[0][10:]


            except HTTPError as http_err:
                self.log.error(f'HTTP Error occurred.\n{http_err}')
                print_stack()

            except Exception as ex:
                self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
                print_stack()

        return userId
