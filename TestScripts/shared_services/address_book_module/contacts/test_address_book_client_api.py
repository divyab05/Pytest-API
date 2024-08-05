""" This module contains all test cases."""
import inspect
import logging
import random
import string
import time
import pytest
from hamcrest import assert_that, equal_to_ignoring_case, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.data_generator import DataGenerator
from FrameworkUtilities.config_utility import ConfigUtility
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_string
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    addressbook = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'data_generator': DataGenerator(app_config)
    }
    yield addressbook


@pytest.mark.usefixtures('initialize')
class TestAddressbook_Contact_Client_API(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, resource):
        exe_status.__init__()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "ADDRESSBOOK_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        self.Failures = []

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_01_verify_create_recipient_US_addr_user_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Addressbook add new contact and validate that contac of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Rec_US_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact Id and verify the details
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created contact
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_02_verify_create_sender_US_addr_user_api(self, resource):
        """
        This test validates that contact of type SENDER can be created successfully (positive scenario)
        Valid Address: US
        Type: SENDER
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Addressbook add new contact and validate that contac of type recipient can be created successfully:
        contact_type = 'SENDER'
        internal_delivery = False
        type = 'S'
        name = "Sender_US_Addr_" + str(random.randint(1, 50000))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created admin:
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_03_verify_create_recipient_CN_addr_user_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: CANADA
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Addressbook add new contact and validate that contac of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Rec_CN_Addr_" + str(random.randint(1, 50000))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created admin:
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_04_verify_create_sender_CN_addr_admin_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: CANADA
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Addressbook add new contact and validate that contac of type recipient can be created successfully:

        contact_type = 'SENDER'
        internal_delivery = False
        type = 'S'
        name = "Sender_CN_Addr_" + str(random.randint(1, 50000))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created contact:
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_05_verify_search_address_api(self, resource):
        """
        This test validates that added address can be fetched successfully  (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')
        # Call search address API and Validate that successful response is obtained in Ascending list
        paramval = 'sort=name,desc'

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # Call search address API and Validate that successful response is obtained in Ascending list
        paramval = 'sort=name,asc'
        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_06_verify_search_address_by_name_api(self, resource):
        """
        This test validates that added address can be fetched by valid name successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call search address API and Validate that successful response is obtained when Address is searched with:
        # 1. Valid Name

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_search_rec" + str(random.randint(1, 200))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        addr_line_1 = 'Auto_line_1'
        city = 'Nashville'
        country_code = 'US'
        postal_cd = '37210'
        state = 'TX'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        paramval = 'fields=name&search=' + name

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # Verify that returned names contain the search string:
        total_records = len(search_address_resp.json())
        if total_records == 0:
            self.Failures.append(
                "No Address fetched for the provided string. ")
        else:
            for i in range(total_records):
                fetched_name = search_address_resp.json()[i]['name']
                is_found = fetched_name.find(name)
                if is_found < 0:
                    self.Failures.append(
                        "Only matching contact names should be returned in search result. Name not containing matched result: " + fetched_name)
                    break

        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.skip(reason="Failing in CI/CD with docker image - sha256:366606c4ffe37b088562a1cec788368cd88b640d32400b03e650493728c96ff3")
    def test_07_verify_search_address_by_company_api(self, resource):
        """
        This test validates that added address can be fetched by valid company name successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call search address API and Validate that successful response is obtained when Address is searched with: Valid company:
        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_rec_" + str(random.randint(1, 200))
        comp = "Auto_Comp_Test_PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        addr_line_1 = 'Auto_line_1'
        city = 'Nashville'
        country_code = 'US'
        postal_cd = '37210'
        state = 'TX'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        paramval = 'fields=company&search=' + comp

        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # "Verify that returned names contain the search string:
        total_records = len(search_address_resp.json())
        if total_records == 0:
            pytest.fail("No Address fetched for the provided string. ")
        else:
            for i in range(total_records):
                fetched_name = search_address_resp.json()[i]['company']
                is_found = fetched_name.find(comp)
                if is_found < 0:
                    pytest.fail(
                        "Only matching company names should be returned. Contact not containing matched result: " + fetched_name)
                    break

        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_08_verify_search_address_by_address_api(self, resource):
        """
        This test validates that added address can be fetched by valid address successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call search address API and Validate that successful response is obtained when Address is searched with:"
        # "Valid Address Line 1"
        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_rec_" + str(random.randint(1, 200))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        addr_line_1 = 'Auto_line_1'
        city = 'Nashville'
        country_code = 'US'
        postal_cd = '37210'
        state = 'TX'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        paramval = 'fields=addresses.addressLine1&search=' + addr_line_1

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # "Verify that returned names contain the search string: "
        total_records = len(search_address_resp.json())
        if total_records == 0:
            pytest.fail("No Address fetched for the provided string. ")

        # "Verify that returned names contain the search string: "
        for i in range(total_records):
            fetched_addrln1 = search_address_resp.json()[i]['addresses'][0]['addressLine1']
            is_found = fetched_addrln1.find(addr_line_1)
            if is_found < 0:
                pytest.fail(
                    "Only matching address should be fetched. Unmatched record: " + fetched_addrln1)
                break

        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_09_verify_search_address_by_city_api(self, resource):
        """
        This test validates that added address can be fetched by valid city successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call search address API and Validate that successful response is obtained when Address is searched with:"
        # "Valid City"
        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_rec_" + str(random.randint(1, 200))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        addr_line_1 = 'Auto_line_1'
        city = 'Nashville'
        country_code = 'US'
        postal_cd = '37210'
        state = 'TX'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        paramval = 'fields=addresses.city&search=' + city

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # "Verify that returned names contain the search string":
        total_records = len(search_address_resp.json())
        if total_records == 0:
            pytest.fail("No Address fetched for the provided string. ")

        else:
            for i in range(total_records):
                fetched_name = search_address_resp.json()[i]['addresses'][0]['city']
                is_found = fetched_name.find(city)
                if is_found < 0:
                    pytest.fail(
                        "Only matching company names should be returned in search result. Name not containing matched result: " + fetched_name)
                    break

        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    def test_10_verify_search_address_by_invalid_string_api(self, resource):
        """
        This test validates that no address is fetched by invalid name (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call search address API and Validate that no response is obtained when contact is searched with:
        # 1. InValid Name":
        search_query = '@%23$'

        paramval = 'fields=name,company,addresses.addressLine1,addresses.city&search=' + search_query

        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # "Verify that returned names contain the search string:"
        total_records = len(search_address_resp.json())
        if total_records > 0:
            self.Failures.append("No Address should be fetched for the provided string. ")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_11_verify_search_address_by_type_api(self, resource):
        """
        This test validates that address can be fetched by their type successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call search address API and Validate that senders address can be fetched in Ascending list:
        paramval = 'sort=name,desc'

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='sender', is_admin='n',
                                                                             param_val=paramval)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Verify that returned address are only of sender type:"
        total_records = len(res)

        if total_records == 0:
            pytest.fail("No address is fetched for the sender type. ")
        else:
            for i in range(total_records):
                fetched_type = res[i]['contactType']
                if fetched_type != 'SENDER':
                    pytest.fail("Only Sender type address should be fetched in the response.")
                    break

        # "Call search address API and Validate that recipients address can be fetched in Ascending list":
        paramval = 'sort=name,asc'

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='recipient', is_admin='n', param_val=paramval)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Verify that returned address are only of sender type: "
        total_records = len(res)
        if total_records == 0:
            pytest.fail(
                "No address is fetched for the sender type. ")
        else:
            for i in range(total_records):
                fetched_type = res[i]['contactType']
                if fetched_type != 'RECIPIENT':
                    pytest.fail(
                        "Only recipient type address should be fetched in the response.")
                    break

    @pytest.mark.address_book_sp360commercial_reg
    def test_12_verify_search_address_by_type_name_search_query_api(self, resource):
        """
        This test validates that address can be fetched by their type successfully based on search query (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Verify that sender address can be fetched for: 1. Valid name:
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        contact_name = str(get_row_data['testInput'])

        paramval = 'fields=name&search=' + contact_name

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='sender', is_admin='n',
                                                                             param_val=paramval)
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Verify that returned names contain the search string":
        total_records = len(res)
        if total_records == 0:
            pytest.fail(
                "No Sender's Address should be fetched for the provided string. ")
        else:
            for i in range(total_records):
                fetched_name = res[i]['name']
                is_found = fetched_name.find(contact_name)
                print(is_found)
                if is_found < 0:
                    pytest.fail(
                        "Only matching contact names should be returned in search result. Name not containing matched result: " + fetched_name)
                    break

        # "Call search address API and Validate that recipients address can be fetched in Ascending list":

        paramval = 'fields=name&search=' + contact_name

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='recipient', is_admin='n',
                                                                             param_val=paramval)
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Verify that returned names contain the search string':
        total_records = len(res)
        if total_records == 0:
            pytest.fail(
                "No Address is fetched for the provided string. ")
        else:
            for i in range(total_records):
                fetched_name = res[i]['name']
                is_found = fetched_name.find(contact_name)
                if is_found < 0:
                    pytest.fail(
                        "Only matching recipient contact names should be returned in search result. Name not containing matched result: " + fetched_name)
                    break

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_13_verify_search_address_by_type_comp_search_query_api(self, resource):
        """
        This test validates that address can be fetched by their type successfully based on search query (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, email, pwd = (resource['addressbook_api']
                              .get_sub_id_user_cred_from_addressbook_file(sub_type='PITNEYSHIP_PRO', user_type='E'))

        # Generate user access token
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # Delete existing contacts
        resource['addressbook_api'].delete_all_contacts(is_admin=True, sub_id=sub_id)

        cont_data = resource['data_generator'].address_book_data_setter()
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

        add_contact_resp = resource['addressbook_api'] \
            .add_contact_api(contact_type='RECIPIENT', int_dlvry=int_dlvry, name=name, comp=comp,
                             email=email, phone=phone, addr1=addr1, city=city, country=country,
                             postal=postal, state=state, sub_id=sub_id, is_admin=False,
                             client_token=user_token)
        assert_that(self.validate_response_code(add_contact_resp, 201))
        created_cont_id = add_contact_resp.json()

        search_address_resp = (resource['addressbook_api']
                               .search_contacts_with_query_api(search=comp, sub_id=sub_id, is_admin=False,
                                                               client_token=user_token))
        assert_that(self.validate_response_code(search_address_resp, 200))
        fetched_cont_id = search_address_resp.json()[0]['id']
        assert_that(created_cont_id, equal_to(fetched_cont_id))

    @pytest.mark.address_book_sp360commercial_reg
    def test_14_verify_search_address_by_type_address_query_user_api(self, resource):
        """
        This test validates that added address can be fetched by valid address successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call search address API and Validate that successful response is obtained when Address is searched with:"
        # "Valid Address Line 1":

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        addr_ln = str(get_row_data['testInput'])

        paramval = 'fields=addresses.addressLine1&search=' + addr_ln

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='sender', is_admin='n',
                                                                             sub_id=sub_id,
                                                                             param_val=paramval)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Verify that returned names contain the search string:"
        total_records = len(res)
        if total_records == 0:
            pytest.fail("No Address fetched for the provided string. ")

        else:
            for i in range(total_records):
                fetched_senders_address = str(res[i]['addresses'][0]['addressLine1'])
                fetched_contact_type = str(res[i]['contactType'])

                assert_that(addr_ln, equal_to_ignoring_case(fetched_senders_address))
                assert_that(fetched_contact_type, equal_to('SENDER'))

        # "Call search address API and Validate that recipients address can be fetched in Ascending list":
        paramval = 'fields=addresses.addressLine1&search=' + addr_ln
        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='recipient', is_admin='n',
                                                                             sub_id=sub_id,
                                                                             param_val=paramval)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True
        # "Verify that returned names contain the search string":
        total_records = len(res)
        if total_records == 0:
            pytest.fail("No sender's Address is fetched for the provided string. ")
        else:
            for i in range(total_records):
                fetched_recipient_addr = str(res[i]['addresses'][0]['addressLine1'])
                fetched_contact_type = str(res[i]['contactType'])
                assert_that(fetched_recipient_addr, equal_to_ignoring_case(addr_ln))
                assert_that(fetched_contact_type, equal_to('RECIPIENT'))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_15_verify_get_address_by_id_client_api(self, resource):
        """
        This test validates that contact can be fetched successfully by Id (positive scenario)

        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')
        # "Call Fetch address by Id API and validate response':
        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_rec_" + str(random.randint(1, 200))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        addr_line_1 = 'Auto_line_1'
        city = 'Nashville'
        country_code = 'US'
        postal_cd = '37210'
        state = 'TX'

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, addr1=addr_line_1, city=city,
                                 country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_16_verify_get_address_by_invalid_id_client_api(self, resource):
        """
        This test validates that contact can not be fetched by invalid Id (positive scenario)

        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call Fetch address by Id API and validate response:"

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        contact_id = str(get_row_data['testInput'])
        err_msg = str(get_row_data['ErrorMsg'])
        expected_err_msg = err_msg.replace("?", contact_id)

        # "Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))
        err_desc = get_cont_resp.json()['errors'][0]['errorDescription']
        assert_that(expected_err_msg, equal_to(err_desc))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_17_verify_search_address_by_invalid_type_user_api(self, resource):
        """
        This test validates that error should be obtained when invalid address type is provided (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call search address API and Validate that senders address can be fetched in Ascending list":
        paramval = 'sort=name,desc'

        res, status_code = resource['addressbook_api'].verify_search_address_by_type_api(addr_type='sende', is_admin='n',
                                                                             param_val=paramval)
        assert self.validate_expected_and_actual_response_code(400, status_code) is True

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.address_book_fedramp_smoke
    def test_18_verify_add_update_del_contact_addr_client_api(self, resource):
        """
        This test validates that contact can be updated successfully (positive scenario)
        Update all details
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call Addressbook add new contact and validate that contact of type recipient can be created successfully: "
        cont_data = resource['data_generator'].address_book_data_setter()
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

        contact_type = 'RECIPIENT'
        type = 'S'
        personal_id = generate_random_string()

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=int_dlvry, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr1,
                                 city=city, country=country, postal=postal, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        cont_id = str(add_cont_resp.json())

        # "Fetch the created contact:"
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        assert_that(personal_id, equal_to(get_cont_resp.json()['personalID']))

        update_cont_data = resource['data_generator'].address_book_data_setter()
        updt_name = update_cont_data[0]
        updt_comp = update_cont_data[1]
        updt_email = update_cont_data[2]
        updt_phone = update_cont_data[3]
        updt_addr1 = update_cont_data[4]
        updt_addr2 = update_cont_data[5]
        updt_city = update_cont_data[7]
        updt_state = update_cont_data[8]
        updt_postal = update_cont_data[9]
        updt_country = update_cont_data[10]
        updt_int_dlvry = update_cont_data[11]
        updt_contact_type = 'SENDER'

        update_cont_resp = resource['addressbook_api']\
            .update_contact_api(id=cont_id, contact_type=updt_contact_type, int_dlvry=updt_int_dlvry, type=type,
                                name=updt_name, comp=updt_comp, email=updt_email, phn=updt_phone,
                                personal_id=personal_id, addr1=updt_addr1, addr2=updt_addr2, city=updt_city,
                                country=updt_country, postal=updt_postal, state=updt_state, cont_id=cont_id)
        assert_that(self.validate_response_code(update_cont_resp, 200))

        # Fetch the updated contact
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        assert_that(updt_name, equal_to(get_cont_resp.json()['name']))

        # Delete the created contact
        del_cont_resp = resource['addressbook_api'].delete_contact_api(cont_id=cont_id, is_admin=False)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Fetch the deleted contact
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial_reg
    def test_19_verify_create_addr_duplicate_personal_Id_check_client_api(self, resource):
        """
        This test validates that contact can't be created with duplicate personal Ids (positive scenario)
        Valid Address: US
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call Addressbook add new contact and validate that contact of type recipient can be created successfully:"

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Rec_US_Addr_" + str(random.randint(1, 50000))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # "Fetch the created contact:"
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # "Create a new contact with same personal Id:"
        expected_err_msg = 'Invalid request: Personal Id ['+str(personal_id)+'] Already Exists'

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 400))
        err_msg = add_cont_resp.json()['errors'][0]['errorDescription']
        assert_that(expected_err_msg, equal_to(err_msg))

        # "Delete the created contact:"
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Fetch the created contact:"
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_20_verify_create_pvt_recipient_US_addr_client_api(self, resource):
        """
        This test validates that private contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'U'
        name = "Pvt_Rec_Contct_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created contact
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_21_verify_delete_contact_method_user_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Addressbook add new contact and validate that contac of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Rec_US_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        get_cont_personal_id_resp = resource['addressbook_api'] \
            .get_contact_by_personal_id_api(personal_id=personal_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=comp, email=email, phn=phone, personal_id=personal_id, addr1=addr_line_1,
                                 city=city, country=country_code, postal=postal_cd, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Fetch the created contact Id and verify the details
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))

        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id,
                                                                      is_admin='n')

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_22_verify_personal_id_uniqueness_check_method_user_api(self, resource):
        """
        This test validates if a personal Id provided by user is unique or not
        Cases covered:
        1. Duplicate: False when personal id is unique
        2. True when personal Id is duplicate
        3. False when personal Id of deleted user is used
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # 1. Fetch an existing contact > Fetch its personal Id > Verify that duplicate is True in the response

        (name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery, personal_id,
         dept_name, office_location, mail_stop_id, accessibility, notification_all, primary_location,
         additional_email_ids) = resource['data_generator'].address_book_data_setter()

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        personal_id = generate_random_string(char_count=8)

        # Verify if personal Id is unique

        get_cont_personal_id_resp = resource['addressbook_api'].get_contact_by_personal_id_api(personal_id=personal_id)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

        add_cont_resp = resource['addressbook_api'] \
            .add_new_contact_api(contact_type=contact_type, int_dlvry=internal_delivery, type=type, name=name,
                                 comp=company, email=email, phn=phone, personal_id=personal_id, addr1=addr1,
                                 city=city, country=country, postal=postal, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        contact_id = str(add_cont_resp.json())

        # Verify that duplicate is true when existing personal Id is fetched

        get_cont_personal_id_resp = resource['addressbook_api'].get_contact_by_personal_id_api(personal_id=personal_id)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('true'))

        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

        # Verify that duplicate is false when personal Id of deleted user if fetched

        get_cont_personal_id_resp = resource['addressbook_api'].get_contact_by_personal_id_api(personal_id=personal_id)
        assert_that(self.validate_response_code(get_cont_personal_id_resp, 200))
        is_duplicate = get_cont_personal_id_resp.json()['duplicate']
        assert_that(is_duplicate, equal_to('false'))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.parametrize('cont_type, cont_edit_field', [('RECIPIENT', 'name'),
                                                            ('SENDER', 'name'),
                                                            ('RECIPIENT', ['name', 'email', 'phone']),
                                                            ('SENDER', ['name', 'email', 'phone'])])
    def test_23_verify_add_update_del_contact_addr_client_api(self, resource, cont_type, cont_edit_field):
        """
        This test validates that the users contact details are updated correctly through patch contact API, which is
        used to update individual contact fields.

        :param resource: The resource required for the api requests.
        :param cont_type: The contact type - Recipient or Sender.
        :param cont_edit_field: The individual fields that are to be updated in the contact.
        :returns: The test execution status and results.
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        cont_data = resource['data_generator'].address_book_data_setter()
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
        check_list = ['name', 'email', 'phone']
        contact_type = str(cont_type)
        type = 'S'

        add_cont_resp = resource['addressbook_api'].add_new_contact_api(contact_type=contact_type,
                                                                        int_dlvry=int_dlvry, type=type,
                                                                        name=name, comp=comp, email=email, phn=phone,
                                                                        addr1=addr1, city=city, country=country,
                                                                        postal=postal, state=state, is_admn=False)
        assert_that(self.validate_response_code(add_cont_resp, 201))
        cont_id = str(add_cont_resp.json())

        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        assert_that(contact_type, equal_to(get_cont_resp.json()['contactType']))
        assert_that(name, equal_to(get_cont_resp.json()['name']))
        assert_that(email, equal_to(get_cont_resp.json()['emails'][0]['email']))
        assert_that(phone, equal_to(get_cont_resp.json()['phones'][0]['phone']))

        update_cont_data = resource['data_generator'].address_book_data_setter()
        updt_name = update_cont_data[0]
        updt_email = update_cont_data[2]
        updt_phone = update_cont_data[3]

        # partial update contact based on parametrized field values
        if cont_edit_field == 'name':
            partial_update_cont_resp = resource['addressbook_api']\
                .patch_update_contact_api(cont_id=cont_id, name=updt_name)
            assert_that(self.validate_response_code(partial_update_cont_resp, 200))

            get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
            assert_that(self.validate_response_code(get_cont_resp, 200))
            assert_that(contact_type, equal_to(get_cont_resp.json()['contactType']))
            assert_that(updt_name, equal_to(get_cont_resp.json()['name']))

        elif all(item in check_list for item in cont_edit_field):
            partial_update_cont_resp = resource['addressbook_api']\
                .patch_update_contact_api(cont_id=cont_id, name=updt_name, email=updt_email, phn=updt_phone)
            assert_that(self.validate_response_code(partial_update_cont_resp, 200))

            get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
            assert_that(self.validate_response_code(get_cont_resp, 200))
            assert_that(contact_type, equal_to(get_cont_resp.json()['contactType']))
            assert_that(updt_name, equal_to(get_cont_resp.json()['name']))
            assert_that(updt_email, equal_to(get_cont_resp.json()['emails'][0]['email']))
            assert_that(updt_phone, equal_to(get_cont_resp.json()['phones'][0]['phone']))
        else:
            pytest.fail('No fields are selected to update contact!')

        # delete the created contact
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=cont_id)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # search with deleted contact id
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=cont_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

