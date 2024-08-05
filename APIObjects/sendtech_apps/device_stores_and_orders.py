
import json


from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils


class Stores:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token

        if str(self.app_config.env_cfg['env']).lower()=="qa":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}

        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])


    def get_store_details(self):

        get_all_store_endpoint = self.baseUri + "/substores/v2"
        resp = self.api.get_api_response(endpoint=get_all_store_endpoint, headers=self.headers)
        return resp

    def get_specific_store_details(self,storeKey,subID):

        get_specific_store_endpoint = self.baseUri + "/subscription/"+subID+"/properties?storeKey="+storeKey
        print("url is",get_specific_store_endpoint)
        resp = self.api.get_api_response(endpoint=get_specific_store_endpoint, headers=self.headers)
        return resp

    def get_specific_substore_details(self,subStoreId):

        get_specific_substore_endpoint = self.baseUri + "/substores/"+subStoreId
        resp = self.api.get_api_response(endpoint=get_specific_substore_endpoint, headers=self.headers)
        return resp



    def add_woo_store(self,consumerSecret,storeUrl,consumerKey):
        self.headers['cartId']="woocommerce"
        self.headers['integratorid']="sp360"
        add_woo_store_endpoint=self.baseUri+"/store/register"
        requestBody="{\"consumerSecret\":\""+consumerSecret+"\",\"storeUrl\":\""+storeUrl+"\",\"consumerKey\":\""+consumerKey+"\"}"
        print("request body ",requestBody)
        resp = self.api.post_api_response(endpoint=add_woo_store_endpoint, headers=self.headers, body=requestBody)
        return resp


    def get_woocommerice_onboarding_screen(self):
        get_onboarding_screen_endpoint = self.baseUri + "/connector/metadata/onboarding/woocommerce"
        resp = self.api.get_api_response(endpoint=get_onboarding_screen_endpoint, headers=self.headers)
        return resp


    def get_shiprequest(self):
        get_shiprequest_endpoint = self.baseUri + "/ship-request"
        resp = self.api.get_api_response(endpoint=get_shiprequest_endpoint, headers=self.headers)
        return resp


    def get_packageslip_configuration(self):

        get_all_store_endpoint = self.baseUri + "/package/configuration/packageslip"
        resp = self.api.get_api_response(endpoint=get_all_store_endpoint, headers=self.headers)
        return resp

    def get_order_sync(self):
        self.headers['integratorid'] = "sp360"
        order_sync_endpoint = "https://shipreq-qa.sendpro360.pitneycloud.com/api/v2/DataSync"
        resp = self.api.get_api_response(endpoint=order_sync_endpoint, headers=self.headers)
        return resp















