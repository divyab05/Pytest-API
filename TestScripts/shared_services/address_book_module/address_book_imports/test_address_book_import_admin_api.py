""" This module contains all test cases."""
import inspect
import json
import logging
import random
import string
import time
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestAddressbookAdminImport(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.configparameter = "ADDRESSBOOK_MGMT"

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    def test_01_verify_import_addressbook_sp_360_admin_api(self, resource):
        """
        This test validates that address book can be created through sp360 Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response:
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        name = "Auto_SP_Import_addr_" + str(random.randint(1, 100))
        company = 'Auto_Test_Comp'
        email = 'auto_test_mail@email.com'
        personal_id = generate_random_string(char_count=8)

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        res = cont_upload_resp.json()

        # Verify the schema of upload file response:
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'mapping_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

        if len(isValid) > 0:
            pytest.fail(f"Response schema of upload file doesn't match with expected schema: {isValid}")

        job_id = str(res['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Verify the schema of import process response:
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'import_status_schema')) as schema:
            expected_schema = json.load(schema)

        res_txt = json.loads(cont_mapping_resp.text)

        isValid = resource['addressbook_api'].verify_res_schema(res=res_txt, expected_schema=expected_schema)

        if len(isValid) > 0:
            pytest.fail(f"Response schema of upload file doesn't match with expected schema: {isValid}")

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name) # fix here
        assert_that(res['status'], equal_to('Processed')) # getting processing error

        paramval = f'fields=name&search={name}'
        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # Delete the created contact
        contact_id = search_address_resp.json()[0]['id']

        del_cont_resp = resource['addressbook_api']\
            .delete_contact_api(cont_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Verify that deleted contact can't be fetched:
        get_cont_resp = resource['addressbook_api']\
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    # fix this
    def test_02_verify_import_addressbook_with_blank_name_admin_api(self, resource):
        """
        This test validates that address book can be created with blank name (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response.
        name = ""
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        company = 'Auto__blnk_nm_adm_Comp'+personal_id

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        res = cont_upload_resp.json()

        # Verify the schema of upload file response
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'mapping_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)
        if len(isValid) > 0:
            pytest.fail(f"Response schema of upload file doesn't match with expected schema: {isValid}")

        job_id = str(res['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Verify the schema of import process response:
        with open(self.prop.get('ADDRESSBOOK_MGMT', 'import_status_schema')) as schema:
            expected_schema = json.load(schema)

        res_txt = json.loads(cont_mapping_resp.text)

        isValid = resource['addressbook_api'].verify_res_schema(res=res_txt, expected_schema=expected_schema)

        if len(isValid) > 0:
            pytest.fail(f"Response schema of upload file doesn't match with expected schema: {isValid}")

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name) # fix here
        assert_that(res['status'], equal_to('Processed')) # getting processing error

        # Fetch the Imported Address
        paramval = f'fields=company&search={company}'
        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert_that(self.validate_response_code(search_address_resp, 200))
        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        del_cont_resp = resource['addressbook_api'] \
            .delete_contact_api(cont_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Verify that error is obtained when deleted contact is fetched:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.skip(reason="Failing in CI/CD with docker image - sha256:366606c4ffe37b088562a1cec788368cd88b640d32400b03e650493728c96ff3")
    def test_03_verify_import_addressbook_with_blank_company_admin_api(self, resource):
        """
        This test validates that address book can be created with blank company (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response with blank company name:
        name = "Auto_SP_Import_addr_" + str(random.randint(1, 50000))
        company = ' '
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        res = cont_upload_resp.json()

        # Fetch the created job Id:
        job_id = str(res['jobId'])

        # Verify the status of uploaded file:

        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert self.validate_values_comparison_code('Processed', res['status']) is True

        paramval = 'fields=name&search=' + name

        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert self.validate_expected_and_actual_response_code(200, search_address_resp.status_code) is True

        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id,
                                                                      sub_id=sub_id,
                                                                      is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_04_verify_import_addressbook_without_name_and_company_admin_api(self, resource):
        """
        This test validates that address book cannot be created with blank company and blank name (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API with blank name and company and Validate the response:
        name = " "
        company = ' '
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))

        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert_that(res['status'], equal_to('ProcessingError'))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.skip(reason="Search performance issue reported: SPSS-5486")
    def test_05_verify_import_addressbook_fedex_admin_api(self, resource):
        """
        This test validates that address book can be created through fedEx Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response:

        name = "Auto_FedEx_Import_addr_" + str(random.randint(1, 100))
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='fedEx', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='fedEx', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert self.validate_values_comparison_code('Processed', res['status']) is True

        paramval = 'fields=name&search=' + name

        time.sleep(10)

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert self.validate_expected_and_actual_response_code(200, search_address_resp.status_code) is True

        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id,
                                                                      sub_id=sub_id,
                                                                      is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.skip(reason="Failing in CI/CD with docker image - sha256:366606c4ffe37b088562a1cec788368cd88b640d32400b03e650493728c96ff3")
    def test_06_verify_import_addressbook_UPS_admin_api(self, resource):
        """
        This test validates that address book can be created through UPS Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response.

        name = "Auto_adm_UPS_Import_addr_" + str(random.randint(1, 100))
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='UPS', is_admin=True, sub_id=sub_id,
                                     email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='UPS', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert self.validate_values_comparison_code('Processed', res['status']) is True

        paramval = 'fields=name&search=' + name

        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_address_api(sub_id=sub_id, param_val=paramval,
                                                                             is_admin=True)
        assert self.validate_expected_and_actual_response_code(200, search_address_resp.status_code) is True

        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id,
                                                                      sub_id=sub_id,
                                                                      is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_07_verify_import_addressbook_with_invalid_email_admin_api(self, resource):
        """
        This test validates that address book cannot be created with invalid email (Negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response.

        name = "Auto_Addr_Import_Name"
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', is_admin=True,
                                     sub_id=sub_id, email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert_that(res['status'], equal_to('ProcessingError'))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_08_verify_import_addressbook_spo_format_admin_api(self, resource):
        """
        This test validates that address book can be created through SPO Import format with double quotes in headers
        and data (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response
        name = "Auto_SPO_Import_addr_" + str(random.randint(1, 50000))
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        schema_name = str(get_row_data['schema_name'])
        email = 'auto_test_mail@emai.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='SPO', is_admin=True, sub_id=sub_id,
                                     email=email, personal_id=personal_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))

        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file: "):
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='SPO', is_admin=True, sub_id=sub_id,
                                     schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        res = resource['addressbook_api'].get_completed_job_status(is_admin='y', job_id=job_id, sub_id=sub_id,
                                                                   schema_name=schema_name)
        assert_that(res['status'], equal_to('Processed'))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.parametrize('no_of_records', [1])
    def test_09_validate_addressbook_import_and_export_with_given_n_records(self, resource, no_of_records):
        """
        This test validates that address book can be created through sp360 Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, email, pwd = (resource['addressbook_api']
                              .get_sub_id_user_cred_from_addressbook_file(sub_type='PITNEYSHIP_PRO', user_type='E'))

        csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'common_addressbook_import')
        export_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'common_addressbook_export')

        # Delete all contacts from the subscription
        resource['addressbook_api'].delete_all_contacts(is_admin=True, sub_id=sub_id)

        (resource['addressbook_api']
         .import_auto_generated_contacts(csv_filepath=csv_filepath, sub_id=sub_id, no_of_records=no_of_records, is_admin=True))

        resource['addressbook_api'] \
            .export_contacts_check_status_and_download_export_file(sub_id=sub_id, is_admin=True,
                                                                   export_csv_filepath=export_csv_filepath)

        assert_that(self.compare_csv_rows(source_file=csv_filepath,
                                          target_file=export_csv_filepath, skip_header=True))
