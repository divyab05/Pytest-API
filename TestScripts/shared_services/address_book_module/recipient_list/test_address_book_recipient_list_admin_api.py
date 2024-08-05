""" This module contains all test cases."""

import inspect
import json
import random
import logging
import allure
import pytest
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
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
class TestAddrbookRecipient_list_Admin_API:
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
    @pytest.mark.address_book_sp360commercial_reg
    def test_01_verify_add_recipient_list_admin_api(self, resource):
        """
        This test validates that new recipient list can be created successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = "AUTO_Test_rec_list_" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code

        with allure.step("Validate that recipient is created successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new recipient list : Expected:201 , Received : " + str(status_code) +" , Obtained error message is: "+str(err_desc))

            else:
                with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_schema')) as schema:
                    expected_schema = json.load(schema)

                isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                if len(isValid) > 0:
                    self.Failures.append(
                        "Create recipient response schema doesn't match with expected schema" + str(isValid))

                else:
                    created_rec_id = str(res['recipientlistID'])

                    with allure.step("Fetch the created recipient list: "):
                        get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id, rect_id=created_rec_id, is_admin=True)
                        res = get_recipient_resp.json()
                        status_code = get_recipient_resp.status_code
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            with open(self.prop.get('ADDRESSBOOK_MGMT', 'get_recipient_schema')) as schema:
                                expected_schema = json.load(schema)

                            isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                            if len(isValid) > 0:
                                self.Failures.append(
                                    "Get recipient response schema doesn't match with expected schema" + str(isValid))

                    with allure.step("Delete the created recipient list: "):
                        status_code =resource['addressbook_api'].verify_delete_recipient_api(sub_id=sub_id, is_admin='y',
                                                                                    rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                    with allure.step("Fetch the deleted department: "):
                        get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id,
                                                                                                      rect_id=created_rec_id,
                                                                                                      is_admin=True)
                        res = get_recipient_resp.json()
                        status_code = get_recipient_resp.status_code
                        if status_code != 404:
                            self.Failures.append(
                                "Deleted recipient list shouldn't be fetched.")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_02_verify_add_contacts_to_recipient_list_admin_api(self, resource):
        """
        This test validates that contacts can be added to newly created recipient list (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = "AUTO_Test_rec_list_" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            cont1 = str(get_row_data['contact1'])
            cont2 = str(get_row_data['contact2'])

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code

        with allure.step("Validate that recipient is created successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new recipient list : Expected:201 , Received : " + str(
                        status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_schema')) as schema:
                    expected_schema = json.load(schema)

                isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                if len(isValid) > 0:
                    self.Failures.append(
                        "Create recipient response schema doesn't match with expected schema" + str(isValid))

                else:
                    created_rec_id = str(res['recipientlistID'])

                    with allure.step("Fetch the created recipient list: "):
                        res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(sub_id=sub_id,
                                                                                               is_admin='y',
                                                                                               rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            total_count = res['pageInfo']['totalCount']

                    with allure.step("Add contacts to the create list: "):
                        patch_rect_resp = resource['addressbook_api'].patch_contacts_in_recipient_list_api(operation_type='add', cont1=cont1, cont2=cont2, sub_id=sub_id, rect_id=created_rec_id, is_admin=True)
                        res = patch_rect_resp.json()
                        status_code = patch_rect_resp.status_code
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            with allure.step("Fetch the updated department and verify that contacts are added to it: "):

                                res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(
                                    sub_id=sub_id,
                                    is_admin='y',
                                    rec_id=created_rec_id)
                                if status_code != 200:
                                    err_desc = res['errors'][0]['errorDescription']
                                    self.Failures.append(
                                        "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                            status_code) + " , Obtained error message is: " + str(err_desc))

                                else:
                                    updt_count = res['pageInfo']['totalCount']

                                    if updt_count < total_count:
                                        self.Failures.append(
                                            "Contacts are not added to the recipient list.")

                    with allure.step("Delete the created recipient list: "):
                        status_code =resource['addressbook_api'].verify_delete_recipient_api(sub_id=sub_id, is_admin='y',
                                                                                  rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_03_verify_delete_contacts_from_recipient_list_admin_api(self, resource):
        """
        This test validates that contacts can be deleted from the created recipient list (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = "AUTO_Test_rec_list_" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            cont1 = str(get_row_data['contact1'])
            cont2 = str(get_row_data['contact2'])

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code

        with allure.step("Validate that recipient is created successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new recipient list : Expected:201 , Received : " + str(
                        status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_schema')) as schema:
                    expected_schema = json.load(schema)

                isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                if len(isValid) > 0:
                    self.Failures.append(
                        "Create recipient response schema doesn't match with expected schema" + str(isValid))

                else:
                    created_rec_id = str(res['recipientlistID'])

                    with allure.step("Fetch the created recipient list: "):
                        res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(sub_id=sub_id,
                                                                                                       is_admin='y',
                                                                                                       rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in fetching the created recipient list. Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            total_count = res['pageInfo']['totalCount']

                    with allure.step("Add contacts to the created list: "):
                        patch_rect_resp = resource['addressbook_api'].patch_contacts_in_recipient_list_api(
                            operation_type='add', cont1=cont1, cont2=cont2, sub_id=sub_id, rect_id=created_rec_id,
                            is_admin=True)
                        res = patch_rect_resp.json()
                        status_code = patch_rect_resp.status_code

                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in adding contacts to recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            with allure.step("Fetch the updated department and verify that contacts are added to it: "):

                                res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(
                                    sub_id=sub_id,
                                    is_admin='y',
                                    rec_id=created_rec_id)
                                if status_code != 200:
                                    err_desc = res['errors'][0]['errorDescription']
                                    self.Failures.append(
                                        "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                            status_code) + " , Obtained error message is: " + str(err_desc))

                                else:
                                    updt_count = res['pageInfo']['totalCount']

                                    if updt_count < total_count:
                                        self.Failures.append(
                                            "Contacts are not added to the recipient list.")

                                    else:
                                        with allure.step("Remove contacts from the created list: "):
                                            patch_rect_resp = resource[
                                                'addressbook_api'].patch_contacts_in_recipient_list_api(
                                                operation_type='add', cont1=cont1, cont2=cont2, sub_id=sub_id,
                                                rect_id=created_rec_id, is_admin=True)
                                            res = patch_rect_resp.json()
                                            status_code = patch_rect_resp.status_code
                                            if status_code != 200:
                                                err_desc = res['errors'][0]['errorDescription']

                                                self.Failures.append(
                                                    "There is a failure in deleting contacts from recipient list : Expected:200 , Received : " + str(
                                                        status_code) + " , Obtained error message is: " + str(err_desc))

                                            else:
                                                with allure.step(
                                                        "Fetch the department and verify that contacts are removed from it: "):

                                                    res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(
                                                        sub_id=sub_id,
                                                        is_admin='y',
                                                        rec_id=created_rec_id)
                                                    if status_code != 200:
                                                        err_desc = res['errors'][0]['errorDescription']
                                                        self.Failures.append(
                                                            "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                                                status_code) + " , Obtained error message is: " + str(
                                                                err_desc))

                                                    else:
                                                        removed_count = res['pageInfo']['totalCount']

                                                        if removed_count > 0:
                                                            self.Failures.append(
                                                                "Contacts are not removed from the recipient list.")

                    with allure.step("Delete the created recipient list: "):
                        status_code =resource['addressbook_api'].verify_delete_recipient_api(sub_id=sub_id, is_admin='y',
                                                                                  rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_04_verify_add_duplicate_recipient_list_admin_api(self, resource):
        """
        This test validates that duplicate recipient list can not be created (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = "AUTO_Test_rec_list_" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            err_msg = str(get_row_data['ErrorMsg'])
            dup_error_msg = err_msg.replace("?", name)

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code

        with allure.step("Validate that recipient is created successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new recipient list : Expected:201 , Received : " + str(
                        status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_schema')) as schema:
                    expected_schema = json.load(schema)

                isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                if len(isValid) > 0:
                    self.Failures.append(
                        "Create recipient response schema doesn't match with expected schema" + str(isValid))

                else:
                    created_rec_id = str(res['recipientlistID'])

                    with allure.step("Fetch the created recipient list: "):
                        get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id,
                                                                                                      rect_id=created_rec_id,
                                                                                                      is_admin=True)
                        res = get_recipient_resp.json()
                        status_code = get_recipient_resp.status_code
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            with open(self.prop.get('ADDRESSBOOK_MGMT', 'get_recipient_schema')) as schema:
                                expected_schema = json.load(schema)

                            isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                            if len(isValid) > 0:
                                self.Failures.append(
                                    "Get recipient response schema doesn't match with expected schema" + str(isValid))

                    with allure.step(
                            "Add duplicate recipient name and verify that error is obtained: "):

                        create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
                        res = create_recipient_resp.json()
                        status_code = create_recipient_resp.status_code

                    with allure.step("Validate that duplicate recipient is not created: "):
                        if status_code != 400:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "Expected error message is not obtained for duplicate recipient list creation. Expected: 400 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                    with allure.step("Delete the created recipient list: "):
                        status_code =resource['addressbook_api'].verify_delete_recipient_api(sub_id=sub_id, is_admin='y',
                                                                                  rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                    with allure.step("Fetch the deleted department: "):
                        get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id,
                                                                                                      rect_id=created_rec_id,
                                                                                                      is_admin=True)
                        res = get_recipient_resp.json()
                        status_code = get_recipient_resp.status_code
                        if status_code != 404:
                            self.Failures.append(
                                "Deleted recipient list shouldn't be fetched.")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_05_verify_get_recipient_by_id_admin_api(self, resource):
        """
        This test validates that recipient can be fetched by Id successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):

            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            rec_id = str(get_row_data['contact1'])

            with allure.step("Fetch the created recipient list: "):
                get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id,
                                                                                              rect_id=rec_id,
                                                                                              is_admin=True)
                res = get_recipient_resp.json()
                status_code = get_recipient_resp.status_code
                if status_code != 200:
                    err_desc = res['errors'][0]['errorDescription']
                    self.Failures.append(
                        "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                            status_code) + " , Obtained error message is: " + str(err_desc))

                else:
                    with open(self.prop.get('ADDRESSBOOK_MGMT', 'get_recipient_schema')) as schema:
                        expected_schema = json.load(schema)

                    isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                    if len(isValid) > 0:
                        self.Failures.append(
                            "Get recipient response schema doesn't match with expected schema" + str(isValid))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_06_verify_get_recipient_by_invalid_id_admin_api(self, resource):
        """
        This test validates that recipient can't be fetched by invalid Id successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):

            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            rec_id = str(get_row_data['contact1'])

            with allure.step("Fetch the created recipient list: "):
                get_recipient_resp = resource['addressbook_api'].get_recipient_list_by_id_api(sub_id=sub_id,
                                                                                              rect_id=rec_id,
                                                                                              is_admin=True)
                res = get_recipient_resp.json()
                status_code = get_recipient_resp.status_code
                if status_code != 404:
                    err_desc = res['errors'][0]['errorDescription']
                    self.Failures.append(
                        "Error should be obtained when an invalid recipient list is fetched. Expected:404 , Received : " + str(
                            status_code) + " , Obtained error message is: " + str(err_desc))

                else:
                    with open(self.prop.get('ADDRESSBOOK_MGMT', 'err_not_found_schema')) as schema:
                        expected_schema = json.load(schema)

                    isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                    if len(isValid) > 0:
                        self.Failures.append(
                            "Error response schema doesn't match with expected error schema" + str(isValid))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_07_verify_update_recipient_list_admin_api(self, resource):
        """
        This test validates that recipient list can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = "AUTO_Test_rec_list_" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            cont1 = str(get_row_data['contact1'])
            cont2 = str(get_row_data['contact2'])

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code

        with allure.step("Validate that recipient is created successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new recipient list : Expected:201 , Received : " + str(
                        status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                with open(self.prop.get('ADDRESSBOOK_MGMT', 'create_recipient_schema')) as schema:
                    expected_schema = json.load(schema)

                isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                if len(isValid) > 0:
                    self.Failures.append(
                        "Create recipient response schema doesn't match with expected schema" + str(isValid))

                else:
                    created_rec_id = str(res['recipientlistID'])

                    with allure.step("Fetch the created recipient list: "):
                        res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(sub_id=sub_id,
                                                                                                       is_admin='y',
                                                                                                       rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            total_count = res['pageInfo']['totalCount']

                    with allure.step("Add contacts to the create list: "):
                        res, status_code =resource['addressbook_api'].verify_updt_recipient_api(name=name, cont1=cont1,
                                                                                         cont2=cont2, is_admin='y',
                                                                                         sub_id=sub_id,
                                                                                         rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in updating the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

                        else:
                            with allure.step("Fetch the updated department and verify that contacts are added to it: "):

                                res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(
                                    sub_id=sub_id,
                                    is_admin='y',
                                    rec_id=created_rec_id)
                                if status_code != 200:
                                    err_desc = res['errors'][0]['errorDescription']
                                    self.Failures.append(
                                        "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                            status_code) + " , Obtained error message is: " + str(err_desc))

                                else:
                                    updt_count = res['pageInfo']['totalCount']

                                    if updt_count < total_count:
                                        self.Failures.append(
                                            "Contacts are not added to the recipient list.")

                    with allure.step("Delete the created recipient list: "):
                        status_code =resource['addressbook_api'].verify_delete_recipient_api(sub_id=sub_id, is_admin='y',
                                                                                  rec_id=created_rec_id)
                        if status_code != 200:
                            err_desc = res['errors'][0]['errorDescription']

                            self.Failures.append(
                                "There is a failure in deleting the recipient list : Expected:200 , Received : " + str(
                                    status_code) + " , Obtained error message is: " + str(err_desc))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_08_verify_search_recipient_in_sub_id_admin_api(self, resource):
        """
        This test validates that created recipient can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step("Call search recipient in sub Id (admin) API and validate response: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])

            res, status_code, is_paginated_flag =resource['addressbook_api'].verify_get_rec_by_sub_id_api(sub_id=sub_id,
                                                                                                is_admin='y')

            if is_paginated_flag == False:
                self.Failures.append(
                    "Pagination is not correctly applied for Get recipient in sub Id API ")

            else:
                with allure.step("Validate that recipients are fetched successfully: "):
                    if status_code != 200:
                        err_desc = res['errors'][0]['errorDescription']
                        self.Failures.append(
                            "There is a failure in fetching the recipients list. Expected:200. Received : " + str(
                                status_code) + " , Obtained error message is: " + str(err_desc))

                    else:
                        with open(self.prop.get('ADDRESSBOOK_MGMT', 'get_rec_by_id_schema')) as get_dept_schema:
                            expected_schema = json.load(get_dept_schema)

                        isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                        if len(isValid) > 0:
                            self.Failures.append(
                                "Response schema of get recipient by Id doesn't match with expected schema" + str(isValid))

                        else:
                            total_depts = res['pageInfo']['totalCount']
                            if total_depts == 0:
                                self.Failures.append(
                                    "Total departments fetched should be > 0 ")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_09_verify_search_recipient_invalid_sub_id_admin_api(self, resource):
        """
        This test validates that error is obtained when invalid sub Id is provided to fetch (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step("Call search recipient in sub Id (admin) API and validate response: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            err_msg = str(get_row_data['ErrorMsg'])
            expected_err_msg = err_msg.replace("?", sub_id)

            res, status_code, is_paginated_flag =resource['addressbook_api'].verify_get_rec_by_sub_id_api(sub_id=sub_id,
                                                                                               is_admin='y')
            err_desc = res['errors'][0]['errorDescription']

            with allure.step("Validate that correct error code and message are fetched successfully: "):
                if status_code != 400 or expected_err_msg !=err_desc:
                    err_desc = res['errors'][0]['errorDescription']
                    self.Failures.append(
                        "There is a failure in fetching the recipients list. Expected:400. Received : " + str(
                            status_code) + " , Expected error message : " + expected_err_msg+" Obtained error message is: " + str(err_desc))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_10_verify_search_recipient_by_search_query_admin_api(self, resource):
        """
        This test validates that recipients can be fetched as per the provided query successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step("Call search recipient in sub Id (admin) API and validate response: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            search_query = 'Rec'

            res, status_code, is_paginated_flag =resource['addressbook_api'].verify_get_rec_by_sub_id_api(sub_id=sub_id,
                                                                                               is_admin='y', query=search_query)

            if is_paginated_flag == False:
                self.Failures.append(
                    "Pagination is not correctly applied for Get recipient in sub Id API ")

            else:
                with allure.step("Validate that recipients are fetched successfully: "):
                    if status_code != 200:
                        err_desc = res['errors'][0]['errorDescription']
                        self.Failures.append(
                            "There is a failure in fetching the recipients list. Expected:200. Received : " + str(
                                status_code) + " , Obtained error message is: " + str(err_desc))

                    else:
                        with open(self.prop.get('ADDRESSBOOK_MGMT', 'get_rec_by_id_schema')) as get_dept_schema:
                            expected_schema = json.load(get_dept_schema)

                        isValid =resource['addressbook_api'].verify_res_schema(res=res, expected_schema=expected_schema)

                        if len(isValid) > 0:
                            self.Failures.append(
                                "Response schema of get recipient by Id doesn't match with expected schema" + str(
                                    isValid))

                        else:
                            total_depts = res['pageInfo']['totalCount']
                            if total_depts == 0:
                                self.Failures.append(
                                    "Total departments fetched should be > 0 ")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_11_verify_search_recipient_by_non_existent_search_query_admin_api(self, resource):
        """
        This test validates that recipients should not be fetched for non existent search query (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step("Call search recipient in sub Id (admin) API and validate response: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            search_query = 'xyz'

            res, status_code, is_paginated_flag =resource['addressbook_api'].verify_get_rec_by_sub_id_api(sub_id=sub_id,
                                                                                               is_admin='y',
                                                                                               query=search_query)

            with allure.step("Validate that recipients are not fetched for invalid search query successfully: "):
                if status_code != 200:
                    err_desc = res['errors'][0]['errorDescription']
                    self.Failures.append(
                        "There is a failure in fetching the recipients list. Expected:200. Received : " + str(
                            status_code) + " , Obtained error message is: " + str(err_desc))

                else:
                    total_depts = res['pageInfo']['totalCount']
                    if total_depts > 0:
                        self.Failures.append(
                            "Total departments fetched should be 0 ")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_12_verify_add_recipient_list_without_name_admin_api(self, resource):
        """
        This test validates that new recipient list can not be created without name (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new recipient list API and validate that successful response is obtained: "):
            name = ''
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            expected_err_msg = str(get_row_data['ErrorMsg'])

            create_recipient_resp = resource['addressbook_api'].create_recipient_list_api(name=name, sub_id=sub_id, is_admin=True)
            res = create_recipient_resp.json()
            status_code = create_recipient_resp.status_code
            err_desc = res['errors'][0]['errorDescription']

        with allure.step("Validate that recipient is created successfully: "):

            if status_code != 400 or expected_err_msg != str(err_desc):
                self.Failures.append(
                    "Correct error should be obtained when no name is provided. Expected error message : " + expected_err_msg + " Obtained error message is: " + str(
                        err_desc))

    @pytest.mark.address_book_sp360commercial_reg
    def test_13_verify_get_contacts_from_rec_list_admin_api(self, resource):
        """
        This test validates that contacts can be fetched from recipient list successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Get contacts from recipient list API and validate that successful response is obtained: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            rec_id = str(get_row_data['contact1'])

            with allure.step("Fetch the created recipient list: "):
                res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(sub_id=sub_id,
                                                                                       is_admin='y',
                                                                                       rec_id=rec_id)
                if status_code != 200:
                    err_desc = res['errors'][0]['errorDescription']
                    self.Failures.append(
                        "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                            status_code) + " , Obtained error message is: " + str(err_desc))

                else:
                    total_contacts = len(res['contacts'])

                    if total_contacts == 0:
                        self.Failures.append(
                            "No contacts are available in the recipient list. ")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_14_verify_get_contacts_from_invalid_rec_admin_api(self, resource):
        """
        This test validates that error should be obtained when contacts are fetched from invalid recipient list (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Get contacts from recipient list API and validate that successful response is obtained: "):
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            rec_id = str(get_row_data['contact1'])

            with allure.step("Fetch the created recipient list: "):
                res, status_code =resource['addressbook_api'].verify_get_contacts_from_recipient_list_api(sub_id=sub_id,
                                                                                               is_admin='y',
                                                                                               rec_id=rec_id)

                if status_code != 400 :
                    self.Failures.append(
                        "Correct error code should be obtained when invalid recipient list Id is provided. Expected : 400. Obtained " + str(
                            status_code))
