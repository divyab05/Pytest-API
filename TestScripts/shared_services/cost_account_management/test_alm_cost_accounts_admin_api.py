""" This module contains all test cases."""
import inspect
import logging
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    account_mgmt = {
        'app_config': app_config,
        'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config)
    }
    yield account_mgmt


@pytest.mark.usefixtures('initialize')
class TestALMAdminAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, resource):
        self.log.info("Starting TestALMAdminAPI...")

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_01_create_del_cost_account_in_alm_enterprise(self, resource):
        """
        This test validates cost accounts can be created successfully in ALM (positive scenario)
        :return: return test status
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        # Validate that cost account can be created successfully
        alm_sub_id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        alm_ent_id = resource['account_mgmt'].get_alm_enterprise_id_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()

        prmsn_by_entity = 'E'
        prmsn_by_value = str(alm_ent_id)
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(cost_acc_id, cost_acc_code, cost_acc_name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=alm_sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_cost_acct_resp, 201))
        created_acc_id = add_cost_acct_resp.json()['accountID']

        # Validate that created account can be fetched successfully and verify the received account id
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=alm_sub_id,
                                                                                      is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_resp, 200))
        received_acc_id = get_cost_acct_resp.json()['accountID']
        assert_that(created_acc_id, equal_to(received_acc_id))

        # Validate that created account can be archived/deleted successfully and verify the status code
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                   sub_id=alm_sub_id, is_admin=True)
        assert_that(self.validate_response_code(archive_cost_acct_resp, 200))

        # Validate that error is obtained when archived cost account is fetched
        get_cost_acct_after_archive_resp = resource['account_mgmt']\
            .get_cost_account_by_acct_id_api(acct_id=created_acc_id, sub_id=alm_sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_after_archive_resp, 404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_02_create_del_division_alm_cost_account_api(self, resource):
        """
        This test validates cost accounts can be created successfully in ALM on division level (positive scenario)
        :return: return test status
        """
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        # Validate that cost account can be created successfully
        alm_sub_Id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        alm_div_id = resource['account_mgmt'].get_alm_divisions_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()

        prmsn_by_entity = 'D'
        prmsn_by_value = str(alm_div_id[0])
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(acct_id=cost_acc_id, code=cost_acc_code,
                                                                           name=cost_acc_name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=alm_sub_Id, is_admin=True)
        assert_that(self.validate_response_code(add_cost_acct_resp, 201))
        created_acc_id = add_cost_acct_resp.json()['accountID']

        # Validate that created account can be fetched successfully and verify the received account Id
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_resp, 200))
        received_acc_id = get_cost_acct_resp.json()['accountID']
        assert_that(created_acc_id, equal_to(received_acc_id))

        # Validate that created account can be archived/deleted successfully and verify the status code
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                   sub_id=alm_sub_Id,
                                                                                   is_admin=True)
        assert_that(self.validate_response_code(archive_cost_acct_resp, 200))

        # Validate that error is obtained when archived cost account is fetched
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_resp, 404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_create_del_loc_alm_cost_account_api(self, resource):
        """
        This test validates cost accounts can be created successfully in ALM on location level (positive scenario)
        :return: return test status
        """

        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        # Validate that cost account can be created successfully
        alm_sub_Id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        alm_loc_id = resource['account_mgmt'].get_alm_locations_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()

        prmsn_by_entity = 'L'
        prmsn_by_value = str(alm_loc_id[0])
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(cost_acc_id, cost_acc_code,
                                                                           cost_acc_name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=alm_sub_Id, is_admin=True)
        assert_that(self.validate_response_code(add_cost_acct_resp, 201))
        created_acc_id = add_cost_acct_resp.json()['accountID']

        # Validate that created account can be fetched successfully and verify the received account id
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_resp, 200))
        received_acc_id = get_cost_acct_resp.json()['accountID']

        assert_that(created_acc_id, equal_to(received_acc_id))

        # Validate that created account can be archived/deleted successfully and verify the status code
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=created_acc_id,
                                                                                   sub_id=alm_sub_Id,
                                                                                   is_admin=True)
        assert_that(self.validate_response_code(archive_cost_acct_resp, 200))

        # Validate that error is obtained when archived cost account is fetched
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=created_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(self.validate_response_code(get_cost_acct_resp, 404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_alm_enterprise_import_admin_api(self, resource):
        """
        This test validates that cost account can be created through Import (Positive scenario)
        :return: return test status
        """
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        # Call Import cost account API and Validate the response:
        alm_sub_Id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        alm_ent_id = resource['account_mgmt'].get_alm_enterprise_id_from_file()
        alm_div_id = resource['account_mgmt'].get_alm_divisions_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()
        name = cost_acc_name
        code = cost_acc_code

        alm_upload_cost_acct_file_resp = resource['account_mgmt'].alm_upload_cost_acc_file_api(sub_id=alm_sub_Id,
                                                                                               name=name, code=code,
                                                                                               is_admin='y')
        assert_that(self.validate_response_code(alm_upload_cost_acct_file_resp, 200))
        job_id = str(alm_upload_cost_acct_file_resp.json()['jobId'])
        prmsn_by_val = alm_ent_id
        param_val = 'permissionByEntity=E&permissionByValue='+prmsn_by_val

        # "Verify the process status of uploaded file":
        alm_job_process_resp = resource['account_mgmt'].alm_job_process_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                             job_id=job_id,
                                                                                             is_admin='y',
                                                                                             param_val=param_val)
        assert_that(self.validate_response_code(alm_job_process_resp, 200))

        # Validate that imported records are uploaded successfully:
        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')
        assert_that(job_status_resp.json()['status'], equal_to('Processed'))
        query_param = 'query='+name
        # "Validate that created account can be fetched successfully and verify the received account Id":
        #res, status_code = resource['account_mgmt'].verify_get_cost_account_by_account_id_api(acc_id=acc_id,sub_id=alm_sub_Id,is_admin='y')
        get_cost_accts_resp = resource['account_mgmt']. get_cost_accounts_by_sub_id_user_id_api(alm_sub_Id, is_admin='Y', query=query_param)

        # "Validate that status code of get cost Account by acount id API is correct":
        assert_that(get_cost_accts_resp.status_code, equal_to(200))

        received_acc_id = get_cost_accts_resp.json()['accounts'][0]['accountID']

        #assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=received_acc_id, sub_id=alm_sub_Id,
                                                                                   is_admin=True)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))
        # "Validate that error is obtained when archived cost account is fetched"):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=received_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_alm_division_import_admin_api(self, rp_logger, resource):
        """
        This test validates that cost account can be created through Import (Positive scenario)
        :return: return test status
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        # Call Import cost account API and Validate the response:
        alm_sub_Id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        #alm_ent_id = resource['account_mgmt'].get_alm_enterprise_id_from_file()
        alm_div_id = resource['account_mgmt'].get_alm_divisions_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()
        name = cost_acc_name
        # acc_id = cost_acc_id
        code = cost_acc_code

        alm_upload_cost_acct_file_resp = resource['account_mgmt'].alm_upload_cost_acc_file_api(sub_id=alm_sub_Id,
                                                                                               name=name, code=code,
                                                                                               is_admin='y')

        # "Validate the response of upload cost account file API: "):
        assert_that(alm_upload_cost_acct_file_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: ":
        job_id = str(alm_upload_cost_acct_file_resp.json()['jobId'])

        prmsn_by_val = alm_div_id[0]
        param_val = 'permissionByEntity=D&permissionByValue=' + prmsn_by_val

        # "Verify the process status of uploaded file":
        alm_job_process_resp = resource['account_mgmt'].alm_job_process_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                             job_id=job_id,
                                                                                             is_admin='y',
                                                                                             param_val=param_val)
        assert_that(alm_job_process_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: ":

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')

        assert_that(job_status_resp.json()['status'], equal_to('Processed'))
        query_param = 'query=' + name
        # "Validate that created account can be fetched successfully and verify the received account Id":
        # res, status_code = resource['account_mgmt'].verify_get_cost_account_by_account_id_api(acc_id=acc_id,sub_id=alm_sub_Id,is_admin='y')
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(alm_sub_Id, is_admin='Y',
                                                                                               query=query_param)

        # "Validate that status code of get cost Account by acount id API is correct":
        assert_that(get_cost_accts_resp.status_code, equal_to(200))

        received_acc_id = get_cost_accts_resp.json()['accounts'][0]['accountID']

        # assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=received_acc_id,
                                                                                   sub_id=alm_sub_Id,
                                                                                   is_admin=True)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))
        # "Validate that error is obtained when archived cost account is fetched"):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=received_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    def test_cost_account_alm_loc_import_admin_api(self, rp_logger, resource):
        """
        This test validates that cost account can be created through Import (Positive scenario)
        :return: return test status
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        # Call Import cost account API and Validate the response:
        alm_sub_Id = resource['account_mgmt'].get_alm_subscription_id_from_file()
        # alm_ent_id = resource['account_mgmt'].get_alm_enterprise_id_from_file()
        alm_loc_id = resource['account_mgmt'].get_alm_locations_from_file()
        cost_acc_name, cost_acc_code, cost_acc_id = resource['account_mgmt'].generate_cost_account_data()
        name = cost_acc_name
        # acc_id = cost_acc_id
        code = cost_acc_code

        alm_upload_cost_acct_file_resp = resource['account_mgmt'].alm_upload_cost_acc_file_api(sub_id=alm_sub_Id,
                                                                                               name=name, code=code,
                                                                                               is_admin='y')

        # "Validate the response of upload cost account file API: "):
        assert_that(alm_upload_cost_acct_file_resp.status_code, equal_to(200))

        # "Fetch the created job Id from the response: ":
        job_id = str(alm_upload_cost_acct_file_resp.json()['jobId'])

        prmsn_by_val = alm_loc_id[0]
        param_val = 'permissionByEntity=L&permissionByValue=' + prmsn_by_val

        # "Verify the process status of uploaded file":
        alm_job_process_resp = resource['account_mgmt'].alm_job_process_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                             job_id=job_id,
                                                                                             is_admin='y',
                                                                                             param_val=param_val)
        assert_that(alm_job_process_resp.status_code, equal_to(200))

        # "Validate that imported records are uploaded successfully: ":

        job_status_resp = resource['account_mgmt'].job_status_by_sub_id_job_id_api(sub_id=alm_sub_Id,
                                                                                   job_id=job_id,
                                                                                   is_admin='y')

        assert_that(job_status_resp.json()['status'], equal_to('Processed'))
        query_param = 'query=' + name
        # "Validate that created account can be fetched successfully and verify the received account Id":
        # res, status_code = resource['account_mgmt'].verify_get_cost_account_by_account_id_api(acc_id=acc_id,sub_id=alm_sub_Id,is_admin='y')
        get_cost_accts_resp = resource['account_mgmt'].get_cost_accounts_by_sub_id_user_id_api(alm_sub_Id, is_admin='Y',
                                                                                               query=query_param)

        # "Validate that status code of get cost Account by acount id API is correct":
        assert_that(get_cost_accts_resp.status_code, equal_to(200))

        received_acc_id = get_cost_accts_resp.json()['accounts'][0]['accountID']

        # assert_that(str(received_acc_id), equal_to(str(acc_id)))

        # "Validate that created account can be archived/deleted successfully and verify the status code":
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=received_acc_id,
                                                                                   sub_id=alm_sub_Id,
                                                                                   is_admin=True)
        assert_that(archive_cost_acct_resp.status_code, equal_to(200))
        # "Validate that error is obtained when archived cost account is fetched"):
        get_cost_acct_resp = resource['account_mgmt'].get_cost_account_by_acct_id_api(acct_id=received_acc_id,
                                                                                      sub_id=alm_sub_Id,
                                                                                      is_admin=True)
        assert_that(get_cost_acct_resp.status_code, equal_to(404))
