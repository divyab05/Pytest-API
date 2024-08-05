import logging
import json
import random
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


class SubscriptionAPI:
    """
    This class encapsulates various methods and element identifications necessary for interacting
    with Subscription Management APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.login = LoginAPI(app_config)
        self.client_mgmt_api = ClientManagementAPI(app_config, access_token, client_token)
        self.prod_metadata_api = ProductMetadata(app_config, access_token, client_token)
        self.prop = self.config.load_properties_file()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.endpoint = str(self.app_config.env_cfg['submgmt_api'])
        self.headers = {"Accept": "*/*"}
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def verify_create_subscription_api(self, SubID , EntID="", PlanIDs="", Carriers=""):
        """
        This function is validates if a subscription gets created successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'create_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['subID'] = SubID
        if EntID != "":
            self.json_data['enterpriseID'] = EntID
        if PlanIDs != "":
            self.json_data['plans'] = PlanIDs
        if Carriers != "":
            self.json_data['carriers'] = Carriers

        create_subscription_enpoint = self.endpoint +"/api/v1/subscriptions"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=create_subscription_enpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def create_subscription_api(self, ent_id=None, plan_ids=None, carriers=None, country='US'):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'create_subscription_body')) as f:
            req_payload = json.load(f)

        okta_group_id = str(self.app_config.env_cfg['okta_group_id'])
        req_payload['properties']['oktaGroupID'] = okta_group_id
        req_payload['oktaGroupID'] = okta_group_id

        if ent_id:
            req_payload['enterpriseID'] = ent_id
        if plan_ids:
            req_payload['plans'] = plan_ids
        if carriers:
            req_payload['carriers'] = carriers
        if country:
            req_payload['countryCode'] = country

        create_subscription_endpoint = self.endpoint + '/api/v1/subscriptions'
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(endpoint=create_subscription_endpoint, headers=self.headers,
                                              body=json.dumps(req_payload))
        return response

    def verify_create_duplicate_subscription_api(self, SubID, EntID=""):
        """
        This function is validates if a duplicate subscription gets created successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'create_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['subID'] = SubID
        if EntID != "":
            self.json_data['enterpriseID'] = EntID

        duplicate_creation_endpoint = self.endpoint + "/api/v1/subscriptions"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=duplicate_creation_endpoint,headers=self.headers,body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)

        return res,status_code

    def verify_update_subscription_api(self, SubID, EntID=""):
        """
        This function is validates if a subscription can be updated successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['subID'] = SubID
        if EntID != "":
            self.json_data['enterpriseID'] = EntID
        update_endpoint = self.endpoint + "/api/v1/subscriptions/" +SubID
        self.headers['Authorization'] = self.admin_token

        res = self.api.put_api_response(
            endpoint=update_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_subscription_plans(self, SubID ):
        """
        This function gets Plan from subscription
        :return: this function returns boolean status of element located
        """
        get_sub_plan_endpoint = self.endpoint+"/api/v1/subscriptions/"+SubID+"/plans"
        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_sub_plan_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def archive_subscription_api(self, sub_id=''):
        """
        This method archives the given subscription id.
        :param sub_id: The subscription id of a subscription.
        """
        if not sub_id:
            pytest.fail('archive_subscription_api :: sub_id cannot be empty!')

        archive_subscription_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/archive'
        self.headers['Authorization'] = self.admin_token
        res = self.api.put_api_response(endpoint=archive_subscription_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def verify_add_location_subscription_api(self, sub_id):
        """
        This function validates that locations can be added to a subscription
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_location_body')) as f:
            self.json_data = json.load(f)
        result = False

        add_location_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/locations"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=add_location_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_locations_from_subscription_plans(self, SubID ):
        """
        This function gets locations from subscription
        :return: this function returns boolean status of element located
        """
        get_locations_endpoint = self.endpoint+"/api/v1/subscriptions/"+SubID+"/locations"
        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_locations_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_add_plans_subscription_api(self, sub_id):
        """
        This function validates that plans can be added to the subscription
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_plans_body')) as f:
            self.json_data = json.load(f)
        result = False

        add_location_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/plans"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=add_location_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_add_carriers_subscription_api(self, sub_id):
        """
        This function validates that carriers can be added to the subscription
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_carriers_body')) as f:
            self.json_data = json.load(f)
        result = False

        add_location_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/carriers"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=add_location_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_carriers_from_subscription_plans_api(self, sub_id ):
        """
        This function fetches the available carriers in a subscription plan
        :return: this function returns boolean status of element located
        """
        get_locations_endpoint = self.endpoint+"/api/v1/subscriptions/"+sub_id+"/carriers"
        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_locations_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_delete_carriers_from_subscription_api(self, sub_id):
        """
        This function deletes the available carriers from a subscription plan
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'delete_carriers_body')) as f:
            self.json_data = json.load(f)
        result = False

        delete_carriers_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/carriers"
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=delete_carriers_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code


    def verify_get_plans_from_subscription_plans_api(self, sub_id ):
        """
        This function gets Plan from subscription
        :return: this function returns boolean status of element located
        """
        get_locations_endpoint = self.endpoint+"/api/v1/subscriptions/"+sub_id+"/plans"
        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_locations_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_delete_plans_from_subscription_api(self, sub_id):
        """
        This function deletes the available plans from a subscription
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'delete_plans_body')) as f:
            self.json_data = json.load(f)
        result = False

        delete_plans_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/plans"
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=delete_plans_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_delete_locations_from_subscription_api(self, sub_id):
        """
        This function deletes the available locations from a subscription
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'delete_locations_body')) as f:
            self.json_data = json.load(f)
        result = False

        delete_locations_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/locations"
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=delete_locations_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_subscriptions_api(self):
        """
        This function gets the list of all subscriptions
        :return: this function returns boolean status of element located
        """
        get_locations_endpoint = self.endpoint +"/api/v1/subscriptions"
        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_locations_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_get_subscription_by_id_api(self, sub_id):
        """
        This function gets the details of subscription as per the provided subscription Id
        :return: this function returns boolean status of element located
        """
        get_sub_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_sub_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_get_subscription_count_api(self):
        """
        This function returns the total subscription count
        :return: this function returns total subscription count
        """
        get_sub_count_endpoint = self.endpoint + "/api/v1/subscriptions/count"
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_sub_count_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def get_subscription_user_by_user_id_api(self, subId, userId):
        """
        This function fetches the list of available users in a subscription
        :return: this function returns boolean status of element located
        """
        get_sub_user_endpoint = self.endpoint + "/api/v1/subscriptions/" + subId + "/users/" + userId
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_sub_user_endpoint, headers=self.headers)
        return response

    def get_user_subscription_details_by_user_id_api(self, user_id):
        """
        This function gets list of all users from subscription
        :return: this function returns boolean status of element located
        """
        get_user_sub_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/subscriptions"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_user_sub_endpoint, headers=self.headers)
        return response

    def get_subscription_by_ent_id_api(self, ent_id=None, is_admin=True, admin_token='', client_token=''):
        """
        Retrieves subscription details for a given enterprise ID.
        :return: this function returns boolean status of element located
        """
        get_sub_by_ent_endpoint = f'{self.endpoint}/api/v1/enterprises/{ent_id}/subscriptions'

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_sub_by_ent_endpoint, headers=self.headers)
        return response

    def verify_get_subscription_properties_api(self, sub_id):
        """
        This function gets properties from subscription
        :return: this function returns boolean status of element located
        """
        get_sub_prop_endpoint = self.endpoint + "/api/v1/subscriptions/" +sub_id +"/properties"
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_sub_prop_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def get_subscription_roles_api(self, sub_id):
        """
        This function gets available roles from a subscription
        :return: this function returns boolean status of element located
        """
        get_sub_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/subscriptionRoles"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_sub_roles_endpoint, headers=self.headers)
        return response

    def verify_update_subscription_properties_api(self, SubID, ledgerProductID):
        """
        This function validates if the properties of a subscription can be updated successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subscription_properties_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['ledgerProductID'] = ledgerProductID
        update_endpoint = self.endpoint + "/api/v1/subscriptions/" +SubID +"/properties"
        self.headers['Authorization'] = self.admin_token

        res = self.api.put_api_response(
            endpoint=update_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_update_locker_size_api(self, SubID, length):
        """
        This function validates if locker size of subscription can be updated successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_locker_size_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data[0]['dimension']['length'] = length
        update_locker_size_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID +"/lockerSize"
        self.headers['Authorization'] = self.admin_token

        res = self.api.patch_api_response(
            endpoint=update_locker_size_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_get_locker_size_api(self, SubID):
        """
        This function fetches the locker size of a subscription
        :return: this function returns boolean status of element located
        """
        get_locker_size_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID +"/lockerSize"
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_locker_size_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_get_locker_sub_properties_api(self, SubID):
        """
        This function fetches locker sub properties
        :return: this function returns boolean status of element located
        """
        get_locker_size_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID +"/lockerSubProperties"
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_locker_size_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def add_subscription_roles_to_subscription_api(self, sub_id=''):
        """
        This function validates if roles can be added to subscription successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_roles_to_subscription_body')) as f:
            self.json_data = json.load(f)
        add_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/subscriptionRoles"
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(endpoint=add_roles_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def update_subscription_role_api(self, sub_id='', role_id='', role_name='', features=None):
        """
        This function validates if roles can updated successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subscription_roles_body')) as f:
            self.json_data = json.load(f)
        self.json_data['roleID'] = role_id
        self.json_data['name'] = role_name

        if features is not None:
            self.json_data['features'] = features

        update_sub_role_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/subscriptionRoles"
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(endpoint=update_sub_role_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def verify_delete_roles_from_subscription_api(self, SubID, roleId):
        """
        This function validates if roles can deleted successfully or not
        :return: this function returns boolean status of element located
        """
        get_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID +"/subscriptionRoles/" +roleId
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=get_roles_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code


    def verify_get_roles_from_subscription_api(self, SubID):
        """
        This function fetches the roles available in a subscription
        :return: this function returns boolean status of element located
        """
        get_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID +"/subscriptionRoles"
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_roles_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_add_features_in_subscription_role_api(self, SubID, roleId):
        """
        This function validates that features can be added to a subscription role
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_features_to_subscription_roles_body')) as f:
            self.json_data = json.load(f)
        result = False
        add_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID + "/subscriptionRoles/" + roleId + "/features"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=add_roles_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_delete_features_in_subscription_role_api(self, SubID, roleId):
        """
        This function validates that features can be deleted from a subscription role
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_features_to_subscription_roles_body')) as f:
            self.json_data = json.load(f)
        result = False
        add_roles_endpoint = self.endpoint + "/api/v1/subscriptions/" + SubID + "/subscriptionRoles/" + roleId + "/features"
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=add_roles_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_subscription_user_from_claim_by_sub_id_api(self):
        """
        This function fetches subscription users from claim as per the sub id
        :return: this function returns boolean status of element located
        """

        get_sub_user_from_claim = self.endpoint + "/api/v1/getUserBySubID"
        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_sub_user_from_claim, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def get_users_by_subscription_api(self, is_admin=False):
        """
        This function fetches subscription users from claim
        :return: this function returns boolean status of element located
        """
        get_sub_user_from_claim = self.endpoint + "/api/v1/usersBySubscription"
        if is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_sub_user_from_claim, headers=self.headers)
        return response

    def verify_get_subscription_user_from_claim_by_user_id_api(self):
        """
        This function fetches subscription users from claim as per the user id
        :return: this function returns boolean status of element located
        """
        get_sub_user_from_claim = self.endpoint+ "/api/v1/subscriptionsByUserID"
        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_sub_user_from_claim, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_add_roles_to_subscription_from_claim_api(self, role_id):
        """
        This function validates if roles can be added to subscription claims successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_roles_to_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['roleID'] = role_id
        add_roles_from_claim_endpoint = self.endpoint+ "/api/v1/subscriptionRoles"
        self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_roles_from_claim_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_delete_subscription_role_from_claim_by_api(self, role_id):
        """
        This function validates if roles can be deleted from subscription claims successfully
        :return: this function returns boolean status of element located
        """
        del_roles_from_claim_endpoint = self.endpoint + "/api/v1/subscriptionRoles/" +role_id
        self.headers['Authorization'] = self.client_token

        res = self.api.delete_api_response(
            endpoint=del_roles_from_claim_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def verify_update_roles_to_subscription_from_claim_api(self, role_id, name):
        """
        This function validates if roles of a subscription can be updated successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_roles_to_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False
        self.json_data['roleID'] = role_id
        self.json_data['name'] = name
        add_roles_from_claim_endpoint = self.endpoint+ "/api/v1/subscriptionRoles"
        self.headers['Authorization'] = self.client_token

        res = self.api.put_api_response(
            endpoint=add_roles_from_claim_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_subscription_roles_from_claim_api(self):
        """
        This function fetches the subscriptions from a claim
        :return: this function returns boolean status of element located
        """
        get_sub_user_from_claim = self.endpoint + "/api/v1/subscriptionRoles"
        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_sub_user_from_claim, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_add_features_to_subscription_from_claim_api(self, role_id):
        """
        This function validates if roles can be added to subscription claims successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_features_to_subscription_roles_body')) as f:
            self.json_data = json.load(f)
        result = False
        add_feature_from_claim_endpoint = self.endpoint + "/api/v1/subscriptionRoles/"+role_id +"/features"
        self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_feature_from_claim_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_delete_subscription_features_from_claim_api(self, role_id):
        """
        This function validates if roles can be added to subscription claims successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_features_to_subscription_roles_body')) as f:
            self.json_data = json.load(f)
        result = False
        delete_feature_from_claim_endpoint = self.endpoint + "/api/v1/subscriptionRoles/"+role_id +"/features"
        self.headers['Authorization'] = self.client_token

        res = self.api.delete_api_response(
            endpoint=delete_feature_from_claim_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_update_subscription_properties_from_claim_api(self):
        """
        This function validates if properties can be updated of a subscription claim
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subscription_claim_properties_body')) as f:
            self.json_data = json.load(f)
        result = False
        update_feature_from_claim_endpoint = self.endpoint + "/api/v1/subscriptions/properties"
        self.headers['Authorization'] = self.client_token

        res = self.api.put_api_response(
            endpoint=update_feature_from_claim_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def verify_get_subscription_prop_from_claim_api(self):
        """
        This function fetches the subscription properties from a claim
        :return: this function returns boolean status of element located
        """
        get_sub_prop_from_claim = self.endpoint + "/api/v1/subscriptions/properties"
        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_sub_prop_from_claim, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    # Test cases of user module starts here

    def get_users_api(self, is_admin=False, sub_id=None, token=None, skip='0', limit='10', archive='false'):
        """
        This function fetches the details of all users
        :return: Response of get all users api
        """
        if is_admin:
            path_params = f'/api/v1/subscriptions/{sub_id}/users'
            query_params = f'?skip={skip}&limit={limit}&archive={archive}'
            self.headers['Authorization'] = self.admin_token
        else:
            query_params = f'?skip={skip}&limit={limit}&archive={archive}'
            path_params = f'/api/v1/users'
            self.headers['Authorization'] = token if token else self.client_token

        get_users_endpoint = f'{self.endpoint}{path_params}{query_params}'

        # query_params = f'?skip={skip}&limit={limit}&archive={archive}'
        # path_params = f'/api/v1/subscriptions/{sub_id}/users' if (is_admin and sub_id) else f'/api/v1/users'
        # get_users_endpoint = f'{self.endpoint}{path_params}{query_params}'
        #
        # self.headers['Authorization'] = token if token else (self.admin_token if is_admin else self.client_token)

        response = self.api.get_api_response(get_users_endpoint, self.headers)
        return response

    def get_all_users_by_token_api(self, is_admin=False, query_param='', sub_id='', token=''):

        if token:
            self.headers['Authorization'] = token
            get_users_endpoint = self.endpoint + '/api/v1/users' + query_param
        elif is_admin:
            self.headers['Authorization'] = self.admin_token
            get_users_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/users' + query_param
        else:
            self.headers['Authorization'] = self.client_token
            get_users_endpoint = self.endpoint + '/api/v1/users' + query_param

        response = self.api.get_api_response(get_users_endpoint, self.headers)
        return response

    def get_user_by_user_id_api(self, user_id, is_admin=False):
        """
        This function fetches the details of user as per the provided user id

        :param user_id: The user id.
        :param is_admin: If true then admin user access token will be used, else client user token.
        :return: The response of the get_user_by_id api.
        """
        get_user_by_id_endpoint = self.endpoint + "/api/v1/users/" + user_id
        if is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_user_by_id_endpoint, self.headers)
        return response

    def get_all_users_list_api(self, limit_count=""):
        """
        This function fetches the details of all users available in db with or without limit as query param.
        :param limit_count: Limit the number of users in the response of users list.
        :return: this function returns boolean status of element located
        """

        self.headers['Authorization'] = self.client_token
        limit = "?limit=" + limit_count

        if limit_count != "":
            get_all_users_list_endpoint = self.endpoint + "/api/v1/userslist" + limit
        else:
            get_all_users_list_endpoint = self.endpoint + "/api/v1/userslist"

        response = self.api.get_api_response(get_all_users_list_endpoint, self.headers)
        return response

    def add_admin_user_api(self, fname='', lname='', email='', disp_name='', group_id='', admin_token=None):
        """
        This function validates if a user can be created successfully or not
        :return: this function returns boolean status of element located
        """

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_user_body')) as f:
            payload = json.load(f)

        payload['profile']['firstName'] = fname
        payload['profile']['lastName'] = lname
        payload['profile']['email'] = email
        payload['profile']['displayName'] = disp_name

        if isinstance(group_id, list):
            payload['groupIds'] = group_id
        else:
            payload['groupIds'][0] = group_id

        add_admin_user_url = f"{self.endpoint}/api/v1/users"
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.post_api_response(add_admin_user_url, self.headers, json.dumps(payload))
        return response

    def update_admin_user_api(self, sub_id='', user_id=''):
        """
        This function validates if a user can be updated successfully or not
        :return: this function returns boolean status of element located
        """

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_user_body')) as f:
            self.json_data = json.load(f)

        self.json_data['subID'] = sub_id
        self.json_data['id'] = user_id

        create_user_endpoint = self.endpoint + '/api/v1/users/' + user_id
        self.headers['Authorization'] = self.admin_token
        payload = json.dumps(self.json_data)

        response = self.api.put_api_response(create_user_endpoint, self.headers, payload)
        return response

    def get_admin_user_by_search_query(self, skip='0', limit='10', archive='false', status='true', query='',
                                       admin_token=None):

        query_params = f"?skip={skip}&limit={limit}&archive={archive}&status={status}&query={query}"
        get_admin_user_by_search_query_url = f"{self.endpoint}/api/v1/users{query_params}"
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        response = self.api.get_api_response(get_admin_user_by_search_query_url, self.headers)
        return response

    def get_user_by_search_query(self, skip='0', limit='5', archive='false', status='', query='', sub_id='',
                                 is_admin=True):

        query_params = f'?skip={skip}&limit={limit}&include_archived={archive}&status={status}&query={query}'
        get_user_by_search_query_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/users{query_params}'

        if is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_user_by_search_query_endpoint, self.headers)
        return response

    def get_admin_users_by_email_api(self, email='', user_type='NON-SSO', admin_token=None):
        get_admin_user_url = f"{self.endpoint}/api/v1/users/email/{email}?userType={user_type}"
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        if user_type == 'SSO':
            self.headers['X-Pb-Source-Idp'] = 'COGNITO_SSO'

        response = self.api.get_api_response(get_admin_user_url, self.headers)
        return response

    def get_search_user_by_email_api(self, sub_id='', ent_id='', email='', user_type='NON-SSO', token=None, is_admin=False):

        if self.prod_name == 'fedramp':
            if is_admin:
                search_user_url = f"{self.endpoint}/api/v1/userbyemail/subID/{sub_id}/email/{email}?userType={user_type}"
                self.headers['Authorization'] = token if token else self.admin_token
            else:
                search_user_url = f"{self.endpoint}/api/v1/userbyemail/email/{email}?userType={user_type}"
                self.headers['Authorization'] = token if token else self.client_token
        else:
            if is_admin:
                search_user_url = f"{self.endpoint}/api/v1/userbyemail/subID/{sub_id}/email/{email}?entID={ent_id}&userType={user_type}"
                self.headers['Authorization'] = token if token else self.admin_token
            else:
                search_user_url = f"{self.endpoint}/api/v1/userbyemail/email/{email}?entID={ent_id}&userType={user_type}"
                self.headers['Authorization'] = token if token else self.client_token

            if user_type == 'SSO':
                self.headers['X-Pb-Source-Idp'] = 'COGNITO_SSO'

        response = self.api.get_api_response(search_user_url, self.headers)
        return response

    def get_sso_user_specific_details(self, sub_id='', ent_id='', email='', user_type='SSO', token=None, is_admin=False):

        user_resp = self.get_search_user_by_email_api(sub_id=sub_id, ent_id=ent_id, email=email, user_type=user_type,
                                                      is_admin=is_admin, token=token)
        assert_that(common_utils.validate_response_code(user_resp, 200))

        user_data = user_resp.json()['usersDetailWithSubLocation'][0]
        user_loc_id = user_data.get('subLocation').get('locationID')
        user_role_id = user_data['subLocation']['subscriptionRoles'][0]
        user_props = user_data.get('subLocation').get('properties')
        user_cost_acct_id = user_props.get('defaultCostAccountID', '')
        uid = user_data['detail']['id']
        user_firstname = user_data['detail']['profile']['firstName']
        user_lastname = user_data['detail']['profile']['lastName']
        user_access_lvl = user_data.get('detail').get('adminLevelAt')
        user_admin_entities = user_data.get('detail').get('adminLevelEntity')

        username = user_data.get('detail').get('externalID')

        return (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
                user_access_lvl, user_admin_entities)

    def verify_add_by_user_id_api(self, location_id='', user_id = '', sub_id= ''):
        """
        This function validates if a user can be added successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_by_user_id_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['locationID'] = location_id
        self.json_data['userID'] = user_id

        add_by_user_id_endpoint = self.endpoint + '/api/v1/subscriptions/' +sub_id+"/userByID"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=add_by_user_id_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def add_client_user_by_sub_id_email_api(self, fname='', lname='', email='', disp_name='', sub_id='',
                                            loc_id='', admin_lvl='', admn_lvl_entity=None, subs_roles=None,
                                            carriers=None, is_admin='y', ent_name=''):
        """
        This function validates if a user can be created successfully or not
        :return: this function returns boolean status of element located
        """

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'add_by_user_email_body')) as f:
            payload = json.load(f)

        if admin_lvl == 'User':
            del payload['adminLevelAt']
            del payload['adminLevelEntity']
        elif admin_lvl != 'User':
            payload['adminLevelAt'] = admin_lvl
            payload['adminLevelEntity'] = admn_lvl_entity

        payload['userProfile']['firstName'] = fname
        payload['userProfile']['lastName'] = lname
        payload['userProfile']['email'] = email
        payload['userProfile']['displayName'] = disp_name
        payload['locationID'] = loc_id
        payload['enterpriseName'] = ent_name
        payload['subscriptionRoles'] = subs_roles
        payload['carrierAccounts'] = carriers

        add_user_email_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + "/userByEmail"
        self.headers['Authorization'] = self.admin_token
        if is_admin == 'n':
            self.headers['Authorization'] = self.client_token
        response = self.api.post_api_response(add_user_email_endpoint, self.headers, json.dumps(payload))
        return response

    def verify_archive_user_api(self, user_id='', sub_id='', is_admin=''):
        """
        This function is archives the created subscription Plan
        :return: this function returns boolean status of element located
        """
        if is_admin=='y':
            archive_user_endpoint = self.endpoint+"/api/v1/subscriptions/"+sub_id+"/users/"+user_id+"/archive"
            self.headers['Authorization'] = self.admin_token

        else:
            archive_user_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/archive"
            self.headers['Authorization'] = self.client_token

        res = self.api.put_api_response(
            endpoint=archive_user_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def delete_user_api(self, user_id='', sub_id='', is_admin=''):
        """
        This function is archives the created subscription Plan
        :return: this function returns boolean status of element located
        """
        if is_admin == 'y':
            del_user_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id
            self.headers['Authorization'] = self.admin_token

        else:
            del_user_endpoint = self.endpoint + "/api/v1/users/" + user_id
            self.headers['Authorization'] = self.client_token

        response = self.api.delete_api_response(del_user_endpoint, self.headers)
        return response

    def delete_admin_user_api(self, user_id=''):

        del_user_endpoint = self.endpoint + "/api/v1/subscriptions/users/" + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.delete_api_response(del_user_endpoint, self.headers)
        return response

    def get_admin_user_profile_by_user_id_api(self, user_id):
        """
        This function fetches the user profile
        :return: this function returns boolean status of element located
        """
        get_user_profile_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/scope/pbadmin"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_user_profile_endpoint, self.headers)
        return response

    def get_admin_user_details_by_user_id_api(self, user_id):
        get_user_profile_endpoint = self.endpoint + "/api/v1/users/" + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_user_profile_endpoint, self.headers)
        return response

    def get_admin_users_profile_api(self):
        """
        This function fetches the user profile
        :return: this function returns boolean status of element located
        """
        get_admin_users_profile_endpoint = self.endpoint + "/api/v1/users/scope/pbadmin"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_admin_users_profile_endpoint, self.headers)
        return response

    def get_user_roll_up_entity_api(self, user_id):
        """
        This function fetches the details of roll up entity as per the provided user id
        :return: this function returns boolean status of element located
        """
        get_roll_up_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/rollupEntity"
        self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_roll_up_endpoint, self.headers)
        return response

    def get_user_by_email_api(self, email):
        """
        This function fetches the details of users by email
        :return: this function returns boolean status of element located
        """
        get_user_by_email_endpoint = self.endpoint + "/api/v1/users/email/" + email
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_user_by_email_endpoint, self.headers)
        return response

    def get_user_properties_api(self, token=''):
        """
        This function fetches the user properties
        :return: this function returns boolean status of element located
        """
        get_user_by_email_endpoint = self.endpoint + "/api/v1/users/properties"
        if not token:
            self.headers['Authorization'] = self.client_token
        else:
            self.headers['Authorization'] = token

        response = self.api.get_api_response(get_user_by_email_endpoint, self.headers)
        return response

    def get_subscription_properties_api(self, token='', is_admin=False, sub_id=''):

        if token:
            query_param = '?subID=' + sub_id
            get_subs_prop_endpoint = self.endpoint + '/api/v1/subscriptionProperties' + query_param
            self.headers['Authorization'] = token
        elif is_admin:
            query_param = '?subID=' + sub_id
            get_subs_prop_endpoint = self.endpoint + '/api/v1/subscriptionProperties' + query_param
            self.headers['Authorization'] = self.admin_token
        else:
            get_subs_prop_endpoint = self.endpoint + '/api/v1/subscriptionProperties'
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_subs_prop_endpoint, headers=self.headers)
        return response

    def get_enterprises_by_user_api(self):
        """
        This function fetches the details of enterprises available for a user
        :return: this function returns boolean status of element located
        """
        get_enterprise_by_user_endpoint = self.endpoint + "/api/v1/enterprisesByUser"
        self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_enterprise_by_user_endpoint, self.headers)
        return response

    def get_user_admin_entity_api(self):
        """
        This test validates that admin entity can be fetched successfully from subscription claim
        :return: this function returns boolean status of element located
        """
        get_admin_entity_endpoint = self.endpoint + "/api/v1/adminEntity"
        self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_admin_entity_endpoint, self.headers)
        return response

    def get_user_admin_entity_by_user_id_api(self, user_id):
        """
        This test validates that admin level entity can be fetched successfully
        :return: this function returns boolean status of element located
        """
        get_admin_level_entity_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/adminEntity"
        self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_admin_level_entity_endpoint, self.headers)
        return response

    def get_user_sub_location_by_user_id_and_prod_id_api(self, user_id, prod_id):
        """
        This test validates that users sub-location can be fetched successfully by valid userid and product Id
        :return: this function returns boolean status of element located
        """
        get_user_sub_location_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/products/" + prod_id
        self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(get_user_sub_location_endpoint, self.headers)
        return response

    def get_user_locations_by_sub_id_api(self, sub_id=''):
        """
        This method is to fetch the user locations using subscription id
        :returns: The response of the get_user_locations_by_sub_id_api api.
        """
        get_locations_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/locations"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_locations_endpoint, self.headers)
        return response

    def get_subscription_details_by_sub_id_api(self, sub_id=''):
        """
        This method is to fetch the subscription details using subscription id.
        :returns: The response of the get_subscription_details_by_sub_id_api api.
        """
        get_subs_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}'
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_subs_url, self.headers)
        return response

