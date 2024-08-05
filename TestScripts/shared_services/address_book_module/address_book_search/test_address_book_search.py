import inspect
import json
import logging
import time
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestAddressbookSearch(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_sp360canada
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp_reg
    def test_01_verify_address_search_v3_api_with_client_user(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')
        is_admin = False
        # Delete existing recipient contacts
        resource['addressbook_api'].delete_all_contacts_api(is_admin=is_admin)
        # Delete existing sender contacts
        resource['addressbook_api'].delete_all_contacts_api(is_admin=is_admin, contact_type='SENDER')
        # import contacts
        # get import file test data directory
        file_path = self.prop.get('ADDRESSBOOK_MGMT', 'import_addressbook_data_for_search')
        resource['addressbook_api'].import_contacts_process_and_check_status(file_path=file_path, is_admin=is_admin)
        time.sleep(5)
        # read address search test data
        results = common_utils.read_excel_data_store("shared_services/addressbook_imports",
                                                     "validate_address_search_results.xlsx",
                                                     "Sheet1")
        # for each test data call the search api and validate the number of addresses in result
        for index in range(0, len(results)):
            address_search_record = results[index]
            page = '0'
            limit = '20'

            search_by_field_name = address_search_record['searchBy_fieldName']
            is_filter_by_required = address_search_record['need_FilterBy']
            filter_by_option = address_search_record['filterBy_Option']
            search_text = address_search_record['search_text']
            expected_num_of_addresses_from_search = address_search_record['expected_no_of_addresses']

            self.log.info(
                'searching with ' + search_by_field_name + ' field, search text as ' + search_text + ', filterBy as ' + filter_by_option + ' and expected contacts ' + expected_num_of_addresses_from_search)
            # if we want to search by filterBy
            if is_filter_by_required == "yes":
                query_params = f'?skip={page}&limit={limit}&searchBy={search_by_field_name}:{search_text}&filterBy={search_by_field_name}:{filter_by_option}'
            else:
                query_params = "?skip=" + page + "&limit=" + limit + "&searchBy=" + search_by_field_name + ":" + search_text
            # call addressbook v3 search api
            response = resource['addressbook_api'].search_contacts_v3_api(is_admin=False, query_params=query_params)
            # verify number of addresses in the result
            assert_that(len(response.json()), equal_to(int(expected_num_of_addresses_from_search)))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_02_verify_v3_address_search_with_filter_by_option_using_admin_client_users(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # Delete all existing contacts
        resource['addressbook_api'].delete_all_contacts_api(is_admin=True, sub_id=sub_id, contact_type='RECIPIENT')
        resource['addressbook_api'].delete_all_contacts_api(is_admin=True, sub_id=sub_id, contact_type='SENDER')

        # import contacts
        # get import file test data directory
        file_path = self.prop.get('ADDRESSBOOK_MGMT', 'import_addressbook_data_for_search')
        resource['addressbook_api'].import_contacts_process_and_check_status(file_path=file_path, sub_id=sub_id,
                                                                             is_admin=True, client_token=user_token)
        time.sleep(5)

        get_contacts_resp = resource['addressbook_api'].search_contacts_v3_api()
        self.log.info(f'get_contacts_resp: {json.dumps(get_contacts_resp.json())}')

        is_admin = [True, False]

        for user_type in is_admin:
            query_params, exp_cont_count = (resource['addressbook_api'].build_v3_search_contacts_query_params(
                file_path='shared_services/addressbook_imports', file_name='validate_address_search_filter_results.xlsx',
                sheet_name='Sheet1', page='0', limit='100', sub_id=sub_id, is_admin=user_type))

            self.log.info(f'query_params: {query_params}')
            self.log.info(f'exp_cont_count: {exp_cont_count}')

            for i in range(0, len(query_params)):
                self.log.info(f'Sending request with query_params: {query_params[i]} and expected contacts count: {exp_cont_count[i]}')
                response = (resource['addressbook_api']
                            .search_contacts_v3_api(query_params=query_params[i], is_admin=user_type, client_token=user_token))
                assert_that(len(response.json()), equal_to(int(exp_cont_count[i])))
