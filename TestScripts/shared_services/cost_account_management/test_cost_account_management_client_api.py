""" This module contains all test cases."""
import json
import random
import inspect
import allure
import pytest
import string
import logging

from hamcrest import assert_that, equal_to, greater_than
from APIObjects.shared_services.cost_account_api import CostAccountManagement
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    account_mgmt = {'app_config': app_config,
                    'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
                    'data_reader': DataReader(app_config)}
    yield account_mgmt


@pytest.mark.usefixtures('initialize')
class TestCostAccountManagementClientAPI(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, resource):

        with open(self.prop.get('COST_Account_MGMT', 'cost_acc_check_import_process_schema')) as f1:
            self.cost_acc_check_import_process_expected_res = json.load(f1)

        with open(self.prop.get('COST_Account_MGMT', 'successful_upload_status_response_schema')) as f2:
            self.successful_upload_status_expected_res = json.load(f2)

        yield

    @pytest.fixture(autouse=True)
    def class_level_setup(self, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """

        self.configparameter = "COST_ACCT_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_smoke
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_01_get_accounts_by_sub_id_client_api(self, resource):
        """
        This test fetches the details of cost accounts by subId as per the provided ID (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        subid = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        user_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        query_param = 'status=true'

        # "Fetch all the active cost accounts: "):
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='N',
                                                                                               user_id=user_id,
                                                                                               query=query_param)
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True
        # "Validate total count and accounts returned in response is > 0 "):
        total_count = len(get_cost_accts_resp.json()['accounts'])
        if total_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            tota_cost_acc = len(get_cost_accts_resp.json()['accounts'])
            for i in range(tota_cost_acc):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)
                is_active = get_cost_accts_resp.json()['accounts'][i]['status']
                self.validate_expected_and_actual_values_code(is_active, True)
                # Validate that fetched cost accounts belong to same subscription
                received_sub_id = str(get_cost_accts_resp.json()['accounts'][i]['subID'])
                self.validate_expected_and_actual_values_code(received_sub_id, subid)

        # "Fetch all the in-active cost accounts: "):
        query_param = 'status=false'
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='N',
                                                                                               user_id=user_id,
                                                                                               query=query_param)

        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True
        # "Validate total count and accounts returned in response is > 0 "):
        total_inactive_count = len(get_cost_accts_resp.json()['accounts'])
        if total_inactive_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            for i in range(total_inactive_count):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)
                is_active = get_cost_accts_resp.json()['accounts'][i]['status']
                self.validate_expected_and_actual_values_code(is_active, False)
                # Validate that fetched cost accounts belong to same subscription
                received_sub_id = str(get_cost_accts_resp.json()['accounts'][i]['subID'])
                self.validate_expected_and_actual_values_code(received_sub_id, subid)

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_cost_accounts_api(self, resource):
        """
        This test fetches the details of cost accounts (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Get Account Management and validate the status code":
        parent = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        skip = '0'
        limit = '10'

        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_search_api(parent, skip, limit, is_admin='n')

        # Validate that status code of get cost Account Management API is correct":
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True
        total_count = get_cost_accts_resp.json()['pageInfo']['totalCount']

        if total_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            tota_cost_acc = len(get_cost_accts_resp.json()['accounts'])
            for i in range(tota_cost_acc):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)
                is_active = get_cost_accts_resp.json()['accounts'][i]['status']
                self.validate_expected_and_actual_values_code(is_active, True)

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_enterprise_cost_account_client_api(self, resource):
        """
        This test validates cost accounts can be created successfully or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "Aut_ent_acc_cln" + str(random.randint(1, 5000))
            code = "Ca_code_" + str(random.randint(1, 5000))
            name = "cost_name_" + str(random.randint(1, 5000))
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'E'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=False)

            with allure.step("Validate that status code of create cost Account API is 201: "):
                assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

            created_acc_id = add_cost_acct_resp.json()['accountID']

            with allure.step(
                    "Validate that created account can be fetched successfully and verify the received account Id"):
                get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                with allure.step("Validate that status code of get cost Account by Id API is 200: "):
                    assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

                    received_acc_id = get_cost_acct_resp.json()['accountID']

                    with allure.step("Validate that fetched and created Id are same: "):
                        assert self.validate_expected_and_actual_values_code(created_acc_id, received_acc_id) is True

            with allure.step(
                    "Validate that created account can be archived/deleted successfully and verify the status code"):
                archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id)

                with allure.step("Validate that status code of delete cost Account API is 200: "):
                    assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

            with allure.step(
                    "Validate that error is obtained when archived cost account is fetched"):
                get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                with allure.step("There is a failure in fetching archived cost Account Response: Expected: 404"):
                    assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_smoke
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_update_cost_account_client_api(self, resource):
        """
        This test validates that cost Account can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "AUT_ACC_Client_" + str(random.randint(1, 3500))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'E'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=False)

        with allure.step("Validate that status code of create cost Account API is 201: "):
            assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']
        with allure.step(
                "Validate that created account can be fetched successfully and verify the received account Id"):
            get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

            with allure.step("Validate that status code of get cost Account by account id API is correct"):
                if get_cost_acct_resp.status_code != 200:
                    self.Failures.append(
                        "There is a failure in get account by account id response : Expected: 200 , Received : " + str(
                            get_cost_acct_resp.status_code))

                else:

                    desc = "Auto_Name_Update"

                    with allure.step("Validate that cost account can be updated again"):
                        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name,
                                                                                                 desc=desc, SubID=sub_id,
                                                                                                 is_admin='n')

                    with allure.step("Validate that status code of update cost Account API is correct"):
                        if update_cost_acct_resp.status_code != 200:
                            err_desc = update_cost_acct_resp.json()['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in update cost account api response : Expected: 200 , Received : " + str(
                                    update_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

                    with allure.step(
                            "Validate the description of updated account"):
                        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                        if get_cost_acct_resp.status_code != 200:
                            self.Failures.append(
                                "There is a failure in get cost account api response : Expected: 200 , Received : " + str(
                                    get_cost_acct_resp.status_code))

                        else:
                            description = get_cost_acct_resp.json()['description']
                            if str(description) != desc:
                                self.Failures.append(
                                    "Fetched updated description doesn't match with the provided one. Expected: " + str(
                                        desc) + " , Received: " + str(description))

                    with allure.step(
                            "Validate that created account can be archived/deleted successfully and verify the status code"):
                        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id)
                        if archive_cost_acct_resp.status_code != 200:
                            self.Failures.append(
                                "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                    archive_cost_acct_resp.status_code))

                        else:
                            with allure.step(
                                    "Validate the description of updated account"):
                                get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                                if get_cost_acct_resp.status_code != 404:
                                    self.Failures.append(
                                        "Deleted cost account should not be fetched")

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_division_cost_account_client_api(self, resource):
        """
        This test validates cost accounts can be created successfully at division level or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "Aut_div_acc_cln_" + str(random.randint(1, 3500))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'D'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=False)

        with allure.step("Validate that status code of create cost Account is correct"):
            if add_cost_acct_resp.status_code != 201:
                self.Failures.append(
                    "There is a failure in create cost account api response : Expected: 201 , Received : " + str(
                        add_cost_acct_resp.status_code))

            else:
                created_acc_id = add_cost_acct_resp.json()['accountID']

                with allure.step(
                        "Validate that created account can be fetched successfully and verify the received account Id"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                    with allure.step("Validate that status code of get cost Account by acount id API is correct"):
                        if get_cost_acct_resp.status_code != 200:
                            self.Failures.append(
                                "There is a failure in get account by account id response : Expected: 200 , Received : " + str(
                                    get_cost_acct_resp.status_code))
                        else:
                            received_acc_id = get_cost_acct_resp.json()['accountID']

                            with allure.step("Validate that received account ID is correct: "):
                                if str(received_acc_id) != str(created_acc_id):
                                    self.Failures.append(
                                        "Expected subID is different from the received one. Expected : " + str(
                                            created_acc_id) + ", Received:  " + str(
                                            received_acc_id))

                with allure.step(
                        "Validate that created account can be archived/deleted successfully and verify the status code"):
                    archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id)
                    if archive_cost_acct_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                archive_cost_acct_resp.status_code))

                with allure.step(
                        "Validate that error is obtained when archived cost account is fetched"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)
                    if get_cost_acct_resp.status_code != 404:
                        self.Failures.append(
                            "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                                get_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_location_cost_account_client_api(self, resource):
        """
        This test validates cost accounts can be created successfully at location level or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "Aut_acc_loc_cln_" + str(random.randint(1, 4000))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'L'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=False)

        with allure.step("Validate that status code of create cost Account is correct"):
            if add_cost_acct_resp.status_code != 201:
                err_desc = add_cost_acct_resp.json()['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in create cost account api response : Expected: 201 , Received : " + str(
                        add_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                created_acc_id = add_cost_acct_resp.json()['accountID']

                with allure.step(
                        "Validate that created account can be fetched successfully and verify the received account Id"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                    with allure.step("Validate that status code of get cost Account by acount id API is correct"):
                        if get_cost_acct_resp.status_code != 200:
                            err_desc = get_cost_acct_resp.json()['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in get account by account id response : Expected: 200 , Received : " + str(
                                    get_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))
                        else:
                            received_acc_id = get_cost_acct_resp.json()['accountID']

                            with allure.step("Validate that received account ID is correct: "):
                                if str(received_acc_id) != str(created_acc_id):
                                    self.Failures.append(
                                        "Expected subID is different from the received one. Expected : " + str(
                                            created_acc_id) + ", Received:  " + str(
                                            received_acc_id))

                with allure.step(
                        "Validate that created account can be archived/deleted successfully and verify the status code"):
                    archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id)
                    if archive_cost_acct_resp.status_code != 200:
                        err_desc = archive_cost_acct_resp.json()['errors'][0]['errorDescription']
                        self.Failures.append(
                            "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                archive_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

                with allure.step(
                        "Validate that error is obtained when archived cost account is fetched"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)
                    if get_cost_acct_resp.status_code != 404:
                        self.Failures.append(
                            "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                                get_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_sub_cost_account_client_api(self, resource):
        """
        This test validates sub cost accounts can be created successfully or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "AUT_ACC_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'E'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=False)

        with allure.step("Validate that status code of create cost Account is correct"):
            if add_cost_acct_resp.status_code != 201:
                err_desc = add_cost_acct_resp.json()['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in create cost account api response : Expected: 201 , Received : " + str(
                        add_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                created_acc_id = add_cost_acct_resp.json()['accountID']

                with allure.step(
                        "Validate that created account can be fetched successfully and verify the received account Id"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)

                    with allure.step("Validate that status code of get cost Account by acount id API is correct"):
                        if get_cost_acct_resp.status_code != 200:
                            err_desc = get_cost_acct_resp.json()['errors'][0]['errorDescription']
                            self.Failures.append(
                                "There is a failure in get account by account id response : Expected: 200 , Received : " + str(
                                    get_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))
                        else:
                            with allure.step("Validate that sub cost account can be created successfully"):
                                sub_cost_accID = "Sub_AUT_ACC_" + ''.join(
                                    random.choices(string.ascii_letters + string.digits, k=5))
                                code = sub_cost_accID
                                name = sub_cost_accID
                                prmsn_by_entity = 'E'
                                prmsn_by_value = str(
                                    resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
                                parent_id = created_acc_id

                                add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(
                                    sub_cost_accID, code,
                                    name,
                                    prmsn_by_entity=prmsn_by_entity,
                                    prmsn_by_value=prmsn_by_value,
                                    parent=parent_id,
                                    sub_id=sub_id, is_admin=False)

                            with allure.step("Validate that status code of created sub cost Account is correct"):
                                if add_cost_acct_resp.status_code != 201:
                                    err_desc = add_cost_acct_resp.json()['errors'][0]['errorDescription']
                                    self.Failures.append(
                                        "There is a failure in create sub cost account api response : Expected: 201 , Received : " + str(
                                            add_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

                                else:
                                    with allure.step(
                                            "Validate that created account can be fetched successfully and verify the received account Id"):
                                        get_cost_acct_resp = resource[
                                            'account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_cost_accID)
                                        with allure.step(
                                                "Validate that status code of get cost Account by acount id API is correct"):
                                            if get_cost_acct_resp.status_code != 200:
                                                err_desc = get_cost_acct_resp.json()['errors'][0]['errorDescription']
                                                self.Failures.append(
                                                    "There is a failure in get account by account id response : Expected: 200 , Received : " + str(
                                                        get_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

                                            else:
                                                parent_id = str(get_cost_acct_resp.json()['parent'])
                                                sub_acc_id = str(get_cost_acct_resp.json()['accountID'])

                                                with allure.step(
                                                        "Validate that parent Id of sub cost account is correct: "):
                                                    if accountID != parent_id:
                                                        self.Failures.append(
                                                            "Parent Id should match with the child parent Id. Expected Id : " + str(
                                                                accountID) + " , Obtained Id : " + str(
                                                                parent_id))

                                                with allure.step(
                                                        "Validate that created sub account can be archived/deleted successfully and verify the status code"):
                                                    archive_cost_acct_resp = resource[
                                                        'account_mgmt'].archive_cost_account_api(acct_id=sub_acc_id, sub_id=sub_id)
                                                    if archive_cost_acct_resp.status_code != 200:
                                                        self.Failures.append(
                                                            "There is a failure in archive sub cost Account response : Expected: 200 , Received : " + str(
                                                                archive_cost_acct_resp.status_code))

                                                with allure.step(
                                                        "Validate that error is obtained when archived sub cost account is fetched"):
                                                    get_cost_acct_resp = resource[
                                                        'account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_acc_id)
                                                    if get_cost_acct_resp.status_code != 404:
                                                        self.Failures.append(
                                                            "There is a failure in fetching archived sub cost Account Response: Expected: 404 , Received : " + str(
                                                                get_cost_acct_resp.status_code))

                with allure.step(
                        "Validate that created account can be archived/deleted successfully and verify the status code"):
                    archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                               sub_id=sub_id)
                    if archive_cost_acct_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                archive_cost_acct_resp.status_code))

                with allure.step(
                        "Validate that error is obtained when archived cost account is fetched"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id)
                    if get_cost_acct_resp.status_code != 404:
                        self.Failures.append(
                            "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                                get_cost_acct_resp.status_code))

    @pytest.mark.skip(reason="Not implemented yet")
    @pytest.mark.regression
    def test_get_accounts_pagination_client_api(self, resource):
        """
        This test validates if pagination is working correctly or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        user_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        # "Call Get Account Management and validate the status code for active cost accounts: ":
        is_paginated_flag = resource['account_mgmt'].cost_accounts_pagination_api(sub_id, is_admin='n',
                                                                                  user_id=user_id, status='true')
        assert self.validate_expected_and_actual_values_code(is_paginated_flag, True) is True

        # if is_paginated_flag == False:
        #        self.Failures.append(
        #            "Pagination is not successfully applied for cost accounts service ")

        # "Call Get Account Management and validate the status code for inactive cost Accounts:":
        is_paginated_flag = resource['account_mgmt'].cost_accounts_pagination_api(sub_id, is_admin='n',
                                                                                  user_id=user_id,
                                                                                  status='false')
        assert self.validate_expected_and_actual_values_code(is_paginated_flag, True) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_search_by_string_client_api(self, resource):
        """
        This test fetches the details of cost accounts by subId as per the provided search string (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        subid = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        user_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        # Search by name
        query_param = 'query=CA'

        # "Fetch all the active cost accounts: "
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='N',
                                                                                               user_id=user_id,
                                                                                               query=query_param)
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True

        total_count = get_cost_accts_resp.json()['pageInfo']['totalCount']

        if total_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            total_cost_acc = len(get_cost_accts_resp.json()['accounts'])
            for i in range(total_cost_acc):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)

        # Search by code
        query_param = 'query=Dw_01'

        # "Fetch all the active cost accounts: "
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='N',
                                                                                               user_id=user_id,
                                                                                               query=query_param)
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True

        total_count = get_cost_accts_resp.json()['pageInfo']['totalCount']

        if total_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            total_cost_acc = len(get_cost_accts_resp.json()['accounts'])
            for i in range(total_cost_acc):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)

        # search by cost account description
        query_param = 'query=paper company'

        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='N',
                                                                                               user_id=user_id,
                                                                                               query=query_param)
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True

        total_count = get_cost_accts_resp.json()['pageInfo']['totalCount']

        if total_count == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        else:
            # Verify that fetched records are active and not in archived state
            total_cost_acc = len(get_cost_accts_resp.json()['accounts'])
            for i in range(total_cost_acc):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_assigned_cost_account_inactive_or_delete(self, resource):
        """
        This test validates that an assigned cost Account can not be made inactive or can not be deleted (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # fetch the details of cost account to be updated
        accountID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=accountID)
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        code = get_cost_acct_resp.json()['code']
        name = get_cost_acct_resp.json()['name']
        status = False
        parent = get_cost_acct_resp.json()['parent']

        # Call update cost account API
        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name, status=status,
                                                                                 parent=parent,
                                                                                 is_admin='n')
        assert self.validate_expected_and_actual_response_code(400, update_cost_acct_resp.status_code) is True
        obtained_err_msg = str(update_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-UP-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

        # Validate that assigned account can not be archived/deleted :
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=accountID)

        assert self.validate_expected_and_actual_response_code(400, archive_cost_acct_resp.status_code) is True
        obtained_err_msg = str(archive_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-AR-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_assigned_sub_cost_account_inactive_or_delete_admin(self, resource):
        """
        This test validates that an assigned cost Account can not be made inactive or can not be deleted (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # fetch the details of cost account to be updated
        accountID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        subId = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=accountID, sub_id=subId)
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        code = get_cost_acct_resp.json()['code']
        name = get_cost_acct_resp.json()['name']
        status = False
        parent = get_cost_acct_resp.json()['parent']

        # Call update cost account API
        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name, status=status,
                                                                                 SubID=subId, parent=parent,
                                                                                 is_admin='n')
        assert self.validate_expected_and_actual_response_code(400, update_cost_acct_resp.status_code) is True
        obtained_err_msg = str(update_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-UP-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

        # Validate that assigned account can not be archived/deleted :
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=accountID, sub_id=subId)

        assert self.validate_expected_and_actual_response_code(400, archive_cost_acct_resp.status_code) is True
        obtained_err_msg = str(archive_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-AR-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

    # Two step import
    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_import_client_api(self, resource):
        """
        This test validates that cost account can be created through 2 step Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response :
        name = "Auto_Cost_Acc_Import_" + str(random.randint(1, 50000))
        acc_id = name
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE'

        upload_cost_acct_file_resp = resource['account_mgmt'].upload_cost_acc_file_api(acc_id=acc_id, sub_id=sub_id,
                                                                                       name=name,
                                                                                       is_admin='N', status=status)

        # Validate the response of upload cost account file API:
        assert_that(upload_cost_acct_file_resp.status_code, equal_to(200))

        # Fetch the created job Id from the response :
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # Verify the process status of uploaded file :
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='N')
        assert_that(job_process_resp.status_code, equal_to(200))

        # Verify the schema of import process response :

        # "Validate that imported records are uploaded successfully: ":

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id, job_id=job_id, is_admin='N')

        assert_that(job_status_resp.status_code, equal_to(200))

        status = str(job_status_resp.json()['status'])

        assert_that(status, equal_to('Processed'))

        # "Validate that created account can be fetched successfully and verify the received account Id":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        # "Validate that status code of get cost Account by acount id API is correct"):
        assert_that(get_cost_acct_resp.status_code, equal_to(200))
        received_acc_id = get_cost_acct_resp.json()['accountID']

        # "Validate that received account ID is correct: ":
        assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_error_response_import_client_api(self, resource):
        """
        This test validates that error is obtained when import file is imported with error data (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Import cost account API and Validate the response. ":
        name = " "
        acc_id = " "
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE1'

        upload_cost_acct_file_resp = resource['account_mgmt'].upload_cost_acc_file_api(acc_id=acc_id, sub_id=sub_id,
                                                                                       name=name,
                                                                                       is_admin='n', status=status)

        # "Validate the response of upload cost account file API: ":
        assert_that(upload_cost_acct_file_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: "):
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # "Verify the process status of uploaded file: ":
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='n')

        assert_that(job_process_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: "):

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='n')

        assert_that(job_status_resp.status_code, equal_to(200))

        file_status = str(job_status_resp.json()['status'])
        assert_that(file_status, equal_to('ProcessingError'))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_export_client_api(self, resource):
        """
        This test validates that cost account can be exported successfully (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call export cost account API and Validate the response. ":
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        export_cost_acct_resp = resource['account_mgmt'].export_cost_acct_by_sub_id_api(sub_id=sub_id,
                                                                                        is_admin='N')

        # "Validate the response of export cost account API: ":
        assert_that(export_cost_acct_resp.status_code, equal_to(201))

        # "Fetch the created job Id from the response: "):
        job_id = str(export_cost_acct_resp.json()['jobId'])

        # Verify the status of exported file:
        export_job_status_resp = resource['account_mgmt'].export_job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                                 job_id=job_id,
                                                                                                 is_admin='N')
        assert_that(export_job_status_resp.status_code, equal_to(200))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    @pytest.mark.skip(reason="need to fix this test")
    def test_cost_account_hierarchy_import_client_api(self, resource):
        """
        This test validates that cost account hierarchy can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response.
        # name = "Auto_Cost_Acc_Import_" + str(random.randint(1, 50000))
        acc_id = 'Auto_SP_XZ_001'
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prnt = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        loc = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Location'))
        div = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Division'))

        upload_cost_acct_hierarchy_resp = resource['account_mgmt'].upload_cost_acct_hierarchy_file_api(sub_id=sub_id,
                                                                                                       prmsn_by_val_parent=prnt,
                                                                                                       prmsn_by_val_loc=loc,
                                                                                                       prmsn_by_val_div=div,
                                                                                                       is_admin='n')

        # "Validate the response of upload hierarchy cost account file API: ":
        assert_that(upload_cost_acct_hierarchy_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: ":
        job_id = str(upload_cost_acct_hierarchy_resp.json()['jobId'])

        # "Verify the process status of uploaded file: ":
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='n')

        assert_that(job_process_resp.status_code, equal_to(200))

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id, job_id=job_id, is_admin='n')

        assert_that(job_status_resp.status_code, equal_to(200))

        status_res = str(job_status_resp.json()['status'])

        assert_that(status_res, equal_to('Processed'))

        # "Validate that created hierarchy can be fetched successfully: ":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        # "Validate that status code of get cost Account by acount id API is correct":
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        received_acc_id = str(get_cost_acct_resp.json()['accountID'])
        child_cost_acc = str(get_cost_acct_resp.json()['children'])
        child_cost_acc_id = str(get_cost_acct_resp.json()['children'][0]['accountID'])
        parent_level_one = str(get_cost_acct_resp.json()['children'][0]['parent'])
        sub_child_cost_acc_id = get_cost_acct_resp.json()['children'][0]['children'][0]['accountID']
        sub_child_parent_id = get_cost_acct_resp.json()['children'][0]['children'][0]['parent']

        assert_that(len(child_cost_acc), greater_than(0))

        # "Validate that created child account can be fetched successfully: "):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        # Validate that sub child account can be fetched successfully:
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        # "Validate that sub child account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=sub_child_cost_acc_id)

        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

        # "Validate that sub child account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource[
            'account_mgmt'].archive_cost_account_api(acct_id=child_cost_acc_id)

        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

        # "Validate that created account can be archived/deleted successfully and verify the status code"):
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_hierarchy_single_step_import_client_api(self, resource):
        """
        This test validates that cost account hierarchy can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Import cost account API and Validate the response. ":
        # name = "Auto_Cost_Acc_Import_" + str(random.randint(1, 50000))
        acc_id = 'Single_Import_01'
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE'

        import_cost_acct_hierarchy_resp = resource['account_mgmt'].import_cost_account_single_hierarchy_api(sub_id=sub_id,
                                                                                                            status=status,
                                                                                                            is_admin='n')

        # "Validate the response of single step Import cost account API is 200 : ":
        assert self.validate_expected_and_actual_response_code(201, import_cost_acct_hierarchy_resp.status_code) is True

        # "Validate that created hierarchy can be fetched successfully: "):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        # "Validate that status code of get cost Account by Id API is 200:"
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        # received_acc_id = str(res['accountID'])
        child_cost_acc = str(get_cost_acct_resp.json()['children'])
        child_cost_acc_id = str(get_cost_acct_resp.json()['children'][0]['accountID'])
        # parent_level_one = str(res['children'][0]['parent'])
        # sub_child_parent_id = res['children'][0]['children'][0]['parent']
        assert_that(len(child_cost_acc), greater_than(0))

        # "Validate that created child account can be fetched successfully: ":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        # "Validate that sub child account can be archived/deleted successfully and verify the status code"):
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=child_cost_acc_id,
                                                                                   sub_id=sub_id)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id, sub_id=sub_id)

        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_make_assigned_cost_accounts_inactive_by_import_client_api(self, resource):
        """
        This test validates that assigned cost accounts can not be made inactive through Import (Positive scenario)
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_val = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        acc_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'account_id'))

        assigned_cost_acct_import_file_resp = resource['account_mgmt'].assigned_cost_acct_import_file_api(
            permission_val=prmsn_by_val, sub_id=sub_id, is_admin='n')

        assert self.validate_expected_and_actual_response_code(200, assigned_cost_acct_import_file_resp.status_code) is True

        # Fetch the created job Id from the response:
        job_id = str(assigned_cost_acct_import_file_resp.json()['jobId'])

        # Verify the process status of uploaded file:
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id, job_id=job_id,
                                                                                     is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, job_process_resp.status_code) is True

        # Validate that error is obtained :

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, job_status_resp.status_code) is True

        file_status = str(job_status_resp.json()['status'])
        assert self.validate_values_comparison_code(file_status, "ProcessingError") is True

        # Verify that status is not updated for assigned cost accounts through import
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id, sub_id=sub_id)
        acc_status = str(get_cost_acct_resp.json()['status'])
        assert self.validate_values_comparison_code(acc_status, "True") is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_unassigned_sub_cost_account_inactive_or_archive_user_api(self, resource):
        """
        This test validates that if a sub cost accounts is not attached with any entity then it can be deleted(positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Validate that cost account can be created successfully:
        accountID = "Sub_aut_acc_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        code = accountID
        name = accountID
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_entity = 'E'
        prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        parent = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'account_id'))

        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           parent=parent,
                                                                           sub_id=sub_id, is_admin=False)

        # Validate that status code of create cost Account is correct:
        assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']

        # Validate that created account can be fetched successfully and verify the received account Id:
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=sub_id)
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        fetched_parent = get_cost_acct_resp.json()['parent']

        assert self.validate_values_comparison_code(parent, fetched_parent) is True

        # Validate that created sub account can be archived/deleted successfully and verify the status code
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id, sub_id=sub_id)

        assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

        # Validate that error is obtained when archived cost account is fetched
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id, sub_id=sub_id)
        assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_import_inactive_cost_acc_client_api(self, resource):
        """
        This test validates that error is obtained when import file is imported with inactive cost accounts data (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response

        name = "TN account"
        acc_id = "TN_01"
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = "False"

        upload_cost_acct_file_resp = resource['account_mgmt'].upload_cost_acc_file_api(acc_id=acc_id, sub_id=sub_id,
                                                                                       name=name,
                                                                                       is_admin='n', status=status)

        assert self.validate_expected_and_actual_response_code(200, upload_cost_acct_file_resp.status_code) is True

        # Fetch the created job Id from the response:
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # Verify the process status of uploaded file:
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='n')
        assert self.validate_expected_and_actual_response_code(200, job_process_resp.status_code) is True

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='n')

        assert self.validate_expected_and_actual_response_code(200, job_status_resp.status_code) is True

        # Verify the schema of import status response:
        status = str(job_status_resp.json()['status'])
        assert self.validate_values_comparison_code(status, 'ProcessingError') is True

        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id, sub_id=sub_id)
        assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_v1_import_client_api(self, resource):
        """
        This test validates that cost account can be created through 2 step Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response :
        name = "Auto_Cost_Acc_Import_" + str(random.randint(1, 50000))
        acc_id = name
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE'

        upload_cost_acct_file_v1_resp = resource['account_mgmt'].upload_cost_acc_file_v1_api(acc_id=acc_id, sub_id=sub_id,
                                                                                             name=name,
                                                                                             is_admin='N', status=status)

        # Validate the response of upload cost account file API:
        assert_that(upload_cost_acct_file_v1_resp.status_code, equal_to(200))

        # Fetch the created job Id from the response :
        job_id = str(upload_cost_acct_file_v1_resp.json()['jobId'])

        # Verify the process status of uploaded file :
        process_file_v1_resp = resource['account_mgmt'].process_file_response_v1_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='N')
        assert_that(process_file_v1_resp.status_code, equal_to(200))

        # Verify the schema of import process response :

        # "Validate that imported records are uploaded successfully: ":

        job_status_v1_resp = resource['account_mgmt'].job_status_v1_by_job_id_api(sub_id=sub_id,
                                                                                  job_id=job_id,
                                                                                  is_admin='N')

        assert_that(job_status_v1_resp.status_code, equal_to(200))

        status = str(job_status_v1_resp.json()['status'])

        assert_that(status, equal_to('Processed'))

        # "Validate that created account can be fetched successfully and verify the received account Id":
        get_cost_acct_v1_resp = resource['account_mgmt'].get_cost_account_by_account_id_v1_api(acc_id, is_admin='n')

        # "Validate that status code of get cost Account by acount id API is correct"):

        assert_that(get_cost_acct_v1_resp.status_code, equal_to(200))

        received_acc_id = get_cost_acct_v1_resp.json()['accountID']

        # "Validate that received account ID is correct: ":
        assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_v1_resp = resource['account_mgmt'].archive_cost_account_v1_api(
            account_id=acc_id, is_admin='n')
        assert_that(archive_cost_acct_v1_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_cost_acct_v1_resp = resource['account_mgmt'].get_cost_account_by_account_id_v1_api(acc_id, is_admin='n')
        assert_that(get_cost_acct_v1_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_error_response_v1_import_client_api(self, resource):
        """
        This test validates that error is obtained when import file is imported with error data (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Import cost account API and Validate the response. ":
        name = " "
        acc_id = " "
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE1'

        upload_cost_acct_file_v1_resp = resource['account_mgmt'].upload_cost_acc_file_v1_api(acc_id=acc_id, sub_id=sub_id,
                                                                                             name=name,
                                                                                             is_admin='n', status=status)
        # "Validate the response of upload cost account file API: ":
        assert_that(upload_cost_acct_file_v1_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: "):
        job_id = str(upload_cost_acct_file_v1_resp.json()['jobId'])

        # "Verify the process status of uploaded file: ":
        process_file_v1_resp = resource['account_mgmt'].process_file_response_v1_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='n')

        assert_that(process_file_v1_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: "):

        job_status_v1_resp = resource['account_mgmt'].job_status_v1_by_job_id_api(sub_id=sub_id,
                                                                                  job_id=job_id,
                                                                                  is_admin='n')

        assert_that(job_status_v1_resp.status_code, equal_to(200))

        file_status = str(job_status_v1_resp.json()['status'])
        assert_that(file_status, equal_to('ProcessingError'))
