import logging
import random
import uuid
import pytest
import json
import pandas as pd
from hamcrest import assert_that

import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.generic_utils import generate_random_string


class ClientManagementAPI:
    """
    This class encapsulates various methods and element identifications necessary for interacting
    with Client Management APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.prop = self.config.load_properties_file()
        self.login = LoginAPI(app_config)
        self.endpoint = str(self.app_config.env_cfg['climgmt_api'])
        self.headers = {"Accept": "*/*"}
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    @staticmethod
    def generate_enterprise_data():
        unique_id = str(uuid.uuid4().hex)[:8]
        enterprise_name = f'Auto_Ent_{unique_id}'
        ent_id = f'Ent_ID_{unique_id}'
        return enterprise_name, ent_id

    def get_subscription_id_from_file(self):
        with open(self.prop.get('CLIENT_MGMT', 'sample_test_data')) as file:
            self.json_data = json.load(file)

        sub_id = self.json_data[self.prod_name][self.env]['subId']
        return sub_id

    def get_enterprise_id_from_file(self):
        with open(self.prop.get('CLIENT_MGMT', 'sample_test_data')) as file:
            self.json_data = json.load(file)

        ent_Id = self.json_data[self.prod_name][self.env]['enterpriseId']
        return ent_Id

    def get_divisions_from_file(self):
        with open(self.prop.get('CLIENT_MGMT', 'sample_test_data')) as file:
            self.json_data = json.load(file)

        # env = self.env
        div_list = self.json_data[self.prod_name][self.env]['divisions']
        return div_list

    def get_sub_id_user_cred_from_testdata_file(self, sub_type='PITNEYSHIP_PRO', user_type=None):
        """
        Retrieves the subscription ID and user credentials from an address book JSON file.
        :param sub_type: The type of subscribed product. ex: PITNEYSHIP_PRO
        :param user_type: The type of client users. ex: Enterprise, Division, Location and User.
        :return: The subscription ID corresponding to the provided subscription type.
        """
        if user_type is None:
            return None

        with open(self.prop.get('COMMON_SHARED_SERVICES', 'common_test_data')) as file:
            json_data = json.load(file)

        data = json_data[self.prod_name][self.env][sub_type]
        sub_id = data['sub_id']
        ent_id = data['ent_id']
        email = None
        pwd = None

        if user_type == 'E':
            email = data['ent_user']
            pwd = data['ent_pwd']
        elif user_type == 'D':
            email = data['div_user']
            pwd = data['div_pwd']
        elif user_type == 'L':
            email = data['loc_user']
            pwd = data['loc_pwd']
        elif user_type == 'User' or user_type == 'U':
            email = data['user']
            pwd = data['user_pwd']

        return sub_id, ent_id, email, pwd

    def get_subs_user_details_from_test_data(self, sub_type='PITNEYSHIP_PRO', user_type=None):

        sub_id, ent_id, email, pwd = self.get_sub_id_user_cred_from_testdata_file(sub_type=sub_type, user_type=user_type)

        self.log.info(f'Fetched Details from test data file: \nsub_id: {sub_id}, ent_id: {ent_id}, '
                      f'user_type: {user_type}, user_email: {email}, user_pwd: {pwd}')

        return sub_id, ent_id, email, pwd

    def add_location_api(self, div_id='', loc_id='', loc_name='', ent_id='', subId='', is_admin=''):
        """
        This function is validates if a new location can be added successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_location')) as f:
            self.json_data = json.load(f)

        if div_id != "":
            self.json_data['divisionID'] = div_id

        if loc_id != "":
            self.json_data['locationID'] = loc_id

        if loc_name != "":
            self.json_data['name'] = loc_name

        if ent_id != "":
            self.json_data['enterpriseID'] = ent_id

        if subId != "":
            self.json_data['subID'] = subId

        if is_admin.lower() == 'y':

            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        add_location_endpoint = self.endpoint + "/api/v1/locations"
        response = self.api.post_api_response(endpoint=add_location_endpoint,
                                              headers=self.headers, body=json.dumps(self.json_data))
        return response

    def create_location_api(self, div_id=None, loc_id=None, loc_name='', ent_id='', sub_id='', bpn='', is_admin=False,
                            admin_token='', client_token=''):

        with open(self.prop.get('CLIENT_MGMT', 'create_location_body')) as f:
            payload = json.load(f)

        if not bpn:
            bpn = generate_random_string(uppercase=False, lowercase=False)

        payload['shipToBPN'] = bpn
        payload['locationProperties']['shipToBPN'] = bpn

        if div_id:
            payload['divisionID'] = div_id
        if loc_id:
            payload['locationID'] = loc_id
            payload['customLocationIdChecked'] = True
        if loc_name:
            payload['name'] = loc_name
            payload['rcName'] = loc_name
        if ent_id != "":
            payload['enterpriseID'] = ent_id
        if sub_id != "":
            payload['subID'] = sub_id

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        create_location_url = f'{self.endpoint}/api/v1/locations'

        response = self.api.post_api_response(endpoint=create_location_url, headers=self.headers, body=json.dumps(payload))
        return response

    def update_location_api(self, div_id='', loc_id='', loc_name='', ent_id='', sub_id='', addr_ln1='', addr_ln2='',
                            city='', state='', postal_code='', email='', phone='', bpn='', is_admin=True,
                            admin_token='', client_token=''):
        """
        This function is validates if a new location can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'create_location_body')) as f:
            payload = json.load(f)

        if not bpn:
            bpn = generate_random_string(uppercase=False, lowercase=False)

        payload['shipToBPN'] = bpn
        payload['locationProperties']['shipToBPN'] = bpn

        if div_id:
            payload['divisionID'] = div_id

        if loc_id:
            payload['locationID'] = loc_id
            payload['customLocationIdChecked'] = True

        if loc_name:
            payload['name'] = loc_name
            payload['rcName'] = loc_name

        if ent_id:
            payload['enterpriseID'] = ent_id

        if sub_id:
            payload['subID'] = sub_id

        if addr_ln1:
            payload['addressLine1'] = addr_ln1
            payload['returnAddressLine1'] = addr_ln1

        if addr_ln2:
            payload['addressLine2'] = addr_ln2
            payload['returnAddressLine2'] = addr_ln2

        if city:
            payload['city'] = city
            payload['returnCity'] = city

        if state:
            payload['state'] = state
            payload['returnState'] = state

        if postal_code:
            payload['postalCode'] = postal_code

        if email:
            payload['email'] = email

        if phone:
            payload['phone'] = phone

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        update_loc_url = f'{self.endpoint}/api/v1/locations/{loc_id}'

        response = self.api.put_api_response(endpoint=update_loc_url, headers=self.headers, body=json.dumps(payload))
        return response

    def delete_location_api(self, loc_id):
        """
        This test deletes the created location
        :return: this function returns boolean status of element located
        """
        del_loc_endpoint = self.endpoint + "/api/v1/locations/" + loc_id

        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=del_loc_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def delete_location_v2_api(self, loc_id='', sub_id='', is_admin=True, admin_token='', client_token=''):

        if is_admin:
            del_loc_endpoint = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/locations/{loc_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            del_loc_endpoint = f'{self.endpoint}/api/v2/locations/{loc_id}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.delete_api_response(endpoint=del_loc_endpoint, headers=self.headers)
        return response

    def get_all_locations_api(self):
        """
        This test fetches the details of all the locations
        :return: this function returns boolean status of element located
        """
        get_locations_endpoint = self.endpoint + "/api/v1/locations"

        self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_locations_endpoint, headers=self.headers)
        return res

    def get_loc_by_id_api(self, loc_id=None, is_admin=True, admin_token=None, client_token=None):
        """
        This test fetches the details of location by location id
        :return: this function returns boolean status of element located
        """
        if loc_id is None:
            pytest.fail('Invalid request in get_loc_by_id_api. loc_id cannot be none!')

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        get_loc_by_id_endpoint = f'{self.endpoint}/api/v1/locations/{loc_id}'
        response = self.api.get_api_response(endpoint=get_loc_by_id_endpoint, headers=self.headers)
        return response

    def verify_get_loc_count_api(self):
        """
        This test fetches the total count of of locations
        :return: this function returns boolean status of element located
        """
        get_loc_count_endpoint = self.endpoint + "/api/v1/locations/count"
        self.headers['Authorization'] = self.client_token
        res = self.api.get_api_response(
            endpoint=get_loc_count_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def archive_location_api(self, loc_id):
        """
        This test archives the created location
        :return: this function returns boolean status of element located
        """
        archive_location_endpoint = self.endpoint + "/api/v1/locations/" + loc_id + "/archive"

        self.headers['Authorization'] = self.admin_token
        res = self.api.put_api_response(
            endpoint=archive_location_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def get_field_list(self):
        """
        This test fetches the field list of location
        :return: this function returns field list
        """
        get_loc_field_list_endpoint = self.endpoint + "/api/v1/locations/fieldList"

        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_loc_field_list_endpoint, headers=self.headers)
        return res

    def export_locations_api(self, fieldList='', sub_Id='', is_admin=''):
        """This API exports the locations"""

        if is_admin.lower() == 'y':

            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        export_loc_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_Id + "/location/export"
        response = self.api.post_api_response(endpoint=export_loc_endpoint,
                                              headers=self.headers, body=json.dumps(fieldList))
        return response

    def fetch_process_status_api(self, jobId='', sub_Id='', is_admin=''):
        """This API returns the process status of Import/Export jobs"""
        if is_admin.lower() == 'y':

            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        check_status_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_Id + "/location/" + jobId + "/status"
        res = self.api.get_api_response(endpoint=check_status_endpoint, headers=self.headers)
        return res

    def get_file_content(self, decoded_string=''):
        file_location_url = decoded_string

        res = self.api.get_api_response(
            endpoint=file_location_url, headers='')

        return res

    # Test functions: Division Module

    def get_all_divisions_api(self):
        """
        This test fetches the details of all the divisions
        :return: this function returns boolean status of element located
        """
        get_divisions_endpoint = self.endpoint + "/api/v1/divisions"

        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_divisions_endpoint, headers=self.headers)

        return res

    def get_div_count_api(self):
        """
        This test fetches the total count of of divisions
        :return: this function returns boolean status of element located
        """
        get_div_count_endpoint = self.endpoint + "/api/v1/divisions/count"

        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_div_count_endpoint, headers=self.headers)
        return res

    def add_division_api(self, div_id='', name='', sub_id ='', ent_id =''):
        """
        This function is validates if a new divisions can be added successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_division')) as f:
            self.json_data = json.load(f)
        result = False

        if div_id != "":
            self.json_data['divisionID'] = div_id

        if name != "":
            self.json_data['name'] = name

        if sub_id !="":
            self.json_data['subID'] = sub_id

        if ent_id !="":
            self.json_data['enterpriseID'] = ent_id

        add_div_endPoint = self.endpoint + "/api/v1/divisions"
        self.headers['Authorization'] = self.admin_token
        res = self.api.post_api_response(
            endpoint=add_div_endPoint, headers=self.headers, body=json.dumps(self.json_data))

        return res

    def create_division_api(self, div_id=None, name='', sub_id='', ent_id='', is_admin=False, admin_token=None,
                            client_token=None):

        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_division')) as f:
            payload = json.load(f)

        if div_id:
            payload['divisionID'] = div_id
            payload['customDivisionIdChecked'] = True
        if name:
            payload['name'] = name
        if sub_id:
            payload['subID'] = sub_id
        if ent_id:
            payload['enterpriseID'] = ent_id

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        create_div_url = f'{self.endpoint}/api/v1/divisions'

        response = self.api.post_api_response(endpoint=create_div_url, headers=self.headers, body=json.dumps(payload))
        return response

    def update_division_api(self, div_id='', name='', sub_id ='', ent_id=''):
        """
        This function is validates that divisions can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_division')) as f:
            self.json_data = json.load(f)

        if div_id != "":
            self.json_data['divisionID'] = div_id

        if name != "":
            self.json_data['name'] = name

        if sub_id != "":
            self.json_data['subID'] = sub_id

        if ent_id != "":
            self.json_data['enterpriseID'] = ent_id

        self.headers['Authorization'] = self.admin_token

        updt_div_endPoint = self.endpoint + "/api/v1/divisions/" + div_id
        res = self.api.put_api_response(
            endpoint=updt_div_endPoint, headers=self.headers, body=json.dumps(self.json_data))

        return res

    def put_update_division_with_loc_id_api(self, loc_id='', div_id='', is_admin=True, admin_token='', client_token=''):
        """
        This API is used to update the location id archive details in the division when the location is deleted.
        :param loc_id: The location id.
        :param div_id: The division id.
        :param is_admin: Admin flag to determine the API is called using admin or client token.
        :param admin_token: The admin access token generated from an admin user credentials.
        :param client_token: The client access token generated from a client user credentials.
        """
        if not loc_id or not div_id:
            pytest.fail("put_update_division_with_loc_id_api :: loc_id and div_id are required!")

        if is_admin:
            update_div_endpoint = f'{self.endpoint}/api/v1/divisions/{div_id}/locations'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            update_div_endpoint = f'{self.endpoint}/api/v1/divisions/{div_id}/locations'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        payload = json.dumps([loc_id])
        response = self.api.put_api_response(endpoint=update_div_endpoint, headers=self.headers, body=payload)
        return response

    def get_div_by_id_api(self, div_id):
        """
        This test fetches the division details as per the provided Id
        :return: this function returns boolean status of element located
        """
        get_div_endpoint = self.endpoint + "/api/v1/divisions/" + div_id

        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_div_endpoint, headers=self.headers)
        return res

    def get_loc_from_div_api(self, div_id):
        """
        This test fetches the division details as per the provided Id
        :return: this function returns boolean status of element located
        """
        get_div_endpoint = self.endpoint + "/api/v1/divisions/" + div_id + "/locations"

        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(endpoint=get_div_endpoint, headers=self.headers)
        return res

    def archive_division_api(self, div_id):
        """
        This test archives the created division
        :return: this function returns boolean status of element located
        """
        archive_division_endpoint = self.endpoint + "/api/v1/divisions/" + div_id + "/archive"

        self.headers['Authorization'] = self.admin_token
        res = self.api.put_api_response(
            endpoint=archive_division_endpoint, headers=self.headers)

        return res

    def delete_division_api(self, div_id):
        """
        This test deletes the created division
        :return: this function returns boolean status of element located
        """
        del_division_endpoint = self.endpoint + "/api/v1/divisions/" + div_id

        self.headers['Authorization'] = self.admin_token

        res = self.api.delete_api_response(
            endpoint=del_division_endpoint, headers=self.headers)
        return res

    def add_locations_in_division_api(self, div_id='', loc=''):
        """
        This function validates that locations can be added to divisions successfully
        :return: this function returns response and status code
        """
        loc_name = f'["{loc}"]'
        loc_bdy = json.loads(loc_name)

        add_loc_endPoint = self.endpoint + "/api/v1/divisions/" + div_id + "/locations"
        self.headers['Authorization'] = self.admin_token
        res = self.api.post_api_response(
            endpoint=add_loc_endPoint, headers=self.headers, body=json.dumps(loc_bdy))
        return res

    def delete_locations_from_division_api(self, div_id='', loc=''):
        """
        This function validates that locations can be deleted from divisions successfully
        :return: this function returns response and status code
        """

        loc_bdy = json.loads(loc)

        del_loc_endPoint = self.endpoint + "/api/v1/divisions/" + div_id + "/locations"
        self.headers['Authorization'] = self.admin_token
        res = self.api.put_api_response(
            endpoint=del_loc_endPoint, headers=self.headers, body=json.dumps(loc_bdy))

        return res

    def add_division_with_location_api(self, div_id='', div_name='', loc=''):
        """
        This function validates if a new divisions can be added with locations successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_division_with_loc')) as f:
            self.json_data = json.load(f)
        result = False

        if div_id != "":
            self.json_data['divisionID'] = div_id

        if div_name != "":
            self.json_data['name'] = div_name

        loc_bdy = json.loads(loc)

        if loc_bdy != "":
            self.json_data['locations'] = loc_bdy

        self.headers['Authorization'] = self.admin_token

        add_div_endPoint = self.endpoint + "/api/v1/divisions"
        res = self.api.post_api_response(
            endpoint=add_div_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        return res

    def get_loc_in_div_paginated_api(self, div_id=None, skip='0', limit='100',
                                     admin_token=None, client_token=None, is_admin=False):
        """
        This test fetches the division details as per the pagination
        :return: this function returns boolean status of element located
        """
        query_param = f'?skip={skip}&limit={limit}'
        locations_paginate_url = f'{self.endpoint}/api/v1/divisions/{div_id}/locations/paginate?{query_param}'

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=locations_paginate_url, headers=self.headers)
        return response

    # Test functions: Enterprise Module

    def get_all_enterprises_api(self):
        """
        This test fetches the details of all the enterprises
        :return: this function returns boolean status of element located
        """
        get_ent_endpoint = self.endpoint + "/api/v1/enterprises"

        self.headers['Authorization'] = self.admin_token
        response = self.api.get_api_response(endpoint=get_ent_endpoint, headers=self.headers)
        return response

    def get_enterprise_count_api(self):
        """
        This test fetches the total count of of enterprises
        :return: this function returns boolean status of element located
        """
        get_ent_count_endpoint = self.endpoint + "/api/v1/enterprises/count"

        self.headers['Authorization'] = self.admin_token
        res = self.api.get_api_response(
            endpoint=get_ent_count_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def add_enterprise_api(self, ent_id='', name=''):
        """
        This function validates if a new enterprise can be added successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_enterprise')) as f:
            self.json_data = json.load(f)

        if ent_id != "":
            self.json_data['enterpriseID'] = ent_id

        if name != "":
            self.json_data['name'] = name

        add_ent_url = self.endpoint + "/api/v1/enterprises"
        self.headers['Authorization'] = self.admin_token

        res = self.api.post_api_response(endpoint=add_ent_url, headers=self.headers, body=json.dumps(self.json_data))
        return res

    def get_enterprise_by_ent_id_api(self, ent_id):
        """
        This test fetches the details of enterprise by enterprise Id
        :return: this function returns boolean status of element located
        """
        get_ent_by_id_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id
        self.headers['Authorization'] = self.admin_token
        response = self.api.get_api_response(endpoint=get_ent_by_id_endpoint, headers=self.headers)
        return response

    def get_divisions_by_ent_id_api(self, ent_id=''):
        """
        This test fetches the details of enterprise by enterprise Id
        :return: this function returns boolean status of element located
        """
        get_div_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/divisions"
        self.headers['Authorization'] = self.admin_token

        response = self.api.get_api_response(endpoint=get_div_endpoint, headers=self.headers)
        return response

    def delete_ent_api(self, ent_id=''):
        """
        This API is to delete the given enterprise.
        :param ent_id: The enterprise ID of an enterprise.
        """
        if not ent_id:
            pytest.fail("delete_ent_api :: ent_id cannot be empty!")

        del_ent_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id
        self.headers['Authorization'] = self.admin_token
        res = self.api.delete_api_response(endpoint=del_ent_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def update_enterprise_api(self, ent_id='', name=''):
        """
        This function is validates that divisions can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_enterprise')) as f:
            self.json_data = json.load(f)
        result = False

        if ent_id != "":
            self.json_data['enterpriseID'] = ent_id

        if name != "":
            self.json_data['name'] = name

        updt_ent_endPoint = self.endpoint + "/api/v1/enterprises/" + ent_id
        self.headers['Authorization'] = self.admin_token

        res = self.api.put_api_response(
            endpoint=updt_ent_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        return status_code

    def get_sap_enterpriseIds_api(self):
        """
        This test fetches the details of all the sap enterprises
        """
        get_sap_ent_endpoint = self.endpoint + "/api/v1/enterprises/sapenterpriseIds"

        self.headers['Authorization'] = self.admin_token
        response = self.api.get_api_response(endpoint=get_sap_ent_endpoint, headers=self.headers)
        return response

    def get_user_enterprise_api(self):
        """
        This test fetches the details of all the sap enterprises
        """
        get_sap_ent_endpoint = self.endpoint + "/api/v1/user/enterprises"

        self.headers['Authorization'] = self.admin_token
        response = self.api.get_api_response(endpoint=get_sap_ent_endpoint, headers=self.headers)
        return response

    def add_division_in_ent_api(self, ent_id='', div=''):
        """
        This function validates that divisions can be added to entities successfully
        :return: this function returns response and status code
        """

        div_bdy = json.loads(div)

        add_div_in_ent_url = f'{self.endpoint}/api/v1/enterprises/{ent_id}/divisions'
        self.headers['Authorization'] = self.admin_token

        resp = self.api.post_api_response(endpoint=add_div_in_ent_url, headers=self.headers, body=json.dumps(div_bdy))
        return resp

    def add_enterprise_with_division_api(self, ent_id='', name='', div=''):
        """
        This function validates that divisions can be added to entities successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_enterprise_with_div')) as f:
            self.json_data = json.load(f)

        if ent_id:
            self.json_data['enterpriseID'] = ent_id
        if name:
            self.json_data['name'] = name

        div_bdy = json.loads(div)

        self.json_data['divisions'] = div_bdy

        add_ent_with_div_url = f'{self.endpoint}/api/v1/enterprises'
        self.headers['Authorization'] = self.admin_token
        res = self.api.post_api_response(endpoint=add_ent_with_div_url, headers=self.headers,
                                         body=json.dumps(self.json_data))
        return res

    def delete_division_from_ent_api(self, ent_id='', div=''):
        """
        This function validates that divisions can be deleted from entities successfully
        :return: this function returns response and status code
        """

        div_bdy = json.loads(div)

        add_ent_endPoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/divisions"
        self.headers['Authorization'] = self.admin_token
        res = self.api.put_api_response(
            endpoint=add_ent_endPoint, headers=self.headers, body=json.dumps(div_bdy))
        status_code = res.status_code
        return status_code

    def archive_ent_api(self, ent_id=''):
        """
        This function validates that divisions can be archived from entities successfully
        :return: this function returns response and status code
        """

        arch_ent_endPoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/archive"
        res = self.api.put_api_response(
            endpoint=arch_ent_endPoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def get_locations_by_ent_id_api(self, ent_id=''):
        """
        This test fetches the details of locations available in enterprise Id
        :return: this function returns boolean status of element located
        """
        get_loc_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/locations"

        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=get_loc_endpoint, headers=self.headers)
        return res

    # Test Cases for location hierarchy

    def verify_add_site_api(self, is_admin='', sub_id='', name='', type=''):
        """
        This function validates if a new site can be added successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_site')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['name'] = name

        self.json_data['type'] = type

        if is_admin == 'Y':
            add_site_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites"
            self.headers['Authorization'] = self.admin_token

        else:
            add_site_endPoint = self.endpoint + "/api/v1/inboundsites"
            self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_site_endPoint, headers=self.headers, body=json.dumps(self.json_data))

        status_code = res.status_code

        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def verify_add_site_with_location_api(self, is_admin='', sub_id='', name='', type='', location_id=''):
        """
        This function validates if a new site can be added successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_with_location')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['name'] = name

        self.json_data['type'] = type

        self.json_data['locationId'] = location_id

        if is_admin == 'Y':
            add_site_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites"
            self.headers['Authorization'] = self.admin_token

        else:
            add_site_endPoint = self.endpoint + "/api/v1/inboundsites"
            self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_site_endPoint, headers=self.headers, body=json.dumps(self.json_data))

        status_code = res.status_code

        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def verify_add_inbound_site_api(self, is_admin='', sub_id='', name='', parent_id='', type=''):
        """
        This function validates if a new site can be added successfully
        :return: this function returns response and status code
        """

        with open(self.prop.get('CLIENT_MGMT', 'body_path_add_inbound_site')) as f:
            self.json_data = json.load(f)
        result = False

        self.json_data['name'] = name

        self.json_data['parent'] = parent_id

        self.json_data['type'] = type

        if is_admin == 'Y':

            add_site_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites"
            self.headers['Authorization'] = self.admin_token

        else:
            add_site_endPoint = self.endpoint + "/api/v1/inboundsites"
            self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_site_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def verify_get_inbound_site_by_id_api(self, is_admin='', sub_id='', site_id=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """
        if is_admin == 'Y':
            get_inbound_site_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites/" + site_id
            self.headers['Authorization'] = self.admin_token

        else:
            get_inbound_site_endpoint = self.endpoint + "/api/v1/inboundsites/" + site_id
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_inbound_site_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def verify_update_site_api(self, is_admin=False, sub_id='', name='', inbound_type='', status='', site_id=''):
        """
        This function validates if a new site can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('CLIENT_MGMT', 'body_path_update_site')) as f:
            payload = json.load(f)

        payload['name'] = name
        payload['type'] = inbound_type
        payload['status'] = status

        if is_admin:
            update_site_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/inboundsites/{site_id}'
            self.headers['Authorization'] = self.admin_token
        else:
            update_site_endpoint = f'{self.endpoint}/api/v1/inboundsites/{site_id}'
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(endpoint=update_site_endpoint,
                                             headers=self.headers, body=json.dumps(payload))
        return response

    def verify_delete_inbound_site_by_id_api(self, is_admin='', sub_id='', site_id=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """
        if is_admin == 'Y':

            del_inbound_site_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites/" + site_id
            self.headers['Authorization'] = self.admin_token

        else:
            del_inbound_site_endpoint = self.endpoint + "/api/v1/inboundsites/" + site_id
            self.headers['Authorization'] = self.client_token

        res = self.api.delete_api_response(
            endpoint=del_inbound_site_endpoint, headers=self.headers)
        status_code = res.status_code

        return status_code

    '''
    def verify_get_inbound_site_by_search_criteria_api(self, is_admin='', sub_id='', search_param=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """

        if is_admin == 'Y':
            get_inbound_site_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites?searchBy=" + search_param

        else:
            get_inbound_site_endpoint = self.endpoint + "/api/v1/inboundsites?searchBy=" + search_param

        res = self.api.get_api_response(
            endpoint=get_inbound_site_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
        return res, status_code
    '''

    def verify_get_inbound_site_by_search_criteria_api(self, is_admin='', sub_id='', search_param=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """

        if is_admin == 'Y':
            get_inbound_site_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites?" + search_param
            self.headers['Authorization'] = self.admin_token

        else:
            get_inbound_site_endpoint = self.endpoint + "/api/v1/inboundsites?" + search_param
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_inbound_site_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def verify_location_hierarchy_pagination_api(self, sub_id=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """
        get_inbound_site_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/inboundsites"

        is_paginated = self.api.pagination_util(endpoint=get_inbound_site_endpoint, headers=self.headers)
        return is_paginated

    def verify_import_locations_api(self, ent_id, loc_id=''):
        """
        This function validates that locations can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        loc_file = self.prop.get('CLIENT_MGMT', 'create_location_import_template')

        df = pd.read_csv(loc_file)
        df.loc[0, 'LocationID'] = loc_id
        df.loc[0, 'Name'] = loc_id
        df.to_csv(loc_file, index=False)

        print(list(df))

        f = open(self.prop.get('CLIENT_MGMT', 'create_location_import_template'))

        files = {"file": (self.prop.get('CLIENT_MGMT', 'create_location_import_template'), f)}

        import_location_endPoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/locations/import"
        res = self.api.post_api_response(endpoint=import_location_endPoint, files=files, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def post_add_new_location_in_division_api(self, div_id='', sub_id='', ent_id='', loc_name='', is_admin='y'):
        with open(self.prop.get('CLIENT_MGMT', 'add_location_request_body')) as f1:
            self.json_data = json.load(f1)

        # clock = datetime.datetime.now()
        # bpn_value = str(clock.timestamp())[0:10]
        #bpn_value = "0010120364"
        bpn_value = generate_random_string(uppercase=False, lowercase=False)

        self.json_data['divisionID'] = div_id
        self.json_data['locationName'] = loc_name
        self.json_data['rcName'] = loc_name
        self.json_data['name'] = loc_name
        self.json_data['shipToBPN'] = bpn_value
        self.json_data['locationProperties']['shipToBPN'] = bpn_value
        self.json_data['enterpriseID'] = ent_id
        self.json_data['subID'] = sub_id

        self.headers['Authorization'] = self.admin_token
        if is_admin == 'n':
            self.headers['Authorization'] = self.client_token

        add_location_endpoint = self.endpoint + "/api/v1/locations"
        response = self.api.post_api_response(endpoint=add_location_endpoint,
                                              headers=self.headers, body=json.dumps(self.json_data))
        return response

    def verify_site_type(self, search_by_site_res, expected_site_type):
        total_sites = len(search_by_site_res['inboundsites'])
        for i in range(total_sites):
            if search_by_site_res['inboundsites'][i]['type'] != expected_site_type:
                return False
        return True

    def verify_get_inbound_site_by_loc_id_api(self, is_admin='', sub_id='', loc_id=''):
        """
        This test fetches the details of inbound site as per the provided Id
        :return: this function returns boolean status of element located
        """

        if is_admin == 'Y':
            get_inbound_site_by_loc_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/locations/" + loc_id+"/inboundsites"
            self.headers['Authorization'] = self.admin_token

        else:
            get_inbound_site_by_loc_endpoint = self.endpoint + "/api/v1/locations/" + loc_id+"/inboundsites"
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_inbound_site_by_loc_endpoint, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def get_div_from_location_id_api(self, loc_id, is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches the details of division by location Id
        :return: this function returns boolean status of element located
        """
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/locations/" + loc_id + "/divisions"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/locations/" + loc_id + "/divisions"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_loc_from_div_id_and_account_number_api(self, div_id, acc_no, is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches the details of location by div Id and account number
        :return: this function returns boolean status of element located
        """
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/divisions/" + div_id + "/accountNumber/" + acc_no + "/locations"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/divisions/" + div_id + "/accountNumber/" + acc_no + "/locations"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_div_from_user_and_sub_id_api(self, user_id, sub_id, is_admin=False, admin_token=None, client_token=None,
                                         skip=None, limit=None):
        """
        This test fetches the details of division by User and Sub Id
        :return: this function returns boolean status of element located
        """
        query_param = "?skip={args1}&limit={args2}".format(args1=skip, args2=limit)
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/divisions" + query_param
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/divisions" + query_param
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_loc_from_user_and_sub_id_api(self, user_id, sub_id, is_admin=False, admin_token=None, client_token=None,
                                     skip=None, limit=None):
        """
        This test fetches the details of locations by User and Sub Id
        :return: this function returns boolean status of element located
        """
        query_param = "?skip={args1}&limit={args2}".format(args1=skip, args2=limit)
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/locations" + query_param
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/locations" + query_param
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_user_ent_api(self, client_token=None):
        """
        This test fetches the details of enterprise by user access token
        :return: this function returns boolean status of element located
        """
        get_loc_by_id_endpoint = self.endpoint + "/api/v1/enterprise"

        self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_ent_from_paginate_api(self, is_admin=False, admin_token=None, client_token=None,
                                  skip=None, limit=None):
        """
        This test fetches the details of enterprise by pagination
        :return: this function returns boolean status of element located
        """
        query_param = "?skip={args1}&limit={args2}".format(args1=skip, args2=limit)
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/enterprises/paginate" + query_param
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/enterprises/paginate" + query_param
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def get_loc_from_ent_id_and_paginate_api(self, ent_id, is_admin=False, admin_token=None, client_token=None, skip=None, limit=None):
        """
        This test fetches the details of all location by enterprise id and pagination
        :return: this function returns boolean status of element located
        """
        query_param = "?skip={args1}&limit={args2}".format(args1=skip, args2=limit)
        if is_admin:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/locations/paginate" + query_param
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_loc_by_id_endpoint = self.endpoint + "/api/v1/enterprises/" + ent_id + "/locations/paginate" + query_param
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.get_api_response(
            endpoint=get_loc_by_id_endpoint, headers=self.headers)

        return res

    def inbound_sitelist_post_api(self, site_id=None, is_admin=False, admin_token=None, client_token=None):
        """
        This function validates if inboundsitelist added successfully
        :return: this function returns response and status code
        """
        site_id_var = [site_id]
        if is_admin:
            add_site_endpoint = self.endpoint + "/api/v1/inboundsiteslist"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            add_site_endpoint = self.endpoint + "/api/v1/inboundsiteslist"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.post_api_response(
            endpoint=add_site_endpoint, headers=self.headers, body=json.dumps(site_id_var))

        return res

    def locationids_post_api(self, loc_id='', is_admin=False, admin_token=None, client_token=None):
        """
        This function validates if a locationids api works successfully
        :return: this function returns response and status code
        """
        loc_id_var = [loc_id]
        if is_admin:
            add_site_endpoint = self.endpoint + "/api/v1/locations/ids"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            add_site_endpoint = self.endpoint + "/api/v1/locations/ids"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        res = self.api.post_api_response(
            endpoint=add_site_endpoint, headers=self.headers, body=json.dumps(loc_id_var))

        return res

    def get_loc_id_of_a_division_using_ent_id(self, ent_id=None):

        if not ent_id:
            return None

        divisions = self.get_divisions_by_ent_id_api(ent_id).json()

        for division in divisions:
            locations = division.get('locations')
            if isinstance(locations, list):
                if locations:
                    return locations[0]
            elif isinstance(locations, str):
                return locations
        return None

    def get_ent_id_having_divisions_and_locations(self):

        ent_resp = self.get_ent_from_paginate_api(is_admin=True, skip=1, limit=50)
        assert_that(common_utils.validate_response_code(ent_resp, 200))

        enterprises = ent_resp.json()['enterprises']

        for ent in enterprises:
            ent_id = ent.get('enterpriseID', [])
            divisions = ent.get('divisions', [])
            if divisions:
                loc = self.get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)
                if loc:
                    return ent_id
        return None

    def create_div_in_ent(self, ent_id=None, sub_id=None):

        if not ent_id:
            ent_id = self.get_enterprise_id_from_file()
        if not sub_id:
            sub_id = self.get_subscription_id_from_file()

        div_id = f'auto_div_id_{generate_random_string()}'
        div_name = f'auto_div_name_{generate_random_string()}'

        add_div_res = self.add_division_api(div_id=div_id, name=div_name, sub_id=sub_id, ent_id=ent_id)

        assert_that(common_utils.validate_response_code(add_div_res, 201))
        created_div_id = add_div_res.json()['divisionID']

        return created_div_id, div_name

    def create_loc_div_in_ent(self, ent_id=None, sub_id=None):

        div_id = f'auto_div_id_{generate_random_string()}'
        div_name = f'auto_div_name_{generate_random_string()}'
        loc_name = f'auto_loc_name_{generate_random_string()}'

        if not ent_id:
            ent_id = self.get_enterprise_id_from_file()
        if not sub_id:
            sub_id = self.get_subscription_id_from_file()

        add_div_resp = self.add_division_api(div_id=div_id, name=div_name, sub_id=sub_id, ent_id=ent_id)
        assert_that(common_utils.validate_response_code(add_div_resp, 201))
        created_div_id = add_div_resp.json()['divisionID']

        add_loc_resp = self.create_location_api(div_id=created_div_id, ent_id=ent_id, sub_id=sub_id, loc_name=loc_name,
                                               is_admin=True)
        assert_that(common_utils.validate_response_code(add_loc_resp, 201))
        created_loc_id = add_loc_resp.json()['locationID']

        return created_div_id, div_name, created_loc_id, loc_name

    def del_div_loc(self, div_id=None, loc_id=None, sub_id=None):
        if div_id:
            del_div_resp = self.delete_division_api(div_id=div_id)
            assert_that(common_utils.validate_response_code(del_div_resp, 200))
            self.log.info(f'Deleted div_id - {div_id}!')
        if loc_id and sub_id:
            del_loc_resp = self.delete_location_v2_api(loc_id=loc_id, sub_id=sub_id, is_admin=True)
            assert_that(common_utils.validate_response_code(del_loc_resp, 200))
            self.log.info(f'Deleted loc_id - {loc_id}!')

    def get_divisions_with_locations(self, ent_id=None, exclude_divs=None):
        divisions = []
        all_locations = []

        # Parse JSON data
        div_resp = self.get_divisions_by_ent_id_api(ent_id=ent_id)
        data = div_resp.json()

        # Iterate over each division
        for division in data:
            if exclude_divs and division["divisionID"] in exclude_divs:
                continue  # Skip this division if it's in the exclusion list

            # Check if locations exist, not None, and not empty
            if division["locations"] is not None and len(division["locations"]) > 0:
                division_info = {
                    "divisionID": division["divisionID"],
                    "name": division["name"],
                    "locations": division["locations"]
                }
                divisions.append(division_info)
                all_locations.extend(division["locations"])

        return divisions, all_locations

    def get_all_loc_id_name_using_ent_id(self, ent_id=None):

        if not ent_id:
            return None

        loc_data = []

        divisions = self.get_divisions_by_ent_id_api(ent_id).json()

        for div in divisions:
            loc_resp = self.get_loc_in_div_paginated_api(div_id=div['divisionID'], is_admin=True)
            assert_that(common_utils.validate_response_code(loc_resp, 200))
            locations = loc_resp.json()['locations']
            for loc in locations:
                if not loc['archived']:
                    loc_data.append({'loc_id': loc['locationID'], 'loc_name': loc['name'], 'div_id': loc['divisionID']})

        return loc_data

    def pick_random_loc_id_name(self, loc_data=None, excluded_loc_ids=None):
        # if excluded_loc_ids is None:
        #     excluded_loc_ids = {'1234', '234252'}
        # if excluded_loc_names is None:
        #     excluded_loc_names = {'Default', 'auto'}

        # Filter loc_data to exclude specific loc_id and loc_name
        filtered_loc_data = [loc for loc in loc_data if loc['loc_id'] not in excluded_loc_ids]

        if filtered_loc_data:
            # Pick a random location from the filtered list
            random_loc = random.choice(filtered_loc_data)
            return random_loc['loc_id'], random_loc['loc_name']
        else:
            return None, None

    # Method to return multiple divisions and one location belonging to the return division
    def pick_random_div_and_loc(self, div_data=None, loc_data=None, no_of_required_div=2):

        # Filter div_data to select required number of divisions
        divisions = random.sample(div_data, min(no_of_required_div, len(div_data)))

        # Collect locations belonging to selected divisions
        selected_divs = []
        selected_loc = None
        for div in divisions:
            selected_divs.append(div['divisionID'])
            if not selected_loc:
                div_locs = [loc for loc in div['locations']]
                if div_locs:
                    selected_loc = random.choice(div_locs)

        return selected_divs, selected_loc

    # Method to return random multiple locations
    def pick_random_locs(self, loc_data=None, excluded_loc_ids=None):
        if excluded_loc_ids is None:
            excluded_loc_ids = set()

        # Filter loc_data to exclude specific loc_id
        filtered_loc_data = [loc for loc in loc_data if loc['loc_id'] not in excluded_loc_ids]

        if filtered_loc_data:
            # Pick a random location from the filtered list
            random_locs = random.sample(filtered_loc_data, min(len(filtered_loc_data), 2))
            return random_locs
        else:
            return None

    def get_multiple_divs_and_loc_in_ent(self, ent_id=None, no_of_req_div=2, exclude_divs=None):
        divs, locs = self.get_divisions_with_locations(ent_id=ent_id, exclude_divs=exclude_divs)
        selected_divs, selected_loc = self.pick_random_div_and_loc(div_data=divs, loc_data=locs,
                                                                   no_of_required_div=no_of_req_div)
        return selected_divs, selected_loc

    def build_exp_error_message_bpn_loc_response(self, bpn=''):
        """
        This method is to build the expected BPN error with BPN value
        so that error code and description can be validated.

        :param bpn: The BPN or account number required in the Location.
        :return: The built expected BPN error response in JSON.
        """

        with open(self.prop.get('CLIENT_MGMT', 'sample_bpn_loc_error_resp')) as file:
            exp_error_resp = json.load(file)

        if not bpn:
            pytest.fail(f'BPN is required to build the expected error message!')

        error_message = f'Invalid request: Location with BPN [{bpn}] already exists'
        exp_error_resp['errors'][0]['errorDescription'] = str(error_message)

        return exp_error_resp
