""" This module contains all test cases."""
import inspect
import json
import logging
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'login_api': LoginAPI(app_config),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token)
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestAddressbookImportDynamicTemplate(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    def test_01_get_contact(self, resource):
        """
        This test validates that dynamic template address book import based on the subscription plans. It verifies
        based on the plans for - import csv template headers,import fields list, import of contacts with columns,
        export the contacts and compares the imported contacts within the exported contacts file.

        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api()
        assert_that(self.validate_response_code(search_address_resp, 200))

        self.log.info(f'search_address_resp: {json.dumps(search_address_resp.json())}')

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.parametrize('is_admin', ['True', 'False'])
    def test_02_validate_add_and_fetch_department_contacts(self, resource, is_admin):

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        created_contacts = resource['addressbook_api'].create_n_contacts(sub_id=sub_id, no_of_contacts=2,
                                                                         del_existing_cont=True)
        contact1 = created_contacts[0]
        contact2 = created_contacts[1]

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        update_dept_resp = resource['addressbook_api'].update_dept_api(cont1=contact1, cont2=contact2, is_admin=True,
                                                                       sub_id=sub_id, dept_id=created_dept_id)
        assert_that(self.validate_response_code(update_dept_resp, 200))

        # validating department contacts fetch from the API
        get_dept_cont_resp = (resource['addressbook_api']
                              .get_dept_contacts_api(sub_id=sub_id, dept_id=created_dept_id, is_admin=is_admin))
        assert_that(self.validate_response_code(get_dept_cont_resp, 200))
        contacts_list = []
        fetched_contacts = get_dept_cont_resp.json()['contacts']
        for contact in fetched_contacts:
            contacts_list.append(contact['id'])
        contacts_list.sort()
        assert_that(contact1, equal_to(contacts_list[0]))
        assert_that(contact2, equal_to(contacts_list[1]))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    # @pytest.mark.parametrize('is_admin, cont_type',
    #                          [(True, 'SENDER'), (True, 'RECIPIENT'), (False, 'SENDER'), (False, 'RECIPIENT')])
    @pytest.mark.parametrize('is_admin, cont_type',
                             [(False, 'SENDER'), (False, 'RECIPIENT')])
    def test_03_validate_add_del_contact(self, resource, is_admin, cont_type):

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        created_contacts = (resource['addressbook_api']
                            .create_n_contacts(sub_id=sub_id, cont_type=cont_type, del_existing_cont=True))
        contact_id = created_contacts[0]

        user_token = None
        if not is_admin:
            user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id,
                                                                               is_admin=is_admin,
                                                                               client_token=user_token)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        fetched_cont_id = get_cont_resp.json()['id']
        assert_that(contact_id, equal_to(fetched_cont_id))

        # Delete the created admin:
        del_cont_resp = (resource['addressbook_api']
                         .patch_v1_delete_contact_api(cont_id=contact_id, sub_id=sub_id,
                                                      is_admin=is_admin, client_token=user_token))
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id,
                                                                               is_admin=is_admin)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    # @pytest.mark.parametrize('is_admin, cont_type',
    #                          [(True, 'SENDER'), (True, 'RECIPIENT'), (False, 'SENDER'), (False, 'RECIPIENT')])
    @pytest.mark.parametrize('is_admin, cont_type', [(False, 'SENDER'), (False, 'RECIPIENT')])
    def test_04_validate_add_del_multiple_contacts(self, resource, is_admin, cont_type):

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        created_contacts = (resource['addressbook_api']
                            .create_n_contacts(sub_id=sub_id, cont_type=cont_type,
                                               del_existing_cont=True, no_of_contacts=2))
        contact1 = created_contacts[0]

        user_token = None
        if not is_admin:
            user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact1, sub_id=sub_id,
                                                                               is_admin=is_admin,
                                                                               client_token=user_token)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        fetched_cont_id = get_cont_resp.json()['id']
        assert_that(contact1, equal_to(fetched_cont_id))

        # Delete the created admin:
        del_cont_resp = resource['addressbook_api'].patch_v2_delete_contact_api(cont_id=created_contacts, sub_id=sub_id,
                                                                                cont_type=cont_type, is_admin=is_admin,
                                                                                client_token=user_token)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact1, sub_id=sub_id,
                                                                               is_admin=is_admin)
        assert_that(self.validate_response_code(get_cont_resp, 404))