# This section covers the test scripts of device module

    def get_devices_api(self, is_admin=False, sub_id=None):
        """
        This test fetches the details of all available devices
        :return: this function returns boolean status of element located
        """

        if is_admin:
            self.headers['Authorization'] = self.admin_token
            get_devices_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/devices'
        else:
            self.headers['Authorization'] = self.client_token
            get_devices_endpoint = f'{self.endpoint}/api/v1/devices'

        response = self.api.get_api_response(endpoint=get_devices_endpoint, headers=self.headers)
        return response

    def verify_get_device_details_by_sub_id_api(self, sub_id):
        """
        This test fetches the details of all available devices
        :return: this function returns boolean status of element located
        """
        get_device_endpoint = self.endpoint + "/api/v1/subscriptions/"+sub_id+"/devices"
        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_device_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_register_device_info_api(self, loc_id='', device_type='', device_sno ='', sub_id=''):
        """
        This function validates if a device can be registered successfully or not
        :return: this function returns boolean status of element located
        """

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'device_info_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['locationID'] = loc_id
        self.json_data['deviceType'] = device_type
        self.json_data['deviceSerialNumber'] = device_sno

        register_device_info_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + "/deviceByDetail"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=register_device_info_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_get_device_details_by_device_sno_api(self, sub_id, dev_sno, dev_type):
        """
        This test fetches the details of devices by device serial number
        :return: this function returns boolean status of element located
        """

        get_device_endpoint = self.endpoint + "/api/v1/subscriptions/"+sub_id+"/devices/"+dev_sno+"/deviceType/"+dev_type
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_device_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_delete_device_details_by_device_sno_api(self, sub_id, dev_sno, dev_type):
        """
        This test deletes the details of devices by device serial number
        :return: this function returns boolean status of element located
        """

        get_device_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/devices/" + dev_sno + "/deviceType/" + dev_type
        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=get_device_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code

    def verify_swap_device_info_api(self, loc_id='', swap_device_type='', swap_device_sno='', sub_id='', device_id=''):
        """
        This function validates that device info can be swapped successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'device_info_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['locationID'] = loc_id
        self.json_data['deviceType'] = swap_device_type
        self.json_data['deviceSerialNumber'] = swap_device_sno

        register_device_info_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + "/devices/"+device_id+"/swap"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(
            endpoint=register_device_info_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_swap_device_info_from_claim_api(self, loc_id='', swap_device_type='', swap_device_sno='', device_id=''):
        """
        This function validates that device info can be swapped successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'device_info_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['locationID'] = loc_id
        self.json_data['deviceType'] = swap_device_type
        self.json_data['deviceSerialNumber'] = swap_device_sno

        register_device_info_endpoint = self.endpoint + '/api/v1/devices/' + device_id + "/swap"
        self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=register_device_info_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def patch_update_integrator_id_in_product_api(self, sub_id='', device_sno='', device_type='DVH', int_id=''):

        query_param = '?integratorID=' + int_id
        update_int_id_url = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/devices/' + device_sno \
                                            + '/deviceType/' + device_type + query_param
        self.headers['Authorization'] = self.admin_token

        response = self.api.patch_api_response(endpoint=update_int_id_url, headers=self.headers)
        return response


    def verify_create_subscription_snap_logic_api(self, event_id='', event_typ='', plan_id='', country='', sub_id=''):
        """
        This function validates that snap logic subscription can be created successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'snap_logic_create_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['eventId'] = event_id
        self.json_data['eventType'] = event_typ
        self.json_data['subscription']['plans'][0]['pbPlanId'] = plan_id
        self.json_data['subscription']['country'] = country
        self.json_data['subscription']['subscriptionId'] = sub_id


        register_device_info_endpoint = self.endpoint + '/api/v1/subscriptions/'
        self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=register_device_info_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_cancel_subscription_snap_logic_api(self, event_id='', sub_id=''):
        """
        This function validates that snap logic subscription can be created successfully
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'snap_logic_cancel_subscription_body')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['eventId'] = event_id
        self.json_data['subId'] = sub_id

        register_device_info_endpoint = self.endpoint + '/api/v1/subscriptions/'
        self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=register_device_info_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def get_group_id(self, get_admin_roles_response, admin_type=None):
        """
        This method is get the admin roles and their group ids for the selected environment.
        The captured group ids are then used in the add_admin_user api call to create the admin user based on the admin
        roles.

        :param get_admin_roles_response: The response from the get_admin_roles api.
        :param admin_type: The admin roles: PB_ADMIN, PB_OPERATOR, PB_SERVICE, PB_SUPPORT, USER_ADMIN
        :return: group_id either of type list or string.
        """
        if type(admin_type) is list:
            group_id = []
            for i in range(0, len(admin_type)):
                for index in range(0, len(get_admin_roles_response)):
                    if get_admin_roles_response[index]['roleID'] == admin_type[i]:
                        group_id.append(get_admin_roles_response[index]['oktaGroupID'])
                        break
        else:
            group_id = ''
            for index in range(0, len(get_admin_roles_response)):
                if get_admin_roles_response[index]['roleID'] == admin_type:
                    group_id = get_admin_roles_response[index]['oktaGroupID']
                    break
        return group_id

    def get_subscription_user_by_email_api(self, sub_id='', email=''):
        """
        This method is to make a get request to the get_subscription_users_by_sub_id_and_search_query api and get the
        required subscription user details like its status, archive, and other details.

        :param sub_id: The subscription id.
        :param email: The email of the selected subscription user.
        :returns: The response of the get_subscription_users_by_sub_id_and_search_query api.
        """
        get_subs_user_by_email_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/users?query=' + email
        self.headers['Authorization'] = self.admin_token
        response = self.api.get_api_response(get_subs_user_by_email_endpoint, self.headers)
        return response

    def change_active_status_for_admin_user_by_user_id_api(self, user_id='', active_flag='false', groupId=None,
                                                           fname='', lname='', disp_name='', email=''):
        """
        This method is to make a put request to the subscription user api to update the status of the selected admin
        user from active to inactive or vice-versa (based on the active_flag value).

        :param user_id: The user_id of the selected admin user.
        :param active_flag: The flag. If the value is true then user active status is updated to true else the active
                            status is updated to false (making it inactive).
        :param groupId: The group_id of the selected user.
        :param fname: The first name of the selected user.
        :param lname: The last name of the selected user.
        :param disp_name: The display name of the selected user.
        :param email: The email address of the selected user.
        :returns: The response of the update subscription user api.
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'change_active_status_admin_user_body')) as file:
            self.json_data = json.load(file)

        self.json_data['id'] = user_id
        self.json_data['active'] = active_flag
        self.json_data['profile']['firstName'] = fname
        self.json_data['profile']['lastName'] = lname
        self.json_data['profile']['displayName'] = disp_name
        self.json_data['profile']['email'] = email
        if type(groupId) is list:
            self.json_data['groupIds'] = groupId
        else:
            self.json_data['groupIds'][0] = groupId

        change_active_status_admin_user_endpoint = self.endpoint + '/api/v1/users/pbadmin/' + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(change_active_status_admin_user_endpoint, self.headers,
                                             json.dumps(self.json_data))
        return response

    def change_active_status_for_subs_user_by_user_id_api(self, user_id='', active_flag=False, sub_id='', fname='',
                                                          lname='', disp_name='', email=''):
        """
        This method is to make a put request to the subscription user api to update the status of the selected
        subscription user from active to inactive or vice-versa (based on the active_flag value).

        :param user_id: The user_id of the selected subscription user.
        :param active_flag: The flag. If the value is true then user active status is updated to true else the active
                            status is updated to false (making it inactive).
        :param sub_id: The subscription_id of the selected user.
        :param fname: The first name of the selected user.
        :param lname: The last name of the selected user.
        :param disp_name: The display name of the selected user.
        :param email: The email address of the selected user.
        :returns: The response of the update subscription user api.
        """
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'change_active_status_subs_user_body')) as file:
            self.json_data = json.load(file)

        self.json_data['id'] = user_id
        self.json_data['active'] = active_flag
        self.json_data['profile']['firstName'] = fname
        self.json_data['profile']['lastName'] = lname
        self.json_data['profile']['displayName'] = disp_name
        self.json_data['profile']['email'] = email
        self.json_data['subID'] = sub_id

        change_active_status_user_endpoint = self.endpoint + '/api/v1/users/' + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(change_active_status_user_endpoint, self.headers,
                                             json.dumps(self.json_data))
        return response

    def put_update_mfa_by_sub_id_api(self, sub_id='', mfa_enabled=False):
        get_subs_details_resp = self.get_subscription_details_by_sub_id_api(sub_id)

        for k, v in get_subs_details_resp.json()['properties'].items():
            if k == 'mfaEnabled':
                get_subs_details_resp.json()['properties']['mfaEnabled'] = mfa_enabled
                break

        get_subscription_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(get_subscription_endpoint, self.headers, body=get_subs_details_resp.json())
        return response

    def put_update_subs_user_details_by_user_id_api(self, user_id='', fname='', lname='', email='', disp_name='',
                                                    sub_id='', loc_id='', admin_lvl='', admn_lvl_entity=None,
                                                    ent_name='', subs_roles=None, is_admin='y', admin_type=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subs_user_request_body')) as file:
            self.json_data = json.load(file)

        self.json_data['id'] = user_id
        self.json_data['enterpriseName'] = ent_name
        self.json_data['subscriptionRoles'] = subs_roles
        self.json_data['locationID'] = loc_id
        self.json_data['profile']['firstName'] = fname
        self.json_data['profile']['lastName'] = lname
        self.json_data['profile']['email'] = email
        self.json_data['profile']['displayName'] = disp_name
        self.json_data['subID'] = sub_id
        if admin_type != 'User':
            self.json_data['adminLevelAt'] = admin_lvl
            self.json_data['adminLevelEntity'] = admn_lvl_entity

        update_subs_user_endpoint = self.endpoint + '/api/v1/users/' + user_id
        self.headers['Authorization'] = self.admin_token
        if is_admin == 'n':
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(update_subs_user_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def put_update_subs_user_details_with_user_type_by_user_id_api(
            self, user_id='', adm_lvl='', adm_lvl_entity=None, ent_name=None, roles=None, active=True, fname='',
            lname='', dispname='', email='', sub_id=None, default_cost_acct=None, is_admin=False, admin_token=None,
            client_token=None):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subs_user_req_body')) as file:
            req_data = json.load(file)

        def set_req_data_value(key, value):
            if value != '':
                keys = key.split('.')
                current_level = req_data
                for k in keys[:-1]:
                    if k not in current_level:
                        current_level[k] = {}
                    current_level = current_level[k]
                current_level[keys[-1]] = value

        set_req_data_value('id', user_id)
        set_req_data_value('adminLevelAt', adm_lvl)
        #set_req_data_value('adminLevelEntity', [adm_lvl_entity])  # adm_lvl_entity should be in list
        set_req_data_value('adminLevelEntity', adm_lvl_entity if isinstance(adm_lvl_entity, list) else [adm_lvl_entity])
        set_req_data_value('enterpriseName', ent_name)
        set_req_data_value('subscriptionRoles', [roles])  # roles should be in list
        set_req_data_value('profile.firstName', fname)
        set_req_data_value('profile.lastName', lname)
        set_req_data_value('profile.displayName', dispname)
        set_req_data_value('profile.email', email)
        set_req_data_value('subID', sub_id)
        set_req_data_value('defaultCostAccount', default_cost_acct)
        set_req_data_value('active', active)

        update_user_url = f'{self.endpoint}/api/v1/users/{user_id}'

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.put_api_response(endpoint=update_user_url, headers=self.headers, body=json.dumps(req_data))
        return response

    def patch_update_subs_user_details_by_user_id_api(self, user_id='', sub_id='', fname='', lname='', disp_name='',
                                                      subs_roles=None, status='ACTIVE'):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'patch_update_subs_user_request_body')) as file:
            self.json_data = json.load(file)

        self.json_data['firstName'] = fname
        self.json_data['lastName'] = lname
        self.json_data['displayName'] = disp_name
        self.json_data['status'] = status
        self.json_data['roles'] = subs_roles

        update_subs_user_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/users/' + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.patch_api_response(update_subs_user_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def put_update_admin_user_details_by_user_id_api(self, user_id='', fname='', lname='', disp_name='',
                                                     admin_lvl_at='', admn_lvl_entity=None, group_id=None,
                                                     email='', status='ACTIVE'):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'put_update_admin_user_request_body')) as file:
            self.json_data = json.load(file)

        self.json_data['id'] = user_id
        self.json_data['profile']['firstName'] = fname
        self.json_data['profile']['lastName'] = lname
        self.json_data['profile']['displayName'] = disp_name
        self.json_data['profile']['email'] = email
        self.json_data['profile']['login'] = email
        self.json_data['profile']['status'] = status
        self.json_data['adminLevelAt'] = admin_lvl_at
        self.json_data['groupIds'] = group_id

        # adminLevelEntity is a list of Enterprise Ids
        if admn_lvl_entity is not None:
            self.json_data['adminLevelEntity'] = admn_lvl_entity

        update_subs_user_endpoint = self.endpoint + '/api/v1/users/pbadmin/' + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(update_subs_user_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def put_update_user_sub_location_properties_api(self, user_id='', sub_id=None, def_fedex_acct_id='',
                                                    def_ups_acct_id='', def_usps_acct_id='', def_cost_acct_id='',
                                                    is_admin=False, token=None):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_user_sub_location_prop_req_body')) as file:
            req_data = json.load(file)

        req_data['defaultFedexCarrierAccountID'] = def_fedex_acct_id
        req_data['defaultUPSCarrierAccountID'] = def_ups_acct_id
        req_data['defaultUSPSCarrierAccountID'] = def_usps_acct_id
        req_data['defaultCostAccountID'] = def_cost_acct_id

        if is_admin:
            update_user_url = f'{self.endpoint}/api/v1/users/{user_id}/subscriptions/{sub_id}/sublocationProperties'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            update_user_url = f'{self.endpoint}/api/v1/users/{user_id}/sublocationProperties'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.put_api_response(endpoint=update_user_url, headers=self.headers, body=json.dumps(req_data))
        return response

    def get_check_access_requests_api(self):
        check_access_requests_endpoint = self.endpoint + '/api/v1/checkAccessRequests'
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(check_access_requests_endpoint, self.headers)
        return response

    def post_send_access_request(self, user_id='', email='', comments='', country_code='US'):
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'post_send_access_request_body')) as file:
            self.json_data = json.load(file)

        self.json_data['emailAddress'] = email
        self.json_data['userID'] = user_id
        self.json_data['countryCode'] = country_code
        if comments != '':
            self.json_data['comments'] = comments

        send_request_endpoint = self.endpoint + '/api/v1/sendRequest'
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(send_request_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def post_grant_access_api(self, user_id='', email=''):
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'post_grant_access_request_body')) as file:
            self.json_data = json.load(file)

        self.json_data['emailAddress'] = email
        self.json_data['userID'] = user_id

        grant_request_endpoint = self.endpoint + '/api/v1/grantAccess'
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(grant_request_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def get_menu_items_by_user_id_sub_id_api(self, user_id='', sub_id='', token='', is_admin=False):

        query_params = '?userID=' + user_id + '&subID=' + sub_id
        get_menu_items_url = self.endpoint + '/api/v1/user/menu' + query_params

        if token:
            self.headers['Authorization'] = token
        elif is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_menu_items_url, headers=self.headers)
        return response

    def get_user_properties_for_user_id_sub_id_api(self, user_id='', sub_id='', token='', is_admin=False):

        query_params = '?userID=' + user_id + '&subID=' + sub_id
        get_user_properties_url = self.endpoint + '/api/v1/userProperties' + query_params

        if token:
            self.headers['Authorization'] = 'Bearer ' + token
        elif is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_user_properties_url, headers=self.headers)
        return response

    def put_update_user_properties_for_user_id_sub_id_api(self, user_id='', sub_id='', country_code='US', token='',
                                                          is_admin=False, showLabelOptions=False, printScanForm=False,
                                                          printShippingLabelReceipt=True, printPostageCostOnLabel=True,
                                                          saveRecipientAddress=True,
                                                          emailToSenderPackageTrackingNumber=True,
                                                          emailToSenderPackageDeliveredEvent=True,
                                                          emailToRecipientPackageTrackingNumber=True,
                                                          emailToRecipientOnPackageDeliveredEvent=True,
                                                          emailSubjectForTrackingNumber='',
                                                          emailSubjectForPackageDelivered='',
                                                          uspsServiceOption=True, printFullSheet=True,
                                                          doNotShowRollPrinter=True, isReturnAddressSame=False,
                                                          defaultSenderAddressID='', defaultDimensionUnit='',
                                                          defaultWeightUnit='', showWelcomeTour=False,
                                                          sameReturnAddressForLabels=False, tncAccepted=False,
                                                          msContactsRequired=False, defaultMeasurementUnit='',
                                                          showCostOnIntLabels=False, isNewEcomUser=False,
                                                          printReturnLabelWithShipping=False, carrierReturnServices=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_user_properties_request_body')) as file:
            self.json_data = json.load(file)

        if showLabelOptions:
            self.json_data['showLabelOptions'] = showLabelOptions
        if printScanForm:
            self.json_data['printScanForm'] = printScanForm
        if printShippingLabelReceipt:
            self.json_data['printShippingLabelReceipt'] = printShippingLabelReceipt
        if printPostageCostOnLabel:
            self.json_data['printPostageCostOnLabel'] = printPostageCostOnLabel
        if saveRecipientAddress:
            self.json_data['saveRecipientAddress'] = saveRecipientAddress
        if emailToSenderPackageTrackingNumber:
            self.json_data['emailToSenderPackageTrackingNumber'] = emailToSenderPackageTrackingNumber
        if emailToSenderPackageDeliveredEvent:
            self.json_data['emailToSenderPackageDeliveredEvent'] = emailToSenderPackageDeliveredEvent
        if emailToRecipientPackageTrackingNumber:
            self.json_data['emailToRecipientPackageTrackingNumber'] = emailToRecipientPackageTrackingNumber
        if emailToRecipientOnPackageDeliveredEvent:
            self.json_data['emailToRecipientOnPackageDeliveredEvent'] = emailToRecipientOnPackageDeliveredEvent
        if emailSubjectForTrackingNumber:
            self.json_data['emailSubjectForTrackingNumber'] = emailSubjectForTrackingNumber
        if emailSubjectForPackageDelivered:
            self.json_data['emailSubjectForPackageDelivered'] = emailSubjectForPackageDelivered
        if uspsServiceOption:
            self.json_data['uspsServiceOption'] = uspsServiceOption
        if printFullSheet:
            self.json_data['printFullSheet'] = printFullSheet
        if doNotShowRollPrinter:
            self.json_data['doNotShowRollPrinter'] = doNotShowRollPrinter
        if isReturnAddressSame:
            self.json_data['isReturnAddressSame'] = isReturnAddressSame
        if defaultSenderAddressID:
            self.json_data['defaultSenderAddressID'] = defaultSenderAddressID
        if defaultDimensionUnit:
            self.json_data['defaultDimensionUnit'] = defaultDimensionUnit
        if defaultWeightUnit:
            self.json_data['defaultWeightUnit'] = defaultWeightUnit
        if showWelcomeTour:
            self.json_data['showWelcomeTour'] = showWelcomeTour
        if sameReturnAddressForLabels:
            self.json_data['sameReturnAddressForLabels'] = sameReturnAddressForLabels
        if tncAccepted:
            self.json_data['tncAccepted'] = tncAccepted
        if msContactsRequired:
            self.json_data['msContactsRequired'] = msContactsRequired
        if defaultMeasurementUnit:
            self.json_data['defaultMeasurementUnit'] = defaultMeasurementUnit
        if showCostOnIntLabels:
            self.json_data['showCostOnIntLabels'] = showCostOnIntLabels
        if isNewEcomUser:
            self.json_data['isNewEcomUser'] = isNewEcomUser
        if printReturnLabelWithShipping:
            self.json_data['printReturnLabelWithShipping'] = printReturnLabelWithShipping
        if carrierReturnServices:
            self.json_data['carrierReturnServices'] = carrierReturnServices

        query_params = '?userID=' + user_id + '&subID=' + sub_id + '&countryCode=' + country_code
        update_user_properties_url = self.endpoint + '/api/v1/userProperties' + query_params

        if token:
            self.headers['Authorization'] = token
        elif is_admin:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(
            endpoint=update_user_properties_url, headers=self.headers, body=json.dumps(self.json_data))
        return response

    def put_update_subs_properties_for_user_id_sub_id_api(self, sub_id='', admin_token=None, client_token=None, is_admin=False, kip=False,
                                                          customerType='commercial', omasCustomer=False,
                                                          sched48Customer=False, sharedAddressBookEnabled=False, federatedUser=False,
                                                          oktaGroupID='', ledgerProductID='', maxTxLimitEnabled=False,
                                                          secMsg='', automaticRefillEnabled=False, minPostageExceedPromptEnabled=False,
                                                          emailNotificationEnabled=False, costAccountSelectionEnabled=False,
                                                          costAccountSettings_costAccountsEnabled=False, costAccountsRequiredForShipments=False,
                                                          costAccountsRequiredForStamps=False, costAccountRequiredForAddingPostage=False,
                                                          costAccountRequiredForERR=False, costAccountRequiredForReceiving=False,
                                                          costAccountRequiredForLocker=False, costAccountRequiredForAddShipRequest=False,
                                                          allowUserToViewPostageAccountBalance=False, allowUserToAddPostage=False,
                                                          allowCostCentreManagement=False, allowUserToBuySupplies=False,
                                                          allowUsersToManageCarriers=False, allowUsersToManageUsers=False,
                                                          officialMailerEnabled=False, costAccountLocAdminAccess=False,
                                                          allowedMaxPostageBalance=False, fraudCheckEnabled=True, deliveryAssurance=False,
                                                          allowShipWithoutSpendingLimit=False, costAccountsEnabled=False,
                                                          costAccountRequireShippingLabel=False, costAccountsRequiredForMailing=False,
                                                          marketPlaceSettings=None, defaultCarrierAccounts=None, nsa=False,
                                                          allowedPurchaseSupplies=False, personalIDOptional=False,
                                                          allowedDownloadDeviceHub=False, mfaEnabled=False, taDeviceSupported=False,
                                                          bpnValidationNotRequired=False, bpnDuplicityCheckRequired=False,
                                                          authProvider='', enableCustomFields=False, recipientEmailAndPhoneRequired=False,
                                                          costAccountUsageLocked=False, costAccountUsageLockedBy=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_subs_properties_req_body')) as file:
            self.json_data = json.load(file)

        if kip:
            self.json_data['kip'] = kip
        if customerType:
            self.json_data['customerType'] = customerType
        if omasCustomer:
            self.json_data['omasCustomer'] = omasCustomer
        if sched48Customer:
            self.json_data['sched48Customer'] = sched48Customer
        if sharedAddressBookEnabled:
            self.json_data['sharedAddressBookEnabled'] = sharedAddressBookEnabled
        if federatedUser:
            self.json_data['federatedUser'] = federatedUser
        if oktaGroupID:
            self.json_data['oktaGroupID'] = oktaGroupID
        if ledgerProductID:
            self.json_data['ledgerProductID'] = ledgerProductID
        if maxTxLimitEnabled:
            self.json_data['maxTxLimitEnabled'] = maxTxLimitEnabled
        if secMsg:
            self.json_data['secMsg'] = secMsg
        if automaticRefillEnabled:
            self.json_data['postageRefillSettings']['automaticRefillEnabled'] = automaticRefillEnabled
        if minPostageExceedPromptEnabled:
            self.json_data['postageRefillSettings']['minPostageExceedPromptEnabled'] = minPostageExceedPromptEnabled
        if emailNotificationEnabled:
            self.json_data['postageRefillSettings']['emailNotificationEnabled'] = emailNotificationEnabled
        if costAccountSelectionEnabled:
            self.json_data['postageRefillSettings']['costAccountSelectionEnabled'] = costAccountSelectionEnabled
        if costAccountSettings_costAccountsEnabled:
            self.json_data['costAccountSettings']['costAccountsEnabled'] = costAccountSettings_costAccountsEnabled
        if costAccountsRequiredForShipments:
            self.json_data['costAccountSettings']['costAccountsRequiredForShipments'] = costAccountsRequiredForShipments
        if costAccountsRequiredForStamps:
            self.json_data['costAccountSettings']['costAccountsRequiredForStamps'] = costAccountsRequiredForStamps
        if costAccountRequiredForAddingPostage:
            self.json_data['costAccountSettings']['costAccountRequiredForAddingPostage'] = costAccountRequiredForAddingPostage
        if costAccountRequiredForERR:
            self.json_data['costAccountSettings']['costAccountRequiredForERR'] = costAccountRequiredForERR
        if costAccountRequiredForReceiving:
            self.json_data['costAccountSettings']['costAccountRequiredForReceiving'] = costAccountRequiredForReceiving
        if costAccountRequiredForLocker:
            self.json_data['costAccountSettings']['costAccountRequiredForLocker'] = costAccountRequiredForLocker
        if costAccountRequiredForAddShipRequest:
            self.json_data['costAccountSettings']['costAccountRequiredForAddShipRequest'] = costAccountRequiredForAddShipRequest
        if allowUserToViewPostageAccountBalance:
            self.json_data['userManagementSettings']['allowUserToViewPostageAccountBalance'] = allowUserToViewPostageAccountBalance
        if allowUserToAddPostage:
            self.json_data['userManagementSettings']['allowUserToAddPostage'] = allowUserToAddPostage
        if allowCostCentreManagement:
            self.json_data['userManagementSettings']['allowCostCentreManagement'] = allowCostCentreManagement
        if allowUserToBuySupplies:
            self.json_data['userManagementSettings']['allowUserToBuySupplies'] = allowUserToBuySupplies
        if allowUsersToManageCarriers:
            self.json_data['userManagementSettings']['allowUsersToManageCarriers'] = allowUsersToManageCarriers
        if allowUsersToManageUsers:
            self.json_data['userManagementSettings']['allowUsersToManageUsers'] = allowUsersToManageUsers
        if officialMailerEnabled:
            self.json_data['officialMailerEnabled'] = officialMailerEnabled
        if costAccountLocAdminAccess:
            self.json_data['costAccountLocAdminAccess'] = costAccountLocAdminAccess
        if allowedMaxPostageBalance:
            self.json_data['allowedMaxPostageBalance'] = allowedMaxPostageBalance
        if fraudCheckEnabled:
            self.json_data['fraudCheckEnabled'] = fraudCheckEnabled
        if deliveryAssurance:
            self.json_data['deliveryAssurance'] = deliveryAssurance
        if allowShipWithoutSpendingLimit:
            self.json_data['allowShipWithoutSpendingLimit'] = allowShipWithoutSpendingLimit
        if costAccountsEnabled:
            self.json_data['costAccountsEnabled'] = costAccountsEnabled
        if costAccountRequireShippingLabel:
            self.json_data['costAccountRequireShippingLabel'] = costAccountRequireShippingLabel
        if costAccountsRequiredForMailing:
            self.json_data['costAccountsRequiredForMailing'] = costAccountsRequiredForMailing
        if marketPlaceSettings:
            self.json_data['marketPlaceSettings'] = marketPlaceSettings
        if defaultCarrierAccounts:
            self.json_data['defaultCarrierAccounts'] = defaultCarrierAccounts
        if nsa:
            self.json_data['nsa'] = nsa
        if allowedPurchaseSupplies:
            self.json_data['allowedPurchaseSupplies'] = allowedPurchaseSupplies
        if personalIDOptional:
            self.json_data['personalIDOptional'] = personalIDOptional
        if allowedDownloadDeviceHub:
            self.json_data['allowedDownloadDeviceHub'] = allowedDownloadDeviceHub
        if mfaEnabled:
            self.json_data['mfaEnabled'] = mfaEnabled
        if taDeviceSupported:
            self.json_data['taDeviceSupported'] = taDeviceSupported
        if bpnValidationNotRequired:
            self.json_data['bpnValidationNotRequired'] = bpnValidationNotRequired
        if bpnDuplicityCheckRequired:
            self.json_data['bpnDuplicityCheckRequired'] = bpnDuplicityCheckRequired
        if authProvider:
            self.json_data['authProvider'] = authProvider
        if enableCustomFields:
            self.json_data['enableCustomFields'] = enableCustomFields
        if recipientEmailAndPhoneRequired:
            self.json_data['recipientEmailAndPhoneRequired'] = recipientEmailAndPhoneRequired
        if costAccountUsageLocked:
            self.json_data['costAccountUsageLocked'] = costAccountUsageLocked
        if costAccountUsageLockedBy:
            self.json_data['costAccountUsageLockedBy'] = costAccountUsageLockedBy

        query_params = '?subID=' + sub_id
        update_user_properties_url = self.endpoint + '/api/v1/subscriptionProperties' + query_params

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.put_api_response(
            endpoint=update_user_properties_url, headers=self.headers, body=json.dumps(self.json_data))
        return response

    def put_update_plans_in_subs_by_sub_id_api(self, is_admin=False, sub_id=None, ent_id=None, country_code='US',
                                               plans=None, okta_group_id=None, admin_token='', client_token=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'update_plans_in_subs_req_body')) as file:
            self.json_data = json.load(file)

        if sub_id:
            self.json_data['subID'] = sub_id
        if ent_id:
            self.json_data['enterpriseID'] = ent_id
        if country_code:
            self.json_data['countryCode'] = country_code
        if plans:
            self.json_data['plans'] = plans
        if okta_group_id:
            self.json_data['properties']['oktaGroupID'] = okta_group_id

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        update_subs_plans_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}'

        response = self.api.put_api_response(endpoint=update_subs_plans_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def users_advance_search_api(self, is_admin=False, sub_id=None, ent_id=None, skip='0', limit='10', archive='false',
                                 status='ACTIVE', payload=None, admin_token='', client_token=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'advance_search_request')) as file:
            json_data = json.load(file)

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
            query_params = f'?subID={sub_id}&skip={skip}&limit={limit}&archive={archive}&entID={ent_id}&status={status}'
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token
            query_params = f'?skip={skip}&limit={limit}&archive={archive}&entID={ent_id}&status={status}'

        request_body = payload if payload else json_data
        advance_search_endpoint = f'{self.endpoint}/api/v1/subscriptions/advanceSearch{query_params}'

        response = self.api.post_api_response(endpoint=advance_search_endpoint, headers=self.headers,
                                              body=json.dumps(request_body))
        return response

    def import_user_api(self, sub_id=None, is_admin=False, file=None, user_type='normalUser'):

        self.headers = {
            'Content-Type': 'multipart/form-data',
            'Authorization': self.admin_token if is_admin else self.client_token
        }

        payload = {
            'file': file,
            'userType': user_type
        }

        import_user_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/importUser' if is_admin \
            else f'{self.endpoint}/api/v1/importUser'

        response = self.api.post_api_response(endpoint=import_user_endpoint, headers=self.headers, body=payload)
        return response

    def import_user_process_api(self, sub_id=None, is_admin=False, job_id=None, user_type='normalUser',
                                access_level='E', access_level_entity=None):

        self.headers = {
            'Content-Type': 'multipart/form-data',
            'Authorization': self.admin_token if is_admin else self.client_token
        }

        payload = {
            'fieldsMapping': '{"FirstName":"First Name","LastName":"Last Name","Email":"E-Mail","SubscriptionRole":'
                             '"Role","Division":"Division","ShipToBPN":"BPN","Location":"Location","Company":'
                             '"Company Name","AddressLine1":"Customer Address","CityTown":"City","StateProvince":'
                             '"State","CountryCode":"Country","PostalCode":"Zip","Phone":"Phone","DefaultCostAccount":'
                             '"Default Cost Account"}',
            'userType': user_type,
            'adminLevelAt': access_level,
            'adminLevelEntity': access_level_entity
        }

        import_user_process_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/importUser/jobs' \
                                       f'/{job_id}/process' if is_admin else \
                                       f'{self.endpoint}/api/v1/importUser/jobs/{job_id}/process'

        response = self.api.post_api_response(endpoint=import_user_process_endpoint, headers=self.headers, body=payload)
        return response

    def put_update_cost_account_settings_in_subs_prop_api(self, sub_id=None, payload=None, is_admin=False,
                                                          admin_token=None, client_token=None, cost_acct_enabled=False,
                                                          cost_acct_req_shipments=False, cost_acct_hierarchy=False,
                                                          cost_acct_req_ship_request=False, cost_acct_req_err=False,
                                                          cost_acct_req_postage=False, cost_acct_req_stamps=False,
                                                          cost_acct_req_locker=False, cost_acct_req_receiving=False):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'cost_account_settings_subs_prop_request')) as file:
            json_data = json.load(file)

        if cost_acct_enabled:
            json_data['costAccountsEnabled'] = cost_acct_enabled
        if cost_acct_req_shipments:
            json_data['costAccountsRequiredForShipments'] = cost_acct_req_shipments
        if cost_acct_req_ship_request:
            json_data['costAccountRequiredForAddShipRequest'] = cost_acct_req_ship_request
        if cost_acct_req_err:
            json_data['costAccountRequiredForERR'] = cost_acct_req_err
        if cost_acct_req_postage:
            json_data['costAccountRequiredForAddingPostage'] = cost_acct_req_postage
        if cost_acct_req_stamps:
            json_data['costAccountsRequiredForStamps'] = cost_acct_req_stamps
        if cost_acct_req_locker:
            json_data['costAccountRequiredForLocker'] = cost_acct_req_locker
        if cost_acct_req_receiving:
            json_data['costAccountRequiredForReceiving'] = cost_acct_req_receiving
        if cost_acct_hierarchy:
            json_data['costAccountsHierarchyEnabled'] = cost_acct_hierarchy

        request_body = payload if payload else json_data
        update_settings_url = f'{self.endpoint}/api/v1/subscription/{sub_id}/CostAccountSettings'

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.put_api_response(endpoint=update_settings_url, headers=self.headers,
                                             body=json.dumps(request_body))
        return response

    def check_all_access_requests(self, user_id=''):
        status = ''
        comments = ''

        check_access_requests_resp = self.get_check_access_requests_api()

        for i in range(len(check_access_requests_resp.json())):
            if check_access_requests_resp.json()[i]['userID'] == user_id:
                status = check_access_requests_resp.json()[i]['status']
                comments = check_access_requests_resp.json()[i]['comments']
                break

        return status, comments

    def get_active_user_email(self):
        get_all_users_resp = self.get_users_api()
        for i in range(len(get_all_users_resp.json()['users'])):
            for k, v in get_all_users_resp.json()['users'][i].items():
                if k == 'active' and v:
                    email = str(get_all_users_resp.json()['users'][i]['profile']['email'])
                    return email
        return None

    def get_active_user_id(self, is_admin=False):
        get_all_users_resp = self.get_users_api(is_admin=is_admin)
        for i in range(len(get_all_users_resp.json()['users'])):
            for k, v in get_all_users_resp.json()['users'][i].items():
                if k == 'active' and v:
                    user_id = str(get_all_users_resp.json()['users'][i]['id'])
                    return user_id
        return None

    def get_active_admin_user_id(self, admin_type='PB_SERVICE', is_admin=True):
        get_all_users_resp = self.get_users_api(is_admin=is_admin, limit='30')
        for i in range(len(get_all_users_resp.json()['users'])):
            for k, v in get_all_users_resp.json()['users'][i].items():
                if k == 'roles' and v[0] == str(admin_type):
                    if get_all_users_resp.json()['users'][i]['active']:
                        user_id = str(get_all_users_resp.json()['users'][i]['id'])
                        self.log.info(f"Active {admin_type} admin user id {user_id} found!")
                        return user_id
        self.log.error(f"No active admin user found for {admin_type} within the search limit!")
        return None

    def set_user_id_in_error_response(self, user_id='', file_path=''):
        with open(self.prop.get('SUBSCRIPTION_MGMT', file_path), 'r+') as f:
            content = json.load(f)
            for k, v in content['errors'][0].items():
                if k == 'errorDescription':
                    content['errors'][0]['errorDescription'] = v.replace('?', user_id)
                    return content

    def get_active_user_id_product_id_from_properties(self):
        properties_resp = self.get_user_properties_api()
        for i in range(len(properties_resp.json())):
            for k, v in properties_resp.json()[i].items():
                if k == 'status' and v:
                    user_id = properties_resp.json()[0]['userID']
                    prod_id = properties_resp.json()[i]['productID']
                    return user_id, prod_id
        return None

    @staticmethod
    def generate_user_profile_data(is_admin=False):
        fname = f"pyauto{generate_random_string(uppercase=False, char_count=4)}"
        if is_admin:
            lname = f"admin{generate_random_string(uppercase=False, char_count=4)}"
        else:
            lname = f"user{generate_random_string(uppercase=False, char_count=4)}"
        dispname = f"{fname}.{lname}"
        mailid = f"{dispname}@yopmail.com"
        password = "Horizon#123"

        return fname, lname, mailid, dispname, password

    def get_ent_details_by_sub_id(self, sub_id):

        get_subscription_details = self.get_subscription_details_by_sub_id_api(sub_id)

        ent_id = [str(get_subscription_details.json().get('enterpriseID', ''))]
        loc_id = str(get_subscription_details.json().get('locations', [''])[0])
        carrier_accounts = get_subscription_details.json().get('carriers', [])
        subs_roles = get_subscription_details.json().get('subscriptionRoles', [])
        subs_role_ids = [role['roleID'] for role in subs_roles]

        if loc_id == '':
            loc_id = self.retrieve_new_location_from_enterprise(ent_id=ent_id, sub_id=sub_id)

        return ent_id, loc_id, carrier_accounts, subs_role_ids

    def get_sub_id_from_file(self, sub_type=''):
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_subscription_ids')) as file:
            self.json_data = json.load(file)

        sub_id = self.json_data[self.prod_name][self.env][sub_type]
        return sub_id

    def retrieve_new_location_from_enterprise(self, current_loc_id='', ent_id=None, sub_id=''):
        new_loc_id = ''

        if isinstance(ent_id, list):
            ent_id = ent_id[0]

        get_div_loc_resp = self.client_mgmt_api.get_divisions_by_ent_id_api(ent_id)

        for i in range(len(get_div_loc_resp.json())):
            if type(get_div_loc_resp.json()[i]['locations']) is list:
                for j in range(len(get_div_loc_resp.json()[i]['locations'])):
                    if get_div_loc_resp.json()[i]['locations'][j] != current_loc_id:
                        new_loc_id = get_div_loc_resp.json()[i]['locations'][j]
                        break
                break

        if new_loc_id == '':
            loc_name = "AutoLocation" + str(random.randint(1, 99))
            div_id = get_div_loc_resp.json()[0]['divisionID']
            add_location_resp = self.client_mgmt_api\
                .post_add_new_location_in_division_api(div_id=div_id, sub_id=sub_id, ent_id=ent_id[0],
                                                       loc_name=loc_name)
            new_loc_id = str(add_location_resp.json()['locationID'])
        return new_loc_id

    def create_subs_user(self, sub_id='', admin_level=''):
        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f:
            self.sample_add_user_exp_resp = json.load(f)

        # Ensure MFA is disabled for the selected Subscription
        self.put_update_mfa_by_sub_id_api(sub_id=sub_id)

        fname, lname, mailid, dispname, password = self.generate_user_profile_data()
        ent_id, loc_id, carrier_accounts, subs_role_ids = self.get_ent_details_by_sub_id(sub_id)

        # Add subscription user
        add_user_by_email_resp = self.add_client_user_by_sub_id_email_api(fname=fname, lname=lname, email=mailid,
                                                                          disp_name=dispname, sub_id=sub_id,
                                                                          loc_id=loc_id, admin_lvl=admin_level,
                                                                          admn_lvl_entity=ent_id,
                                                                          subs_roles=subs_role_ids,
                                                                          carriers=carrier_accounts)
        assert_that(self.common.validate_response_template(add_user_by_email_resp, self.sample_add_user_exp_resp, 201))

        # new_user = False
        # for k, v in dict(add_user_by_email_resp.json()).items():
        #     if k == 'newUser':
        #         new_user = True
        #         break
        # if not new_user:
        #     self.create_active_subs_user(sub_id=sub_id, admin_level=admin_level)

        user_id = add_user_by_email_resp.json()['userID']
        token = add_user_by_email_resp.json()['token']

        self.login.user_account_claim(password, token)
        self.login.check_user_login_status(mailid, password)

        self.log.info(f'Email: {mailid}, UserId: {user_id}, SubId: {sub_id}, AdminLevel: {admin_level}, '
                      f'Ent_Id: {ent_id}, Location: {loc_id}')

        return fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids

    def create_active_subs_user(self, sub_id=None, admin_level=None, fname=None, lname=None, mailid=None, dispname=None,
                                password=None, ent_name=None, division_id=None, location_id=None, ent_id=None,
                                subs_role_ids=None, del_existing_user=False):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f:
            self.sample_add_user_exp_resp = json.load(f)

        carrier_accounts = None

        if not fname:
            fname, lname, mailid, dispname, password = self.generate_user_profile_data()

        if del_existing_user:
            self.delete_created_subs_users(sub_id=sub_id, query=mailid)

        if not ent_name:
            ent_id, ent_name, division_id, location_id, carrier_accounts, subs_role_ids = \
                self.get_ent_div_loc_carrier_subs_details_from_sub_id(sub_id=sub_id)

        admn_lvl_entity_id = []

        if admin_level == 'E':
            admn_lvl_entity_id = ent_id
        elif admin_level == 'D':
            admn_lvl_entity_id = division_id
        elif admin_level == 'L':
            admn_lvl_entity_id = [location_id]

        # Add subscription user
        add_user_by_email_resp = self.add_client_user_by_sub_id_email_api(fname=fname, lname=lname, email=mailid,
                                                                          disp_name=dispname, sub_id=sub_id,
                                                                          loc_id=location_id, admin_lvl=admin_level,
                                                                          admn_lvl_entity=admn_lvl_entity_id,
                                                                          ent_name=ent_name,
                                                                          subs_roles=subs_role_ids,
                                                                          carriers=carrier_accounts)
        if add_user_by_email_resp.status_code == 400:
            self.log.error("Error creating user " + mailid + ": \n" + json.dumps(add_user_by_email_resp.json()))
            return True
        else:
            assert_that(self.common.validate_response_template(add_user_by_email_resp, self.sample_add_user_exp_resp, 201))

            user_id = add_user_by_email_resp.json()['userID']
            token = add_user_by_email_resp.json()['token']

            self.login.user_account_claim(password, token)
            self.login.check_user_login_status(mailid, password)

            self.patch_update_subs_user_details_by_user_id_api(user_id=user_id, sub_id=sub_id, fname=fname, lname=lname,
                                                               disp_name=dispname, subs_roles=subs_role_ids)

            self.log.info(f'Email: {mailid}, UserId: {user_id}, SubId: {sub_id}, AdminLevel: {admin_level}, '
                          f'Ent_Id: {ent_id}, Location: {location_id}')

            return fname, lname, mailid, dispname, password, user_id, ent_id, location_id, carrier_accounts, subs_role_ids

    def create_invited_subs_user(self, sub_id='', admin_level='', fname='', lname='', mailid='', dispname='',
                                 password='', ent_name='', ent_id='', division_id='', location_id='', subs_role_ids=None,
                                 del_existing_user=False):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f:
            sample_add_user_exp_resp = json.load(f)

        loc_id = None
        carrier_accounts = None
        #subs_role_ids = None

        if not fname:
            fname, lname, mailid, dispname, password = self.generate_user_profile_data()

        if del_existing_user:
            self.delete_created_subs_users(sub_id=sub_id, query=mailid)

        if not ent_id or not ent_name:
            ent_id, ent_name, division_id, loc_id, carrier_accounts, subs_role_ids = \
                self.get_ent_div_loc_carrier_subs_details_from_sub_id(sub_id=sub_id)

        if not location_id:
            location_id = str(loc_id)

        admn_lvl_entity_id = []

        if admin_level == 'E':
            admn_lvl_entity_id = ent_id
            loc_id = location_id
        elif admin_level == 'D':
            admn_lvl_entity_id = division_id
            loc_id = location_id
        elif admin_level == 'L':
            admn_lvl_entity_id = [location_id]
            loc_id = location_id
        elif admin_level == 'User':
            loc_id = location_id

        # Add subscription user
        add_user_by_email_resp = self.add_client_user_by_sub_id_email_api(fname=fname, lname=lname, email=mailid,
                                                                          disp_name=dispname, sub_id=sub_id,
                                                                          loc_id=loc_id, admin_lvl=admin_level,
                                                                          admn_lvl_entity=admn_lvl_entity_id,
                                                                          ent_name=ent_name,
                                                                          subs_roles=subs_role_ids,
                                                                          carriers=carrier_accounts)
        if add_user_by_email_resp.status_code == 400:
            self.log.info("Error creating user " + mailid + ": \n" + json.dumps(add_user_by_email_resp.json()))
            return True

        assert_that(self.common.validate_response_template(add_user_by_email_resp, sample_add_user_exp_resp, 201))

        user_id = add_user_by_email_resp.json()['userID']

        self.log.info(f'Email: {mailid}, UserId: {user_id}, SubId: {sub_id}, AdminLevel: {admin_level}, '
                      f'Ent_Id: {ent_id}, Location: {loc_id}')

        return fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids

    def get_ent_div_loc_carrier_subs_details_from_sub_id(self, sub_id=''):

        divisions = ''
        ent_name = ''

        ent_id, loc_id, carrier_accounts, subs_role_ids = self.get_ent_details_by_sub_id(sub_id)

        get_enterprise_resp = self.client_mgmt_api.get_enterprise_by_ent_id_api(ent_id[0])

        if get_enterprise_resp.status_code == 200:
            divisions = get_enterprise_resp.json()['divisions']
            ent_name = get_enterprise_resp.json()['name']

        return ent_id, ent_name, divisions, loc_id, carrier_accounts, subs_role_ids

    def get_users_detail_with_sub_location(self, sub_id='', email='', admin_level='', ent_id=''):
        admin_level_at = ''
        admin_level_entity = ''

        get_subs_user_resp = self.get_user_by_search_query(skip='0', limit='5', archive='false',
                                                           query=email, sub_id=sub_id)
        user_id = get_subs_user_resp.json()['usersDetailWithSubLocation'][0]['detail']['id']
        location_id = get_subs_user_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['locationID']

        if admin_level != 'User':
            admin_level_at = get_subs_user_resp.json()['usersDetailWithSubLocation'][0]['detail']['adminLevelAt']
            admin_level_entity = get_subs_user_resp.json()['usersDetailWithSubLocation'][0]['detail']['adminLevelEntity']

        get_enterprise_resp = self.client_mgmt_api.get_enterprise_by_ent_id_api(ent_id[0])
        ent_name = get_enterprise_resp.json()['name']

        get_user_details_resp = self.get_user_subscription_details_by_user_id_api(user_id)
        subs_roles = get_user_details_resp.json()[0]['subscriptionRoles']

        return user_id, admin_level_at, admin_level_entity, location_id, ent_name, subs_roles

    def delete_created_subs_users(self, sub_id='', query='PyAuto'):
        get_subs_user_resp = self.get_user_by_search_query(limit='100', sub_id=sub_id, query=query)
        if len(get_subs_user_resp.json()['usersDetailWithSubLocation']) != 0:
            for i in range(len(get_subs_user_resp.json()['usersDetailWithSubLocation'])):
                user_id = get_subs_user_resp.json()['usersDetailWithSubLocation'][i]['subLocation']['userID']
                self.delete_user_api(user_id=user_id, sub_id=sub_id, is_admin='y')
                self.log.info(f'Archived user id: {user_id}')
        else:
            self.log.info(f'No user available with {query} in the subscription {sub_id}')

    def get_subs_roles_details(self, sub_id=''):
        role_id = []
        role_name = []
        features = []

        subs_roles_resp = self.get_subscription_roles_api(sub_id=sub_id)
        for i in range(len(subs_roles_resp.json())):
            role_id.append(subs_roles_resp.json()[i]['roleID'])
            role_name.append(subs_roles_resp.json()[i]['name'])
            features.append(subs_roles_resp.json()[i]['features'])

        return role_id, role_name, features

    def get_non_default_subs_roles_details(self, sub_id=''):
        role_id = []
        role_name = []
        features = []
        default_roles = {'ADMIN', 'USER'}

        subs_roles_resp = self.get_subscription_roles_api(sub_id=sub_id)
        for i in range(len(subs_roles_resp.json())):
            for k, v in subs_roles_resp.json()[i].items():
                if k == 'roleID' and v not in default_roles:
                    role_id.append(subs_roles_resp.json()[i]['roleID'])
                    role_name.append(subs_roles_resp.json()[i]['name'])
                    features.append(subs_roles_resp.json()[i]['features'])
                break
        return role_id, role_name, features

    def create_active_admin_user(self, admin_type=''):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f:
            self.sample_add_user_exp_resp = json.load(f)

        fname, lname, mailid, dispname, password = self.generate_user_profile_data()

        get_admin_roles_resp = self.prod_metadata_api.get_admin_roles_from_token_api()
        group_id = self.get_group_id(get_admin_roles_resp.json(), admin_type)

        add_user_resp = self.add_admin_user_api(fname, lname, mailid, dispname, group_id)
        assert_that(self.common.validate_response_template(add_user_resp, self.sample_add_user_exp_resp, 201))

        new_user = False
        for k, v in dict(add_user_resp.json()).items():
            if k == 'newUser':
                new_user = True
                break
        if not new_user:
            self.create_active_admin_user(admin_type=admin_type)

        user_id = add_user_resp.json()['userID']
        resp_token = add_user_resp.json()['token']

        self.login.user_account_claim(password, resp_token)
        self.login.check_user_login_status(username=mailid, password=password, admin=True)
        self.log.info(f'Email: {mailid}, UserId: {user_id}, AdminType: {admin_type}')

        return fname, lname, mailid, dispname, password, user_id, group_id

    def create_invited_admin_user(self, admin_type=None, group_id=None):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f:
            payload = json.load(f)

        fname, lname, mailid, dispname, password = self.generate_user_profile_data(is_admin=True)

        if not group_id:
            get_admin_roles_resp = self.prod_metadata_api.get_admin_roles_from_token_api()
            group_id = self.get_group_id(get_admin_roles_resp.json(), admin_type)

        add_user_resp = self.add_admin_user_api(fname, lname, mailid, dispname, group_id)
        assert_that(self.common.validate_response_template(add_user_resp, payload, 201))

        user_id = add_user_resp.json()['userID']
        self.log.info(f'Email: {mailid}, UserId: {user_id}, AdminType: {admin_type}')

        return fname, lname, mailid, dispname, password, user_id, group_id

    def delete_created_admin_users(self, query='PyAuto'):
        get_admin_user_resp = self.get_admin_user_by_search_query(limit='100', query=query)
        if len(get_admin_user_resp.json()['users']) != 0:
            for i in range(len(get_admin_user_resp.json()['users'])):
                user_id = get_admin_user_resp.json()['users'][i]['id']
                email = get_admin_user_resp.json()['users'][i]['profile']['email']
                self.delete_admin_user_api(user_id=user_id)
                self.log.info(f'Archived admin user - {email}, id: {user_id}')
        else:
            self.log.info(f'No admin user available with {query} !')

    def get_admin_user_details(self, user_id):
        response = self.get_admin_user_details_by_user_id_api(user_id=user_id)
        admin_level_at = response.json()['adminLevelAt']
        group_ids = response.json()['groupIds']

        return admin_level_at, group_ids

    def get_device_sn_integrator_id(self, sub_id=None, is_admin=False):
        get_devices_resp = self.get_devices_api(sub_id=sub_id, is_admin=is_admin)
        assert_that(self.common.validate_response_code(get_devices_resp, 200))
        devices = get_devices_resp.json()

        device = next((d for d in devices if d['deviceDetails']['deviceType'] == 'DVH'), None)
        if device:
            device_sn = device['deviceDetails']['deviceSerialNumber']
            integrator_id = device['deviceDetails']['integratorID']
            return device_sn, integrator_id
        else:
            self.log.error(f'No Device Hub product available for the subscription - {sub_id}')
            return None, None

    def retrieve_user_credentials_from_ent(self, sub_id=None, ent_id=None, user_type='E', is_admin=True, user_status='ACTIVE'):
        user_id = None
        email = None
        fname = None
        lname = None
        disp_name = None
        password = 'Horizon#123'

        users = self.users_advance_search_api(sub_id=sub_id, ent_id=ent_id, status=user_status, is_admin=is_admin)
        assert_that(self.common.validate_response_code(users, 200))

        users_data = users.json().get('usersDetailWithSubLocation')
        if users_data:
            for user in users_data:
                user_al = user['detail'].get('adminLevelAt')
                if user_type.lower() == 'user' or user_type == user_al:
                    if user['detail']['active'] and user['subLocation']['status'] == user_status:
                        user_id = user['detail']['id']
                        email = user['detail']['profile']['email']
                        fname = user['detail']['profile']['firstName']
                        lname = user['detail']['profile']['lastName']
                        disp_name = user['detail']['profile']['displayName']
                        break
        return user_id, email, password, fname, lname, disp_name

    def get_client_user_and_its_access_token_from_ent(self, sub_id=None, ent_id=None, user_type='E', is_admin=True):
        user_id, email, pwd, fname, lname, disp_name = self.retrieve_user_credentials_from_ent(sub_id=sub_id, ent_id=ent_id, user_type=user_type, is_admin=is_admin)
        client_access_token = self.login.get_access_token_for_user_credentials(username=email, password=pwd)
        return user_id, email, pwd, client_access_token

    def update_plans_in_subscription(self, is_admin=False, ent_id=None, sub_id=None, plans=None,
                                     admin_token='', client_token=''):

        # Retrieving the existing plan details of subscription
        get_subs_details_resp = self.get_subscription_by_ent_id_api(ent_id=ent_id, is_admin=is_admin,
                                                                    admin_token=admin_token, client_token=client_token)
        assert_that(self.common.validate_response_code(get_subs_details_resp, 200))
        initial_subs_plans = get_subs_details_resp.json()[0]['plans']
        okta_group_id = get_subs_details_resp.json()[0]['properties']['oktaGroupID']

        update_plans_resp = self.put_update_plans_in_subs_by_sub_id_api(is_admin=is_admin, sub_id=sub_id, ent_id=ent_id,
                                                                        okta_group_id=okta_group_id, plans=plans,
                                                                        admin_token=admin_token,
                                                                        client_token=client_token)
        assert_that(self.common.validate_response_code(update_plans_resp, 200))

        get_subs_details_after_update_resp = self.get_subscription_by_ent_id_api(ent_id=ent_id, is_admin=is_admin,
                                                                                 admin_token=admin_token,
                                                                                 client_token=client_token)
        assert_that(self.common.validate_response_code(get_subs_details_after_update_resp, 200))

        updated_subs_plans = get_subs_details_after_update_resp.json()[0]['plans']
        assert_that(updated_subs_plans, equal_to(plans))

    def get_sso_users_mappings_api(self, is_admin=False, sub_id=None, search_by='', page='0', limit='100', token=None):

        if is_admin:
            get_sso_users_mappings_search_url = f'{self.endpoint}/api/v1/federation/users/subscription/{sub_id}' \
                                                f'/mappings?skip={page}&limit={limit}&searchBy={search_by}'
            self.headers['Authorization'] = self.admin_token
        elif token:
            get_sso_users_mappings_search_url = f'{self.endpoint}/api/v1/federation/users/mappings' \
                                                f'?skip={page}&limit={limit}&searchBy={search_by}'
            self.headers['Authorization'] = token
        else:
            get_sso_users_mappings_search_url = f'{self.endpoint}/api/v1/federation/users/mappings' \
                                                f'?skip={page}&limit={limit}&searchBy={search_by}'
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_sso_users_mappings_search_url, headers=self.headers)
        return response

    def delete_sso_users_mappings_api(self, is_admin=False, token=None, sub_id=None, fed_user_mapping_id=None,
                                      uid=None, loc_id=None, loc_name=None, role_id=None, role_name=None,
                                      archived=True):

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'del_sso_user_mapping_req_payload')) as f:
            payload = json.load(f)

        if is_admin:
            del_sso_user_mapping_url = f'{self.endpoint}/api/v1/federation/users/mapping'
            self.headers['Authorization'] = self.admin_token
        elif token:
            del_sso_user_mapping_url = f'{self.endpoint}/api/v1/federation/users/mapping'
            self.headers['Authorization'] = token
        else:
            del_sso_user_mapping_url = f'{self.endpoint}/api/v1/federation/users/mapping'
            self.headers['Authorization'] = self.client_token

        if fed_user_mapping_id:
            payload['fedUserMappingID'] = fed_user_mapping_id
        if sub_id:
            payload['subID'] = sub_id
        if uid:
            payload['uid'] = uid
        if loc_id:
            payload['locationID'] = loc_id
        if loc_name:
            payload['locationName'] = loc_name
        if role_id:
            payload['roleID'] = role_id
        if role_name:
            payload['roleName'] = role_name
        if archived:
            payload['archived'] = archived

        response = self.api.post_api_response(endpoint=del_sso_user_mapping_url,
                                              headers=self.headers, body=json.dumps(payload))
        return response

    def create_sso_admin_users_mappings_api(self, admin_token=None, admin_lvl_at='E', admin_lvl_entity=None,
                                            group_id=None, analytics_rollup_by=None, rollup_entity=None,
                                            roles=None, user_id=None):
        if group_id is None or roles is None or user_id is None:
            return None

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'create_sso_admin_user_mapping_req_payload')) as f:
            payload = json.load(f)

        if admin_lvl_entity:
            payload['adminLevelEntity'] = admin_lvl_entity
        if group_id:
            payload['groupIds'] = group_id
        if roles:
            payload['roles'] = roles
        if user_id:
            payload['userID'] = user_id
        if admin_lvl_at == '':
            payload['adminLevelAt'] = 'E'
        if analytics_rollup_by:
            payload['analyticsRollupBy'] = analytics_rollup_by
        if rollup_entity:
            payload['rollupEntity'] = rollup_entity

        create_sso_admin_mapping_url = f"{self.endpoint}/api/v1/adminusermappings"
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.post_api_response(endpoint=create_sso_admin_mapping_url, headers=self.headers,
                                              body=json.dumps(payload))
        return response

    def get_federation_mapping_api(self, ent_name='', admin_token=None):

        query_param = f'?bu={ent_name}'
        get_fed_mapping_url = f'{self.endpoint}/api/v1/federationMapping{query_param}'
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.get_api_response(endpoint=get_fed_mapping_url, headers=self.headers)
        return response

    def get_idp_api(self, domain='', admin_token=None):

        query_param = f'?providerName={domain}'
        get_idp_url = f'{self.endpoint}/api/v1/idp{query_param}'
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.get_api_response(endpoint=get_idp_url, headers=self.headers)
        return response

    def put_update_idp_api(self, domain='', archived=False, enabled=True, admin_token=None):

        with open(self.prop.get('SSO_SETUP', 'saml_idp_data_req')) as f:
            req_data = json.load(f)

        def set_req_data_value(key, value):
            if value != '':
                req_data[key] = value

        set_req_data_value('providerName', domain)
        set_req_data_value('archived', archived)
        set_req_data_value('enabled', enabled)

        idp_url = f'{self.endpoint}/api/v1/idp/{domain}'
        self.headers = {
            'Content-Type': 'multipart/form-data',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': admin_token if admin_token else self.admin_token
        }

        payload = {
            'idpData': req_data
        }

        # payload = {
        #     'idpData': (None, req_data, 'text/plain')
        # }

        # in put_api_response the "files" are not available and this multipart/form-data request is failing, so using direct put request
        response = self.api.put_api_response(endpoint=idp_url, headers=self.headers, body=payload)
        #response = requests.put(url=idp_url, headers=self.headers, files=payload)
        return response

    def post_update_sync_federation_api(self, sub_id='', admin_token=None):

        with open(self.prop.get('SSO_SETUP', 'sync_federation_req')) as f:
            payload = json.load(f)

        sync_fed_url = f'{self.endpoint}/api/v1/syncFederation/{sub_id}'
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.post_api_response(endpoint=sync_fed_url, headers=self.headers, body=json.dumps(payload))
        return response

    def put_update_ccbs_sso_domain_api(self, name='', products=None, domains=None, primary_domain='', admin_token=None):

        with open(self.prop.get('SSO_SETUP', 'ccbs_sso_domain_req')) as f:
            req_data = json.load(f)

        def set_req_data_value(key, value):
            if value != '':
                req_data[key] = value

        set_req_data_value('name', name)
        set_req_data_value('domains', domains)  # domain should be in list
        set_req_data_value('idp', primary_domain)
        if products:
            set_req_data_value('products', products)  # products should be in list

        domain_url = f'{self.endpoint}/api/v1/domain/{name}'
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.put_api_response(endpoint=domain_url, headers=self.headers, body=json.dumps(req_data))
        return response

    def post_update_federation_mapping_api(self, fed_id='', sub_id='', ent_name='', domain='', archived=False,
                                           jit_update=False, admin_token=None):

        with open(self.prop.get('SSO_SETUP', 'federation_mapping_req')) as f:
            req_data = json.load(f)

        def set_req_data_value(key, value):
            if value != '':
                req_data[key] = value

        set_req_data_value('fedMappingID', fed_id)
        set_req_data_value('subID', sub_id)
        set_req_data_value('businessUnit', ent_name)
        set_req_data_value('identityProviderName', domain)
        set_req_data_value('archived', archived)
        set_req_data_value('allowUpdate', jit_update)

        fed_mapping_url = f'{self.endpoint}/api/v1/federationMapping'
        self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        response = self.api.post_api_response(endpoint=fed_mapping_url, headers=self.headers, body=json.dumps(req_data))
        return response

    def update_sso_domain_setup(self, sub_id='', domain='', domains=None, name='', products=None, archived=False,
                                enabled=True, fed_id='', ent_name='', jit_update=False, admin_token=None):

        update_idp_resp = self.put_update_idp_api(domain=domain, archived=archived, enabled=enabled,
                                                  admin_token=admin_token)
        assert_that(common_utils.validate_response_code(update_idp_resp, 200))

        update_sync_fed_resp = self.post_update_sync_federation_api(sub_id=sub_id, admin_token=admin_token)
        assert_that(common_utils.validate_response_code(update_sync_fed_resp, 200))

        update_ccbs_domain_resp = self.put_update_ccbs_sso_domain_api(name=name, products=products, domains=domains,
                                                                      primary_domain=domain, admin_token=admin_token)
        assert_that(common_utils.validate_response_code(update_ccbs_domain_resp, 200))

        update_fed_mapping_resp = self.post_update_federation_mapping_api(fed_id=fed_id, sub_id=sub_id,
                                                                          ent_name=ent_name, domain=domain,
                                                                          archived=archived, jit_update=jit_update,
                                                                          admin_token=admin_token)
        assert_that(common_utils.validate_response_code(update_fed_mapping_resp, 201))

    def get_sso_user_details_from_sample_file(self, protocol='saml', user_key=''):

        if user_key is None:
            return None

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_sso_users_details')) as file:
            json_data = json.load(file)

        data = json_data[self.prod_name][self.env][protocol]
        sub_id = data['sub_id']
        ent_id = data['ent_id']
        ent_name = data['ent_name']
        domain = data['domain']

        email_pwd_map = {
            "po": (data['po_user'], data['po_pwd'], data['po_user_okta_id']),
            "user1": (data['sso_user1'], data['sso_user1_pwd'], data['sso_user1_okta_id']),
            "user2": (data['sso_user2'], data['sso_user2_pwd'], data['sso_user2_okta_id']),
            "user3": (data['sso_user3'], data['sso_user3_pwd'], data['sso_user3_okta_id']),
            "user4": (data['sso_user4'], data['sso_user4_pwd'], data['sso_user4_okta_id']) if protocol == 'saml' else (None, None)
        }

        email, pwd, okta_id = email_pwd_map.get(user_key, (None, None))

        return sub_id, ent_id, ent_name, domain, email, pwd, okta_id

    def get_all_subs_roles_using_sub_id(self, sub_id=None):
        role_data = []
        roles_resp = self.get_subscription_roles_api(sub_id=sub_id)
        assert_that(common_utils.validate_response_code(roles_resp, 200))
        roles = roles_resp.json()
        # for role in roles:
        #     role_data.append({'role_id': role['roleID'], 'role_name': role['name']})

        for role in roles:
            role_entry = {
                'role_id': role['roleID'],
                'role_name': role['name'],
                'access_level': role.get('accessLevel', 'N/A')  # Default to 'N/A' if accessLevel is missing or None
            }
            role_data.append(role_entry)

        return role_data

    def pick_random_role_id_name(self, role_data=None, excluded_role_ids=None):

        # Filter role_data to exclude specific role_id and role_name
        filtered_role_data = [role for role in role_data if role['role_id'] not in excluded_role_ids]

        if filtered_role_data:
            # Pick a random role from the filtered list
            random_role = random.choice(filtered_role_data)
            return random_role['role_id'], random_role['role_name']
        else:
            return None, None

    def pick_random_role_id_name_with_access_level(self, role_data=None, excluded_role_ids=None, access_lvl=None):

        if excluded_role_ids is None:
            excluded_role_ids = []

        def access_level_filter(role):
            if access_lvl == 'User':
                return role.get('access_level') in (access_lvl, 'N/A')
            else:
                return role.get('access_level') == access_lvl

            # Filter role_data to exclude specific role_id and role_name, and match the specified access level

        filtered_role_data = [role for role in role_data if
                              role['role_id'] not in excluded_role_ids and access_level_filter(role)]

        if filtered_role_data:
            # Pick a random role from the filtered list
            random_role = random.choice(filtered_role_data)
            return random_role['role_id'], random_role['role_name'], random_role['access_level']
        else:
            return None, None, None

    def update_admin_access_level_for_user(self, sub_id=None, ent_id=None, ent_name=None, email=None, admin_lvl=None,
                                           admin_lvl_entity=None, default_cost_acct=None, is_admin=True,
                                           admin_token=None, client_token=None):

        (user_data, loc_id, role_id, user_cost_acct_id, uid, fname, lname, username, user_access_lvl,
         user_admin_entities) = (self.get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email,
                                                                    is_admin=is_admin))

        self.log.info(f'Loc ID: {loc_id}, Role ID: {role_id}, Cost Account ID: {user_cost_acct_id}, UID: {uid}, '
                      f'First Name: {fname}, Last Name: {lname}, Username: {username}')

        existing_adm_lvl = user_data.get('detail').get('adminLevelAt')
        existing_adm_lvl_entity = user_data.get('detail').get('adminLevelEntity')
        dispname = user_data['detail']['profile']['displayName']

        # send the updated admin_level and admin_level_entity
        self.log.info(f'Existing admin access level is {existing_adm_lvl} and {existing_adm_lvl_entity}')

        update_user_details_resp = self.put_update_subs_user_details_with_user_type_by_user_id_api(
            user_id=uid, adm_lvl=admin_lvl, adm_lvl_entity=admin_lvl_entity, ent_name=ent_name, roles=role_id,
            fname=fname, lname=lname, dispname=dispname, email=email, sub_id=sub_id,
            default_cost_acct=default_cost_acct, is_admin=is_admin, admin_token=admin_token, client_token=client_token)
        assert_that(common_utils.validate_response_code(update_user_details_resp, 200))

        return update_user_details_resp

    def update_user_admin_access_level_to_division(self, no_of_req_div=2, ent_id=None, ent_name=None, sub_id=None,
                                                   email=None, exclude_divs=None):
        selected_divs, selected_loc = (
            self.client_mgmt_api.get_multiple_divs_and_loc_in_ent(ent_id=ent_id, no_of_req_div=no_of_req_div,
                                                                  exclude_divs=exclude_divs))
        self.log.info(f'Selected Divs: {selected_divs}, selected loc: {selected_loc}')
        self.update_admin_access_level_for_user(sub_id=sub_id, ent_id=ent_id, email=email, admin_lvl='D',
                                                admin_lvl_entity=selected_divs, ent_name=ent_name, is_admin=True)
        get_loc_by_id_res = self.client_mgmt_api.get_loc_by_id_api(loc_id=selected_loc)
        assert_that(common_utils.validate_response_code(get_loc_by_id_res, 200))

        selected_loc_id = get_loc_by_id_res.json()['locationID']
        selected_loc_name = get_loc_by_id_res.json()['name']

        return selected_divs, selected_loc_id, selected_loc_name
