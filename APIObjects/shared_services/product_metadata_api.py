import json
import logging
import random
from collections import OrderedDict

from hamcrest import assert_that, equal_to

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_string


class ProductMetadata:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['prodmgmt_api'])
        self.headers = {
            "Authorization": "Bearer {}".format(self.access_token)
        }
        # self.log = log_utils.custom_logger(logging.INFO)

        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def get_product_details_from_token_api(self, token=''):

        get_product_endpoint = self.endpoint + '/api/v1/products'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_product_endpoint, self.headers)
        return response

    def get_product_count_from_token_api(self, token=''):

        get_product_endpoint = self.endpoint + '/api/v1/products/count'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_product_endpoint, self.headers)
        return response

    def get_product_details_by_prod_id_api(self, prod_id=''):

        get_product_endpoint = self.endpoint + '/api/v1/products/' + prod_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_product_endpoint, self.headers)
        return response

    def post_create_product_api(self, prod_id='', name=''):

        with open(self.prop.get('PROD_METADATA', 'create_product_req_body')) as create_prod:
            self.json_data = json.load(create_prod)

        self.json_data['productID'] = prod_id
        self.json_data['name'] = name

        create_prod_endpoint = self.endpoint + '/api/v1/products'

        response = self.api.post_api_response(endpoint=create_prod_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_product_by_prod_id_api(self, prod_id='', name=''):

        with open(self.prop.get('PROD_METADATA', 'create_product_req_body')) as update_prod:
            self.json_data = json.load(update_prod)

        self.json_data['productID'] = prod_id
        self.json_data['name'] = name

        update_product_endpoint = self.endpoint + "/api/v1/products/" + prod_id

        response = self.api.put_api_response(endpoint=update_product_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_product_by_prod_id_api(self, prod_id=''):

        archive_product_endpoint = self.endpoint + "/api/v1/products/" + prod_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_product_endpoint, headers=self.headers)
        return response

    def del_product_by_prod_id_api(self, prod_id=''):

        del_product_endpoint = self.endpoint + "/api/v1/products/" + prod_id

        response = self.api.delete_api_response(endpoint=del_product_endpoint, headers=self.headers)
        return response

    def check_and_delete_product_by_prod_id(self, prod_id=''):
        get_prod_details_resp = self.get_product_details_by_prod_id_api(prod_id=prod_id)
        if get_prod_details_resp.status_code == 200:
            if get_prod_details_resp.json()['productID'] == prod_id:
                self.del_product_by_prod_id_api(prod_id=prod_id)

    def get_carriers_from_token_api(self, token=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        get_carriers_endpoint = self.endpoint + '/api/v1/carriers'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_carriers_endpoint, self.headers)
        return response

    def get_carriers_count_from_token_api(self, token=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        get_carriers_endpoint = self.endpoint + '/api/v1/carriers/count'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_carriers_endpoint, self.headers)
        return response

    def get_carrier_details_by_carrier_id_api(self, carrier_id=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        get_carrier_endpoint = self.endpoint + '/api/v1/carriers/' + carrier_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_carrier_endpoint, self.headers)
        return response

    def post_create_carrier_api(self, carrier_id='', name='', country='US', prepay=False):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
            API: https://config-service-dev.sendpro360.pitneycloud.com/api/v1/carriers
        """

        with open(self.prop.get('PROD_METADATA', 'create_carrier_req_body')) as create_carrier:
            self.json_data = json.load(create_carrier)

        self.json_data['carrierID'] = carrier_id
        self.json_data['name'] = name
        self.json_data['originCountry'] = country
        self.json_data['properties']['prePay'] = prepay

        create_carrier_endpoint = self.endpoint + '/api/v1/carriers'

        response = self.api.post_api_response(endpoint=create_carrier_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_carrier_by_carrier_id_api(self, carrier_id='', name='', country='US', prepay=False):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        with open(self.prop.get('PROD_METADATA', 'create_carrier_req_body')) as update_carrier:
            self.json_data = json.load(update_carrier)

        self.json_data['carrierID'] = carrier_id
        self.json_data['name'] = name
        self.json_data['originCountry'] = country
        self.json_data['properties']['prePay'] = prepay

        update_carrier_endpoint = self.endpoint + '/api/v1/carriers/' + carrier_id

        response = self.api.put_api_response(endpoint=update_carrier_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_carrier_by_carrier_id_api(self, carrier_id=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        archive_carrier_endpoint = self.endpoint + "/api/v1/carriers/" + carrier_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_carrier_endpoint, headers=self.headers)
        return response

    def del_carrier_by_carrier_id_api(self, carrier_id=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """

        del_carrier_endpoint = self.endpoint + "/api/v1/carriers/" + carrier_id

        response = self.api.delete_api_response(endpoint=del_carrier_endpoint, headers=self.headers)
        return response

    def check_and_delete_carrier_by_carrier_id(self, carrier_id=''):
        """
            Comment Date: 18-Jan-2024
            This API has been removed from product-metadata and the create carrier API is now
            available in the config-service. Onkar Sutar has confirmed this and reference
            ticket - https://pbapps.atlassian.net/browse/PE-4040
        """
        get_carrier_details_resp = self.get_carrier_details_by_carrier_id_api(carrier_id=carrier_id)
        if get_carrier_details_resp.status_code == 200:
            if get_carrier_details_resp.json()['carrierID'] == carrier_id:
                self.del_carrier_by_carrier_id_api(carrier_id=carrier_id)

    def get_country_codes_api(self, supported='true'):

        query_param = '?supported=' + supported

        country_codes_endpoint = self.endpoint + "/api/v1/countryCodes" + query_param

        response = self.api.get_api_response(endpoint=country_codes_endpoint, headers=self.headers)
        return response

    def get_features_from_token_api(self, token=''):

        get_features_endpoint = self.endpoint + '/api/v1/features'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_features_endpoint, self.headers)
        return response

    def get_features_count_from_token_api(self, token=''):

        get_features_endpoint = self.endpoint + '/api/v1/features/count'
        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(get_features_endpoint, self.headers)
        return response

    def get_feature_details_by_ft_id_api(self, ft_id=''):

        get_feature_endpoint = self.endpoint + '/api/v1/features/' + ft_id
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(get_feature_endpoint, self.headers)
        return response

    def post_create_feature_api(self, ft_id='', name='', funct_tag='', resource_value='',
                                operations=None, supported_countries=None):

        with open(self.prop.get('PROD_METADATA', 'create_feature_req_body')) as create_feature:
            self.json_data = json.load(create_feature)

        self.json_data['featureID'] = ft_id
        self.json_data['name'] = name
        self.json_data['functionalityTag'] = funct_tag
        self.json_data['resource'] = resource_value
        self.json_data['operations'] = operations
        self.json_data['supportedCountries'] = supported_countries

        create_feature_endpoint = self.endpoint + '/api/v1/features'

        response = self.api.post_api_response(endpoint=create_feature_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_feature_by_ft_id_api(self, ft_id='', name='', funct_tag='', resource_value='',
                                        operations=None, supported_countries=None):

        with open(self.prop.get('PROD_METADATA', 'create_feature_req_body')) as update_feature:
            self.json_data = json.load(update_feature)

        self.json_data['featureID'] = ft_id
        self.json_data['name'] = name
        self.json_data['functionalityTag'] = funct_tag
        self.json_data['resource'] = resource_value
        self.json_data['operations'] = operations
        self.json_data['supportedCountries'] = supported_countries

        update_feature_endpoint = self.endpoint + '/api/v1/features/' + ft_id

        response = self.api.put_api_response(endpoint=update_feature_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_feature_by_ft_id_api(self, ft_id=''):

        archive_feature_endpoint = self.endpoint + "/api/v1/features/" + ft_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_feature_endpoint, headers=self.headers)
        return response

    def del_feature_by_ft_id_api(self, ft_id=''):

        del_feature_endpoint = self.endpoint + "/api/v1/features/" + ft_id

        response = self.api.delete_api_response(endpoint=del_feature_endpoint, headers=self.headers)
        return response

    def check_and_delete_feature_by_ft_id(self, ft_id=''):
        get_feature_details_resp = self.get_feature_details_by_ft_id_api(ft_id=ft_id)
        if get_feature_details_resp.status_code == 200:
            if get_feature_details_resp.json()['featureID'] == ft_id:
                self.del_feature_by_ft_id_api(ft_id=ft_id)

    def get_plans_from_token_api(self, token=''):

        get_plans_endpoint = self.endpoint + "/api/v1/plans"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_plans_endpoint, headers=self.headers)
        return response

    def get_plans_count_from_token_api(self, token=''):

        get_plans_count_endpoint = self.endpoint + "/api/v1/plans/count"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_plans_count_endpoint, headers=self.headers)
        return response

    def get_plan_by_plan_id_api(self, plan_id=''):

        get_plan_endpoint = self.endpoint + "/api/v1/plans/" + plan_id

        response = self.api.get_api_response(endpoint=get_plan_endpoint, headers=self.headers)
        return response

    def get_plan_features_by_plan_id_api(self, plan_id=''):

        get_plan_features_endpoint = self.endpoint + "/api/v1/plans/" + plan_id + "/features"

        response = self.api.get_api_response(endpoint=get_plan_features_endpoint, headers=self.headers)
        return response

    def post_create_plan_api(self, plan_id='', name='', status='ACTIVE', features=None, desc=''):

        with open(self.prop.get('PROD_METADATA', 'create_plan_req_body')) as create_plan:
            self.json_data = json.load(create_plan)

        self.json_data['planID'] = plan_id
        self.json_data['name'] = name
        self.json_data['status'] = status
        self.json_data['desc'] = desc
        self.json_data['features'] = features

        create_plan_endpoint = self.endpoint + '/api/v1/plans'

        response = self.api.post_api_response(endpoint=create_plan_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def post_add_features_to_plan_api(self, plan_id='', features=None):

        add_features_to_plan_endpoint = self.endpoint + '/api/v1/plans/' + plan_id + '/features'

        response = self.api.post_api_response(endpoint=add_features_to_plan_endpoint, headers=self.headers,
                                              body=json.dumps(features))
        return response

    def del_features_from_plan_api(self, plan_id='', features=None):

        del_features_from_plan_endpoint = self.endpoint + '/api/v1/plans/' + plan_id + '/features'

        response = self.api.delete_api_response(endpoint=del_features_from_plan_endpoint, headers=self.headers,
                                                body=json.dumps(features))
        return response

    def post_get_plans_by_plan_ids_api(self, plan_ids=None):

        get_plans_by_plan_ids_endpoint = self.endpoint + '/api/v1/plans/planids'

        response = self.api.post_api_response(endpoint=get_plans_by_plan_ids_endpoint, headers=self.headers,
                                              body=json.dumps(plan_ids))
        return response

    def put_update_plan_api(self, plan_id='', name='', status='ACTIVE', features=None, desc=''):

        with open(self.prop.get('PROD_METADATA', 'create_plan_req_body')) as update_plan:
            self.json_data = json.load(update_plan)

        self.json_data['planID'] = plan_id
        self.json_data['name'] = name
        self.json_data['status'] = status
        self.json_data['desc'] = desc
        self.json_data['features'] = features

        update_plan_endpoint = self.endpoint + '/api/v1/plans/' + plan_id

        response = self.api.put_api_response(endpoint=update_plan_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_plan_by_plan_id_api(self, plan_id=''):

        archive_plan_endpoint = self.endpoint + "/api/v1/plans/" + plan_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_plan_endpoint, headers=self.headers)
        return response

    def del_plan_by_plan_id_api(self, plan_id=''):

        del_plan_endpoint = self.endpoint + "/api/v1/plans/" + plan_id

        response = self.api.delete_api_response(endpoint=del_plan_endpoint, headers=self.headers)
        return response

    def check_and_delete_plan_by_plan_id(self, plan_id=None):
        if not plan_id:
            return

        get_plan_details_resp = self.get_plan_by_plan_id_api(plan_id=plan_id)
        if get_plan_details_resp.status_code == 200 and get_plan_details_resp.json()['planID'] == plan_id:
            self.del_plan_by_plan_id_api(plan_id=plan_id)

    def create_plan_data(self, archive_plan=False):
        number = str(random.randint(1, 999))
        random_str = generate_random_string(char_count=4)
        plan_prefix = 'ASPSS' if archive_plan else 'SPSS'

        plan_id = plan_prefix + random_str
        name = f'SPSS Test {"Archive " if archive_plan else ""}{number}'
        desc = f'SPSS Plan Feature Test {number}'
        status = 'ACTIVE'
        feature_list = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER']
        features = sorted(feature_list)

        # Check and delete if the plan id exists
        self.check_and_delete_plan_by_plan_id(plan_id=plan_id)

        return plan_id, name, desc, status, features

    @staticmethod
    def append_elements_from_feature_list(ft_list_1=None, ft_list_2=None):
        for i in range(len(ft_list_2)):
            ft_list_1.append(ft_list_2[i])

        return sorted(ft_list_1)

    @staticmethod
    def remove_elements_from_feature_list(ft_list_1=None, ft_list_2=None):

        for i in range(len(ft_list_2)):
            ft_list_1.remove(ft_list_2[i])

        return sorted(ft_list_1)

    def build_exp_error_message_plan_response(self, plan_id='', features=None):

        with open(self.prop.get('PROD_METADATA', 'sample_duplicate_feature_in_plan_error_resp')) as error_resp:
            self.json_data = json.load(error_resp)

        feature_name = ''

        for i in range(len(features)):
            feature_name = features[i]
            break

        error_message = str(feature_name) + ' is already added to Plan : ' + str(plan_id)
        self.json_data['errors'][0]['errorDescription'] = str(error_message)

        return self.json_data

    def build_exp_error_message_role_response(self, role_id='', features=None):

        with open(self.prop.get('PROD_METADATA', 'sample_duplicate_feature_in_role_error_resp')) as error_resp:
            self.json_data = json.load(error_resp)

        feature_name = ''

        for i in range(len(features)):
            feature_name = features[i]
            break

        error_message = str(feature_name) + ' is already added to role : ' + str(role_id)
        self.json_data['errors'][0]['errorDescription'] = str(error_message)

        return self.json_data

    def get_role_templates_from_token_api(self, token=''):

        get_role_template_endpoint = self.endpoint + "/api/v1/roleTemplates"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_role_template_endpoint, headers=self.headers)
        return response

    def get_role_templates_count_from_token_api(self, token=''):

        get_role_template_count_endpoint = self.endpoint + "/api/v1/roleTemplates/count"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_role_template_count_endpoint, headers=self.headers)
        return response

    def get_role_template_by_role_id_api(self, role_id=''):

        get_role_endpoint = self.endpoint + "/api/v1/roleTemplates/" + role_id

        response = self.api.get_api_response(endpoint=get_role_endpoint, headers=self.headers)
        return response

    def get_role_template_features_by_role_id_api(self, role_id=''):

        get_role_template_features_endpoint = self.endpoint + "/api/v1/roleTemplates/" + role_id + "/features"

        response = self.api.get_api_response(endpoint=get_role_template_features_endpoint, headers=self.headers)
        return response

    def post_create_role_template_api(self, role_id='', name='', features=None):

        with open(self.prop.get('PROD_METADATA', 'create_role_template_req_body')) as create_role_template:
            self.json_data = json.load(create_role_template)

        self.json_data['roleID'] = role_id
        self.json_data['name'] = name
        self.json_data['features'] = features

        create_role_template_endpoint = self.endpoint + '/api/v1/roleTemplates'

        response = self.api.post_api_response(endpoint=create_role_template_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def post_add_features_to_role_template_api(self, role_id='', features=None):

        add_features_to_role_template_endpoint = self.endpoint + '/api/v1/roleTemplates/' + role_id + '/features'

        response = self.api.post_api_response(endpoint=add_features_to_role_template_endpoint, headers=self.headers,
                                              body=json.dumps(features))
        return response

    def del_features_from_role_template_api(self, role_id='', features=None):

        del_features_from_role_template_endpoint = self.endpoint + '/api/v1/roleTemplates/' + role_id + '/features'

        response = self.api.delete_api_response(endpoint=del_features_from_role_template_endpoint, headers=self.headers,
                                                body=json.dumps(features))
        return response

    def put_update_role_template_api(self, role_id='', name='', features=None):

        with open(self.prop.get('PROD_METADATA', 'create_role_template_req_body')) as update_role_template:
            self.json_data = json.load(update_role_template)

        self.json_data['roleID'] = role_id
        self.json_data['name'] = name
        if features:
            self.json_data['features'] = features
        else:
            del self.json_data['features']

        update_role_template_endpoint = self.endpoint + '/api/v1/roleTemplates/' + role_id

        response = self.api.put_api_response(endpoint=update_role_template_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_role_template_by_role_id_api(self, role_id=''):

        archive_role_template_endpoint = self.endpoint + "/api/v1/roleTemplates/" + role_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_role_template_endpoint, headers=self.headers)
        return response

    def del_role_template_by_role_id_api(self, role_id=''):

        del_role_template_endpoint = self.endpoint + "/api/v1/roleTemplates/" + role_id

        response = self.api.delete_api_response(endpoint=del_role_template_endpoint, headers=self.headers)
        return response

    def check_and_delete_role_template_by_role_id(self, role_id=''):
        get_role_template_resp = self.get_role_template_by_role_id_api(role_id=role_id)
        if get_role_template_resp.status_code == 200:
            if get_role_template_resp.json()['roleID'] == role_id:
                self.del_role_template_by_role_id_api(role_id=role_id)

    def create_role_template_data(self, archive_plan=False):
        random_str = generate_random_string(char_count=10)
        if archive_plan:
            role_id = f'ASPSS{random_str}'
            name = role_id
        else:
            role_id = f'SPSS{random_str}'
            name = role_id

        feature_list = ['MANAGE_CONTACTS', 'VIEW_COST_ACCOUNT', 'VIEW_USER']
        features = sorted(feature_list)

        # Check and delete if the plan id exists
        self.check_and_delete_role_template_by_role_id(role_id=role_id)

        return role_id, name, features

    def get_admin_roles_from_token_api(self, token=''):

        get_admin_roles_endpoint = self.endpoint + "/api/v1/adminRoles"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_admin_roles_endpoint, headers=self.headers)
        return response

    def get_admin_roles_by_role_id_api(self, role_id=''):

        get_admin_role_endpoint = self.endpoint + "/api/v1/adminRoles/" + role_id

        response = self.api.get_api_response(endpoint=get_admin_role_endpoint, headers=self.headers)
        return response

    def get_admin_role_by_group_id_api(self, group_id=''):

        get_admin_role_endpoint = self.endpoint + "/api/v1/adminRoles/oktaGroupID/" + group_id

        response = self.api.get_api_response(endpoint=get_admin_role_endpoint, headers=self.headers)
        return response

    def post_create_admin_roles_api(self, role_id='', name='', group_id='', group_name='', features=None):

        with open(self.prop.get('PROD_METADATA', 'create_admin_roles_req_body')) as create_admin_roles:
            self.json_data = json.load(create_admin_roles)

        self.json_data['roleID'] = role_id
        self.json_data['name'] = name
        self.json_data['oktaGroupID'] = group_id
        self.json_data['oktaGroupName'] = group_name
        self.json_data['features'] = features

        create_admin_roles_endpoint = self.endpoint + '/api/v1/adminRoles'

        response = self.api.post_api_response(endpoint=create_admin_roles_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def post_get_admin_roles_by_group_id_api(self, group_id=None):

        get_admin_roles_endpoint = self.endpoint + '/api/v1/adminRoles/oktaGroupID'

        response = self.api.post_api_response(endpoint=get_admin_roles_endpoint, headers=self.headers,
                                              body=json.dumps(group_id))
        return response

    def post_get_admin_roles_by_group_name_api(self, group_name=None):

        req_body = []
        if type(group_name) == str:
            req_body.append(group_name)
        else:
            req_body = group_name

        get_admin_roles_endpoint = self.endpoint + '/api/v1/adminRoles/oktaGroupName'

        response = self.api.post_api_response(endpoint=get_admin_roles_endpoint, headers=self.headers,
                                              body=json.dumps(req_body))
        return response

    def post_add_features_to_admin_role_api(self, role_id='', features=None):

        add_features_to_admin_role_endpoint = self.endpoint + '/api/v1/adminRoles/' + role_id + '/features'

        response = self.api.post_api_response(endpoint=add_features_to_admin_role_endpoint, headers=self.headers,
                                              body=json.dumps(features))
        return response

    def del_features_from_admin_role_api(self, role_id='', features=None):

        del_features_from_admin_role_endpoint = self.endpoint + '/api/v1/adminRoles/' + role_id + '/features'

        response = self.api.delete_api_response(endpoint=del_features_from_admin_role_endpoint, headers=self.headers,
                                                body=json.dumps(features))
        return response

    def del_admin_role_by_role_id_api(self, role_id=''):

        del_admin_role_endpoint = self.endpoint + "/api/v1/adminRoles/" + role_id

        response = self.api.delete_api_response(endpoint=del_admin_role_endpoint, headers=self.headers)
        return response

    def check_and_delete_admin_role_by_role_id(self, role_id=''):
        get_admin_role_resp = self.get_admin_roles_by_role_id_api(role_id=role_id)
        if get_admin_role_resp.status_code == 200:
            if get_admin_role_resp.json()['roleID'] == role_id:
                self.del_admin_role_by_role_id_api(role_id=role_id)

    def create_admin_role_template_data(self, admin_type=None, archive_plan=False):
        random_str = generate_random_string(char_count=10)
        if archive_plan:
            role_id = f'ASPSS{random_str}'
            name = role_id
        else:
            role_id = f'SPSS{random_str}'
            name = role_id

        group_id, group_name, feature_list = self.get_admin_role_details_by_admin_type(admin_type=admin_type)
        features = sorted(feature_list)

        # Check and delete if the plan id exists
        self.check_and_delete_admin_role_by_role_id(role_id=role_id)

        return role_id, name, group_id, group_name, features

    def get_subs_role_id(self):
        admin_role_ids = ['PB_ADMIN', 'PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT', 'USER_ADMIN']
        role_id = None

        resp = self.get_admin_roles_from_token_api()
        for i in range(0, len(resp.json())):
            if resp.json()[i]['roleID'] not in admin_role_ids:
                role_id = str(resp.json()[i]['roleID'])
                break
        if not role_id:
            role_id, name, group_id, group_name, features = self.create_admin_role_template_data(admin_type='PB_SERVICE')
            response = self.post_create_admin_roles_api(role_id=role_id, name=name, group_id=group_id, group_name=group_name, features=features)
            assert_that(response.status_code, equal_to(201))
        return role_id

    def get_admin_role_details_by_admin_type(self, admin_type=None):

        if type(admin_type) is list:
            group_id = []
            group_name = []
            features = []
            for i in range(0, len(admin_type)):
                response = self.get_admin_roles_by_role_id_api(role_id=admin_type[i])
                if response.json()['roleID'] == admin_type[i]:
                    group_id.append(response.json()['oktaGroupID'])
                    group_name.append(response.json()['oktaGroupName'])
                    for j in range(0, len(response.json()['features'])):
                        features.append(response.json()['features'][j])
        else:
            group_id = ''
            group_name = ''
            features = None
            response = self.get_admin_roles_by_role_id_api(role_id=admin_type)
            if response.status_code == 200:
                if response.json()['roleID'] == admin_type:
                    group_id = response.json()['oktaGroupID']
                    group_name = response.json()['oktaGroupName']
                    features = response.json()['features']
        return group_id, group_name, features

    def get_hubs_from_token_api(self, token=''):

        get_hubs_endpoint = self.endpoint + "/api/v1/hubs"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_hubs_endpoint, headers=self.headers)
        return response

    def get_hubs_count_from_token_api(self, token=''):

        get_hubs_count_endpoint = self.endpoint + "/api/v1/hubs/count"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_hubs_count_endpoint, headers=self.headers)
        return response

    def get_hub_by_hub_id_api(self, hub_id=''):

        get_hub_endpoint = self.endpoint + "/api/v1/hubs/" + hub_id

        response = self.api.get_api_response(endpoint=get_hub_endpoint, headers=self.headers)
        return response

    def post_create_hub_api(self, hub_id='', name='', market='', country='US'):

        with open(self.prop.get('PROD_METADATA', 'create_hub_req_body')) as create_hub:
            self.json_data = json.load(create_hub)

        self.json_data['hubID'] = hub_id
        self.json_data['name'] = name
        self.json_data['carrierMarket'] = market
        self.json_data['countryCode'] = country

        create_hub_endpoint = self.endpoint + '/api/v1/hubs'

        response = self.api.post_api_response(endpoint=create_hub_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_hub_api(self, hub_id='', name='', market='', country='US'):

        with open(self.prop.get('PROD_METADATA', 'create_hub_req_body')) as update_hub:
            self.json_data = json.load(update_hub)

        self.json_data['hubID'] = hub_id
        self.json_data['name'] = name
        self.json_data['carrierMarket'] = market
        self.json_data['countryCode'] = country

        update_hub_endpoint = self.endpoint + '/api/v1/hubs/' + hub_id

        response = self.api.put_api_response(endpoint=update_hub_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def put_archive_hub_by_hub_id_api(self, hub_id=''):

        archive_hub_endpoint = self.endpoint + "/api/v1/hubs/" + hub_id + "/archive"

        response = self.api.put_api_response(endpoint=archive_hub_endpoint, headers=self.headers)
        return response

    def del_hub_by_hub_id_api(self, hub_id=''):

        del_hub_endpoint = self.endpoint + "/api/v1/hubs/" + hub_id

        response = self.api.delete_api_response(endpoint=del_hub_endpoint, headers=self.headers)
        return response

    def check_and_delete_hub_by_hub_id(self, hub_id=''):
        get_hub_resp = self.get_hub_by_hub_id_api(hub_id=hub_id)
        if get_hub_resp.status_code == 200:
            if get_hub_resp.json()['hubID'] == hub_id:
                self.del_hub_by_hub_id_api(hub_id=hub_id)

    def create_hub_data(self, archive_plan=False):
        number = str(random.randint(1, 999))
        random_str = generate_random_string(char_count=4)
        if archive_plan:
            hub_id = 'ASPSSHub' + random_str
            name = 'SPSS Hub Test Archive ' + number
        else:
            hub_id = 'SPSSHub' + random_str
            name = 'SPSS Hub Test ' + number

        market = 'FedEx'
        country = 'US'

        # Check and delete if the plan id exists
        self.check_and_delete_hub_by_hub_id(hub_id=hub_id)

        return hub_id, name, market, country

    def get_postage_values_from_token_api(self, token=''):

        get_postage_values_endpoint = self.endpoint + "/api/v1/postageValues"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_postage_values_endpoint, headers=self.headers)
        return response

    def get_postage_value_by_postage_value_id_api(self, postage_value_id=''):

        get_postage_value_endpoint = self.endpoint + "/api/v1/postageValues/" + postage_value_id

        response = self.api.get_api_response(endpoint=get_postage_value_endpoint, headers=self.headers)
        return response

    def post_create_postage_value_api(self, display_value='', value=''):

        with open(self.prop.get('PROD_METADATA', 'create_postage_value_req_body')) as create_postage_value:
            self.json_data = json.load(create_postage_value)

        self.json_data['displayValue'] = display_value
        self.json_data['value'] = value

        create_postage_value_endpoint = self.endpoint + '/api/v1/postageValues'

        response = self.api.post_api_response(endpoint=create_postage_value_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def get_integrators_from_token_api(self, token=''):

        get_integrators_endpoint = self.endpoint + "/api/v1/integrators"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_integrators_endpoint, headers=self.headers)
        return response

    def get_integrator_by_integrator_id_api(self, integrator_id=''):

        get_integrator_endpoint = self.endpoint + "/api/v1/integrators/" + integrator_id

        response = self.api.get_api_response(endpoint=get_integrator_endpoint, headers=self.headers)
        return response

    def post_create_integrator_api(self, integrator_id='', client_id='', name='', q_url='',
                                   notify_flag='', notification_q_url=''):

        with open(self.prop.get('PROD_METADATA', 'create_integrator_req_body')) as create_integrator:
            self.json_data = json.load(create_integrator)

        self.json_data['integratorID'] = integrator_id
        self.json_data['clientID'] = client_id
        self.json_data['name'] = name
        self.json_data['qURL'] = q_url
        self.json_data['notifyFlag'] = notify_flag
        self.json_data['notificationQURL'] = notification_q_url

        create_integrator_endpoint = self.endpoint + '/api/v1/integrators'

        response = self.api.post_api_response(endpoint=create_integrator_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    @staticmethod
    def create_integrator_data():
        number = str(random.randint(1, 999))
        integrator_id = 'SPSS' + generate_random_string(char_count=4)
        client_id = number
        name = 'SPSS Integrator ' + number
        q_url = 'http://localhost'
        notification_q_url = 'http://localhost'
        notify_flag = True

        return integrator_id, client_id, name, q_url, notify_flag, notification_q_url

    def get_locales_from_token_api(self, token='', country=''):

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        if country:
            query_param = '?code=' + country
            get_locales_endpoint = self.endpoint + "/api/v1/locales" + query_param
        else:
            get_locales_endpoint = self.endpoint + "/api/v1/locales"

        response = self.api.get_api_response(endpoint=get_locales_endpoint, headers=self.headers)
        return response

    def get_locales_count_from_token_api(self, token=''):

        get_locales_count_endpoint = self.endpoint + "/api/v1/locales/count"

        if not token:
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = "Bearer " + token

        response = self.api.get_api_response(endpoint=get_locales_count_endpoint, headers=self.headers)
        return response

    def get_locale_by_locale_id_api(self, locale_id=''):

        get_locale_endpoint = self.endpoint + "/api/v1/locales/" + locale_id

        response = self.api.get_api_response(endpoint=get_locale_endpoint, headers=self.headers)
        return response

    def post_create_locale_api(self, locale_id='', country='', supported_locales=None):

        with open(self.prop.get('PROD_METADATA', 'create_locale_req_body')) as create_locale:
            self.json_data = json.load(create_locale)

        self.json_data['localeID'] = locale_id
        self.json_data['countryCode'] = country
        self.json_data['supportedLocales'] = supported_locales

        create_locale_endpoint = self.endpoint + '/api/v1/locales'

        response = self.api.post_api_response(endpoint=create_locale_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_locale_api(self, locale_id='', country='', supported_locales=None, archived=False):

        with open(self.prop.get('PROD_METADATA', 'update_locale_req_body')) as update_locale:
            self.json_data = json.load(update_locale)

        self.json_data['localeID'] = locale_id
        self.json_data['countryCode'] = country
        self.json_data['supportedLocales'] = supported_locales
        self.json_data['archived'] = archived

        update_locale_endpoint = self.endpoint + '/api/v1/locales/' + locale_id

        response = self.api.put_api_response(endpoint=update_locale_endpoint, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def del_locale_by_locale_id_api(self, locale_id=''):

        del_locale_endpoint = self.endpoint + "/api/v1/locales/" + locale_id

        response = self.api.delete_api_response(endpoint=del_locale_endpoint, headers=self.headers)
        return response

    def check_and_delete_locale_by_locale_id(self, locale_id=''):
        get_locale_resp = self.get_locale_by_locale_id_api(locale_id=locale_id)
        if get_locale_resp.status_code == 200:
            if get_locale_resp.json()['localeID'] == locale_id:
                self.del_locale_by_locale_id_api(locale_id=locale_id)

    def create_locale_data(self):
        number = str(random.randint(1, 999))
        locale_id = 'SPSS_Locale_' + generate_random_string(char_count=4)
        country = 'US' + number
        supported_locales = ['en_US']

        # Check and delete if the plan id exists
        self.check_and_delete_locale_by_locale_id(locale_id=locale_id)

        return locale_id, country, supported_locales

    def verify_res_schema(self, res, expected_schema):

        isValid = self.api.schema_validation(response_schema=res, expected_schema=expected_schema)

        return isValid

    def get_admin_roles(self):
        # Adding endpoint here as the prodmgmt is always picking dev as env. Need to fix it later.
        host = 'https://prodmgmt-temp.sendpro360.pitneycloud.com'
        env = str(self.app_config.env_cfg['env']).lower()
        url = host.replace("temp", env)
        get_admin_roles_endpoint = url + '/api/v1/adminRoles'
        headers = {"Host": url[8:], 'Authorization': self.admin_token}

        response = self.api.get_api_response(get_admin_roles_endpoint, headers)
        return response

    def derive_group_name(self, group_name=None):
        env = self.app_config.env_cfg['env'].lower()
        suffix = '-' + env + ('-us' if env == 'ppd' else '')
        return group_name + suffix
