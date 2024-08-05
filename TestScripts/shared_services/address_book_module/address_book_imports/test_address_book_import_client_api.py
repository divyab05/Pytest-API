""" This module contains all test cases."""
import inspect
import logging
import random
import string
import time
import pytest
from hamcrest import assert_that, equal_to, is_not
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import get_current_timestamp, generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    addressbook = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'data_generator': DataGenerator,
    }
    yield addressbook


@pytest.mark.usefixtures('initialize')
class TestAddressbookClientImport(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.configparameter = "ADDRESSBOOK_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    def test_01_verify_import_addressbook_sp_360_user_api(self, resource):
        """
        This test validates that address book can be created through sp360 Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response:
        name = "Auto_SP_Import_addr_" + str(random.randint(1, 100))
        company = 'Auto_Test_Comp'
        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api'].contact_upload_file_api(nick_name=name, comp=company,
                                                                               import_file_type='sp_360', email=email,
                                                                               personal_id=personal_id)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api'].addressbook_mapping_api(job_id=job_id, import_file_type='sp_360')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        resource['addressbook_api'].check_job_status(job_id=job_id, is_admin=False)

        paramval = 'fields=name&search=' + name
        time.sleep(2)
        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        # Delete the created contact
        contact_id = search_address_resp.json()[0]['id']
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Verify that deleted contact can't be fetched:
        get_cont_resp = resource['addressbook_api'] \
            .get_contact_by_cont_id_api(contact_id=contact_id, sub_id=sub_id, is_admin=False)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_02_verify_import_addressbook_with_blank_name_user_api(self, resource):
        """
        This test validates that address book can be created with blank name (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response.
        name = " "

        email = 'auto_import@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        company = 'Auto_blnk_nm_Comp'+personal_id

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', email=email,
                                     personal_id=personal_id)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api'].addressbook_mapping_api(job_id=job_id, import_file_type='sp_360')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        resource['addressbook_api'].check_job_status(is_admin=False, job_id=job_id)

        # Fetch the Imported Address
        paramval = 'fields=company&search=' + company
        time.sleep(2)
        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Verify that error is obtained when deleted contact is fetched:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_03_verify_import_addressbook_with_blank_company_user_api(self, resource):

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response with blank company name:
        name = "Auto_SP_Import_addr_" + str(random.randint(1, 50000))
        company = ' '
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', email=email,
                                     personal_id=personal_id)
        assert_that(self.validate_response_code(cont_upload_resp, 200))

        # Fetch the created job id:
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api'].addressbook_mapping_api(job_id=job_id, import_file_type='sp_360')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        resource['addressbook_api'].check_job_status(is_admin=False, job_id=job_id)

        paramval = 'fields=name&search=' + name
        time.sleep(2)
        search_address_resp = resource['addressbook_api'].search_address_api(param_val=paramval)
        assert_that(self.validate_response_code(search_address_resp, 200))

        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        status_code = resource['addressbook_api'].verify_delete_contact_admin_api(cont_id=contact_id, is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_04_verify_import_addressbook_without_name_and_company_user_api(self, resource):
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

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='sp_360', sub_id=sub_id,
                                     email=email, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='sp_360', sub_id=sub_id, schema_name=schema_name)
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are failed:
        job_status = resource['addressbook_api'].check_job_status(job_id=job_id, sub_id=sub_id)
        assert_that(job_status, equal_to('ProcessingError'))
        self.log.info(f'Import job status is {job_status} as expected!')

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_05_validate_import_addressbook_fedex_by_user(self, resource):
        """
        This test validates that address book can be created through FedEx Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response:
        name = f'Auto_FedEx_Name_{generate_random_string(uppercase=False, char_count=4)}'
        company = f'Auto_FedEx_Comp_{generate_random_string(uppercase=False, char_count=4)}'
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='fedEx', email=email,
                                     personal_id=personal_id)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api'].addressbook_mapping_api(job_id=job_id, import_file_type='fedEx')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        job_status = resource['addressbook_api'].check_job_status(is_admin=False, job_id=job_id)
        assert_that(job_status, equal_to('Processed'))

        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api(search=name, is_admin=False)
        assert_that(self.validate_response_code(search_address_resp, 200))
        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        del_cont_resp = resource['addressbook_api'].delete_contact_api(cont_id=contact_id, is_admin=False)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_06_validate_import_addressbook_ups_by_user(self, resource):
        """
        This test validates that address book can be created through UPS Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        # Call Import address API and Validate the response.
        name = f'Auto_UPS_Name_{generate_random_string(uppercase=False, char_count=4)}'
        company = f'Auto_UPS_Comp_{generate_random_string(uppercase=False, char_count=4)}'
        email = 'auto_test_mail@email.com'
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        cont_upload_resp = resource['addressbook_api']\
            .contact_upload_file_api(nick_name=name, comp=company, import_file_type='UPS', email=email,
                                     personal_id=personal_id)
        assert_that(self.validate_response_code(cont_upload_resp, 200))
        job_id = str(cont_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api'].addressbook_mapping_api(job_id=job_id, import_file_type='UPS')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        job_status = resource['addressbook_api'].check_job_status(is_admin=False, job_id=job_id)
        assert_that(job_status, equal_to('Processed'))

        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api(search=name, is_admin=False)
        assert_that(self.validate_response_code(search_address_resp, 200))
        contact_id = search_address_resp.json()[0]['id']

        # Delete the created contact:
        del_cont_resp = resource['addressbook_api'].delete_contact_api(cont_id=contact_id, is_admin=False)
        assert_that(self.validate_response_code(del_cont_resp, 200))

        # Fetch the created contact:
        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=contact_id)
        assert_that(self.validate_response_code(get_cont_resp, 404))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.skip(reason="Contact override is not working with import, need to check with team on this")
    def test_07_verify_recipient_contact_overwrite_import_api(self, resource):
        """
        This test validates that address book can be created through sp360 Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        personal_id = generate_random_string(char_count=8)

        resource['addressbook_api'].delete_all_contacts(sub_id=sub_id, cont_type='SENDER', del_type='ALL', is_admin=True)
        resource['addressbook_api'].delete_all_contacts(sub_id=sub_id, cont_type='RECIPIENT', del_type='ALL', is_admin=True)

        resource['addressbook_api'].create_n_contacts(sub_id=sub_id, cont_type='SENDER')
        resource['addressbook_api'].create_n_contacts(sub_id=sub_id, cont_type='RECIPIENT', personal_id=personal_id)

        time.sleep(5)
        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api(client_token=user_token)
        assert_that(self.validate_response_code(search_address_resp, 200))

        contact_names_before_import = {'SENDER': None, 'RECIPIENT': None}

        for contact in search_address_resp.json():
            contact_type = contact['contactType']
            contact_name = contact['name']

            if contact_type == 'SENDER' and contact_names_before_import['SENDER'] is None:
                contact_names_before_import['SENDER'] = contact_name
            elif contact_type == 'RECIPIENT' and contact_names_before_import['RECIPIENT'] is None:
                contact_names_before_import['RECIPIENT'] = contact_name

        sender_name_before_import = contact_names_before_import['SENDER']
        rec_name_before_import = contact_names_before_import['RECIPIENT']

        # Call Import address API and Overwrite Recipient Address Validate the response :
        over_write_name = "Overwrite_rect_cont_" + str(random.randint(1, 100))
        overwrite_upload_resp = (resource['addressbook_api']
                                 .import_overwrite_upload_file_api(name=over_write_name, contact_type='RECIPIENT',
                                                                   address_type='S', personal_id=personal_id,
                                                                   client_token=user_token))
        assert_that(self.validate_response_code(overwrite_upload_resp, 200))
        job_id = str(overwrite_upload_resp.json()['jobId'])

        # Verify the status of uploaded file:
        cont_mapping_resp = resource['addressbook_api']\
            .addressbook_mapping_api(job_id=job_id, import_file_type='dataload', overwrite=True, type_overridden='S')
        assert_that(self.validate_response_code(cont_mapping_resp, 200))

        # Validate that imported records are uploaded successfully:
        resource['addressbook_api'].check_job_status(is_admin=False, job_id=job_id)

        time.sleep(5)
        second_search_address_resp = resource['addressbook_api'].search_contacts_with_query_api(client_token=user_token)
        assert_that(self.validate_response_code(second_search_address_resp, 200))

        contact_names_after_import = {'SENDER': None, 'RECIPIENT': None}

        for contact in second_search_address_resp.json():
            contact_type = contact['contactType']
            contact_name = contact['name']

            if contact_type == 'SENDER' and contact_names_after_import['SENDER'] is None:
                contact_names_after_import['SENDER'] = contact_name
            elif contact_type == 'RECIPIENT' and contact_names_after_import['RECIPIENT'] is None:
                contact_names_after_import['RECIPIENT'] = contact_name

        sender_name_after_import = contact_names_after_import['SENDER']
        rec_name_after_import = contact_names_after_import['RECIPIENT']

        # Verify that when only recipient is overridden then only recipient is overwritten
        # and there's no change on Sender or Private
        # 1. Validate that sender is not updated
        assert_that(sender_name_before_import, equal_to(sender_name_after_import))

        # 2. Validate that recipient is updated
        assert_that(rec_name_before_import, is_not(equal_to(rec_name_after_import)))

        # 3. Validate that recipient name is updated correctly
        assert_that(rec_name_after_import, equal_to(over_write_name))

        # Combined assertions
        assert_that(sender_name_before_import, equal_to(sender_name_after_import) and
                    rec_name_before_import != rec_name_after_import and
                    rec_name_after_import == over_write_name)

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_smoke
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_smoke
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.skip(reason="Contact override is not working with import, need to check with team on this")
    def test_08_verify_private_contact_overwrite_import_api(self, resource):
        """
        This test validates that address book can be created through sp360 Import format (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        sub_id = str(get_row_data['subId'])

        rec_name_before_import = ''
        sender_name_before_import = ''
        pvt_name_before_import = ''
        sender_name_after_import = ''
        pvt_name_after_import = ''
        rec_name_after_import = ''

        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api()
        assert_that(self.validate_response_code(search_address_resp, 200))

        # store the names and types of contacts before import
        for i in range(len(search_address_resp.json())):
            contactType = search_address_resp.json()[i]['contactType']
            type = search_address_resp.json()[i]['type']
            if type == 'S' and contactType == 'SENDER':
                sender_name_before_import = search_address_resp.json()[i]['name']
            elif type == 'S' and contactType == 'RECIPIENT':
                rec_name_before_import = search_address_resp.json()[i]['name']
            else:
                pvt_name_before_import = search_address_resp.json()[i]['name']

        # Call Import address API and Overwrite Recipient Address Validate the response :
        over_write_name = "Overwrite_pvt_contact_" + str(random.randint(1, 100))
        personal_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        cont_type = 'RECIPIENT',
        type = 'U'

        resource['addressbook_api'].process_import_contacts(name=over_write_name, contact_type=cont_type,
                                                            level_type=type, personal_id=personal_id, sub_id=sub_id,
                                                            type_overridden='U')

        time.sleep(2)

        search_address_resp = resource['addressbook_api'].search_contacts_with_query_api()
        assert_that(self.validate_response_code(search_address_resp, 200))

        # store the names and types of contacts after import
        for j in range(len(search_address_resp.json())):
            contactType = search_address_resp.json()[j]['contactType']
            type = search_address_resp.json()[j]['type']
            if type == 'S' and contactType == 'SENDER':
                sender_name_after_import = search_address_resp.json()[j]['name']
            elif type == 'S' and contactType == 'RECIPIENT':
                rec_name_after_import = search_address_resp.json()[j]['name']
            else:
                pvt_name_after_import = search_address_resp.json()[j]['name']

        assert_that(sender_name_before_import, equal_to(sender_name_after_import))
        assert_that(rec_name_before_import, equal_to(rec_name_after_import))
        assert_that(pvt_name_before_import, is_not(equal_to(pvt_name_after_import)))
        assert_that(over_write_name, equal_to(pvt_name_after_import))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    def test_09_get_updated_archived_contacts_after_given_timestamp_api(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        resource['addressbook_api'].delete_all_contacts(sub_id=sub_id, cont_type='SENDER', del_type='ALL',
                                                        is_admin=True)
        resource['addressbook_api'].delete_all_contacts(sub_id=sub_id, cont_type='RECIPIENT', del_type='ALL',
                                                        is_admin=True)

        (name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery, personal_id,
         dept_name, office_location, mail_stop_id, accessibility, notification_all, primary_location,
         additional_email_ids) = resource['data_generator'].address_book_data_setter()

        add_contact_resp = (resource['addressbook_api']
                            .add_contact_api(contact_type='RECIPIENT', int_dlvry=internal_delivery, name=name,
                                             comp=company, email=email, phone=phone, addr1=addr1, city=city,
                                             country=country, postal=postal, state=state, client_token=user_token))
        assert_that(self.validate_response_code(add_contact_resp, 201))
        created_contact_id = add_contact_resp.json()

        tstmp1 = get_current_timestamp(utc=True, iso_format=True)
        time.sleep(3)

        updated_name = generate_random_string(lowercase=False, digits=False, char_count=15)
        update_contact_resp = resource['addressbook_api'] \
            .update_contact_using_client_user_api(contact_type='RECIPIENT', int_dlvry=internal_delivery,
                                                  name=updated_name, comp=company, email=email, phone=phone,
                                                  addr1=addr1, city=city, country=country, postal=postal,
                                                  state=state, contact_id=created_contact_id, client_token=user_token)
        assert_that(self.validate_response_code(update_contact_resp, 200))

        time.sleep(3)

        get_cont_resp = resource['addressbook_api'].get_contact_by_cont_id_api(contact_id=created_contact_id,
                                                                               client_token=user_token)
        assert_that(get_cont_resp.json()['name'], equal_to(updated_name))
        assert_that(get_cont_resp.json()['id'], equal_to(created_contact_id))

        get_updated_contact_resp = resource['addressbook_api'] \
            .get_updated_contacts_after_given_timestamp_api(time_stamp=tstmp1, client_token=user_token)
        assert_that(self.validate_response_code(get_updated_contact_resp, 200))
        assert_that(get_updated_contact_resp.json()['contacts'][0]['id'], equal_to(created_contact_id))
        assert_that(get_updated_contact_resp.json()['contacts'][0]['updateTimestamp'], is_not(equal_to(tstmp1)))

        tstmp2 = get_current_timestamp(utc=True, iso_format=True)
        time.sleep(3)

        del_contact_resp = (resource['addressbook_api']
                            .delete_address_by_contact_id_api(contact_id=created_contact_id, client_token=user_token))
        assert_that(self.validate_response_code(del_contact_resp, 200))

        get_archived_contact_resp = resource['addressbook_api'] \
            .get_archived_contacts_after_given_timestamp_api(time_stamp=tstmp2, client_token=user_token)
        assert_that(self.validate_response_code(get_archived_contact_resp, 200))
        assert_that(get_archived_contact_resp.json()['contacts'][0]['id'], equal_to(created_contact_id))
        assert_that(get_archived_contact_resp.json()['contacts'][0]['deletedTimestamp'], is_not(equal_to(tstmp2)))
