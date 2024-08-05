""" This module contains all test cases."""
import random
import string
import inspect
import time
import logging
import allure
import pytest
from hamcrest import assert_that, equal_to, greater_than
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    account_mgmt = {'app_config': app_config,
                    'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
                    'data_reader': DataReader(app_config)}
    account_mgmt['login_api']: LoginAPI(app_config)
    yield account_mgmt


@pytest.mark.usefixtures('initialize')
class TestCostAccountManagementAdminAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):

        self.configparameter = "COST_ACCT_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_cost_accounts_api(self, resource):
        """
        This test fetches the details of cost accounts (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Get Account Management and validate the status code"
        parent = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        skip = '0'
        limit = '10'
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_search_api(parent, skip, limit, sub_id=sub_id,
                                                                                    is_admin='y')
        # "Validate that status code of get cost Account Management API is 200: "
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
    def test_get_accounts_by_sub_id_api(self, resource):
        """
        This test fetches the details of cost accounts by subId as per the provided ID (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        subid = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        query_param = 'status=true'

        # "Fetch all the active cost accounts: "
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='Y',
                                                                                               query=query_param)

        # "Validate that status code of get cost Account Management API is 200:"
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True

        # "Validate total count and accounts returned in response is > 0 "
        total_accounts = len(get_cost_accts_resp.json()['accounts'])
        if total_accounts == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        # Verify received subId and status is as per the provided parameters:
        for i in range(total_accounts):
            fetched_status = get_cost_accts_resp.json()['accounts'][i]['status']
            assert self.validate_expected_and_actual_values_code(fetched_status, True) is True
            # Verify that fetched cost accounts are not archived:
            is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
            self.validate_expected_and_actual_values_code(is_archived, False)
            received_sub_id = get_cost_accts_resp.json()['accounts'][i]['subID']
            assert self.validate_expected_and_actual_values_code(received_sub_id, subid) is True

        # "Fetch all the in-active cost accounts:"
        query_param = 'status=false'
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='Y',
                                                                                               query=query_param)

        # "Validate that status code of get cost Account Management API is 200:"
        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True

        # "Validate total count and accounts returned in response is > 0 ":
        total_inactive_accounts = len(get_cost_accts_resp.json()['accounts'])
        if total_inactive_accounts == 0:
            pytest.fail("No cost accounts is returned in response. Expected count > 0.")

        # Verify received subId and status is as per the provided parameters:
        for i in range(total_inactive_accounts):
            fetched_status = get_cost_accts_resp.json()['accounts'][i]['status']
            assert self.validate_expected_and_actual_values_code(fetched_status, False) is True
            # Verify that fetched cost accounts are not archived:
            is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
            self.validate_expected_and_actual_values_code(is_archived, False)
            received_sub_id = get_cost_accts_resp.json()['accounts'][i]['subID']
            assert self.validate_expected_and_actual_values_code(received_sub_id, subid) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_cost_account_by_account_id_api(self, resource):
        """
        This test fetches the details of cost accounts as per the provided account ID (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        acc_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'account_id'))
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        # Call Get Account Management and validate the status code"
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        # Validate that status code of get cost Account by Id API is 200:
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        # "Validate Received account ID is correct: "
        received_acc_id = str(get_cost_acct_resp.json()['accountID'])
        assert self.validate_expected_and_actual_values_code(received_acc_id, acc_id) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_enterprise_cost_account_api(self, resource):
        """
        This test validates cost accounts can be created successfully or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Validate that cost account can be created successfully":
        accountID = 'Aut_Acc_ent_adm_' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        code = accountID
        name = accountID
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_entity = 'E'
        prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=sub_id, is_admin=True)
        # "Validate that status code of create cost Account API is 201":
        assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']

        # "Validate that created account can be fetched successfully and verify the received account Id":

        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        # "Validate that status code of get cost Account by Id API is 200" :
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        received_acc_id = get_cost_acct_resp.json()['accountID']

        # "Validate that fetched and created Id are same" :
        assert self.validate_expected_and_actual_values_code(created_acc_id, received_acc_id) is True
        # "Validate that created account can be archived/deleted successfully and verify the status code"):

        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id, sub_id=sub_id,
                                                                                   is_admin=True)

        # "Validate that status code of delete cost Account API is 200":
        assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

        # "Validate that error is obtained when archived cost account is fetched" :
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        # "There is a failure in fetching archived cost Account Response: Expected: 404"):
        assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_update_cost_account_api(self, resource):
        """
        This test validates that cost Account can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Validate that cost account can be created successfully"):
        accountID = 'Aut_Acc_ent_' + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        code = accountID
        name = accountID
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_entity = 'E'
        prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=sub_id, is_admin=True)

        # "Validate that status code of create cost Account API is 201" :
        assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']
        # "Validate that created account can be fetched successfully and verify the received account Id"):
        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=created_acc_id, sub_id=sub_id, is_admin=True))
        # "Validate that status code of get cost Account by acount id API is correct":
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        desc = "Auto_Name_Update"

        # "Validate that cost account can be updated again"):
        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name,
                                                                                 desc=desc, SubID=sub_id, is_admin='y')

        # "Validate that status code of update cost Account API is correct":
        assert self.validate_expected_and_actual_response_code(200, update_cost_acct_resp.status_code) is True

        # "Validate the description of updated account" :
        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=created_acc_id, sub_id=sub_id, is_admin=True))
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        description = get_cost_acct_resp.json()['description']
        assert self.validate_expected_and_actual_values_code(str(description), desc) is True

        # "Validate that created account can be archived/deleted successfully and verify the status code"):
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                   sub_id=sub_id, is_admin=True)

        assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_valid_pass_code_api(self, resource):
        """
        This test verifies that successful response is obtained when a valid passcode is provided (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        acc_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'account_id'))
        pwd = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        with allure.step("Call Validate pass code API and verify response for correct passcode"):
            validate_passcode_resp = resource['account_mgmt'].validate_passcode_api(sub_id, acc_id, pwd)
            if validate_passcode_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in validate pass code response : Expected:200 , Received : " + str(validate_passcode_resp.status_code))

            else:
                val = str(validate_passcode_resp.json()['validate'])
                if val != 'True':
                    self.Failures.append(
                        "Response returned is not corect. Expected true, received " + str(val))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_invalid_pass_code_api(self, resource):
        """
        This test verifies that false should be obtained when an in-valid passcode is provided (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        acc_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'account_id'))
        pwd = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        with allure.step("Call Validate pass code API and verify response for in correct passcode"):
            validate_passcode_resp = resource['account_mgmt'].validate_passcode_api(sub_id, acc_id, pwd)

            if validate_passcode_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in validate pass code response : Expected:200 , Received : " + str(validate_passcode_resp.status_code))

            else:
                val = str(validate_passcode_resp.json()['validate'])
                if val != 'False':
                    self.Failures.append(
                        "Response returned is not corect. Expected False, received " + str(val))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_import_cost_account_api(self, resource):
        """
        This test validates that FedEx subcarrier can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call import cost account API and Validate":
        name = "Single_Auto_Cost_Acc_Import_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        acc_id = name
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE'

        import_cost_acct_resp = resource['account_mgmt'].import_cost_account_api(acc_id=acc_id, sub_id=sub_id,
                                                                                 name=name,
                                                                                 status=status, is_admin='y')

        # "Validate that creation is successful through import":
        assert_that(import_cost_acct_resp.status_code, equal_to(201))

        # Validate that records are created":
        assert_that(import_cost_acct_resp.json()['uploadedRecords'], greater_than(0))

        # "Validate that created account can be archived/deleted successfully and verify the status code"):
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id,
                                                                                   sub_id=sub_id,
                                                                                   is_admin=True)

        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_cost_account_by_location_and_sub_id_api(self, resource):
        """
        This test fetches the details of cost accounts as per the provided location Id and sub Id (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        loc_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'location_id'))
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        # "Call Get Account Management and validate the status code":
        get_cost_acct_by_loc_sub_id_resp = resource['account_mgmt'].get_cost_account_by_location_and_sub_id_api(loc_id,
                                                                                                                sub_id,
                                                                                                                is_admin='y')

        # "Validate that status code of get cost Account by location and subId API is correct":
        assert_that(get_cost_acct_by_loc_sub_id_resp.status_code, equal_to(200))

        assert_that(len(get_cost_acct_by_loc_sub_id_resp.json()['accounts']), greater_than(0))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_cost_account_by_user_and_sub_id_api(self, resource):
        """
        This test fetches the details of cost accounts as per the provided user Id and sub Id (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        user_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        with allure.step("Call Get Account Management and validate the status code"):
            get_cost_acct_by_user_sub_id_resp = resource['account_mgmt'].get_cost_account_by_user_and_sub_id_api(user_id, sub_id,
                                                                                                                 is_admin='y')

        with allure.step("Validate that status code of get cost Account by location and subId API is correct"):
            if get_cost_acct_by_user_sub_id_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in get cost Account by location and subId response : Expected: 200 , Received : " + str(
                        get_cost_acct_by_user_sub_id_resp.status_code))

            else:
                accounts = len(get_cost_acct_by_user_sub_id_resp.json()['accounts'])
                with allure.step("Validate that accounts are returned in response"):
                    if accounts == 0:
                        self.Failures.append(
                            "No cost Account is returned in response : Expected: >=1 , Received : " + str(accounts))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_cost_account_invalid_subId_api(self, resource):
        """
        This test validates cost accounts can not be created with invalid subId (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "AUT_ACC_" + str(random.randint(1, 3500))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'D'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=True)
        with allure.step("Validate that correct error code and error message is obtained when sub Id is invalid"):
            if add_cost_acct_resp.status_code != 400:
                self.Failures.append(
                    "There is a failure in create cost account api response : Expected: 400 , Received : " + str(
                        add_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_accounts_pagination_api(self, resource):
        """
        This test validates if pagination is working correctly or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        # "Call Get Account Management and validate the status code for active cost accounts: ":
        is_paginated_flag = resource['account_mgmt'].cost_accounts_pagination_api(sub_id, is_admin='Y',
                                                                                  status='true')
        assert self.validate_expected_and_actual_values_code(is_paginated_flag, True) is True

        # if is_paginated_flag == False:
        #        self.Failures.append(
        #            "Pagination is not successfully applied for cost accounts service ")

        # "Call Get Account Management and validate the status code for inactive cost Accounts:":
        is_paginated_flag = resource['account_mgmt'].cost_accounts_pagination_api(sub_id, is_admin='Y',
                                                                                  status='false')
        assert self.validate_expected_and_actual_values_code(is_paginated_flag, True) is True

    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_get_accounts_sorting_api(self, resource):
        """
        This test validates if sorting functionality is working correctly or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        with allure.step("Call Get Account Management and validate the sorting of results"):
            sort_col = 'name'
            is_sorted_flag = resource['account_mgmt'].cost_accounts_sorting_api(sort_col, sub_id, is_admin='Y')

            if is_sorted_flag == False:
                self.Failures.append(
                    "Sorting is not successfully applied for cost accounts service ")

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_division_cost_account_api(self, resource):
        """
        This test validates cost accounts can be created successfully at division level or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "AUT_Div_ACC_adm_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'D'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=True)

        with allure.step("Validate that status code of create cost Account is correct"):
            if add_cost_acct_resp.status_code != 201:
                self.Failures.append(
                    "There is a failure in create cost account api response : Expected: 201 , Received : " + str(
                        add_cost_acct_resp.status_code))

            else:
                created_acc_id = add_cost_acct_resp.json()['accountID']

                with allure.step(
                        "Validate that created account can be fetched successfully and verify the received account Id"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                        acct_id=created_acc_id, sub_id=sub_id, is_admin=True)

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
                    archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                               sub_id=sub_id,
                                                                                               is_admin=True)
                    if archive_cost_acct_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                archive_cost_acct_resp.status_code))

                with allure.step(
                        "Validate that error is obtained when archived cost account is fetched"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                        acct_id=created_acc_id, sub_id=sub_id, is_admin=True)
                    if get_cost_acct_resp.status_code != 404:
                        self.Failures.append(
                            "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                                get_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_location_cost_account_api(self, resource):
        """
        This test validates cost accounts can be created successfully at location level or not (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with allure.step("Validate that cost account can be created successfully"):
            accountID = "AUT_ACC_loc_adm_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            code = accountID
            name = accountID
            sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
            prmsn_by_entity = 'L'
            prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
            add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                               prmsn_by_entity=prmsn_by_entity,
                                                                               prmsn_by_value=prmsn_by_value,
                                                                               sub_id=sub_id, is_admin=True)

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
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                        acct_id=created_acc_id, sub_id=sub_id, is_admin=True)

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
                    archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                               sub_id=sub_id,
                                                                                               is_admin=True)
                    if archive_cost_acct_resp.status_code != 200:
                        err_desc = archive_cost_acct_resp.json()['errors'][0]['errorDescription']
                        self.Failures.append(
                            "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                                archive_cost_acct_resp.status_code) + " , Obtained error message is: " + str(err_desc))

                with allure.step(
                        "Validate that error is obtained when archived cost account is fetched"):
                    get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                        acct_id=created_acc_id, sub_id=sub_id, is_admin=True)
                    if get_cost_acct_resp.status_code != 404:
                        self.Failures.append(
                            "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                                get_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_search_by_string_api(self, resource):
        """
        This test fetches the details of cost accounts as per the provided search string (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        subid = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        query_param = 'query=CA'

        # "Fetch all the active cost accounts as per the provided string:
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='Y',
                                                                                               query=query_param)

        assert self.validate_expected_and_actual_response_code(200, get_cost_accts_resp.status_code) is True
        # "Validate total count and accounts returned in response is > 0 ":
        total_accounts = len(get_cost_accts_resp.json()['accounts'])
        if total_accounts == 0:
            pytest.fail("No accounts are returned in response. Expected count > 0")

        else:
            # Verify that fetched records are not in archived state
            for i in range(total_accounts):
                is_archived = get_cost_accts_resp.json()['accounts'][i]['archived']
                self.validate_expected_and_actual_values_code(is_archived, False)
                # Verify that received subId is correct:
                received_sub_id = str(get_cost_accts_resp.json()['accounts'][i]['subID'])
                self.validate_expected_and_actual_values_code(received_sub_id, subid)

            # Search by code
        query_param = 'query=Dw_01'

        # "Fetch all the active cost accounts: "
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(subid, is_admin='Y',
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

    # Code for two step import process

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_import_admin_api(self, resource):
        """
        This test validates that cost account can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call Import cost account API and Validate the response:
        name = "ca_imp_" + str(random.randint(1, 35000))
        acc_id = name
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE'

        upload_cost_acct_file_resp = resource['account_mgmt'].upload_cost_acc_file_api(acc_id=acc_id, sub_id=sub_id,
                                                                                       name=name,
                                                                                       is_admin='y', status=status)

        # "Validate the response of upload cost account file API: "):
        assert_that(upload_cost_acct_file_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: ":
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # "Verify the process status of uploaded file":
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='y')
        assert_that(job_process_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: ":

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')

        assert_that(job_status_resp.json()['status'], equal_to('Processed'))

        # "Validate that created account can be fetched successfully and verify the received account Id":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        # "Validate that status code of get cost Account by acount id API is correct":
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        received_acc_id = get_cost_acct_resp['accountID']

        assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id, sub_id=sub_id,
                                                                                   is_admin=True)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))
        # "Validate that error is obtained when archived cost account is fetched"):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_error_response_import_admin_api(self, resource):
        """
        This test validates that error is obtained when import file is imported with error data (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call Import cost account API and Validate the response. ":
        name = ' '
        acc_id = ' '
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        status = 'TRUE1'

        upload_cost_acct_file_resp = resource['account_mgmt'].upload_cost_acc_file_api(acc_id=acc_id, sub_id=sub_id,
                                                                                       name=name,
                                                                                       is_admin='y', status=status)

        # "Validate the response of upload cost account file API: ":
        assert_that(upload_cost_acct_file_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: ":
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # "Verify the process status of uploaded file: "):
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='y')
        assert_that(job_process_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: ":

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id, job_id=job_id,
                                                                                   is_admin='y')

        assert_that(job_status_resp.status_code, equal_to(200))

        assert_that(str(job_status_resp.json()['status']), equal_to('ProcessingError'))

    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_export_admin_api(self, resource):
        """
        This test validates that cost account can be exported successfully (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call export cost account API and Validate the response
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        export_cost_acct_resp = resource['account_mgmt'].export_cost_acct_by_sub_id_api(sub_id=sub_id,
                                                                                        is_admin='y')

        # Validate the response of export cost account API
        assert self.validate_expected_and_actual_response_code(201, export_cost_acct_resp.status_code) is True

        # Fetch the created job Id from the response
        job_id = str(export_cost_acct_resp.json()['jobId'])

        # Verify the status of exported file:
        export_job_status_resp = resource['account_mgmt'].export_job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                                 job_id=job_id,
                                                                                                 is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, export_job_status_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    @pytest.mark.skip(reason="need to fix this test, access levels are at the import dialog and not in file")
    def test_cost_account_hierarchy_import_admin_api(self, resource):
        """
        This test validates that cost account hierarchy can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        with ((((((((allure.step("Call Import cost account API and Validate the response. "))))))))):
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
                                                                                                           is_admin='y')

            # Validate the response of upload hierarchy cost account file API:
            assert_that(upload_cost_acct_hierarchy_resp.status_code, equal_to(200))

            # Fetch the created job Id from the response:
            job_id = str(upload_cost_acct_hierarchy_resp.json()['jobId'])

            # Verify the process status of uploaded file :
            job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                         job_id=job_id,
                                                                                         is_admin='y')
            assert_that(job_process_resp.status_code, equal_to(200))

            # Validate that imported records are uploaded successfully:

            job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                       job_id=job_id,
                                                                                       is_admin='y')

            assert_that(job_status_resp.status_code, equal_to(200))

            status = str(job_status_resp.json()['status'])

            assert_that(status, equal_to('Processed'))

            # Validate that created hierarchy can be fetched successfully:
            get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                          sub_id=sub_id,
                                                                                          is_admin=True)
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
            get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                acct_id=child_cost_acc_id, sub_id=sub_id, is_admin=True)
            assert_that(get_cost_acct_resp.status_code, equal_to(200))

            # Validate that sub child account can be fetched successfully:
            get_sub_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                acct_id=sub_child_cost_acc_id, sub_id=sub_id, is_admin=True)
            assert_that(get_sub_cost_acct_resp.status_code, equal_to(200))

            # Validate that sub child account can be archived/deleted successfully and verify the status code:
            archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=sub_child_cost_acc_id,
                                                                                       sub_id=sub_id, is_admin=True)

            assert_that(archive_cost_acct_resp.status_code, equal_to(200))

            # "Validate that error is obtained when archived cost account is fetched":

            get_archived_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                acct_id=sub_child_cost_acc_id, sub_id=sub_id, is_admin=True)

            assert_that(get_archived_cost_acct_resp.status_code, equal_to(404))

            # Validate that sub child account can be archived/deleted successfully and verify the status code:
            archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=child_cost_acc_id,
                                                                                       sub_id=sub_id, is_admin=True)
            assert_that(archive_cost_acct_resp.status_code, equal_to(200))

            # "Validate that error is obtained when archived cost account is fetched":
            get_archived_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                acct_id=child_cost_acc_id, sub_id=sub_id, is_admin=True)
            assert_that(get_archived_cost_acct_resp.status_code, equal_to(404))

            # "Validate that created account can be archived/deleted successfully and verify the status code":
            archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id, sub_id=sub_id,
                                                                                       is_admin=True)

            assert_that(archive_cost_acct_resp.status_code, equal_to(200))

            # "Validate that error is obtained when archived cost account is fetched":
            get_archived_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                                   sub_id=sub_id,
                                                                                                   is_admin=True)
            assert_that(get_archived_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_sub_cost_account_api(self, resource):
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
                                                                               sub_id=sub_id, is_admin=True)

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
                get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                    acct_id=created_acc_id, sub_id=sub_id, is_admin=True)

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
                                sub_id=sub_id, is_admin=True)

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
                                        'account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_cost_accID, sub_id=sub_id, is_admin=True)

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
                                                    'account_mgmt'].archive_cost_account_api(
                                                    acct_id=
                                                    sub_acc_id, sub_id=sub_id, is_admin=True)
                                                if archive_cost_acct_resp.status_code != 200:
                                                    self.Failures.append(
                                                        "There is a failure in archive sub cost Account response : Expected: 200 , Received : " + str(
                                                            archive_cost_acct_resp.status_code))

                                            with allure.step(
                                                    "Validate that error is obtained when archived sub cost account is fetched"):
                                                get_cost_acct_resp = resource[
                                                    'account_mgmt'].get_cost_account_by_acct_id_api(acct_id=sub_acc_id, sub_id=sub_id, is_admin=True)
                                                if get_cost_acct_resp.status_code != 404:
                                                    self.Failures.append(
                                                        "There is a failure in fetching archived sub cost Account Response: Expected: 404 , Received : " + str(
                                                            get_cost_acct_resp.status_code))

            with allure.step(
                    "Validate that created account can be archived/deleted successfully and verify the status code"):
                archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                           sub_id=sub_id,
                                                                                           is_admin=True)
                if archive_cost_acct_resp.status_code != 200:
                    self.Failures.append(
                        "There is a failure in archive cost Account response : Expected: 200 , Received : " + str(
                            archive_cost_acct_resp.status_code))

            with allure.step(
                    "Validate that error is obtained when archived cost account is fetched"):
                get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
                    acct_id=created_acc_id, sub_id=sub_id, is_admin=True)
                if get_cost_acct_resp.status_code != 404:
                    self.Failures.append(
                        "There is a failure in fetching archived cost Account Response: Expected: 404 , Received : " + str(
                            get_cost_acct_resp.status_code))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_sub_cost_account_with_invalid_parent_api(self, resource):
        """
        This test validates that error is obtained when sub cost account is created with invalid parent Id (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Validate that cost account can be created successfully"):
        accountID = "AUT_ACC_" + str(random.randint(1, 3500))
        code = accountID
        name = accountID
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_entity = 'E'
        prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        parent_id = 'Test_Par_01'

        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code,
                                                                           name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           parent=parent_id,
                                                                           sub_id=sub_id, is_admin=True)

        # "Validate that correct error code is obtained: ":
        assert_that(add_cost_acct_resp.status_code, equal_to(400))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_duplicate_cost_account_api(self, resource):
        """
        This test validates that duplicate cost accounts can not be created (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Validate that cost account can be created successfully":
        accountID = "Dup_acc_check_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        code = accountID
        name = accountID
        sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        prmsn_by_entity = 'E'
        prmsn_by_value = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        # "Call create Cost Account API and validate status code: ":
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=sub_id, is_admin=True)

        # "Validate that tus code of create cost Account API is 201: ":
        assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']

        # "Validate that created account can be fetched successfully and verify the received account Id":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
            acct_id=created_acc_id, sub_id=sub_id, is_admin=True)

        # "Validate that status code of get cost Account by Id API is 200: "
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        received_acc_id = get_cost_acct_resp.json()['accountID']

        # "Validate that fetched and created Id are same: "
        assert self.validate_expected_and_actual_values_code(created_acc_id, received_acc_id) is True

        # "Call create Cost Account API again and validate correct error code (400) is obtained : "
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=sub_id, is_admin=True)

        # "Validate that error should be obtained when duplicate cost account is created 400":
        assert self.validate_expected_and_actual_response_code(400, add_cost_acct_resp.status_code) is True
        err_msg = str(add_cost_acct_resp.json()['errors'][0]['errorCode'])
        expected_err = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'ErrorMsg'))

        # "Validate that expected error and obtained error are same: ":
        assert self.validate_expected_and_actual_values_code(err_msg, expected_err) is True

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                   sub_id=sub_id,
                                                                                   is_admin=True)

        # "Validate that status code of delete cost Account API is 200: ":
        assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_hierarchy_single_step_import_admin_api(self, resource):
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
                                                                                                            is_admin='y')

        # "Validate the response of single step Import cost account API is 200 : "):
        assert self.validate_expected_and_actual_response_code(201, import_cost_acct_hierarchy_resp.status_code) is True

        # "Validate that created hierarchy can be fetched successfully: ":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        # "Validate that status code of get cost Account by Id API is 200: ":
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        # received_acc_id = str(res['accountID'])
        child_cost_acc = str(get_cost_acct_resp.json()['children'])
        child_cost_acc_id = str(get_cost_acct_resp.json()['children'][0]['accountID'])
        # parent_level_one = str(res['children'][0]['parent'])
        # sub_child_parent_id = res['children'][0]['children'][0]['parent']
        assert_that(len(child_cost_acc), greater_than(0))

        # "Validate that created child account can be fetched successfully: ":
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        assert_that(get_cost_acct_resp.status_code, equal_to(200))

        # "Validate that sub child account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=child_cost_acc_id,
                                                                                   sub_id=sub_id, is_admin='y')
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_archived_cost_acct_resp = (resource['account_mgmt'].
                                       get_cost_account_by_acct_id_api(acct_id=child_cost_acc_id,
                                                                       sub_id=sub_id, is_admin=True))
        assert_that(get_archived_cost_acct_resp.status_code, equal_to(404))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=acc_id,
                                                                                   sub_id=sub_id,
                                                                                   is_admin=True)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))

        # "Validate that error is obtained when archived cost account is fetched":
        get_archived_cost_acct_resp = (resource['account_mgmt']
                                       .get_cost_account_by_acct_id_api(acct_id=acc_id, sub_id=sub_id, is_admin=True))
        assert_that(get_archived_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_assigned_cost_account_inactive_or_delete_admin(self, resource):
        """
        This test validates that an assigned cost Account can not be made inactive or can not be deleted (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # fetch the details of cost account to be updated
        accountID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))
        subId = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))

        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=accountID, sub_id=subId, is_admin=True))
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        code = get_cost_acct_resp.json()['code']
        name = get_cost_acct_resp.json()['name']
        status = False
        parent = get_cost_acct_resp.json()['parent']

        # Call update cost account API
        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name, status=status,
                                                                                 SubID=subId, parent=parent,
                                                                                 is_admin='y')
        assert self.validate_expected_and_actual_response_code(400, update_cost_acct_resp.status_code) is True

        obtained_err_msg = str(update_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-UP-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

        # Validate that assigned account can not be archived/deleted :
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=accountID, sub_id=subId,
                                                                                   is_admin=True)

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

        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=accountID, sub_id=subId, is_admin=True))
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        code = get_cost_acct_resp.json()['code']
        name = get_cost_acct_resp.json()['name']
        status = False
        parent = get_cost_acct_resp.json()['parent']

        # Call update cost account API
        update_cost_acct_resp = resource['account_mgmt'].update_cost_account_api(accountID, code, name, status=status,
                                                                                 SubID=subId, parent=parent,
                                                                                 is_admin='y')
        assert self.validate_expected_and_actual_response_code(400, update_cost_acct_resp.status_code) is True

        obtained_err_msg = str(update_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-UP-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

        # Validate that assigned account can not be archived/deleted :
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=accountID, sub_id=subId,
                                                                                   is_admin=True)

        assert self.validate_expected_and_actual_response_code(400, archive_cost_acct_resp.status_code) is True

        obtained_err_msg = str(archive_cost_acct_resp.json()['errors'][0]['errorCode'])

        assert self.validate_expected_and_actual_values_code('DC-AR-AMAC2-E-costAccountID.referencefound',
                                                             obtained_err_msg) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_assigned_cost_accounts_inactive_by_import_admin_api(self, resource):
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
            permission_val=prmsn_by_val, sub_id=sub_id, is_admin='y')

        assert self.validate_expected_and_actual_response_code(200, assigned_cost_acct_import_file_resp.status_code) is True

        # Fetch the created job Id from the response:
        job_id = str(assigned_cost_acct_import_file_resp.json()['jobId'])

        # Verify the process status of uploaded file:
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id, job_id=job_id,
                                                                                     is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, job_process_resp.status_code) is True

        # Validate that error is obtained :

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, job_status_resp.status_code) is True

        file_status = str(job_status_resp.json()['status'])
        assert self.validate_values_comparison_code(file_status, "ProcessingError") is True

        # Verify that status is not updated for assigned cost accounts through import

        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=acc_id, sub_id=sub_id, is_admin=True))
        acc_status = str(get_cost_acct_resp.json()['status'])
        assert self.validate_values_comparison_code(acc_status, "True") is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_make_unassigned_sub_cost_account_inactive_or_archive_admin_api(self, resource):
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
                                                                           sub_id=sub_id, is_admin=True)

        # Validate that status code of create cost Account is correct:
        assert self.validate_expected_and_actual_response_code(201, add_cost_acct_resp.status_code) is True

        created_acc_id = add_cost_acct_resp.json()['accountID']

        # Validate that created account can be fetched successfully and verify the received account Id:
        get_cost_acct_resp = (resource['account_mgmt']
                              .get_cost_account_by_acct_id_api(acct_id=created_acc_id, sub_id=sub_id, is_admin=True))
        assert self.validate_expected_and_actual_response_code(200, get_cost_acct_resp.status_code) is True

        fetched_parent = get_cost_acct_resp.json()['parent']

        assert self.validate_values_comparison_code(parent, fetched_parent) is True

        # Validate that created sub account can be archived/deleted successfully and verify the status code
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id, sub_id=sub_id,
                                                                                   is_admin=True)

        assert self.validate_expected_and_actual_response_code(200, archive_cost_acct_resp.status_code) is True

        # Validate that error is obtained when archived cost account is fetched
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(
            acct_id=created_acc_id, sub_id=sub_id, is_admin=True)
        assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_import_inactive_cost_acc_admin_api(self, resource):
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
                                                                                       is_admin='y', status=status)

        assert self.validate_expected_and_actual_response_code(200, upload_cost_acct_file_resp.status_code) is True

        # Fetch the created job Id from the response:
        job_id = str(upload_cost_acct_file_resp.json()['jobId'])

        # Verify the process status of uploaded file:
        job_process_resp = resource['account_mgmt'].job_process_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                     job_id=job_id,
                                                                                     is_admin='y')
        assert self.validate_expected_and_actual_response_code(200, job_process_resp.status_code) is True

        time.sleep(4)

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=sub_id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')

        assert self.validate_expected_and_actual_response_code(200, job_status_resp.status_code) is True

        # Verify the schema of import status response:

        file_status = str(job_status_resp.json()['status'])
        # assert self.validate_values_comparison_code(status, 'ProcessingError') is True
        assert_that(file_status, equal_to('ProcessingError'))

        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=acc_id,
                                                                                      sub_id=sub_id,
                                                                                      is_admin=True)
        assert self.validate_expected_and_actual_response_code(404, get_cost_acct_resp.status_code) is True
