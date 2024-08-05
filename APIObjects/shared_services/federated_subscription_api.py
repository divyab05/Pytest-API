"""This module is used for main page objects."""

from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
import json
import logging


class FederatedSubscriptionAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.login = LoginAPI(app_config)
        self.subs_mgmt_api = SubscriptionAPI(app_config, access_token, client_token)
        self.client_mgmt_api = ClientManagementAPI(app_config, access_token, client_token)
        self.prod_metadata_api = ProductMetadata(app_config, access_token, client_token)
        self.prop = self.config.load_properties_file()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.submgmt_endpoint = str(self.app_config.env_cfg['submgmt_api'])
        self.sso_endpoint = str(self.app_config.env_cfg['sso_url']) + '/api/v1/users/'
        self.headers = {"Accept": "*/*"}
        self.sso_header = {"Authorization": "SSWS 00kk7rPctv0skxLe9UJEf1jmGw-Cr6AADp6rZhTVZN"}
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    @staticmethod
    def generate_federated_user_profile_data(email=''):
        fname = "Federated"
        lname = "AutoUser"
        dispname = str(fname + " " + lname)
        if not email:
            email = 'spauser6-fed@mailinator.com'
        password = "Group!234"

        return fname, lname, email, dispname, password

    def get_subs_id_from_file(self, sub_type=''):
        with open(self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'sample_federated_subs_ids')) as file:
            self.json_data = json.load(file)

        sub_id = self.json_data[self.env][sub_type]
        return sub_id

    def get_federated_user_profile_from_file(self, subs_type='single-subs', n=0):
        """
        This method fetches the test SSO/Federated user details from the sample JSON file.

        :param subs_type: The SSO subscription type.
                          "single-subs" means a unique SSO Client IDP/Domain is configured only in a single subscription.
                          "multi-subs" means a same SSO Client IDP/Domain is configured in multiple subscriptions.
        :param n: The index to fetch the nth user profile from the sample JSON file.

        :return: The SSO/federated user profile details.
        """

        with open(self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'sample_federated_user_profile')) as file:
            self.json_data = json.load(file)

        try:
            user = self.json_data[self.env][subs_type][n]

            fname = user['firstName']
            lname = user['lastName']
            dispname = user['displayName']
            sec_id = user['sec_id']
            login_id = user['login']
            email = user['email']
            password = user['password']
            ent_name = user['ent_name']
            sub_id = user['sub_id']
            domain = user['domain']

        except (KeyError, IndexError) as e:
            raise ValueError(f"Invalid subs_type or user index: {e}")

        return fname, lname, email, dispname, sec_id, login_id, password, ent_name, sub_id, domain

    def add_federated_user_by_sub_id_login_id_api(self, fname='', lname='', email='', disp_name='', sub_id='',
                                                  ent_name='', loc_id='', login_id='', admin_lvl='', admn_lvl_entity=None,
                                                  subs_roles=None, default_cost_acct=None, token=None):

        with open(self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'add_federated_user_request_body')) as f:
            self.json_data = json.load(f)

        user_profile_fields = ['login', 'firstName', 'lastName', 'displayName', 'email']
        values = [login_id, fname, lname, disp_name, email]

        for field, value in zip(user_profile_fields, values):
            self.json_data[field] = value
            self.json_data['userProfile'][field] = value
            self.json_data['profile'][field] = value

        self.json_data.update({
            'locationID': loc_id,
            'subID': sub_id,
            'enterpriseName': ent_name
        })

        if default_cost_acct is not None:
            self.json_data['defaultCostAccount'] = default_cost_acct

        if admin_lvl != 'User':
            self.json_data.update({
                'adminLevelAt': admin_lvl,
                'adminLevelEntity': admn_lvl_entity,
                'subscriptionRoles': subs_roles
            })
        else:
            self.json_data['subscriptionRoles'] = ['User']
            self.json_data.pop('adminLevelAt', None)
            self.json_data.pop('adminLevelEntity', None)

        add_user_email_endpoint = f'{self.submgmt_endpoint}/api/v1/subscriptions/{sub_id}/federatedusers'
        self.headers['Authorization'] = token if token else self.admin_token

        response = self.api.post_api_response(add_user_email_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def add_ta_user_by_sub_id_api(self, fname='', lname='', email='', disp_name='', sub_id='', loc_id='', admin_lvl='',
                                  admn_lvl_entity=None, subs_roles=None, default_cost_acct=None, is_admin=True, token=None):

        with open(self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'add_ta_user_request_body')) as f:
            self.json_data = json.load(f)

        self.json_data['userProfile']['firstName'] = fname
        self.json_data['userProfile']['lastName'] = lname
        self.json_data['userProfile']['displayName'] = disp_name
        self.json_data['userProfile']['email'] = email
        self.json_data['userProfile']['login'] = email

        self.json_data['locationID'] = loc_id
        self.json_data['subID'] = sub_id

        if default_cost_acct is not None:
            self.json_data['defaultCostAccount'] = default_cost_acct

        if admin_lvl != 'User':
            self.json_data.update({
                'adminLevelAt': admin_lvl,
                'adminLevelEntity': admn_lvl_entity,
                'subscriptionRoles': subs_roles
            })
        else:
            self.json_data['subscriptionRoles'] = ['User']
            self.json_data.pop('adminLevelAt', None)
            self.json_data.pop('adminLevelEntity', None)

        if is_admin:
            add_user_email_endpoint = f'{self.submgmt_endpoint}/api/v1/subscriptions/{sub_id}/addTAUser'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            add_user_email_endpoint = f'{self.submgmt_endpoint}/api/v1/addTAUser'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.post_api_response(add_user_email_endpoint, self.headers, json.dumps(self.json_data))
        return response

    def get_subs_details_by_sub_id_api(self, sub_id=''):

        get_subs_details_endpoint = self.submgmt_endpoint + "/api/v1/subscriptions/" + sub_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_subs_details_endpoint, headers=self.headers)
        return response

    def put_update_federation_enabled_in_subs(self, sub_id='', country_code='', okta_group_id='',
                                              federated_user=False):
        with open(
                self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'put_update_federation_enabled_in_subs_request_body')) as f:
            self.json_data = json.load(f)

        self.json_data['subID'] = sub_id
        self.json_data['countryCode'] = country_code
        self.json_data['properties']['oktaGroupID'] = okta_group_id
        self.json_data['oktaGroupID'] = okta_group_id
        self.json_data['properties']['federatedUser'] = federated_user

        update_subs_endpoint = self.submgmt_endpoint + '/api/v1/subscriptions/' + sub_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(endpoint=update_subs_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_update_ta_device_support_in_subs(self, sub_id='', country_code='', okta_group_id='',
                                              ta_device_support=False):
        with open(
                self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'put_update_ta_device_support_in_subs_request_body')) as f:
            self.json_data = json.load(f)

        self.json_data['subID'] = sub_id
        self.json_data['countryCode'] = country_code
        self.json_data['properties']['oktaGroupID'] = okta_group_id
        self.json_data['oktaGroupID'] = okta_group_id
        self.json_data['federationEnabled'] = ta_device_support

        update_subs_endpoint = self.submgmt_endpoint + '/api/v1/subscriptions/' + sub_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.put_api_response(endpoint=update_subs_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def get_user_details_by_user_id_api(self, user_id=''):

        get_user_details_endpoint = self.submgmt_endpoint + '/api/v1/users/' + user_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_user_details_endpoint, headers=self.headers)
        return response

    def get_user_subscription_details_by_user_id_api(self, user_id=''):

        get_user_details_endpoint = self.submgmt_endpoint + '/api/v1/users/' + user_id + '/subscriptions'
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_user_details_endpoint, headers=self.headers)
        return response

    def get_federated_user_sec_id_login_id(self, user_id=''):
        user_resp = self.get_user_details_by_user_id_api(user_id=user_id)
        sec_id = user_resp.json()['profile']['login']  # Ex: 0000034405@0oascjusmn8xmHTbI0h7.idp
        login_id = sec_id.split('@')[0]
        return sec_id, login_id

    def get_user_profile_from_sso_api(self, sec_id=''):

        get_user_profile_endpoint = self.sso_endpoint + sec_id

        response = self.api.get_api_response(endpoint=get_user_profile_endpoint, headers=self.sso_header)
        return response

    def post_deactivate_federated_user_api(self, sec_id=''):

        deactivate_endpoint = self.sso_endpoint + sec_id + '/lifecycle/deactivate'

        response = self.api.post_api_response(endpoint=deactivate_endpoint, headers=self.sso_header)
        return response

    def delete_deactivated_federated_user_api(self, sec_id=''):

        delete_endpoint = self.sso_endpoint + sec_id

        response = self.api.delete_api_response(endpoint=delete_endpoint, headers=self.sso_header)
        return response

    def post_deactivate_ta_user_api(self, email=''):

        deactivate_endpoint = self.sso_endpoint + email + '/lifecycle/deactivate'

        response = self.api.post_api_response(endpoint=deactivate_endpoint, headers=self.sso_header)
        return response

    def delete_deactivated_ta_user_api(self, email=''):

        delete_endpoint = self.sso_endpoint + email

        response = self.api.delete_api_response(endpoint=delete_endpoint, headers=self.sso_header)
        return response

    def delete_federated_user(self, sec_id=''):
        self.post_deactivate_federated_user_api(sec_id=sec_id)
        self.delete_deactivated_federated_user_api(sec_id=sec_id)

    def delete_federated_and_ta_user(self, sec_id='', email=''):
        self.post_deactivate_federated_user_api(sec_id=sec_id)
        self.delete_deactivated_federated_user_api(sec_id=sec_id)

        self.post_deactivate_ta_user_api(email=email)
        self.delete_deactivated_ta_user_api(email=email)

    def get_federated_subscription_user_details(self, sub_id):
        ent_id = []
        loc_id = ''
        carrier_accounts = []
        subs_role_ids = []

        get_subs_details = self.get_subs_details_by_sub_id_api(sub_id)
        country_code = get_subs_details.json()['countryCode']
        okta_group_id = get_subs_details.json()['properties']['oktaGroupID']

        if not get_subs_details.json()['properties']['federatedUser']:
            self.put_update_federation_enabled_in_subs(sub_id=sub_id, country_code=country_code,
                                                       okta_group_id=okta_group_id, federated_user=True)

        for k, v in dict(get_subs_details.json()).items():
            if k == 'enterpriseID':
                ent_id = [str(v)]
            if k == 'locations':
                loc_id = str(v[0])
            if k == 'carriers':
                carrier_accounts = v
            if k == 'subscriptionRoles':
                subs_roles = v
                for i in range(len(subs_roles)):
                    subs_role_ids.append(subs_roles[i]['roleID'])
        if loc_id == '':
            loc_id = self.subs_mgmt_api.retrieve_new_location_from_enterprise(ent_id=ent_id, sub_id=sub_id)
        return ent_id, loc_id, carrier_accounts, subs_role_ids
