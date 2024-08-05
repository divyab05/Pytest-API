"""This module is used for main page objects."""

import logging
import json
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


class Custom_fields:
    """This class defines the method and element identifications for main page."""

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
        self.endpoint = str(self.app_config.env_cfg['custom_field_endpoint'])
        self.headers = {"Accept": "*/*"}
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def retrieve_user_credentials(self):
        with open(self.prop.get('CUSTOM_FIELDS', 'sample_subscription_ids_and_email_file')) as f:
            data = json.load(f)

        admin_user = data[self.prod_name][self.env]['admin_email_id']
        admin_pwd = data[self.prod_name][self.env]['admin_password']
        client_user = data[self.prod_name][self.env]['client_email_id']
        client_pwd = data[self.prod_name][self.env]['client_password']
        sub_id = data[self.prod_name][self.env]['subid']

        return admin_user, admin_pwd, client_user, client_pwd, sub_id

    def get_custom_field_required_details(self, resource=None, admin_level=None, sub_id=None, user_emailID=None):

        name = 'Auto_' + generate_random_string(char_count=5)
        asignpageform = ["NOTIFICATIONS", "CONTACTS_ADDRESS_BOOK"]

        sub_id = sub_id
        user_emailID = user_emailID

        cf_list_values = ["mon", "tue", "wed"]

        ent_id, ent_name, division_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].get_ent_div_loc_carrier_subs_details_from_sub_id(sub_id=sub_id)

        user_id, admin_level_at, admin_level_entity, location_id, ent_name, subs_roles = \
            resource['subscription_api'].get_users_detail_with_sub_location(sub_id=sub_id,
                                                                            email=user_emailID,
                                                                            admin_level=admin_level, ent_id=ent_id)
        new_loction_id = resource['subscription_api'].retrieve_new_location_from_enterprise(ent_id=ent_id,
                                                                                            sub_id=sub_id)

        if location_id != new_loction_id:
            location_id_list = [location_id, new_loction_id]
        else:
            location_id_list = [new_loction_id]

        type = 'site'
        site_name1 = 'Autosite_' + generate_random_string(char_count=5)
        site_name2 = 'Autosite_' + generate_random_string(char_count=5)

        site_on_def_loc, status_code = resource['client_mgmt']. \
            verify_add_site_with_location_api(is_admin='Y', sub_id=sub_id,
                                              name=site_name1,
                                              type=type, location_id=location_id)
        siteid_on_def_loc = site_on_def_loc['inboundSiteID']
        site_noton_def_loc, status_code = resource['client_mgmt']. \
            verify_add_site_with_location_api(is_admin='Y', sub_id=sub_id,
                                              name=site_name2,
                                              type=type, location_id=new_loction_id)
        siteid_noton_def_loc = site_noton_def_loc['inboundSiteID']
        site_list = [siteid_on_def_loc, siteid_noton_def_loc]

        return name, asignpageform, sub_id, ent_id, division_id, [loc_id], \
               user_emailID, [location_id], location_id_list, [siteid_on_def_loc], site_list, cf_list_values

    def get_custom_field_api(self, is_admin=False, config_id=None, query=None, noskip=False, limit='300',
                             status='ACTIVE',
                             sub_id=None, token=None):

        query_params = '?skip={arg1}&limit={arg2}&searchBy=status:{arg3}&query={arg4}' \
            .format(arg1=noskip, arg2=limit, arg3=status, arg4=query)

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields' + config_id
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields' + query_params
        else:
            self.headers['Authorization'] = token if token else self.client_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customfields/' + config_id
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customfields/' + query_params

        response = self.api.get_api_response(get_custom_field_endpoint, self.headers)

        return response

    def add_custom_field_api(self, is_admin=False, sub_id=None, admin_level=None, name=None, ent_id=None,
                             ent_name=None, div_id=None, loc_id=None, asignPageForm=None, site=None,
                             token=None, cf_list_values=None, cf_type="TEXT"):

        permissionByValue = None
        assignPageForm = asignPageForm

        if admin_level == 'E':
            permissionByValue = ent_id

        elif admin_level == 'L':
            permissionByValue = loc_id

        elif admin_level == 'D':
            permissionByValue = div_id
        elif admin_level == 'S':
            permissionByValue = site

        with open(self.prop.get('CUSTOM_FIELDS', 'add_new_custom_field')) as f1:
            self.json_data = json.load(f1)

        self.json_data['name'] = name
        self.json_data['permission']['permissionByEntity'] = admin_level
        self.json_data['permission']['permissionByValue'] = permissionByValue
        self.json_data['assignPageForm'] = assignPageForm
        self.json_data['values'] = cf_list_values
        self.json_data['customFieldType'] = cf_type

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            add_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields'
        else:
            self.headers['Authorization'] = token if token else self.client_token
            add_custom_field_endpoint = self.endpoint + '/api/v1/customfields'

        response = self.api.post_api_response(endpoint=add_custom_field_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_custom_field_api(self, is_admin=False, sub_id=None, admin_level=None, name=None, ent_id=None,
                                    ent_name=None, div_id=None, loc_id=None, config_id=None, asignPageForm=None,
                                    status='ACTIVE', site=None, token=None, cf_type=None, cf_list_values=None):

        permissionByValue = ''
        asignform = asignPageForm

        if admin_level == 'E':
            permissionByValue = ent_id
        elif admin_level == 'L':
            permissionByValue = loc_id
        elif admin_level == 'D':
            permissionByValue = div_id
        elif admin_level == 'S':
            permissionByValue = site

        # where to add the file name
        with open(self.prop.get('CUSTOM_FIELDS', 'add_new_custom_field')) as f1:
            self.json_data = json.load(f1)

        self.json_data['name'] = name
        self.json_data['permission']['permissionByEntity'] = admin_level
        self.json_data['permission']['permissionByValue'] = permissionByValue
        self.json_data['assignPageForm'] = asignform
        self.json_data['status'] = status
        self.json_data['customFieldType'] = cf_type
        self.json_data['values'] = cf_list_values


        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            update_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields/' + str(
                config_id)
        else:
            self.headers['Authorization'] = token if token else self.client_token
            update_custom_field_endpoint = self.endpoint + '/api/v1/customfields/' + str(config_id)

        response = self.api.put_api_response(endpoint=update_custom_field_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))

        return response

    def delete_custom_field_api(self, is_admin=False, sub_id=None, config_id=None, token=None):

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            del_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields/' + config_id
        else:
            self.headers['Authorization'] = token if token else self.client_token
            del_custom_field_endpoint = self.endpoint + "/api/v1/customfields/" + config_id

        response = self.api.delete_api_response(endpoint=del_custom_field_endpoint, headers=self.headers)
        return response

    def get_used_custom_field_api(self, is_admin=False, config_id=None, query=None, noskip=False, limit='1000',
                                  status='ACTIVE', token=None, sub_id=None, asignPageForm=None):

        query_params = '?skip={arg1}&limit={arg2}&searchBy=customFieldID:{arg3},assignPageForm:{arg4},status:{arg5}' \
            .format(arg1=0, arg2=limit, arg3=config_id, arg4=asignPageForm, arg5=status)

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields' + config_id
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customfields' + query_params
        else:
            self.headers['Authorization'] = token if token else self.client_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v2/useCustomfields/?searchBy=customFieldID:' + config_id
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v2/useCustomfields/' + query_params

        response = self.api.get_api_response(get_custom_field_endpoint, self.headers)

        return response

    def get_custom_field_in_address_book(self, is_admin=False, config_id=None, query=None, noskip=False, limit='1000',
                                         status='ACTIVE', token=None, sub_id=None, contact_id=None, cf_value=None,
                                         customResourceValueID=None):

        query_params = '?skip={arg1}&limit={arg2}&searchBy=customFieldID:{arg3},customResourceValueID:{arg4}' \
            .format(arg1=0, arg2=limit, arg3=config_id, arg4=customResourceValueID)

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource/' + query_params
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource/' + query_params
        else:
            self.headers['Authorization'] = token if token else self.client_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource/' + query_params
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource/' + query_params

        response = self.api.get_api_response(get_custom_field_endpoint, self.headers)

        return response

    def add_custom_field_in_address_book(self, is_admin=False, config_id=None, query=None, noskip=False, limit='1000',
                                         status='ACTIVE', token=None, sub_id=None, contact_id=None, cf_value=None,
                                         customResourceValueID=None):

        with open(self.prop.get('CUSTOM_FIELDS', 'json_to_add_custom_field_in_contact')) as f:
            self.json_data = json.load(f)

        self.json_data['resourceID'] = contact_id
        self.json_data['customFieldID'] = config_id
        self.json_data['customFieldValueName'] = cf_value

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource/' + customResourceValueID
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource'
        else:
            self.headers['Authorization'] = token if token else self.client_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource/' + customResourceValueID
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource'

        response = self.api.post_api_response(endpoint=get_custom_field_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))

        return response

    def update_custom_field_in_address_book(self, is_admin=False, config_id=None, query=None, noskip=False,
                                            limit='1000',
                                            status='ACTIVE', token=None, sub_id=None, contact_id=None, cf_value=None,
                                            customResourceValueID=None):

        with open(self.prop.get('CUSTOM_FIELDS', 'json_to_add_custom_field_in_contact')) as f:
            self.json_data = json.load(f)

        self.json_data['resourceID'] = contact_id
        self.json_data['customFieldID'] = config_id
        self.json_data['customFieldValueName'] = cf_value

        if is_admin:
            self.headers['Authorization'] = token if token else self.admin_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource/' + customResourceValueID
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/subscriptions/' + sub_id + '/customResource/' + customResourceValueID
        else:
            self.headers['Authorization'] = token if token else self.client_token
            if noskip:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource/' + customResourceValueID
            else:
                get_custom_field_endpoint = self.endpoint + '/api/v1/customResource/' + customResourceValueID

        response = self.api.put_api_response(endpoint=get_custom_field_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))

        return response
