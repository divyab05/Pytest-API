""" This module contains all test cases."""

import inspect
import json
import pytest
import random
import logging
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    addressbook = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config)}
    yield addressbook


@pytest.mark.usefixtures('initialize')
class TestAddressbook_Contact_Admin_API(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, resource):
        exe_status.__init__()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, resource, app_config):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "ADDRESSBOOK_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        self.Failures = []

    @pytest.mark.address_book_sp360commercial_reg
    def test_01_verify_create_subscription_rcpnt_admin_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : Subscription
        :return: return test status
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_ssto_subscription__Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'S'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(201, status_code) is True

        contact_id = str(res)

        # Fetch the created contact Id and verify the details from SSTO list
        # 1. Validate personal ID is generated
        # 2. Validate that details are correctly reflected in SSTO

        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        res = get_cont_resp.json()
        # Validate that personal Id is not null
        personal_id = len(res['personalID'])
        created_type = res['contactType']

        if personal_id == 0:
            pytest.fail("Personal Id should not be blank")

        # Validate that created contact type is correct
        contact_lvl_type = res['type']
        assert self.validate_expected_and_actual_values_code(contact_lvl_type, type) is True

        created_type = res['contactType']
        assert self.validate_expected_and_actual_values_code(created_type, contact_type) is True
        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_ssto_api(cont_id=contact_id, sub_id=sub_id,
                                                                                 is_admin='y',
                                                                                 schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial_reg
    def test_02_verify_create_div_rcpnt_admin_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : Division
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'D'
        name = "Auto_ssto_div_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'D'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        div_id = str(get_row_data['testInput'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state, div_id=div_id,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(201, status_code) is True

        contact_id = str(res)

        # Fetch the created contact Id and verify the details
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        res = get_cont_resp.json()
        personal_id = len(res['personalID'])

        if personal_id == 0:
            pytest.fail("Personal Id should not be blank")

        # Validate that created contact type is correct
        lvl_type = res['type']
        assert self.validate_expected_and_actual_values_code(lvl_type, type) is True

        created_type = res['contactType']
        assert self.validate_expected_and_actual_values_code(created_type, contact_type) is True

        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_ssto_api(cont_id=contact_id, sub_id=sub_id,
                                                                                 is_admin='y',
                                                                                 schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial_reg
    def test_03_verify_create_loc_rcpnt_admin_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : Location
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'L'
        name = "Auto_ssto_loc_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'L'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        loc_id = str(get_row_data['testInput'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state, loc_id=loc_id,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(201, status_code) is True

        contact_id = str(res)

        # Fetch the created contact Id and verify the details
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        res = get_cont_resp.json()
        personal_id = len(res['personalID'])

        if personal_id == 0:
            pytest.fail("Personal Id should not be blank")

        # Validate that created contact type is correct
        lvl_type = res['type']
        assert self.validate_expected_and_actual_values_code(lvl_type, type) is True

        created_type = res['contactType']
        assert self.validate_expected_and_actual_values_code(created_type, contact_type) is True

        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_ssto_api(cont_id=contact_id,
                                                                                 schema_name=schema_name,
                                                                                 sub_id=sub_id, is_admin='y')

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial_reg
    def test_04_verify_import_addressbook_ssto_sub_admn_api(self, resource):
        """
        This test validates that imported contacts are reflected in SSTO list (Positive scenario)
        Shared Level: Subscription
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response:
        name = "Auto_SSTO_sub_admin_Import_" + str(random.randint(1, 100))
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='ssto', is_admin=True,
                                     sub_id=sub_id, email=email, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))

        # Verify the schema of upload file response:
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'mapping_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['addressbook_api'].verify_res_schema(res=cont_upload_resp.json(), expected_schema=expected_schema)

        if len(isValid) > 0:
            self.Failures.append(
                "Response schema of upload file doesn't match with expected schema" + str(isValid))

        # Fetch the created job Id:
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='ssto', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Verify the schema of import process response:
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'import_status_schema')) as schema:
            expected_schema = json.load(schema)

        res_txt = json.loads(res.text)

        isValid = resource['addressbook_api'].verify_res_schema(res=res_txt, expected_schema=expected_schema)

        if len(isValid) > 0:
            self.Failures.append(
                "Response schema doesn't match with expected schema" + str(isValid))

        # Validate that imported records are uploaded successfully:

        res, status_code = resource['addressbook_api'].verify_import_status_api(job_id=job_id, subId=sub_id,
                                                                                is_admin='y',
                                                                                schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        status = str(res['status'])

        assert self.validate_expected_and_actual_values_code('Processed', status)

        paramval = 'fields=name&search=' + name

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert_that(self.validate_response_code(search_address_resp, 200))

        personal_id = len(search_address_resp.json()[0]['id'])

        if (personal_id == 0):
            pytest.fail("Personal Id should not be null")

        # Validate that created contact type is correct
        created_type = search_address_resp.json()[0]['type']
        assert self.validate_expected_and_actual_values_code(created_type, 'S') is True

        # Delete the created contact
        contact_id = search_address_resp.json()[0]['id']
        status_code = resource['addressbook_api'].verify_delete_contact_ssto_api(cont_id=contact_id,
                                                                                 schema_name=schema_name,
                                                                                 sub_id=sub_id,
                                                                                 is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Verify that deleted contact can't be fetched:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 200))

    @pytest.mark.address_book_sp360commercial_reg
    def test_05_verify_update_contact_ssto_admin_api(self, resource):
        """
        This test validates that contact can be updated successfully (positive scenario)
        Update all details
        Type: Recipient
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # "Call Addressbook add new contact and validate that contact of type recipient can be created successfully: "

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'S'
        name = "Auto_ssto_sub_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'S'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(201, status_code) is True
        contact_id = str(res)

        # "Fetch the created contact:"
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        res = get_cont_resp.json()
        personal_id = len(res['personalID'])
        created_type = res['contactType']
        if personal_id == 0:
            pytest.fail("Personal Id should not be blank")

        assert_that(created_type, equal_to(contact_type))

        # Validate that created contact type is correct
        contact_lvl_type = res['type']
        assert self.validate_expected_and_actual_values_code(contact_lvl_type, type) is True

        id = res['id']
        personal_id = res['personalID']
        updt_contact_type = 'SENDER'
        internal_delivery = False
        type = 'S'
        updt_name = "Updt_Rec_" + str(random.randint(1, 50000))
        updt_comp = "Test PB New"
        updt_email = updt_name + "@yopmail.com"
        updt_phone = '9876543215'

        updt_addr_line_1 = '599 Heather Sees Way'
        updt_addr_line_2 = 'Euclid Street'
        # updt_addr_line_3 = 'House 2'
        updt_city = 'Owosso'

        updt_postal_cd = '48867'
        updt_state = 'MI'

        status_code = resource['addressbook_api'].verify_update_ssto_contact_api(id=id, contact_type=updt_contact_type,
                                                                                 int_dlvry=internal_delivery,
                                                                                 type=type,
                                                                                 name=updt_name, comp=updt_comp,
                                                                                 email=updt_email,
                                                                                 phn=updt_phone,
                                                                                 personal_id=personal_id,
                                                                                 addr1=updt_addr_line_1,
                                                                                 addr2=updt_addr_line_2,
                                                                                 city=updt_city, country=country_code,
                                                                                 postal=updt_postal_cd,
                                                                                 state=updt_state,
                                                                                 sub_id=sub_id, is_admn='y',
                                                                                 cont_id=contact_id,
                                                                                 schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Fetch the Updated contact:"
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        fetched_name = get_cont_resp.json()['name']
        assert_that(updt_name, equal_to(fetched_name))

        # "Delete the created admin:"
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=contact_id, sub_id=sub_id, schema_name=schema_name, is_admin=True)
        status_code = del_cont_resp.status_code
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Fetch the Deleted contact:"
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial_reg
    def test_06_verify_create_blank_div_rcpnt_admin_api(self, resource):
        """
        This test validates that error is obtained contact of type recipient is created without div Id (negative scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : Division
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'D'
        name = "Auto_ssto_div_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'D'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        err_desc = str(get_row_data['ErrorMsg'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        obtained_err = str(res['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_response_code(400, status_code) is True

        assert self.validate_expected_and_actual_values_code(err_desc, obtained_err) is True

    @pytest.mark.address_book_sp360commercial_reg
    def test_07_verify_create_blank_loc_rcpnt_admin_api(self, resource):
        """
        This test validates that error is obtained contact of type recipient is created without location Id (negative scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : loc
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = False
        type = 'L'
        name = "Auto_ssto_loc_Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'L'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])
        err_desc = str(get_row_data['ErrorMsg'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        obtained_err = str(res['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_response_code(400, status_code) is True

        assert self.validate_expected_and_actual_values_code(err_desc, obtained_err) is True

    @pytest.mark.address_book_sp360commercial_reg
    def test_08_verify_create_subscription_rcpnt_internal_with_delivery_admin_api(self, resource):
        """
        This test validates that contact of type recipient can be created successfully (positive scenario)
        Valid Address: US
        Type: Recipient
        Shared Address Level : Subscription
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call add new contact and validate that contact of type recipient can be created successfully:

        contact_type = 'RECIPIENT'
        internal_delivery = True
        type = 'S'
        name = "Auto_ssto_subscription__Addr_" + str(random.randint(1, 500))
        comp = "Test PB"
        email = name + "@yopmail.com"
        phone = '9876543210'
        receiving_acc_lvl = 'S'

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        addr_line_1 = str(get_row_data['addr1'])
        city = str(get_row_data['city'])
        country_code = str(get_row_data['country'])
        postal_cd = str(get_row_data['postalCode'])
        state = str(get_row_data['state'])

        res, status_code = resource['addressbook_api'].verify_add_new_contact_ssto_api(contact_type=contact_type,
                                                                                       int_dlvry=internal_delivery,
                                                                                       type=type,
                                                                                       name=name, comp=comp,
                                                                                       email=email,
                                                                                       phn=phone, addr1=addr_line_1,
                                                                                       city=city, country=country_code,
                                                                                       postal=postal_cd,
                                                                                       state=state,
                                                                                       receiving_access_lvl=receiving_acc_lvl,
                                                                                       sub_id=sub_id, is_admn='y',
                                                                                       schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(201, status_code) is True

        contact_id = str(res)

        # Fetch the created contact Id and verify the details from SSTO list
        # 1. Validate personal ID is generated
        # 2. Validate that details are correctly reflected in SSTO

        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 200))
        res = get_cont_resp.json()
        # Validate that personal Id is not null
        personal_id = len(res['personalID'])

        if personal_id == 0:
            pytest.fail("Personal Id should not be blank")

        # Validate that created contact type is correct
        contact_lvl_type = res['type']
        assert self.validate_expected_and_actual_values_code(contact_lvl_type, type) is True

        created_type = res['contactType']
        assert self.validate_expected_and_actual_values_code(created_type, contact_type) is True

        intrnl_delivery = str(res['internalDelivery'])
        assert self.validate_expected_and_actual_values_code(intrnl_delivery, 'True') is True
        # Delete the created contact

        status_code = resource['addressbook_api'].verify_delete_contact_ssto_api(cont_id=contact_id, sub_id=sub_id,
                                                                                 is_admin='y',
                                                                                 schema_name=schema_name)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the deleted contact and verify error code
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))
