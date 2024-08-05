"""This module is used for addressbook api."""

import json
import logging
import time
import pandas as pd
from hamcrest import assert_that
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_string


class AddressbookAPI:
    """This class defines the method and element identifications for addressbook api."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.common = common_utils()
        self.api = APIUtilily()
        self.data_generator = DataGenerator(app_config)
        self.subs_api = SubscriptionAPI(app_config, access_token, client_token)
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['addrbook_api'])
        self.headers = {"Accept": "*/*"}
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def get_sub_id_from_addressbook_file(self, sub_type=None):
        """
        Retrieves the subscription ID from an address book JSON file.
        :param sub_type: The type of subscribed product. ex: PITNEYSHIP_PRO
        :return: The subscription ID corresponding to the provided subscription type.
        """
        if sub_type is None:
            return None

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'sample_addressbook_sub_ids')) as file:
            self.json_data = json.load(file)

        sub_id = self.json_data[self.prod_name][self.env][sub_type]
        return sub_id

    def get_sub_id_user_cred_from_addressbook_file(self, sub_type=None, user_type='E'):
        """
        Retrieves the subscription ID and user credentials from an address book JSON file.
        :param sub_type: The type of subscribed product. ex: PITNEYSHIP_PRO
        :param user_type: The type of client users. ex: Enterprise, Division, Location and User.
        :return: The subscription ID corresponding to the provided subscription type.
        """
        if sub_type is None:
            return None

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'sample_addressbook_subs_all_details')) as file:
            json_data = json.load(file)

        data = json_data[self.prod_name][self.env][sub_type]
        sub_id = data['sub_id']
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

        return sub_id, email, pwd

    def get_sub_id_ent_id_user_cred_from_addressbook_file(self, sub_type='PITNEYSHIP_PRO', user_type='E'):
        """
        Retrieves the subscription ID and user credentials from an address book JSON file.
        :param sub_type: The type of subscribed product. ex: PITNEYSHIP_PRO
        :param user_type: The type of client users. ex: Enterprise, Division, Location and User.
        :return: The subscription ID corresponding to the provided subscription type.
        """

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'sample_addressbook_subs_all_details')) as file:
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

    def get_plans_from_dynamic_template_file(self, plan_case=None):
        """
        Retrieves the plans from an address book dynamic template JSON file.
        :param plan_case: The plans case serves as key to retrieve the plans based on the case number.
        :return: The plans corresponding to the provided plan case.
        """
        if plan_case is None:
            return None

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'dynamic_template_plan_cases')) as file:
            json_data = json.load(file)

        plans = json_data[plan_case]['plans']
        csv_headers = json_data[plan_case]['csv_headers']

        return plans, csv_headers

    def add_new_contact_api(self, contact_type='', int_dlvry='', type='', name='', comp='', email='', phn='',
                            personal_id='', addr1='', city='', country='', postal='', state='', schema_name='',
                            sub_id='', is_admn=False, token=''):
        """
        This api is to create a new contact based on the user token.
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_new_contact_body')) as f:
            self.json_data = json.load(f)

        if contact_type:
            self.json_data['contactType'] = contact_type
        if int_dlvry:
            self.json_data['internalDelivery'] = int_dlvry
        if type:
            self.json_data['type'] = type
        if name:
            self.json_data['name'] = name
        if comp:
            self.json_data['company'] = comp
        if email:
            self.json_data['emails'][0]['email'] = email
        if phn:
            self.json_data['phones'][0]['phone'] = phn
        if personal_id:
            self.json_data['personalID'] = personal_id
        if addr1:
            self.json_data['addresses'][0]['addressLine1'] = addr1
        if city:
            self.json_data['addresses'][0]['city'] = city
        if country:
            self.json_data['addresses'][0]['countryCode'] = country
        if postal:
            self.json_data['addresses'][0]['postalCode'] = postal
        if state:
            self.json_data['addresses'][0]['state'] = state
        if sub_id:
            self.json_data['subscriptionId'] = sub_id

        if is_admn:
            create_contact_url = self.endpoint + '/api/v1/contact?admin=1&sId=' + sub_id + '&schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token
        elif token:
            create_contact_url = self.endpoint + '/api/v1/contact'
            self.headers['Authorization'] = token
        else:
            create_contact_url = self.endpoint + '/api/v1/contact'
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=create_contact_url, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def verify_add_new_contact_ssto_api(self, contact_type='', int_dlvry='', type='', name='', comp='', email='',
                                   phn='', personal_id='', addr1='', city='', country='', postal='', state='',
                                    div_id='',loc_id='',receiving_access_lvl='',
                                   sub_id='', is_admn='', schema_name=''):
        """
        This function is validates if a new admin contact can be created successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_new_contact_ssto_body')) as f:
            self.json_data = json.load(f)
        result = False

        if contact_type != "":
            self.json_data['contactType'] = contact_type

        if int_dlvry != "":
            self.json_data['internalDelivery'] = int_dlvry

        if type != "":
            self.json_data['type'] = type

        if name != "":
            self.json_data['name'] = name

        if comp != "":
            self.json_data['company'] = comp

        if email != "":
            self.json_data['emails'][0]['email'] = email

        if phn != "":
            self.json_data['phones'][0]['phone'] = phn

        if personal_id != "":
            self.json_data['personalID'] = personal_id

        if addr1 != "":
            self.json_data['addresses'][0]['addressLine1'] = addr1

        if city != "":
            self.json_data['addresses'][0]['city'] = city

        if country != "":
            self.json_data['addresses'][0]['countryCode'] = country

        if postal != "":
            self.json_data['addresses'][0]['postalCode'] = postal

        if state != "":
            self.json_data['addresses'][0]['state'] = state

        if div_id != "":
            self.json_data['divisionId'] = div_id

        if loc_id != "":
            self.json_data['locationId'] = loc_id

        if receiving_access_lvl !="":
            self.json_data['receivingAccessLevel'] = receiving_access_lvl

        if sub_id != "":
            self.json_data['subscriptionId'] = sub_id

        if is_admn == 'y':
            create_contact_endPoint = self.endpoint + "/api/v1/contact?admin=1&sId=" + sub_id + "&schema_name=" + schema_name
            self.headers['Authorization'] = self.admin_token

        else:
            create_contact_endPoint = self.endpoint + "/api/v1/contact"
            self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=create_contact_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def add_contact_api(self, cont_id='', contact_type='', int_dlvry='', type='S', name='', comp='',
                        email='', label='Home', phone='', personal_id='', addr1='', city='',
                        country='', postal='', state='', schema='', sub_id=None, is_admin=False,
                        admin_token=None, client_token=None):

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_contact_req')) as f:
            self.json_data = json.load(f)

        if cont_id:
            self.json_data['id'] = cont_id
            self.json_data['emails'][0]['id'] = cont_id
            self.json_data['phones'][0]['id'] = cont_id
            self.json_data['addresses'][0]['id'] = cont_id

        if label:
            self.json_data['emails'][0]['label'] = label
            self.json_data['phones'][0]['label'] = label
            self.json_data['addresses'][0]['label'] = label

        if contact_type:
            self.json_data['contactType'] = contact_type

        if int_dlvry:
            self.json_data['internalDelivery'] = int_dlvry

        if type:
            self.json_data['type'] = type

        if name:
            self.json_data['name'] = name

        if comp:
            self.json_data['company'] = comp

        if email:
            self.json_data['emails'][0]['email'] = email

        if phone:
            self.json_data['phones'][0]['phone'] = phone

        if personal_id:
            self.json_data['personalID'] = personal_id

        if addr1:
            self.json_data['addresses'][0]['addressLine1'] = addr1

        if city:
            self.json_data['addresses'][0]['city'] = city

        if country:
            self.json_data['addresses'][0]['countryCode'] = country

        if postal:
            self.json_data['addresses'][0]['postalCode'] = postal

        if state:
            self.json_data['addresses'][0]['state'] = state

        if not schema:
            schema = generate_random_string(uppercase=False, char_count=8)

        if is_admin:
            self.json_data['subscriptionId'] = sub_id
            add_contact_url = f'{self.endpoint}/api/v2/contact?admin=true&sId={sub_id}&schema_name={schema}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            add_contact_url = f'{self.endpoint}/api/v2/contact'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=add_contact_url,
                                              headers=self.headers, body=json.dumps(self.json_data))
        return response

    def update_contact_using_client_user_api(self, cont_id='', contact_type='', int_dlvry='', address_type='S', name='',
                                             comp='', email='', label='Home', phone='', personal_id='', addr1='',
                                             city='', country='', postal='', state='', contact_id='', client_token=None):

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_contact_req')) as f:
            payload = json.load(f)

        def set_payload_value(key, value):
            if value != '':
                payload[key] = value

        set_payload_value('id', cont_id)
        set_payload_value('email', email)
        set_payload_value('phone', phone)
        set_payload_value('addressLine1', addr1)
        set_payload_value('label', label)
        set_payload_value('contactType', contact_type)
        set_payload_value('internalDelivery', int_dlvry)
        set_payload_value('type', address_type)
        set_payload_value('name', name)
        set_payload_value('company', comp)
        set_payload_value('personalID', personal_id)
        set_payload_value('addressLine1', addr1)
        set_payload_value('city', city)
        set_payload_value('countryCode', country)
        set_payload_value('postalCode', postal)
        set_payload_value('state', state)

        add_contact_url = f"{self.endpoint}/api/v1/contact/{contact_id}"
        self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.put_api_response(endpoint=add_contact_url,
                                             headers=self.headers, body=json.dumps(payload))
        return response

    def verify_search_admin_api(self, sub_id):
        """
        This test fetches the details of admin
        :return: this function returns boolean status of element located
        """
        search_admin_endpoint = self.endpoint + "/api/v1/contacts?admin=1&sId=" + sub_id
        self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(endpoint=search_admin_endpoint, headers=self.headers)

        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def get_contact_by_personal_id_api(self, sub_id='', personal_id='', is_admin=False, token=''):
        """
        This test fetches the details of admin
        :return: this function returns boolean status of element located
        """
        if is_admin:
            get_contact_per_id_url = self.endpoint + '/api/v1/contacts/subscriptions/' \
                                     + sub_id + '/personalId/' + personal_id
            self.headers['Authorization'] = self.admin_token
        elif token:
            get_contact_per_id_url = self.endpoint + '/api/v1/contacts/personalId/' + personal_id
            self.headers['Authorization'] = token
        else:
            get_contact_per_id_url = self.endpoint + '/api/v1/contacts/personalId/' + personal_id
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_contact_per_id_url, headers=self.headers)
        return response

    def patch_v1_delete_contact_api(self, cont_id='', schema_name='', sub_id=None,
                                    is_admin=False, admin_token=None, client_token=None):
        """
               This test deletes the created contact from sp360
               :return: this function returns boolean status of element located
               """

        if is_admin:
            del_contact_url = f"{self.endpoint}/api/v1/contacts/delete?admin=1&sId={sub_id}&schema_name={schema_name}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            del_contact_url = f"{self.endpoint}/api/v1/contacts/delete"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.patch_api_response(endpoint=del_contact_url, headers=self.headers,
                                               body=json.dumps([cont_id]))
        return response

    def patch_v2_delete_contact_api(self, cont_id=None, cont_type='RECIPIENT', address_type='ALL', sub_id=None,
                                    is_admin=False, admin_token=None, client_token=None):

        payload = cont_id

        if not isinstance(cont_id, list):
            payload = [cont_id]

        if is_admin:
            # the admin url needs to be updated, checking with dev
            del_contact_url = f"{self.endpoint}/api/v2/contacts/delete?admin=True&sId={sub_id}&contactType={cont_type}&type={address_type}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            del_contact_url = f"{self.endpoint}/api/v2/contacts/delete?contactType={cont_type}&type={address_type}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.patch_api_response(endpoint=del_contact_url, headers=self.headers, body=json.dumps(payload))
        return response

    def verify_delete_contact_ssto_api(self, cont_id='', schema_name='', sub_id='', is_admin=''):
        """
               This test deletes the created contact from sp360
               :return: this function returns boolean status of element located
               """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'delete_address_body')) as f:
            self.json_data = json.load(f)
        result = False

        if is_admin == 'y':
            del_contact_endpoint = (self.endpoint + "/api/v1/contacts/delete?admin=1&sId=" + sub_id +
                                    "&schema_name=" + schema_name + "&ssto=true")
            self.headers['Authorization'] = self.admin_token
        else:
            del_contact_endpoint = self.endpoint + "/api/v1/contacts/delete?ssto=true"
            self.headers['Authorization'] = self.client_token

        res = self.api.patch_api_response(endpoint=del_contact_endpoint, headers=self.headers,
                                          body=json.dumps([cont_id]))
        status_code = res.status_code
        return status_code

    def verify_delete_contact_admin_api(self, cont_id, sub_id='', is_admin=''):
        """
        This test deletes the created address
        :return: this function returns boolean status of element located
        """
        if is_admin=='y':

            del_contact_endpoint = self.endpoint + "/api/v1/contact/" + cont_id + "?admin=1&sId=" + sub_id
            self.headers['Authorization'] = self.admin_token
        else:
            del_contact_endpoint = self.endpoint + "/api/v1/contact/" + cont_id
            self.headers['Authorization'] = self.client_token

        res = self.api.delete_api_response(
            endpoint=del_contact_endpoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def delete_address_by_contact_id_api(self, contact_id='', client_token=None):

        del_address_url = f"{self.endpoint}/api/v1/contact/{contact_id}"
        self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.delete_api_response(endpoint=del_address_url, headers=self.headers)
        return response

    def get_contact_by_cont_id_api(self, contact_id='', sub_id=None, is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches the details of contact by contact Id
        :return: this function returns boolean status of element located
        """

        if is_admin:
            get_contact_url = f"{self.endpoint}/api/v1/contact/{contact_id}?admin=1&sId={sub_id}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_contact_url = f"{self.endpoint}/api/v1/contact/{contact_id}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_contact_url, headers=self.headers)
        return response

    def update_contact_api(self, id='', contact_type='', int_dlvry='', type='', name='', comp='', email='',
                           phn='', personal_id='', addr1='', addr2='', addr3='', city='', country='', postal='',
                           state='', sub_id='', is_admn=False, cont_id='', schema_name='', token=''):
        """
        This function is validates if a created contact can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_new_contact_body')) as f:
            self.json_data = json.load(f)

        if id:
            self.json_data['id'] = id
        if contact_type:
            self.json_data['contactType'] = contact_type
        if int_dlvry:
            self.json_data['internalDelivery'] = int_dlvry
        if type:
            self.json_data['type'] = type
        if name:
            self.json_data['name'] = name
        if comp:
            self.json_data['company'] = comp
        if email:
            self.json_data['emails'][0]['email'] = email
        if phn:
            self.json_data['phones'][0]['phone'] = phn
        if personal_id:
            self.json_data['personalID'] = personal_id
        if addr1:
            self.json_data['addresses'][0]['addressLine1'] = addr1
        if addr2:
            self.json_data['addresses'][0]['addressLine2'] = addr2
        if addr3:
            self.json_data['addresses'][0]['addressLine3'] = addr3
        if city:
            self.json_data['addresses'][0]['city'] = city
        if country:
            self.json_data['addresses'][0]['countryCode'] = country
        if postal:
            self.json_data['addresses'][0]['postalCode'] = postal
        if state:
            self.json_data['addresses'][0]['state'] = state
        if sub_id:
            self.json_data['subscriptionId'] = sub_id

        if is_admn:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id + '?admin=1&sId=' \
                                 + sub_id + '&schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token
        elif token:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id
            self.headers['Authorization'] = token
        else:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(endpoint=update_contact_url, headers=self.headers,
                                             body=json.dumps(self.json_data))
        return response

    def patch_update_contact_api(self, id='', contact_type='', int_dlvry='', type='', name='', comp='', email='',
                                   phn='', personal_id='', addr1='', addr2='', addr3='', city='', country='', postal='',
                                   state='', addedDepartmentIds=None, enableVisitorLimit='', sub_id='', is_admn=False,
                                   cont_id='', schema_name='', token=''):

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'patch_partial_update_contact_req')) as f:
            self.json_data = json.load(f)

        if id:
            self.json_data['id'] = id
        if contact_type:
            self.json_data['contactType'] = contact_type
        if int_dlvry:
            self.json_data['internalDelivery'] = int_dlvry
        if type:
            self.json_data['type'] = type
        if name:
            self.json_data['name'] = name
        if comp:
            self.json_data['company'] = comp
        if email:
            self.json_data['emails'][0]['email'] = email
        if phn:
            self.json_data['phones'][0]['phone'] = phn
        if personal_id:
            self.json_data['personalID'] = personal_id
        if addr1:
            self.json_data['addresses'][0]['addressLine1'] = addr1
        if addr2:
            self.json_data['addresses'][0]['addressLine2'] = addr2
        if addr3:
            self.json_data['addresses'][0]['addressLine3'] = addr3
        if city:
            self.json_data['addresses'][0]['city'] = city
        if country:
            self.json_data['addresses'][0]['countryCode'] = country
        if postal:
            self.json_data['addresses'][0]['postalCode'] = postal
        if state:
            self.json_data['addresses'][0]['state'] = state
        if sub_id:
            self.json_data['subscriptionId'] = sub_id
        if addedDepartmentIds:
            self.json_data['addedDepartmentIds'] = addedDepartmentIds
        if enableVisitorLimit:
            self.json_data['staff']['enableVisitorLimit'] = enableVisitorLimit

        if is_admn:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id + '?admin=1&sId=' \
                                 + sub_id + '&schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token
        elif token:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id
            self.headers['Authorization'] = token
        else:
            update_contact_url = self.endpoint + '/api/v1/contact/' + cont_id
            self.headers['Authorization'] = self.client_token

        response = self.api.patch_api_response(endpoint=update_contact_url, headers=self.headers,
                                               body=json.dumps(self.json_data))
        return response

    def verify_update_ssto_contact_api(self, id='', contact_type='', int_dlvry='', type='', name='', comp='', email='',
                                         phn='', personal_id='', addr1='', addr2='', addr3='', city='', country='', postal='', state='',
                                         receiving_access_lvl='',sub_id='', is_admn='', cont_id='', schema_name=''
                                         ):
        """
        This function is validates if a created contact can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_new_contact_body')) as f:
            self.json_data = json.load(f)
        result = False

        if id != "":
            self.json_data['id'] = id

        if contact_type != "":
            self.json_data['contactType'] = contact_type

        if int_dlvry != "":
            self.json_data['internalDelivery'] = int_dlvry

        if type != "":
            self.json_data['type'] = type

        if name != "":
            self.json_data['name'] = name

        if comp != "":
            self.json_data['company'] = comp

        if email != "":
            self.json_data['emails'][0]['email'] = email

        if phn != "":
            self.json_data['phones'][0]['phone'] = phn

        if personal_id != "":
            self.json_data['personalID'] = personal_id

        if addr1 != "":
            self.json_data['addresses'][0]['addressLine1'] = addr1

        if addr2 != "":
            self.json_data['addresses'][0]['addressLine2'] = addr2

        if addr3 != "":
            self.json_data['addresses'][0]['addressLine3'] = addr3

        if city != "":
            self.json_data['addresses'][0]['city'] = city

        if country != "":
            self.json_data['addresses'][0]['countryCode'] = country

        if postal != "":
            self.json_data['addresses'][0]['postalCode'] = postal

        if state != "":
            self.json_data['addresses'][0]['state'] = state

        if receiving_access_lvl != "":
            self.json_data['receivingAccessLevel'] = receiving_access_lvl

        if sub_id != "":
            self.json_data['subscriptionId'] = sub_id

        if is_admn == 'y':
            updt_contact_endPoint = self.endpoint + "/api/v1/contact/"+cont_id+"?admin=1&sId=" + sub_id+"&schema_name="+schema_name
            self.headers['Authorization'] = self.admin_token

        else:
            updt_contact_endPoint = self.endpoint + "/api/v1/contact/"+cont_id
            self.headers['Authorization'] = self.client_token

        res = self.api.put_api_response(
            endpoint=updt_contact_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if status_code !=200:
            return res, status_code
        else:
            return status_code

    def search_address_api(self, sub_id=None, param_val='', is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches the details of contact by user Id
        :return: this function returns boolean status of element located
        """

        if is_admin:
            search_address_url = f"{self.endpoint}/api/v1/contacts?&admin=1&sId={sub_id}&{param_val}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            search_address_url = f"{self.endpoint}/api/v1/contacts?&{param_val}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=search_address_url, headers=self.headers)
        return response

    def verify_search_address_by_type_api(self, addr_type='', is_admin='', sub_id='',param_val=''):
        """
        This test fetches the details of contact by user Id
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            search_addr_endpoint = (self.endpoint + "/api/v1/contacts/"+addr_type+"?&admin=1&sId="
                                    + sub_id + "&" + param_val)
            self.headers['Authorization'] = self.admin_token

        else:
            search_addr_endpoint = self.endpoint + "/api/v1/contacts/"+addr_type+"?&"+param_val
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(endpoint=search_addr_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            res = res.json()
        return res, status_code

    def contact_upload_file_api(self, nick_name='', comp='', import_file_type='', sub_id='', offc_id='', mail_id='',
                                email='', personal_id='', pvt_personal_id='', schema_name='', is_admin=False,
                                admin_token=None, client_token=None):
        """
        This function validates that locations can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if import_file_type == 'sp_360':
            addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'sp_360_template')

            df = pd.read_csv(addr_file)
            df.loc[0, 'Nick Name'] = nick_name
            df.loc[0, 'Company'] = comp
            df.loc[0, 'Email'] = email
            df.loc[0, 'PersonalID'] = personal_id
            df.to_csv(addr_file, index=False)

            f = open(self.prop.get('ADDRESSBOOK_MGMT', 'sp_360_template'))

            files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'sp_360_template'), f)}

        elif import_file_type == 'UPS':
            addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'ups_import_template')

            df = pd.read_csv(addr_file)
            df.loc[0, 'Nick Name'] = nick_name
            df.loc[0, 'Contact Name'] = nick_name
            df.loc[0, 'Company Name'] = comp
            df.loc[0, 'Contact Email'] = email
            df.loc[0, 'PersonalID'] = personal_id
            df.to_csv(addr_file, index=False)

            f = open(self.prop.get('ADDRESSBOOK_MGMT', 'ups_import_template'))

            files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'ups_import_template'), f)}

        elif import_file_type == 'fedEx':
            addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'fedex_import_template')

            df = pd.read_csv(addr_file)
            df.loc[0, 'Nickname'] = nick_name
            df.loc[0, 'FullName'] = nick_name
            df.loc[0, 'Company'] = comp
            df.loc[0, 'EmailAddress'] = email
            df.loc[0, 'PersonalID'] = personal_id
            df.to_csv(addr_file, index=False)

            f = open(self.prop.get('ADDRESSBOOK_MGMT', 'fedex_import_template'))
            files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'fedex_import_template'), f)}

        elif import_file_type == 'SPO':
            addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'spo_import_template')

            df = pd.read_csv(addr_file)
            df.loc[0, 'Name'] = nick_name
            df.loc[0, 'Company'] = comp
            df.loc[0, 'Email'] = email
            df.loc[0, 'PersonalID'] = personal_id
            df.to_csv(addr_file, index=False)

            f = open(self.prop.get('ADDRESSBOOK_MGMT', 'spo_import_template'))

            files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'spo_import_template'), f)}

        elif import_file_type == 'ssto':
            addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'ssto_import_template')

            df = pd.read_csv(addr_file)
            df.loc[0, 'Name'] = nick_name
            df.loc[0, 'Company'] = comp
            df.loc[0, 'Email'] = email
            df.loc[0, 'PersonalID'] = personal_id

            if offc_id !='':
                df.loc[0, 'OfficeLocation'] = offc_id

            if mail_id !='':
                df.loc[0, 'MailStopID'] = mail_id

            df.to_csv(addr_file, index=False)

            f = open(self.prop.get('ADDRESSBOOK_MGMT', 'ssto_import_template'))

            files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'ssto_import_template'), f)}

        if is_admin:
            import_contact_url = f'{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks' \
                                 f'/upload?schema_name={schema_name}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            import_contact_url = f'{self.endpoint}/api/v1/contacts/addressbooks/upload'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=import_contact_url, files=files, headers=self.headers)
        return response

    def import_overwrite_upload_file_api(self, name='', contact_type='', address_type='', personal_id='', sub_id=None,
                                         schema_name='', is_admin=False, admin_token=None, client_token=None):
        """
        This function validates that contacts can be overwritten through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        overwrite_addr_file = self.prop.get('ADDRESSBOOK_MGMT', 'data_load_file')

        df = pd.read_csv(overwrite_addr_file)
        df.loc[0, 'Name'] = name
        df.loc[0, 'ContactType'] = contact_type
        df.loc[0, 'Type'] = address_type
        df.loc[0,'PersonalID'] = personal_id

        df.to_csv(overwrite_addr_file, index=False)

        f = open(self.prop.get('ADDRESSBOOK_MGMT', 'data_load_file'))
        files = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'data_load_file'), f)}

        if is_admin:
            address_upload_url = (f"{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}"
                                  f"/addressbooks/upload?schema_name={schema_name}")
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            address_upload_url = f"{self.endpoint}/api/v1/contacts/addressbooks/upload"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=address_upload_url, files=files, headers=self.headers)
        return response

    def addressbook_mapping_api(self, job_id='', import_file_type='', sub_id='', schema_name='', overwrite='',
                                type_overridden='', is_admin=False, admin_token=None, client_token=None):
        """
        This function uploads the file with suggested mapping (Positive scenario)
        :return: this function returns boolean status of element located
        """
        payload = None
        if import_file_type == 'sp_360':
            payload = {
                'fieldsMapping': '{"Name": "Nick Name", "CountryCode": "Country", "Company": "Company", "StateProvince": "State", "PostalCode": "Postal/ZIP Code", "Email": "Email", "PersonalID":"PersonalID"}'}

        elif import_file_type == 'UPS':
            payload = {
                'fieldsMapping': '{"Name": "Contact Name", "CountryCode": "Country", "Company": "Company Name","StateProvince":"St/Prov", "PostalCode": "Postal Cd", "CityTown" :  "City", "Email" : "Contact Email", "Phone" :"Contact Phone", "LocationID" : "Loc ID", "StateProvince" : "St/Prov", "AddressLine1": "Street Address Line 1", "AddressLine2" : "Street Address Line 2" , "AddressLine3" : "Street Address Line 3","PersonalID":"PersonalID"}'}

        elif import_file_type == 'fedEx':
            payload = {
                'fieldsMapping': '{"Name": "FullName", "CountryCode": "CountryCode", "Company": "Company", "StateProvince": "State", "PostalCode": "Zip", "AddressLine1": "AddressOne", "AddressLine2": "AddressTwo", "Email": "EmailAddress", "State": "StateProvince", "PostalCode": "Zip", "Title": "Title","PersonalID":"PersonalID"}'}

        elif import_file_type == 'SPO':
            payload = {
                'fieldsMapping': '{"City":"CityTown","Company":"Company","Country":"CountryCode","Email":"Email","Name":"Name","Phone":"Phone","Postal/ZIP Code":"PostalCode","State/Province":"StateProvince","Street Address 1":"AddressLine1","Street Address 2":"AddressLine2","Street Address 3":"AddressLine3"}'}


        elif import_file_type == 'ssto':
            payload = {
                'fieldsMapping': '{"Type":"Type", "Company":"Company","Name": "Name","AddressLine1": "Street Address 1","AddressLine2": "Street Address 2","AddressLine3": "Street Address 3","CityTown": "City", "StateProvince": "State/Province", "PostalCode": "Postal/ZIPCode", "CountryCode": "Country", "Email": "Email", "Phone": "Phone", "PersonalID": "PersonalID","OfficeLocation": "OfficeLocation", "NotificationAll": "NotificationAll", "Accessibility": "Accessibility","MailStopID": "MailStopID"}'}

        elif import_file_type == 'dataload' and overwrite==True and type_overridden=='S':
            payload = {
                'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": "AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", "Company": "Company", "Company": "Company",  "CountryCode": "CountryCode", "PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", "StateProvince": "StateProvince", "Type": "Type"}', 'overwrite': 'true','typeOverridden': 'S'}

        elif import_file_type == 'dataload' and overwrite == True and type_overridden == 'U':
            payload = {
                'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": "AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", "Company": "Company", "Company": "Company",  "CountryCode": "CountryCode", "PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", "StateProvince": "StateProvince", "Type": "Type"}',
                'overwrite': 'true', 'typeOverridden': 'U'}

        elif import_file_type == 'dataload' and overwrite == True and type_overridden == 'ALL':
            payload = {
                'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": "AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", "Company": "Company", "Company": "Company",  "CountryCode": "CountryCode", "PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", "StateProvince": "StateProvince", "Type": "Type"}',
                'overwrite': 'true', 'typeOverridden': 'ALL'}

        else:
            self.log.error("Please provide a valid file type")

        if is_admin:
            import_status_url = f'{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks' \
                                f'/jobs/{job_id}/process?schema_name={schema_name}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            import_status_url = f'{self.endpoint}/api/v1/contacts/addressbooks/jobs/{job_id}/process'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=import_status_url, headers=self.headers, body=payload)
        return response

    def verify_import_status_api(self, job_id='', subId='', is_admin='', schema_name=''):
        """
        This test fetches the status of uploaded records
        :return: this function returns boolean status of element located
        """

        if is_admin=='y':
            uploaded_records_url = self.endpoint + "/api/v1/contacts/subscriptions/" + subId + "/addressbooks/jobs/" \
                                   + job_id + "/status?schema_name=" + schema_name
            self.headers['Authorization'] = self.admin_token
        else:
            uploaded_records_url = self.endpoint + "/api/v1/contacts/addressbooks/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(endpoint=uploaded_records_url, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
        return res, status_code

    def process_import_contacts(self, name='', contact_type='', level_type='', personal_id='',  is_admin=False,
                                sub_id='', schema_name='', import_file_type='dataload', overwrite=True,
                                type_overridden=''):

        import_contact_file = self.prop.get('ADDRESSBOOK_MGMT', 'import_address_book')

        df = pd.read_csv(import_contact_file)
        df.loc[0, 'Name'] = name
        df.loc[0, 'ContactType'] = contact_type
        df.loc[0, 'Type'] = level_type
        df.loc[0, 'PersonalID'] = personal_id

        df.to_csv(import_contact_file, index=False)

        f = open(self.prop.get('ADDRESSBOOK_MGMT', 'import_address_book'))

        files = {"file": (import_contact_file, f)}

        if is_admin:
            upload_url = self.endpoint + '/api/v1/contacts/subscriptions/' + sub_id \
                         + '/addressbooks/upload?schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token
        else:
            upload_url = self.endpoint + '/api/v1/contacts/addressbooks/upload'
            self.headers['Authorization'] = self.client_token

        upload_resp = self.api.post_api_response(endpoint=upload_url, files=files, headers=self.headers)
        assert_that(self.common.validate_response_code(upload_resp, 200))
        job_id = upload_resp.json()['jobId']

        if import_file_type == 'sp_360':
            payload = {'fieldsMapping': '{"Name": "Nick Name", "CountryCode": "Country", "Company": "Company", '
                                        '"StateProvince": "State", "PostalCode": "Postal/ZIP Code", "Email": "Email", '
                                        '"PersonalID":"PersonalID"}'}

        elif import_file_type == 'UPS':
            payload = {'fieldsMapping': '{"Name": "Contact Name", "CountryCode": "Country", "Company": "Company Name",'
                                        '"StateProvince": "St/Prov", "PostalCode": "Postal Cd", "CityTown" : "City", '
                                        '"Email" : "Contact Email", "Phone" : "Contact Phone", "LocationID" : '
                                        '"Loc ID", "StateProvince" : "St/Prov", "AddressLine1": '
                                        '"Street Address Line 1", "AddressLine2" : "Street Address Line 2" , '
                                        '"AddressLine3" : "Street Address Line 3","PersonalID":"PersonalID"}'}

        elif import_file_type == 'fedEx':
            payload = {'fieldsMapping': '{"Name": "FullName", "CountryCode": "CountryCode", "Company": "Company", '
                                        '"StateProvince": "State", "PostalCode": "Zip", "AddressLine1": "AddressOne", '
                                        '"AddressLine2": "AddressTwo", "Email": "EmailAddress", "State": '
                                        '"StateProvince", "PostalCode": "Zip", "Title": "Title",'
                                        '"PersonalID":"PersonalID"}'}

        elif import_file_type == 'SPO':
            payload = {'fieldsMapping': '{"City": "CityTown", "Company": "Company", "Country": "CountryCode", '
                                        '"Email": "Email", "Name":"Name", "Phone": "Phone", '
                                        '"Postal/ZIP Code": "PostalCode", "State/Province": "StateProvince", '
                                        '"Street Address 1": "AddressLine1", "Street Address 2": "AddressLine2", '
                                        '"Street Address 3": "AddressLine3"}'}

        elif import_file_type == 'ssto':
            payload = {'fieldsMapping': '{"Type": "Type", "Company": "Company", "Name": "Name", '
                                        '"AddressLine1": "Street Address 1", "AddressLine2": "Street Address 2", '
                                        '"AddressLine3": "Street Address 3", "CityTown": "City", "StateProvince": '
                                        '"State/Province", "PostalCode": "Postal/ZIPCode", "CountryCode": "Country", '
                                        '"Email": "Email", "Phone": "Phone", "PersonalID": "PersonalID", '
                                        '"OfficeLocation": "OfficeLocation", "NotificationAll": "NotificationAll", '
                                        '"Accessibility": "Accessibility", "MailStopID": "MailStopID"}'}

        elif import_file_type == 'dataload' and overwrite and type_overridden == 'S':
            payload = {'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": '
                                        '"AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", '
                                        '"Company": "Company", "Company": "Company", "CountryCode": "CountryCode", '
                                        '"PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", '
                                        '"StateProvince": "StateProvince", "Type": "Type"}',
                       'overwrite': 'true', 'typeOverridden': 'S'}

        elif import_file_type == 'dataload' and overwrite and type_overridden == 'U':
            payload = {'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": '
                                        '"AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", '
                                        '"Company": "Company", "Company": "Company", "CountryCode": "CountryCode", '
                                        '"PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", '
                                        '"StateProvince": "StateProvince", "Type": "Type"}',
                       'overwrite': 'true', 'typeOverridden': 'U'}

        elif import_file_type == 'dataload' and overwrite and type_overridden == 'ALL':
            payload = {'fieldsMapping': '{"Name": "Name", "AddressLine1": "AddressLine1", "AddressLine2": '
                                        '"AddressLine2", "AddressLine3": "AddressLine3", "CityTown": "CityTown", '
                                        '"Company": "Company", "Company": "Company", "CountryCode": "CountryCode", '
                                        '"PersonalID": "PersonalID", "Phone": "Phone", "PostalCode": "PostalCode", '
                                        '"StateProvince": "StateProvince", "Type": "Type"}',
                       'overwrite': 'true', 'typeOverridden': 'ALL'}

        else:
            self.log.error("Please provide a valid file type")

        if is_admin:
            process_url = self.endpoint + '/api/v1/contacts/subscriptions/' + sub_id + '/addressbooks/jobs/' \
                          + job_id + '/process?schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token

        else:
            process_url = self.endpoint + '/api/v1/contacts/addressbooks/jobs/' + job_id + '/process'
            self.headers['Authorization'] = self.client_token

        process_resp = self.api.post_api_response(endpoint=process_url, headers=self.headers, body=payload)
        assert_that(self.common.validate_response_code(process_resp, 200))
        import_job_status = process_resp.json()['Status']

        if is_admin:
            job_status_url = self.endpoint + '/api/v1/contacts/subscriptions/' + sub_id + '/addressbooks/jobs/' \
                             + job_id + '/status?schema_name=' + schema_name
            self.headers['Authorization'] = self.admin_token
        else:
            job_status_url = self.endpoint + '/api/v1/contacts/addressbooks/jobs/' + job_id + '/status'
            self.headers['Authorization'] = self.client_token

        while import_job_status != 'Processed':
            job_status_resp = self.api.get_api_response(endpoint=job_status_url, headers=self.headers)
            import_job_status = job_status_resp.json()['status']

    def get_completed_job_status(self, is_admin='y', job_id='', sub_id='', schema_name=''):

        job_status = 'FileInProgress'
        res = None
        while job_status == 'FileInProgress':
            res, status_code = self.verify_import_status_api(job_id=job_id, subId=sub_id, is_admin=is_admin,
                                                             schema_name=schema_name)
            job_status = str(res['status'])
        else:
            return res

    def check_job_status(self, job_id='', sub_id='', is_admin=True, admin_token=None, client_token=None):
        job_status = None
        max_iterations = 10
        wait_time = 10

        for itr in range(1, max_iterations + 1):
            self.log.info(f'{itr}. Waiting for {wait_time} seconds before checking for the job status!')
            time.sleep(wait_time)

            status_resp = self.contacts_import_job_status_api(job_id=job_id, sub_id=sub_id, is_admin=is_admin,
                                                              admin_token=admin_token, client_token=client_token)
            assert_that(self.common.validate_response_code(status_resp, 200))
            job_status = status_resp.json()['status']

            if job_status == 'Processed':
                self.log.info(f'Import job {job_id} Processed!')
                return job_status
            elif job_status == 'ProcessingError':
                records = status_resp.json().get('records')
                failed_records = status_resp.json().get('failedRecords')
                success_records = status_resp.json().get('successfulRecords')
                error_file_base64 = status_resp.json().get('errorsFileLocation')
                error_file_location = self.common.decode_base_64(coded_string=error_file_base64)

                self.log.error(f'Import job {job_id} failed! '
                               f'\nTotal records: {records}, success: {success_records}, failed: {failed_records}'
                               f'\n Download error import file: {error_file_location}')
                return job_status

        self.log.error(f'Import job {job_id} is taking longer time and stuck at {job_status}!')
        return job_status

    # Methods for Department APIs

    def get_departments_api(self, sub_id=None, skip='0', limit='20', query='',
                            is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches all the departments present in a subId
        :return: this function returns boolean status of element located
        """

        if is_admin:
            get_dept_url = f'{self.endpoint}/api/v2/departments?subID={sub_id}&skip={skip}&limit={limit}&query={query}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_dept_url = f'{self.endpoint}/api/v2/departments?skip={skip}&limit={limit}&query={query}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_dept_url, headers=self.headers)
        return response

    def verify_get_dept_by_loc_id_api(self, sub_id='', loc_id='', is_admin=''):
        """
        This test fetches all the departments present in a location
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            get_dept_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/location/" + loc_id + "/departments?"
            self.headers['Authorization'] = self.admin_token

        else:
            get_dept_endpoint = self.endpoint + "/api/v1/location/" + loc_id + "/departments?"
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_dept_endpoint, headers=self.headers)
        status_code = res.status_code

        if status_code == 200:
            is_paginated = self.api.pagination_util(endpoint=get_dept_endpoint, headers=self.headers)

        else:
            is_paginated = False

        if res is not None:
            res = res.json()
        return res, status_code, is_paginated

    def add_dept_api(self, name='', loc_id='', sub_id='', is_admin=False, admin_token=None, client_token=None):
        """
        This function validates if a department can be created successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_department_with_loc')) as dept_body:
            payload = json.load(dept_body)

        if name:
            payload['name'] = name
        if loc_id:
            payload['locationID'] = loc_id

        if is_admin:
            add_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            add_dept_url = f'{self.endpoint}/api/v1/departments'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=add_dept_url, headers=self.headers, body=json.dumps(payload))
        return response

    def verify_add_dept_without_loc_api(self, name='', is_admin='', sub_id=''):
        """
        This function validates if a department can be created successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'add_department_without_loc')) as dept_body:
            self.json_data = json.load(dept_body)
        result = False

        if name != "":
            self.json_data['name'] = name

        if is_admin == 'y':

            add_dept_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/departments"
            self.headers['Authorization'] = self.admin_token

        else:
            add_dept_endPoint = self.endpoint + "/api/v1/departments"
            self.headers['Authorization'] = self.client_token

        res = self.api.post_api_response(
            endpoint=add_dept_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def update_dept_api(self, cont1=None, cont2=None, sub_id=None, dept_id=None, is_key_cont1=False, is_key_cont2=False,
                        is_remove_cont1=False, is_remove_cont2=False, is_admin=False, admin_token=False, client_token=False):
        """
        This function validates if a department can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'update_dept')) as file:
            payload = json.load(file)

        if cont1:
            payload[0]['contactId'] = cont1
            payload[0]['isKeyContact'] = is_key_cont1
            payload[0]['isRemove'] = is_remove_cont1

        if cont2:
            payload[1]['contactId'] = cont2
            payload[1]['isKeyContact'] = is_key_cont2
            payload[1]['isRemove'] = is_remove_cont2

        if is_admin:
            update_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            update_dept_url = f'{self.endpoint}/api/v1/departments/{dept_id}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.put_api_response(endpoint=update_dept_url, headers=self.headers, body=json.dumps(payload))
        return response

    def patch_update_dept_api(self, operation_type='', cont1='', cont2='', is_key_cont1=False, is_key_cont2=False, sub_id=None, dept_id=None,
                              is_admin=False, admin_token=None, client_token=None):
        """
        This function validates that department can be updated by patch APIs successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'patch_update_dept_req')) as file:
            payload = json.load(file)

        if operation_type:
            payload['operationType'] = operation_type

        if cont1:
            payload['contacts'][0]['contactId'] = cont1
            payload['contacts'][0]['isKeyContact'] = is_key_cont1

        if cont2:
            payload['contacts'][1]['contactId'] = cont2
            payload['contacts'][1]['isKeyContact'] = is_key_cont2

        if is_admin:
            update_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}/contacts'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            update_dept_url = f'{self.endpoint}/api/v1/departments/{dept_id}/contacts'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.patch_api_response(endpoint=update_dept_url, headers=self.headers, body=json.dumps(payload))
        return response

    def get_dept_by_dept_id_loc_id_api(self, sub_id=None, dept_id=None, loc_id=None,
                                       is_admin=False, admin_token=None, client_token=None):
        """
        This test fetches the details of department for a given dept_id and location_id
        :return: this function returns boolean status of element located
        """
        if not dept_id:
            return None

        if is_admin:
            if loc_id:
                get_dept_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}?locationId={loc_id}'
            else:
                get_dept_endpoint = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            if loc_id:
                get_dept_endpoint = f'{self.endpoint}/api/v1/departments/{dept_id}?locationId={loc_id}'
            else:
                get_dept_endpoint = f'{self.endpoint}/api/v1/departments/{dept_id}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_dept_endpoint, headers=self.headers)
        return response

    def get_dept_contacts_api(self, sub_id=None, dept_id=None, is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            get_dept_contacts_url = f"{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}/contacts"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            get_dept_contacts_url = f"{self.endpoint}/api/v1/departments/{dept_id}/contacts"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_dept_contacts_url, headers=self.headers)
        return response

    def search_dept_with_query_api(self, sub_id=None, skip='0', limit='20', query='', is_admin=False, admin_token=None,
                                   client_token=None):

        if is_admin:
            search_dept_url = f'{self.endpoint}/api/v2/departments?subID={sub_id}&skip={skip}&limit={limit}&query={query}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            search_dept_url = f'{self.endpoint}/api/v2/departments?skip={skip}&limit={limit}&query={query}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=search_dept_url, headers=self.headers)
        return response

    def delete_dept_by_dept_id_loc_id_api(self, sub_id=None, dept_id=None, loc_id=None,
                                          is_admin=False, admin_token=None, client_token=None):
        """
        This test deletes the department
        :return: this function returns boolean status of element located
        """
        if not dept_id:
            return None

        if is_admin:
            if loc_id:
                del_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}?locationId={loc_id}'
            else:
                del_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            if loc_id:
                del_dept_url = f'{self.endpoint}/api/v1/departments/{dept_id}?locationId={loc_id}'
            else:
                del_dept_url = f'{self.endpoint}/api/v1/departments/{dept_id}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.delete_api_response(endpoint=del_dept_url, headers=self.headers)
        if response.status_code == 200:
            self.log.info(f'Deleted the department - {dept_id} with location - {loc_id} successfully!')
        return response

    def delete_all_dept_by_dept_id_loc_id(self, sub_id=None, skip='0', limit='100', query='', is_admin=False,
                                          admin_token=None, client_token=None):

        dept_resp = self.get_departments_api(sub_id=sub_id, skip=skip, limit=limit, query=query,
                                             is_admin=is_admin, admin_token=admin_token, client_token=client_token)

        departments = dept_resp.json().get('departments', [])
        if departments:
            for dept in departments:
                dept_id = dept['departmentID']
                loc_id = dept['locationID']
                del_resp = self.delete_dept_by_dept_id_loc_id_api(sub_id=sub_id, dept_id=dept_id, loc_id=loc_id,
                                                                  is_admin=is_admin, admin_token=admin_token,
                                                                  client_token=client_token)
                assert_that(common_utils.validate_response_code(del_resp, 200))
        else:
            self.log.info(f'No department available in the subs - {sub_id}')

    def import_contacts_in_dept_api(self, sub_id=None, dept_id=None, is_admin=False, admin_token=None, client_token=None):
        """
        This function validates that locations can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        import_dept_file = open(self.prop.get('ADDRESSBOOK_MGMT', 'dept_import'))
        import_file = {"file": (self.prop.get('ADDRESSBOOK_MGMT', 'dept_import'), import_dept_file)}

        if is_admin:
            import_dept_url = f'{self.endpoint}/api/v1/subscriptions/{sub_id}/departments/{dept_id}/contacts/import'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            import_dept_url = f'{self.endpoint}/api/v1/departments/{dept_id}/contacts/import'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=import_dept_url, files=import_file, headers=self.headers)
        return response

    # Recipient List Test Methods

    def create_recipient_list_api(self, name='', sub_id=None, is_admin=False, admin_token=None, client_token=None):
        """
        This function validates if a recipient list can be created successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_body')) as recipient_body:
            payload = json.load(recipient_body)

        if name:
            payload['name'] = name

        if is_admin:
            create_recipient_url = f"{self.endpoint}/api/v1/subscriptions/{sub_id}/recipientlist"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            create_recipient_url = f"{self.endpoint}/api/v1/recipientlist"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=create_recipient_url, headers=self.headers, body=json.dumps(payload))
        return response

    def get_recipient_list_by_id_api(self, sub_id=None, rect_id=None, is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            get_recipient_url = f"{self.endpoint}/api/v1/subscriptions/{sub_id}/recipientlist/{rect_id}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_recipient_url = f"{self.endpoint}/api/v1/recipientlist/{rect_id}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_recipient_url, headers=self.headers)
        return response

    def verify_get_contacts_from_recipient_list_api(self, sub_id='', is_admin='', rec_id=''):
        """
        This test fetches the details of recipient by Id
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            get_contacts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/recipientlist/" + rec_id + "/contacts"
            self.headers['Authorization'] = self.admin_token

        else:
            get_contacts_endpoint = self.endpoint + "/api/v1/recipientlist/" + rec_id + "/contacts"
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_contacts_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            res = res.json()
        return res, status_code

    def verify_delete_recipient_api(self, sub_id='', is_admin='', rec_id=''):
        """
        This test deletes the recipient
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            del_rec_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/recipientlist/" + rec_id
            self.headers['Authorization'] = self.admin_token


        else:
            del_rec_endpoint = self.endpoint + "/api/v1/recipientlist/" + rec_id
            self.headers['Authorization'] = self.client_token

        res = self.api.delete_api_response(
            endpoint=del_rec_endpoint, headers=self.headers)
        status_code = res.status_code

        return status_code

    def patch_contacts_in_recipient_list_api(self, operation_type='', cont1='', cont2='', sub_id=None, rect_id=None,
                                             is_admin=False, admin_token=None, client_token=None):
        """
        This function validates that department can be updated by patch APIs successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'patch_update_dept_req')) as updt_dept_patch_body:
            payload = json.load(updt_dept_patch_body)

        if operation_type:
            payload['operationType'] = operation_type

        if cont1:
            payload['contacts'][0]['contactId'] = cont1

        if cont2:
            payload['contacts'][1]['contactId'] = cont2

        if is_admin:
            patch_contacts_rect_url = f"{self.endpoint}/api/v1/subscriptions/{sub_id}/recipientlist/{rect_id}/contacts"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            patch_contacts_rect_url = f"{self.endpoint}/api/v1/recipientlist/{rect_id}/contacts"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.patch_api_response(endpoint=patch_contacts_rect_url, headers=self.headers, body=json.dumps(payload))
        return response

    def verify_updt_recipient_api(self, name='', cont1='', cont2='', is_admin='', sub_id='', rec_id=''):
        """
        This function validates that department can be updated successfully
        :return: this function returns response and status code
        """
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'updt_recipient_body')) as updt_dept_patch_body:
            self.json_data = json.load(updt_dept_patch_body)
        result = False

        if name != "":
            self.json_data['name'] = name

        if cont1 != "":
            self.json_data['contacts'][0]['contactId'] = cont1

        if cont2 != "":
            self.json_data['contacts'][1]['contactId'] = cont2

        if is_admin == 'y':

            updt_dept_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/recipientlist/" + rec_id
            self.headers['Authorization'] = self.admin_token

        else:
            updt_dept_endPoint = self.endpoint + "/api/v1/recipientlist/" + rec_id
            self.headers['Authorization'] = self.client_token

        res = self.api.put_api_response(
            endpoint=updt_dept_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            res = res.json()
            result = True
        return res, status_code

    def verify_get_rec_by_sub_id_api(self, sub_id='', is_admin='', query=''):
        """
        This test fetches all the recipients available in a subscription
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            get_rec_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/recipientlist?query=" + query
            self.headers['Authorization'] = self.admin_token

        else:
            get_rec_endpoint = self.endpoint + "/api/v1/recipientlist?query=" + query
            self.headers['Authorization'] = self.client_token

        res = self.api.get_api_response(
            endpoint=get_rec_endpoint, headers=self.headers)
        status_code = res.status_code

        if status_code == 200:
            is_paginated = self.api.pagination_util(endpoint=get_rec_endpoint, headers=self.headers)

        else:
            is_paginated = False

        if res is not None:
            res = res.json()
        return res, status_code, is_paginated

    def verify_res_schema(self, res, expected_schema):

        isValid = self.api.schema_validation(response_schema=res, expected_schema=expected_schema)

        return isValid

    def export_contacts_api(self, sub_id=None, contact_filter=None, is_admin=False, admin_token='', client_token=''):
        """
        This function hits export contacts API
        :return: this function returns response and status code
        """

        query_param = f'?excludeIDs=false&contactFilter={contact_filter}'

        if is_admin:
            export_contacts_url = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/contacts/export/file{query_param}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            export_contacts_url = f'{self.endpoint}/api/v2/contacts/export/file{query_param}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=export_contacts_url, headers=self.headers)
        return response

    def contacts_export_job_status_api(self, job_id='', sub_id='', is_admin=False, admin_token='', client_token=''):

        if is_admin:
            export_status_url = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/contacts/export/jobs/{job_id}/status'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            export_status_url = f'{self.endpoint}/api/v2/contacts/export/jobs/{job_id}/status'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=export_status_url, headers=self.headers)
        return response

    def get_file_content(self, decoded_string=''):
        file_location_url = decoded_string

        # if is_admin == 'y':
        #     self.headers['Authorization'] = self.admin_token
        #
        # else:
        #     self.headers['Authorization'] = self.admin_token

        res = self.api.get_api_response(
            endpoint=file_location_url, headers='')

        status_code = res.status_code
        return res, status_code

    def contacts_upload_using_import_file_api(self, file_path='', sub_id='', schema_name='', is_admin=True,
                                              admin_token=None, client_token=None):

        file = {'file': open(file_path, 'rb')}

        if not schema_name:
            schema_name = generate_random_string(uppercase=False, char_count=8)

        if is_admin:
            upload_endpoint = (f'{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks/'
                               f'upload?schema_name={schema_name}')
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            upload_endpoint = f'{self.endpoint}/api/v1/contacts/addressbooks/upload'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=upload_endpoint, files=file, headers=self.headers)
        return response

    def contacts_mapping_process_api(self, job_id='', sub_id='', listing=None, schema_name='', is_admin=True,
                                     admin_token=None, client_token=None):

        if not schema_name:
            schema_name = generate_random_string(uppercase=False, char_count=8)

        if listing:
            payload = {'fieldsMapping': json.dumps(listing),
                       'label': 'home'
                       }
        else:
            payload = {
                'fieldsMapping': '{ "Name": "Name", "Company": "Company", "Email": "Email", "Phone": "Phone", '
                                 '"AddressLine1": "Street Address 1", "AddressLine2": "Street Address 2", '
                                 '"AddressLine3": "Street Address 3", "CityTown": "CityTownArea", "StateProvince": '
                                 '"StateProvinceRegion", "PostalCode": "Postal/ZIP Code", "CountryCode": "Country", '
                                 '"PersonnelID": "PersonnelID", "Department Name": "Department Name", "Accessibility": '
                                 '"Accessibility", "NotificationAll": "NotificationAll", "AdditionalEmailIds": '
                                 '"AdditionalEmailIds", "InternalDelivery": "InternalDelivery", "OfficeLocation": '
                                 '"OfficeLocation", "MailStopID": "MailStopID", "ContactType": "" }',
                'name': '{"label": "home"}'
            }
        if is_admin:
            process_endpoint = (f"{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks/jobs/"
                                f"{job_id}/process?schema_name={schema_name}")
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token

        else:
            process_endpoint = f"{self.endpoint}/api/v1/contacts/addressbooks/jobs/{job_id}/process"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=process_endpoint, headers=self.headers, body=payload)
        return response

    def contacts_import_job_status_api(self, job_id='', sub_id='', schema_name='', is_admin=False,
                                       admin_token='', client_token=''):

        if is_admin:
            import_status_url = f'{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks/jobs/{job_id}/status'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            import_status_url = f'{self.endpoint}/api/v1/contacts/addressbooks/jobs/{job_id}/status'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=import_status_url, headers=self.headers)
        return response

    def get_updated_contacts_after_given_timestamp_api(self, time_stamp='', sub_id=None,
                                                       is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            get_updated_contacts_url = f"{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/addressbooks/{time_stamp}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_updated_contacts_url = f"{self.endpoint}/api/v1/contacts/addressbooks/{time_stamp}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_updated_contacts_url, headers=self.headers)
        return response

    def get_archived_contacts_after_given_timestamp_api(self, time_stamp='', sub_id=None,
                                                        is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            get_archived_contacts_url = f"{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}/archived/{time_stamp}"
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_archived_contacts_url = f"{self.endpoint}/api/v1/contacts/archived/{time_stamp}"
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_archived_contacts_url, headers=self.headers)
        return response

    def get_search_contact_address_access_level_by_receipent_api(self, contact_type='', token=''):

        get_search_contact_url = self.endpoint + '/api/v1/contacts/' + contact_type
        self.headers['Authorization'] = token
        response = self.api.get_api_response(endpoint=get_search_contact_url, headers= self.headers)
        return response

    def get_user_access_details_from_file(self, user_type=''):
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'user_access_level')) as file:
            self.json_data = json.load(file)
            user_name = self.json_data[self.env][user_type]
        return user_name

    def get_user_access_location(self, location=''):
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'user_location_info')) as file:
            self.json_data = json.load(file)
            location = self.json_data[self.env][location]
        return location

    def get_user_access_division(self, division=''):
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'user_division_info')) as file:
            self.json_data = json.load(file)
            division = self.json_data[self.env][division]
        return division

    def get_user_subscription(self, sub_id=''):
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'user_subscription_info')) as file:
            self.json_data = json.load(file)
            subscription = self.json_data[self.env][sub_id]
        return subscription

    def get_sample_import_fields_api(self, is_admin=False, admin_token='', client_token='', sub_id=None,
                                     exclude_ids=True, locale='en-US'):

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
            query_params = f'?subID={sub_id}'
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token
            query_params = f'?excludeIDs={exclude_ids}&locale={locale}'

        import_fields_list_endpoint = f'{self.endpoint}/api/v1/contacts/import/fieldsList{query_params}'
        response = self.api.get_api_response(endpoint=import_fields_list_endpoint, headers=self.headers)
        return response

    def import_contacts_process_and_check_status(self, file_path='', sub_id='', schema_name='', is_admin=True,
                                                 admin_token=None, client_token=None):

        self.log.info("Starting import contacts...")
        if not schema_name:
            schema_name = generate_random_string(uppercase=False, char_count=8)

        upload_resp = self.contacts_upload_using_import_file_api(file_path=file_path, sub_id=sub_id,
                                                                 schema_name=schema_name, is_admin=is_admin,
                                                                 admin_token=admin_token, client_token=client_token)
        assert_that(self.common.validate_response_code(upload_resp, 200))
        job_id = upload_resp.json()['jobId']
        # listing = upload_resp.json()['listing']

        process_resp = self.contacts_mapping_process_api(job_id=job_id, is_admin=is_admin, sub_id=sub_id,
                                                         schema_name=schema_name)

        assert_that(self.common.validate_response_code(process_resp, 200))
        status = process_resp.json()['Status']
        self.log.info(f'Initial job id {job_id} status is {status}')

        max_iterations = 10
        wait_time = 10

        for itr in range(1, max_iterations + 1):
            self.log.info(f'{itr}. Waiting for {wait_time} seconds before checking for the import job status!')
            time.sleep(wait_time)

            status_resp = self.contacts_import_job_status_api(job_id=job_id, sub_id=sub_id, is_admin=is_admin,
                                                              schema_name=schema_name, admin_token=admin_token,
                                                              client_token=client_token)
            assert_that(self.common.validate_response_code(status_resp, 200))
            status = status_resp.json()['status']

            if status == 'Processed':
                self.log.info(f'Import job {job_id} Processed!')
                return True
            elif status == 'ProcessingError':
                records = status_resp.json().get('records')
                failed_records = status_resp.json().get('failedRecords')
                success_records = status_resp.json().get('successfulRecords')
                error_file_base64 = status_resp.json().get('errorsFileLocation')
                error_file_location = self.common.decode_base_64(coded_string=error_file_base64)
                self.log.error(f'Import job {job_id} failed! '
                               f'\nTotal records: {records}, success: {success_records}, failed: {failed_records}'
                               f'\n Download error import file: {error_file_location}')
                raise ImportError(f'Import job {job_id} failed!')

        self.log.error(f'Import job {job_id} is taking longer time and stuck at {status}!')
        raise ImportError(f'Import job {job_id} is stuck!')

    def import_auto_generated_contacts(self, sub_id=None, csv_filepath=None, no_of_records=2, is_admin=False,
                                       admin_token='', client_token=''):

        if not csv_filepath:
            csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'common_addressbook_import')

        else:
            self.data_generator.\
                create_addressbook_import_file(no_of_records=no_of_records, filepath=csv_filepath)

        self.import_contacts_process_and_check_status(file_path=csv_filepath, sub_id=sub_id, is_admin=is_admin,
                                                      admin_token=admin_token, client_token=client_token)

    def import_contacts_process_and_check_status_dynamic_template(self, import_file_case=None, csv_filepath=None,
                                                                  is_admin=False, sub_id=None, schema_name='',
                                                                  admin_token='', client_token=''):
        with open(self.prop.get('ADDRESSBOOK_MGMT',
                                f'{import_file_case}_exp_dynamic_addressbook_import_upload_listing_resp')) as f1:
            exp_import_upload_listing_resp = json.load(f1)

        if is_admin:
            import_addr_endpoint = f'{self.endpoint}/api/v1/contacts/subscriptions/{sub_id}' \
                                   f'/addressbooks/upload?schema_name={schema_name}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            import_addr_endpoint = f'{self.endpoint}/api/v1/contacts/addressbooks/upload'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        with open(csv_filepath, 'rb') as f:
            csvfile = {"file": (csv_filepath, f)}
            import_upload_resp = self.api.post_api_response(endpoint=import_addr_endpoint, files=csvfile,
                                                            headers=self.headers)
            assert_that(self.common.validate_response_template(import_upload_resp, exp_import_upload_listing_resp, 200))

            job_id = import_upload_resp.json()['jobId']
            listing = import_upload_resp.json()['listing']

        process_resp = self.contacts_mapping_process_api(job_id=job_id, listing=listing, is_admin=is_admin,
                                                         sub_id=sub_id,
                                                         schema_name=schema_name, admin_token=admin_token,
                                                         client_token=client_token)
        assert_that(self.common.validate_response_code(process_resp, 200))
        status = process_resp.json()['Status']
        self.log.info(f'Initial job id {job_id} status is {status}')

        max_iterations = 10
        wait_time = 10

        for itr in range(1, max_iterations + 1):
            self.log.info(f'{itr}. Waiting for {wait_time} seconds before checking for the import job status!')
            time.sleep(wait_time)

            status_resp = self.contacts_import_job_status_api(job_id=job_id, sub_id=sub_id, is_admin=is_admin,
                                                              schema_name=schema_name, admin_token=admin_token,
                                                              client_token=client_token)
            assert_that(self.common.validate_response_code(status_resp, 200))
            status = status_resp.json()['status']

            if status == 'Processed':
                self.log.info(f'Import job {job_id} Processed!')
                return True
            elif status == 'ProcessingError':
                records = status_resp.json().get('records')
                failed_records = status_resp.json().get('failedRecords')
                success_records = status_resp.json().get('successfulRecords')
                error_file_base64 = status_resp.json().get('errorsFileLocation')
                error_file_location = self.common.decode_base_64(coded_string=error_file_base64)
                self.log.error(f'Import job {job_id} failed! '
                               f'\nTotal records: {records}, success: {success_records}, failed: {failed_records}'
                               f'\n Download error import file: {error_file_location}')
                raise ImportError(f'Import job {job_id} failed!')

        self.log.error(f'Import job {job_id} is taking longer time and stuck at {status}!')
        raise ImportError(f'Import job {job_id} is stuck!')

    def import_contacts_for_dynamic_template(self, import_file_case=None, plan_headers=None, is_admin=False,
                                             sub_id=None, schema_name='', admin_token='', client_token=''):

        if import_file_case and plan_headers:
            csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', f'{import_file_case}_dynamic_addressbook_import_file')

            if csv_filepath:
                self.data_generator.\
                    create_addressbook_dynamic_template_import_file(plan_case=import_file_case,
                                                                    filepath=csv_filepath, plan_headers=plan_headers)
            else:
                raise ValueError(f'Invalid import_file_case: {import_file_case}')

            if not schema_name:
                schema_name = generate_random_string(uppercase=False, char_count=8)

            self.import_contacts_process_and_check_status_dynamic_template(import_file_case=import_file_case,
                                                                           csv_filepath=csv_filepath, is_admin=is_admin,
                                                                           sub_id=sub_id, schema_name=schema_name,
                                                                           admin_token=admin_token,
                                                                           client_token=client_token)
        else:
            raise ValueError(f'Dynamic Template Import file case and headers are not provided!')

    def export_contacts_check_status_and_download_export_file(self, sub_id='', contact_type='', export_csv_filepath='',
                                                              is_admin=False, admin_token='', client_token=''):
        export_resp = self.export_contacts_api(sub_id=sub_id, contact_filter=contact_type, is_admin=is_admin,
                                               admin_token=admin_token, client_token=client_token)
        job_id = export_resp.json()['jobId']
        status = None
        max_iterations = 10
        wait_time = 10

        for itr in range(1, max_iterations + 1):
            self.log.info(f'{itr}. Waiting for {wait_time} seconds before checking the export job status!')
            time.sleep(wait_time)

            status_resp = self.contacts_export_job_status_api(job_id=job_id, sub_id=sub_id, is_admin=is_admin,
                                                              admin_token=admin_token, client_token=client_token)
            assert_that(self.common.validate_response_code(status_resp, 200))
            status = status_resp.json()['status']

            if status == 'Processed':
                export_file_location = status_resp.json()['exportFileLocation']
                self.data_generator.download_export_file_into_csv(filepath=export_csv_filepath,
                                                                  encoded_link=export_file_location)
                self.log.info(f'Import job {job_id} Processed!')
                return True
            elif status == 'ProcessingError':
                self.log.error(f'Export job {job_id} failed!')
                raise ImportError(f'Import job {job_id} failed!')

        self.log.error(f'Export job {job_id} is taking longer time and stuck at {status}!')
        raise ImportError(f'Export job {job_id} is stuck!')

    def get_required_details_for_dynamic_template(self, sub_type=None, plan_case=None, user_type=None, is_admin=False):

        sub_id, email, pwd = self.get_sub_id_user_cred_from_addressbook_file(sub_type=sub_type, user_type=user_type)

        ent_id, loc_id, carrier_accounts, subs_role_ids = self.subs_api.get_ent_details_by_sub_id(sub_id)
        plans, csv_headers = self.get_plans_from_dynamic_template_file(plan_case=plan_case)

        log_message = (f"Fetched Details for {plan_case}: \nSub_id - {sub_id}, ent_id - {ent_id}, "
                       f"\nplans - {plans}, \nemail - {email}, pwd - {pwd}")

        self.log.info(log_message)
        return sub_id, email, pwd, ent_id, plans, csv_headers

    def delete_contact_api(self, cont_id=None, sub_id='', is_admin=True, admin_token=None, client_token=None):

        if is_admin:
            del_contact_url = f'{self.endpoint}/api/v1/contact/{cont_id}?admin=1&sId={sub_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            del_contact_url = f'{self.endpoint}/api/v1/contact/{cont_id}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        self.log.info(f'Deleting contact - {cont_id}')
        response = self.api.delete_api_response(endpoint=del_contact_url, headers=self.headers)
        return response

    def delete_all_contacts_api(self, is_admin=False, sub_id=None, contact_type='RECIPIENT', del_type='ALL',
                                admin_token='', client_token=''):

        if is_admin:
            del_contacts_url = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/contacts' \
                               f'/delete?contactType={contact_type}&type={del_type}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            del_contacts_url = f'{self.endpoint}/api/v2/contacts/delete?contactType={contact_type}&type={del_type}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        self.log.info(f'Deleting all contacts of type - {contact_type}')
        response = self.api.patch_api_response(endpoint=del_contacts_url, headers=self.headers)
        return response

    def search_contacts_with_query_api(self, sub_id=None, fields='', search='', sort='asc', page='0', limit='100',
                                       query='', is_admin=False, admin_token='', client_token=''):

        if not fields:
            fields = (f'name,company,addresses.addressLine1,addresses.city,emails.value,pID,'
                      f'phones.phone,addresses.state,lID')

        if is_admin:
            search_contacts_url = f'{self.endpoint}/api/v1/contacts?fields={fields}&search={search}&sort={sort}' \
                                  f'&skip={page}&limit={limit}&searchBy={query}&admin=1&sId={sub_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            search_contacts_url = f'{self.endpoint}/api/v1/contacts?fields={fields}&search={search}&sort={sort}' \
                                  f'&skip={page}&limit={limit}&searchBy={query}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=search_contacts_url, headers=self.headers)
        return response

    def delete_all_contacts(self, sub_id=None, cont_type='RECIPIENT', del_type='ALL',
                            is_admin=False, admin_token='', client_token=''):

        get_contacts_resp = self.search_contacts_with_query_api(is_admin=is_admin, sub_id=sub_id,
                                                                admin_token=admin_token, client_token=client_token)
        assert_that(self.common.validate_response_code(get_contacts_resp, 200))

        del_resp = self.delete_all_contacts_api(is_admin=is_admin, sub_id=sub_id, contact_type=cont_type,
                                                del_type=del_type, admin_token=admin_token, client_token=client_token)
        assert_that(common_utils.validate_response_code(del_resp, 200))
        self.log.info(f"check_and_delete_all_contacts - {cont_type}: {del_resp.json()}")

    def build_exp_error_message_dept_loc_response(self, check_error_for='Department', searched_id=''):

        with open(self.prop.get('ADDRESSBOOK_MGMT', 'sample_dept_loc_error_resp')) as file:
            exp_error_resp = json.load(file)

        if check_error_for == 'Department':
            error_code = 'department.notfound'
            error_message = f'Invalid request: Department id [{searched_id}] not found'

            exp_error_resp['errors'][0]['errorCode'] = str(error_code)
            exp_error_resp['errors'][0]['errorDescription'] = str(error_message)

        if check_error_for == 'Location':
            error_code = 'location.notfound'
            error_message = f'Invalid request: Location id [{searched_id}] not found'

            exp_error_resp['errors'][0]['errorCode'] = str(error_code)
            exp_error_resp['errors'][0]['errorDescription'] = str(error_message)

        return exp_error_resp

    def create_n_contacts(self, personal_id='', del_existing_cont=False, no_of_contacts=1,
                          sub_id=None, cont_type='RECIPIENT'):

        created_contacts = []

        if del_existing_cont:  # Delete existing contacts
            self.delete_all_contacts(is_admin=True, sub_id=sub_id, cont_type=cont_type)

        for _ in range(no_of_contacts):

            cont_data = DataGenerator.address_book_data_setter()
            name = cont_data[0]
            comp = cont_data[1]
            email = cont_data[2]
            phone = cont_data[3]
            addr1 = cont_data[4]
            city = cont_data[7]
            state = cont_data[8]
            postal = cont_data[9]
            country = cont_data[10]
            int_dlvry = cont_data[11]

            add_contact_resp = self \
                .add_contact_api(contact_type=cont_type, int_dlvry=int_dlvry, name=name, comp=comp,
                                 email=email, phone=phone, addr1=addr1, city=city, country=country,
                                 postal=postal, state=state, personal_id=personal_id, sub_id=sub_id, is_admin=True)
            assert_that(common_utils.validate_response_code(add_contact_resp, 201))
            cont_id = add_contact_resp.json()
            created_contacts.append(cont_id)

        created_contacts.sort()
        return created_contacts

    def search_contacts_v3_api(self, query_params='', is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        v3_search_contacts_url = f"{self.endpoint}/api/v3/contacts/search{query_params}"
        response = self.api.get_api_response(v3_search_contacts_url, self.headers)
        self.log.info(f"url: {v3_search_contacts_url}")
        return response

    def build_v3_search_contacts_query_params(self, file_path='', file_name='', sheet_name='', page='0', limit='100',
                                              sub_id='', is_admin=False):

        query_params = {}
        exp_cont_count = {}

        results = common_utils.read_excel_data_store(folder_name=file_path, file_name=file_name, sheet_name=sheet_name)

        # for each test data call the search api and validate the number of addresses in result
        for index, data in enumerate(results):
            search_by = data['searchBy_fieldName']
            filter_by = data['filterBy_fieldName']
            is_filter = data['need_FilterBy']
            filter_option = data['filterBy_Option']
            search_text = data['search_text']
            exp_cont_count[index] = (data['expected_no_of_addresses'])

            if is_admin:
                if is_filter == "yes":
                    if filter_by == "None":
                        params = (f'?skip={page}&limit={limit}&searchBy={search_by}:{search_text}'
                                  f'&filterBy={search_by}:{filter_option}&admin=true&sId={sub_id}')
                    else:
                        params = (f'?skip={page}&limit={limit}&searchBy={search_by}:{search_text}'
                                  f'&filterBy={filter_by}:{filter_option}&admin=true&sId={sub_id}')
                else:
                    params = f"?skip={page}&limit={limit}&searchBy={search_by}:{search_text}&admin=true&sId={sub_id}"

            else:
                if is_filter == "yes":
                    if filter_by == "None":
                        params = (f'?skip={page}&limit={limit}&searchBy={search_by}:{search_text}'
                                  f'&filterBy={search_by}:{filter_option}')
                    else:
                        params = (f'?skip={page}&limit={limit}&searchBy={search_by}:{search_text}'
                                  f'&filterBy={filter_by}:{filter_option}')
                else:
                    params = f"?skip={page}&limit={limit}&searchBy={search_by}:{search_text}"

            query_params[index] = params

        return query_params, exp_cont_count
