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


class NotificationAPI:
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
        self.headers = json.loads(self.prop.get('NOTIFICATION_API_MGMT', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(self.access_token)
        self.headers["X-UserId"] = common_utils.get_x_user_id_from_okta(self.access_token)
        # self.log = log_utils.custom_logger(logging.INFO)

    def verify_notification_search_api_response(self):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns response body and status code
        """
        get_notification_search_endpoint = self.endpoint + "/notification/scherep/subscription/search"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            

        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_search_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            self.log.info("Notification API response:")
            result = True
        return res,status_code


    def verify_notification_search_api_response_with_custom_keys_and_values_in_payload(self,key,value):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload.
        :return: this function returns response body and status code
        """
        get_notification_search_endpoint = self.endpoint + "/notification/scherep/subscription/search"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data[key] = value
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            if key == "orgId":
                self.json_data[key] = "SP360FedRAMP"
            elif key == "ownerDesc":
                self.json_data[key] = "SP360FedRAMPowner"
            elif key == "ownerId":
                self.json_data[key] = "SP360FedRAMPownerId"

        res = self.api.post_api_response(
            endpoint=get_notification_search_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code

    def verify_notification_search_api_response_with_deleting_keys_in_payload(self,key):
        """
        This function is validates if analytics notification api gets response or not
        with deleting keys in payload.
        :return: this function returns response body and status code
        """
        get_notification_search_endpoint = self.endpoint + "/notification/scherep/subscription/search"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search').replace("temp", str(
            self.app_config.env_cfg['env']).lower())
        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        del self.json_data[key]

        res = self.api.post_api_response(
            endpoint=get_notification_search_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_notification_search_api_authorisation(self,expired_token):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_notification_search_endpoint = self.endpoint + "/notification/scherep/subscription/search"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())


        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_search_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_notification_search_api_header(self,invalid_header):

        """
                This function is validates if analytics assest api gets response or not
                with different header type.
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_notification_search_endpoint = self.endpoint + "/notification/scherep/subscription/search"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_search_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())


        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_search_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code



#-------------------------------------------scherep/subscription for creating report----------------------------------------

    def verify_notification_subscription_api_response(self):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_subscription').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code


    def verify_notification_subscription_api_authorisation(self,expired_token):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())


        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code




    def verify_notification_subscription_api_header(self,invalid_header):

        """
                This function is validates if analytics assest api gets response or not
                with different header type.
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        header1['Content-Type']=invalid_header
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())


        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=header1, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    def verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(self,key,value):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload.
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_subscription').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data[key] = value

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code

    def verify_notification_subscription_api_response_with_deleting_keys_in_payload(self,key):
        """
        This function is validates if analytics notification api gets response or not
        with deleting keys in payload.
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_subscription').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        del self.json_data[key]

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload_for_channels(self,key,value):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in channel key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_subscription').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['channels'][0][key]= value

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_notification_subscription_api_response_with_deleting_keys_in_payload_for_channels(self,key):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_subscription').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_subscription_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())
            
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        del self.json_data['channels'][0][key]

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code



# -------------------------------------------scherep/subscription/delete for Deleting report----------------------------------------
    def verify_notification_delete_api_response(self,notSubID):
        """
        This function is validates if analytics notification api gets response or not
        :return: this function returns response body and status code
        """
        get_notification_subscription_delete_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(arg1=notSubID)



        result = False

        res = self.api.delete_api_response(
            endpoint=get_notification_subscription_delete_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code



    def verify_notification_delete_api_authorisation(self,expired_token,notSubID):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns response body and status code
                """

        header1=self.headers.copy()
        if expired_token=='yes':
            header1['Authorization']="Bearer {}".format(str(self.app_config.env_cfg['expired_access_token']))
        get_notification_subscription_delete_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(arg1=notSubID)


        result = False

        res = self.api.delete_api_response(
            endpoint=get_notification_subscription_delete_endpoint, headers=header1)
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    # -------------------------------------------scherep/subscription/update for Updating report----------------------------------------
    def verify_notification_update_api_authorisation(self,key, value,notSubID, expired_token):

        """
                This function is validates if analytics assest api is well authorized or not
                :return: this function returns response body and status code
                """

        header1 = self.headers.copy()
        header1['Authorization'] = "Bearer {}".format(expired_token)
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(
            arg1=notSubID)
        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key] = value

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=header1,
            body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_notification_update_api_header(self,key, value,notSubID, invalid_header):

        """
                This function is validates if analytics assest api gets response or not
                with different header type.
                :return: this function returns response body and status code
                """

        header1 = self.headers.copy()
        header1['Content-Type'] = invalid_header
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(
            arg1=notSubID)

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key] = value

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=header1,
            body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code

    def verify_notification_update_api_response_with_custom_keys_and_values_in_kvp_key_payload(self, key, value,notSubID):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in kvp key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(arg1=notSubID)
        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key] = value

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code



    def verify_notification_update_api_response_with_custom_keys_and_values_in_kvp_with_2_keys(self, key1, value1,key2,value2,notSubID):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in kvp key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(arg1=notSubID)
        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key1] = value1
        self.json_data['kvp'][key2] = value2

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code





    def verify_notification_subscription_update_api_response_with_custom_keys_and_values_in_payload_for_channels(self,template,notSubID):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in channel key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(
            arg1=notSubID)
        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['channels'].append(template)



        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code






    def verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(self,key,value,notSubID,keyTobeChange,Changed_Value):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in kvp key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(
            arg1=notSubID)
        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key] = value
        self.json_data[keyTobeChange]=Changed_Value

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=self.headers,
            body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code


    def verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(self,key,value,notSubID,keyTobeDeleted):
        """
        This function is validates if analytics notification api gets response or not
        with replacing keys value in payload in kvp key.
        :return: this function returns response body and status code
        """
        get_notification_subscription_update_endpoint = self.endpoint + "/notification/scherep/subscription/{arg1}".format(
            arg1=notSubID)

        file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update').replace("temp", str(
            self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_update_fedramp').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        
        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        self.json_data['kvp'][key] = value
        del self.json_data[keyTobeDeleted]

        res = self.api.put_api_response(
            endpoint=get_notification_subscription_update_endpoint, headers=self.headers,
            body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res, status_code


#-------------------------------------------setup----------------------------------------------------
    def function_for_crate_one_report(self):
        """
        This function is validates if analytics notification api gets response or not,
        When we hit the request to notification search api then if their is not any report then
        it gives error as their is not data key. For this problem we are using this function.
        :return: this function returns response body and status code
        """
        get_notification_subscription_endpoint = self.endpoint + "/notification/scherep/subscription"
        file_path=self.prop.get('NOTIFICATION_API_MGMT','body_path_setup').replace("temp", str(self.app_config.env_cfg['env']).lower())

        if self.app_config.env_cfg['product_name'] == 'fedramp':
            file_path = self.prop.get('NOTIFICATION_API_MGMT', 'body_path_setup').replace("temp", str(
                self.app_config.env_cfg['env']).lower())

        with open(file_path) as f:
            self.json_data = json.load(f)

        result = False

        res = self.api.post_api_response(
            endpoint=get_notification_subscription_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            #self.log.info("Notification API response:")
            #self.log.info(res)
            result = True
        return res,status_code