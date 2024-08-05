import json

from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils


class Subscription:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + str(access_token)

        if str(self.app_config.env_cfg['env']) == "QA":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}

        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])

    def get_accounts(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/accounts"
        print("get users endpoint is", get_users_endpoint)
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def post_add_fund(self, fundAmt):
        # self.headers['Authorization'] = self.admin_token
        self.body = json.dumps({"carrierCode": "usps", "fundingAmount": fundAmt})
        get_users_endpoint = self.baseUri + "/accounts/fund"
        resp = self.api.post_api_response(endpoint=get_users_endpoint, headers=self.headers, body=self.body)
        return resp

    def get_user_profile(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/users/profile"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_accounts(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/accounts"
        print("get users endpoint is", get_users_endpoint)
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_customer_preference(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/customer-preferences"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_customer_context(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/customer-context"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_user_prefernces(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/user-preferences"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_user_context(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/user-context"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_default_sender_address(self):
        # self.headers['Authorization'] = self.admin_token
        get_users_endpoint = self.baseUri + "/address/default-sender"
        resp = self.api.get_api_response(endpoint=get_users_endpoint, headers=self.headers)
        return resp

    def get_enterprise_subscription_details(self):
        # self.headers['Authorization'] = self.admin_token
        get_enterprise_subscriptions_endpoint = self.baseUri + "/enterprises/subscriptions?getPaymentStatus=true"
        print("enterprise url", get_enterprise_subscriptions_endpoint)
        resp = self.api.get_api_response(endpoint=get_enterprise_subscriptions_endpoint, headers=self.headers)
        return resp

    def get_autorefill(self):
        get_autorefill_endpoint = self.baseUri + "/rules/autorefill"
        print("get_autorefill_endpoint ", get_autorefill_endpoint)
        resp = self.api.get_api_response(endpoint=get_autorefill_endpoint, headers=self.headers)
        return resp

    def get_costaccounts(self):
        get_costaccount_endpoint = self.baseUri + "/costaccounts?page=0&size=5&defaultfirst=true&sort=lastUsedDate,desc&toshowall=false&status=active"
        print("get costaccount endpoint ", get_costaccount_endpoint)
        resp = self.api.get_api_response(endpoint=get_costaccount_endpoint, headers=self.headers)
        return resp

    def verify_autorefill(self, costAccountID, costAccountName, postageAmount):
        put_enable_autorefill_endpoint = self.baseUri + "/rules/autorefill?id=100"
        print("enable autorefill endpoint ", put_enable_autorefill_endpoint)

        requestBody = "{\"addAmount\":" + str(
            postageAmount) + ",\"costAccount\":{\"id\":\"" + costAccountID + "\",\"name\":\"" + costAccountName + "\"},\"createDate\":\"0001-01-01T00:00:00Z\",\"displayConfirmation\":true,\"enabled\":true,\"id\":100,\"isArchived\":false,\"minThreshold\":10,\"modifyDate\":\"2024-05-18T08:13:29Z\",\"version\":0}"
        print("request body ", requestBody)

        resp = self.api.put_api_response(put_enable_autorefill_endpoint, self.headers, body=requestBody)
        return resp

    def shippingtransactions_limit(self, amount):
        requestBody = "{\"maximumPostageValue\":{\"amount\":" + str(amount) + ",\"currency\":\"USD\"}}"
        requestUrl = self.baseUri + "/customer-preferences"

        resp = self.api.patch_api_response(requestUrl, self.headers, body=requestBody)
        return resp

    def userPreferencesAPIPatch(self, payload):
        requestUrl = self.baseUri + "/user-preferences"

        resp = self.api.patch_api_response(requestUrl, self.headers, body=payload)
        return resp
