import inspect
import json
import pytest
import logging
from hamcrest import assert_that, equal_to

from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.custom_fields_api import Custom_fields
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestUserSubscriptionManagementAPI.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: Subscription_API object.
    """
    custom_fields_api = {
        'app_config': app_config,
        'custom_fields_api': Custom_fields(app_config, generate_access_token, client_token),
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'product_metadata_api': ProductMetadata(app_config, generate_access_token, client_token),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token)
    }
    yield custom_fields_api


@pytest.mark.usefixtures('initialize')
class TestUserCustomFieldsManagementAPI(common_utils):
    """
    The test class to place all the tests of Custom Field APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - CustomFieldAPI.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.login = LoginAPI(app_config)

        self.admin_user, admin_pwd, self.client_user, client_pwd, self.sub_id = resource[
            'custom_fields_api'].retrieve_user_credentials()
        self.admin_token = self.login.get_access_token_for_user_credentials(username=self.admin_user,
                                                                            password=admin_pwd)
        self.client_token = self.login.get_access_token_for_user_credentials(username=self.client_user,
                                                                             password=client_pwd)

        with open(self.prop.get('CUSTOM_FIELDS', 'sample_subscription_ids_and_email_file')) as f01:
            self.json_data = json.load(f01)

        with open(self.prop.get('CUSTOM_FIELDS', 'add_new_custom_field')) as f25:
            self.add_new_custom_field_file = json.load(f25)
        with open(self.prop.get('CUSTOM_FIELDS', 'add_new_custom_field_response')) as f26:
            self.add_new_custom_field_response_file = json.load(f26)

        yield

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_01_add_update_del_custom_field_using_admin_user(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=True,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=location_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type)

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))

        assert_that(self.compare_response_objects(add_custom_field_resp.json(),
                                                  self.add_new_custom_field_response_file))

        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=True,
                                                                                                token=self.admin_token)
        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))

        count = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']
        assert_that(count, equal_to(1))

        # validating the creation of custom fields on different features i.e usage
        if admin_level != 'S':
            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='ACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='CONTACTS_ADDRESS_BOOK',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

        # update custom filed

        asignpageform = ["NOTIFICATIONS", "CONTACTS_ADDRESS_BOOK", "LOCKER_RESERVATION_KIOSK",
                         "MANAGE_ORDERS", "RECEIVE_EDIT_DELIVER_POUCH",
                         "SHIPPING_LABELS_STAMPS_CERTIFIED"]
        name = 'Auto_' + generate_random_string(char_count=5)
        cf_list_values = cf_list_values + ["thu", "fri", "sat"]

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name, ent_id=ent_id,
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=True,
                                                                                  site=site_list,
                                                                                  token=self.admin_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type)
        assert_that(self.validate_response_code(update_status, 200))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=True,
                                                                                                token=self.admin_token
                                                                                                )
        assert_that(get_custom_field_search_query_resp.json()['customFields'][0]['assignPageForm'],
                    equal_to(asignpageform))
        if cf_type == "LIST":
            assert_that(get_custom_field_search_query_resp.json()['customFields'][0]['values'],
                        equal_to(cf_list_values))

        # 'Delete custom field':

        del_status = resource['custom_fields_api'].delete_custom_field_api(sub_id=sub_id,
                                                                           is_admin=True,
                                                                           config_id=fetch_configID,
                                                                           token=self.admin_token)
        assert_that(self.validate_response_code(del_status, 200))

        # 'Verify that deleted custom field is not available'
        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=True,
                                                                                                token=self.admin_token)
        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(0))

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_02_add_update_del_custom_field_using_client_user(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=False,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=location_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type)

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))

        assert_that(self.compare_response_objects(add_custom_field_resp.json(),
                                                  self.add_new_custom_field_response_file))

        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                token=self.client_token
                                                                                                )
        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))

        count = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']
        assert_that(count, equal_to(1))

        # validating the creation of custom fields on different features i.e usage
        if admin_level != 'S':
            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='ACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='CONTACTS_ADDRESS_BOOK',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

        # update custom filed

        asignpageform = ["NOTIFICATIONS", "CONTACTS_ADDRESS_BOOK", "LOCKER_RESERVATION_KIOSK",
                         "MANAGE_ORDERS", "RECEIVE_EDIT_DELIVER_POUCH",
                         "SHIPPING_LABELS_STAMPS_CERTIFIED"]
        name = 'Auto_' + generate_random_string(char_count=5)
        cf_list_values = cf_list_values + ["thu", "fri", "sat"]

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name, ent_id=ent_id,
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=False,
                                                                                  site=site_list,
                                                                                  token=self.client_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type)
        assert_that(self.validate_response_code(update_status, 200))

        # validating the Updation of custom fields on different features i.e usage
        if admin_level != 'S':
            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='ACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='RECEIVE_EDIT_DELIVER_POUCH',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                token=self.client_token
                                                                                                )
        assert_that(get_custom_field_search_query_resp.json()['customFields'][0]['assignPageForm'],
                    equal_to(asignpageform))
        if cf_type == "LIST":
            assert_that(get_custom_field_search_query_resp.json()['customFields'][0]['values'],
                        equal_to(cf_list_values))

        # 'Delete custom field':

        del_status = resource['custom_fields_api'].delete_custom_field_api(sub_id=sub_id,
                                                                           config_id=fetch_configID,
                                                                           token=self.client_token)
        assert_that(self.validate_response_code(del_status, 200))

        # 'Verify that deleted custom field is not available'
        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                )
        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(0))

        # validating the Deletion of custom fields on different features i.e usage
        get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                        sub_id=sub_id,
                                                                                        status='ACTIVE',
                                                                                        is_admin=False,
                                                                                        token=self.client_token,
                                                                                        asignPageForm='CONTACTS_ADDRESS_BOOK',
                                                                                        config_id=fetch_configID)

        assert_that(self.validate_response_code(get_used_custom_field, 200))

        count = get_used_custom_field.json()['pageInfo']['totalCount']
        assert_that(count, equal_to(0))

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_03_add_duplicate_custom_field_using_admin_user(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = True
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # checking duplicate on same name as above
        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=location_id_list,
                                                                                   div_id=division_id,
                                                                                   asignPageForm=asignpageform,
                                                                                   site=site_list,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_code(add_custom_field_resp, 400))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                token=self.admin_token)

        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(1))

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID,
                                                              token=self.admin_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_04_add_duplicate_custom_field_using_client_user(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = False
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # checking duplicate on same name as above
        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=location_id_list,
                                                                                   div_id=division_id,
                                                                                   asignPageForm=asignpageform,
                                                                                   site=site_list,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_code(add_custom_field_resp, 400))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                token=self.client_token)

        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(1))

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID,
                                                              token=self.client_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_05_add_duplicate_by_editing_custom_field_using_admin(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = True
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))

        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # adding one more to check update duplicate case

        name1 = 'Auto_' + generate_random_string(char_count=5)
        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name1, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )
        assert_that(self.validate_response_code(add_custom_field_resp, 201))
        fetch_configID1 = str(add_custom_field_resp.json()['customFieldID'])

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name1, ent_id=ent_id,
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=is_admin,
                                                                                  site=site_list,
                                                                                  token=self.admin_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type
                                                                                  )
        assert_that(self.validate_response_code(update_status, 400))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                token=self.admin_token)

        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(1))
        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.admin_token)
        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID1, token=self.admin_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_06_add_duplicate_by_editing_custom_field_using_client(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = False
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))

        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # adding one more to check update duplicate case

        name1 = 'Auto_' + generate_random_string(char_count=5)
        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name1, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )
        assert_that(self.validate_response_code(add_custom_field_resp, 201))
        fetch_configID1 = str(add_custom_field_resp.json()['customFieldID'])

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name1, ent_id=ent_id,
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=is_admin,
                                                                                  site=site_list,
                                                                                  token=self.client_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type
                                                                                  )
        assert_that(self.validate_response_code(update_status, 400))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(query=name,
                                                                                                noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='ACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                token=self.client_token)

        var = get_custom_field_search_query_resp.json()['pageInfo']['totalCount']

        assert_that(self.validate_response_code(get_custom_field_search_query_resp, 200))
        assert_that(var, equal_to(1))
        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.client_token)
        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID1, token=self.client_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_07_active_inactive_custom_field_admin(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = True
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        asignpageform = ["NOTIFICATIONS", "CONTACTS_ADDRESS_BOOK", "RECEIVE_EDIT_DELIVER_POUCH"]

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name, ent_id=ent_id,
                                                                                  status='INACTIVE',
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=is_admin,
                                                                                  site=site_list,
                                                                                  token=self.admin_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type
                                                                                  )
        assert_that(self.validate_response_code(update_status, 200))

        # validating the creation of custom fields on different features for INACTIVE field i.e usage
        if admin_level != 'S':
            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='INACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='CONTACTS_ADDRESS_BOOK',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='INACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='RECEIVE_EDIT_DELIVER_POUCH',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='INACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                config_id=fetch_configID,
                                                                                                token=self.admin_token)
        assert_that(get_custom_field_search_query_resp.json(), 200)

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.admin_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_08_active_inactive_custom_field_client(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = False
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])
        asignpageform = ["NOTIFICATIONS", "CONTACTS_ADDRESS_BOOK", "RECEIVE_EDIT_DELIVER_POUCH"]

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=sub_id,
                                                                                  admin_level=admin_level,
                                                                                  name=name, ent_id=ent_id,
                                                                                  status='INACTIVE',
                                                                                  config_id=fetch_configID,
                                                                                  asignPageForm=asignpageform,
                                                                                  loc_id=location_id_list,
                                                                                  div_id=division_id,
                                                                                  is_admin=is_admin,
                                                                                  site=site_list,
                                                                                  token=self.client_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type=cf_type
                                                                                  )
        assert_that(self.validate_response_code(update_status, 200))

        # validating the creation of custom fields on different features for INACTIVE field i.e usage
        if admin_level != 'S':
            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='INACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='CONTACTS_ADDRESS_BOOK',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

            get_used_custom_field = resource['custom_fields_api'].get_used_custom_field_api(query=name,
                                                                                            sub_id=sub_id,
                                                                                            status='INACTIVE',
                                                                                            is_admin=False,
                                                                                            token=self.client_token,
                                                                                            asignPageForm='RECEIVE_EDIT_DELIVER_POUCH',
                                                                                            config_id=fetch_configID)

            assert_that(self.validate_response_code(get_used_custom_field, 200))

            count = get_used_custom_field.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))

        get_custom_field_search_query_resp = resource['custom_fields_api'].get_custom_field_api(noskip=False,
                                                                                                sub_id=sub_id,
                                                                                                status='INACTIVE',
                                                                                                is_admin=is_admin,
                                                                                                config_id=fetch_configID,
                                                                                                token=self.client_token)
        assert_that(get_custom_field_search_query_resp.json(), 200)

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.client_token)

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.skip(reason="tests are failing as /api/v1/customResource is not in use, and it is being called "
                             "directly from address book apis")
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_09_use_created_custom_field_admin(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = True
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource,
                                                                            admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # add contact in address book
        contact_name = 'Auto_contact_' + generate_random_string(char_count=3)
        add_cont_resp = resource['addressbook_api'].add_new_contact_api(name=contact_name, token=self.client_token,
                                                                        sub_id=sub_id, type='S')
        contact_id = str(add_cont_resp.json())

        cf_value = 'Auto_inset_value_' + generate_random_string(char_count=3)
        if cf_type == "LIST":
            cf_value = cf_list_values[0]
        post_cf_in_address_book_response = resource['custom_fields_api']. \
            add_custom_field_in_address_book(sub_id=sub_id, token=self.admin_token,
                                             is_admin=is_admin, cf_value=cf_value,
                                             config_id=fetch_configID, contact_id=contact_id)
        customResourceValueID = post_cf_in_address_book_response.json()['customResourceValueID']

        get_cf_in_address_book_response = resource['custom_fields_api']. \
            get_custom_field_in_address_book(sub_id=sub_id, token=self.admin_token,
                                             is_admin=is_admin, customResourceValueID=customResourceValueID,
                                             config_id=fetch_configID, contact_id=contact_id)
        if admin_level != 'S':
            count = get_cf_in_address_book_response.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))
            assert_that(cf_value, equal_to(
                get_cf_in_address_book_response.json()['customResourceValues'][0]['customFieldValueName']))

        # update the custom field value in address book

        print("\n*******8Update start********8\n")
        cf_new_value = 'Auto_update_value_' + generate_random_string(char_count=3)
        if cf_type == "LIST":
            cf_new_value = cf_list_values[1]
        update_cf_in_address_book_response = resource['custom_fields_api']. \
            update_custom_field_in_address_book(sub_id=sub_id, token=self.admin_token,
                                                customResourceValueID=customResourceValueID,
                                                is_admin=is_admin, cf_value=cf_new_value,
                                                config_id=fetch_configID, contact_id=contact_id)
        assert_that(self.validate_response_code(update_cf_in_address_book_response, 200))

        get_cf_in_address_book_response = resource['custom_fields_api']. \
            get_custom_field_in_address_book(sub_id=sub_id, token=self.admin_token,
                                             is_admin=is_admin, customResourceValueID=customResourceValueID,
                                             config_id=fetch_configID, contact_id=contact_id)
        if admin_level != 'S':
            count = get_cf_in_address_book_response.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))
            assert_that(cf_new_value, equal_to(
                get_cf_in_address_book_response.json()['customResourceValues'][0]['customFieldValueName']))

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.admin_token)

        resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, sub_id=sub_id,
                                                                    is_admin='y')

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])

    @pytest.mark.custom_fields_management_sp360commercial_reg
    @pytest.mark.custom_fields_management_sp360commercial
    @pytest.mark.custom_fields_management_fedramp
    @pytest.mark.custom_fields_management_fedramp_reg
    @pytest.mark.skip(reason="tests are failing as /api/v1/customResource is not in use, and it is being called "
                             "directly from address book apis")
    @pytest.mark.parametrize('admin_level, cf_type', [('E', 'TEXT'), ('D', 'TEXT'), ('L', 'TEXT'), ('S', 'TEXT'),
                                                      ('E', 'LIST'), ('D', 'LIST'), ('L', 'LIST'), ('S', 'LIST')])
    def test_10_use_created_custom_field_client(self, resource, admin_level, cf_type):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        is_admin = False
        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource,
                                                                            admin_level=admin_level,
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)

        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=sub_id,
                                                                                   is_admin=is_admin,
                                                                                   admin_level=admin_level,
                                                                                   name=name, ent_id=ent_id,
                                                                                   loc_id=loc_id,
                                                                                   div_id=[division_id[0]],
                                                                                   asignPageForm=asignpageform,
                                                                                   site=siteid_on_def_loc,
                                                                                   token=self.client_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type=cf_type
                                                                                   )

        assert_that(self.validate_response_template(add_custom_field_resp, self.add_new_custom_field_file, 201))
        fetch_configID = str(add_custom_field_resp.json()['customFieldID'])

        # add contact in address book
        contact_name = 'Auto_contact_' + generate_random_string(char_count=3)
        add_cont_resp = resource['addressbook_api'].add_new_contact_api(name=contact_name, token=self.client_token,
                                                                        sub_id=sub_id, type='S')
        contact_id = str(add_cont_resp.json())

        cf_value = 'Auto_inset_value_' + generate_random_string(char_count=3)
        if cf_type == "LIST":
            cf_value = cf_value[0]
        post_cf_in_address_book_response = resource['custom_fields_api']. \
            add_custom_field_in_address_book(sub_id=sub_id, token=self.client_token,
                                             is_admin=is_admin, cf_value=cf_value,
                                             config_id=fetch_configID, contact_id=contact_id)
        customResourceValueID = post_cf_in_address_book_response.json()['customResourceValueID']

        get_cf_in_address_book_response = resource['custom_fields_api']. \
            get_custom_field_in_address_book(sub_id=sub_id, token=self.client_token,
                                             is_admin=is_admin, customResourceValueID=customResourceValueID,
                                             config_id=fetch_configID, contact_id=contact_id)
        if admin_level != 'S':
            count = get_cf_in_address_book_response.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))
            assert_that(cf_value, equal_to(
                get_cf_in_address_book_response.json()['customResourceValues'][0]['customFieldValueName']))

        # update the custom field value in address book

        print("\n*******8Update start********8\n")
        cf_new_value = 'Auto_update_value_' + generate_random_string(char_count=3)
        if cf_type == "LIST":
            cf_new_value = cf_list_values[1]
        update_cf_in_address_book_response = resource['custom_fields_api']. \
            update_custom_field_in_address_book(sub_id=sub_id, token=self.client_token,
                                                customResourceValueID=customResourceValueID,
                                                is_admin=is_admin, cf_value=cf_new_value,
                                                config_id=fetch_configID, contact_id=contact_id)
        assert_that(self.validate_response_code(update_cf_in_address_book_response, 200))

        get_cf_in_address_book_response = resource['custom_fields_api']. \
            get_custom_field_in_address_book(sub_id=sub_id, token=self.client_token,
                                             is_admin=is_admin, customResourceValueID=customResourceValueID,
                                             config_id=fetch_configID, contact_id=contact_id)
        if admin_level != 'S':
            count = get_cf_in_address_book_response.json()['pageInfo']['totalCount']
            assert_that(count, equal_to(1))
            assert_that(cf_new_value, equal_to(
                get_cf_in_address_book_response.json()['customResourceValues'][0]['customFieldValueName']))

        resource['custom_fields_api'].delete_custom_field_api(is_admin=is_admin, sub_id=sub_id,
                                                              config_id=fetch_configID, token=self.client_token)

        resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, sub_id=sub_id,
                                                                    is_admin='y')

        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[0])
        resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='', sub_id=sub_id, site_id=site_list[1])
