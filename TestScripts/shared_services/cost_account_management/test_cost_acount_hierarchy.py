import inspect
import json
import time
import pytest
import logging
from hamcrest import assert_that, equal_to, is_not
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestCostAccountHierarchy.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: resource_instances object.
    """
    resource_instances = {
        'app_config': app_config,
        'cost_acct_api': CostAccountManagement(app_config, generate_access_token, client_token),
        'subs_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'data_generator': DataGenerator(app_config),
        'login_api': LoginAPI(app_config)
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestCostAccountHierarchy(common_utils):
    """
    The test class to place all the tests of cost account hierarchy related validations.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestUserImportExport.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_all_users_expected_response_body')) as f1:
            self.sample_get_all_users_exp_resp = json.load(f1)

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    @pytest.mark.cost_account_management_sp360commercial_smoke
    @pytest.mark.cost_account_management_fedramp
    @pytest.mark.cost_account_management_fedramp_reg
    @pytest.mark.cost_account_management_fedramp_smoke
    @pytest.mark.parametrize('is_admin, cost_acct_access_level, user_access_level',
                             [(True, 'E', None), (True, 'D', None), (True, 'L', None),
                              (False, 'E', 'E'), (False, 'D', 'E'), (False, 'L', 'E'),
                              (False, 'D', 'D'), (False, 'L', 'D'), (False, 'L', 'L')])
    def test_01_add_parent_child_cost_accounts_at_different_access_level(self, resource, is_admin,
                                                                         cost_acct_access_level, user_access_level):
        """
        This test method verifies the creation of parent, sub and sub-sub cost account at different access levels
        using admin user and client users with different admin access levels.

        :param resource: The resource fixture used in the test.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses client user.
        :param cost_acct_access_level: The flag to determine the cost account access level.
        :param user_access_level: The flag to determine the client user's admin access level.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        wait_time = 10
        sub_id, email, pwd = resource['cost_acct_api'].get_sub_id_user_cred_from_cost_acct_file(user_type=user_access_level)
        ent_id, ent_name, divisions, loc_id, carrier_accounts, subs_role_ids = (
            resource['subs_api'].get_ent_div_loc_carrier_subs_details_from_sub_id(sub_id=sub_id))

        user_token = None
        parent_acct_id = None
        if not is_admin:
            # Generate user access token
            user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        entity_value = None
        if cost_acct_access_level == 'E':
            entity_value = ent_id
        elif cost_acct_access_level == 'D':
            entity_value = divisions
        elif cost_acct_access_level == 'L':
            entity_value = [loc_id]

        # Create parent cost account
        parent_acct_data = resource['data_generator'].cost_account_data_setter()
        # [name, code, desc, pwd_enabled, pwd_code, status, parent_name, next_parent_name, billable]

        add_cost_acct_resp = (resource['cost_acct_api']
                              .add_cost_account_api(code=parent_acct_data[1], name=parent_acct_data[0],
                                                    desc=parent_acct_data[2], prmsn_by_entity=cost_acct_access_level,
                                                    billable=parent_acct_data[8], prmsn_by_value=entity_value,
                                                    sub_id=sub_id, is_admin=is_admin, token=user_token))

        assert_that(self.validate_response_code(add_cost_acct_resp, 201))
        created_parent_acct_id = add_cost_acct_resp.json()['accountID']
        self.log.info(f'Created parent cost account - "{parent_acct_data[0]}" with '
                      f'access level "{cost_acct_access_level}" using "{user_access_level}" user successfully!')

        time.sleep(wait_time)

        try:
            get_parent_cost_act_resp = (resource['cost_acct_api']
                                        .advance_search_cost_accounts_api(query=parent_acct_data[0], sub_id=sub_id,
                                                                          is_admin=is_admin, token=user_token))
            assert_that(self.validate_response_code(get_parent_cost_act_resp, 200))

            parent_acct_id = get_parent_cost_act_resp.json()['accounts'][0]['accountID']
            parent_acct_name = get_parent_cost_act_resp.json()['accounts'][0]['name']
            parent_acct_code = get_parent_cost_act_resp.json()['accounts'][0]['code']
            parent_sub_acct_count = get_parent_cost_act_resp.json()['accounts'][0]['SubAcctCounts']
            parent_entity = get_parent_cost_act_resp.json()['accounts'][0]['permission']['permissionByEntity']
            parent_entity_value = get_parent_cost_act_resp.json()['accounts'][0]['permission']['permissionByValue']

            assert_that(created_parent_acct_id, equal_to(parent_acct_id))
            assert_that(parent_acct_data[0], equal_to(parent_acct_name))
            assert_that(parent_acct_data[1], equal_to(parent_acct_code))
            assert_that(0, equal_to(parent_sub_acct_count))
            assert_that(cost_acct_access_level, equal_to(parent_entity))
            assert_that(entity_value, equal_to(parent_entity_value))

            # Create sub cost account
            sub_acct_data = resource['data_generator'].cost_account_data_setter()

            add_sub_cost_acct_resp = (resource['cost_acct_api']
                                      .add_cost_account_api(code=sub_acct_data[1], name=sub_acct_data[0],
                                                            desc=sub_acct_data[2], prmsn_by_entity=cost_acct_access_level,
                                                            billable=sub_acct_data[8], prmsn_by_value=entity_value,
                                                            parent=parent_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token))

            assert_that(self.validate_response_code(add_sub_cost_acct_resp, 201))
            created_sub_acct_id = add_sub_cost_acct_resp.json()['accountID']

            self.log.info(f'Created sub cost account - "{sub_acct_data[0]}" within parent '
                          f'cost account - "{parent_acct_data[0]}" having access level '
                          f'"{cost_acct_access_level}" using "{user_access_level}" user successfully!')

            time.sleep(wait_time)

            sub_cost_act_resp = (resource['cost_acct_api']
                                 .get_sub_cost_accounts_api(sub_id=sub_id, parent_acct_id=parent_acct_id, is_admin=is_admin, token=user_token))
            assert_that(common_utils.validate_response_code(sub_cost_act_resp, 200))

            sub_acct_id = sub_cost_act_resp.json()['accounts'][0]['accountID']
            sub_acct_name = sub_cost_act_resp.json()['accounts'][0]['name']
            sub_acct_code = sub_cost_act_resp.json()['accounts'][0]['code']
            child_sub_acct_count = sub_cost_act_resp.json()['accounts'][0]['SubAcctCounts']
            sub_entity = sub_cost_act_resp.json()['accounts'][0]['permission']['permissionByEntity']
            sub_entity_value = sub_cost_act_resp.json()['accounts'][0]['permission']['permissionByValue']
            sub_parent_id = sub_cost_act_resp.json()['accounts'][0]['parent']
            sub_parent_name = sub_cost_act_resp.json()['accounts'][0]['parentName']

            assert_that(created_sub_acct_id, equal_to(sub_acct_id))
            assert_that(sub_acct_data[0], equal_to(sub_acct_name))
            assert_that(sub_acct_data[1], equal_to(sub_acct_code))
            assert_that(0, equal_to(child_sub_acct_count))
            assert_that(cost_acct_access_level, equal_to(sub_entity))
            assert_that(entity_value, equal_to(sub_entity_value))
            assert_that(parent_acct_id, equal_to(sub_parent_id))
            assert_that(parent_acct_name, equal_to(sub_parent_name))

            # Create sub-sub cost account
            sub_sub_acct_data = resource['data_generator'].cost_account_data_setter()

            add_sub_sub_cost_acct_resp = (resource['cost_acct_api']
                                          .add_cost_account_api(code=sub_sub_acct_data[1], name=sub_sub_acct_data[0],
                                                                desc=sub_sub_acct_data[2], prmsn_by_entity=cost_acct_access_level,
                                                                billable=sub_sub_acct_data[8], prmsn_by_value=entity_value,
                                                                parent=sub_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token))

            assert_that(self.validate_response_code(add_sub_sub_cost_acct_resp, 201))
            created_sub_sub_acct_id = add_sub_sub_cost_acct_resp.json()['accountID']

            self.log.info(f'Created sub-sub cost account - "{sub_sub_acct_data[0]}" within sub cost account '
                          f'- "{sub_acct_data[0]}" of parent cost account - "{parent_acct_data[0]}" having access '
                          f'level "{cost_acct_access_level}" using "{user_access_level}" user successfully!')

            time.sleep(wait_time)

            sub_sub_cost_act_resp = (resource['cost_acct_api']
                                     .get_sub_cost_accounts_api(sub_id=sub_id, parent_acct_id=sub_acct_id, is_admin=is_admin, token=user_token))
            assert_that(common_utils.validate_response_code(sub_sub_cost_act_resp, 200))

            sub_sub_acct_id = sub_sub_cost_act_resp.json()['accounts'][0]['accountID']
            sub_sub_acct_name = sub_sub_cost_act_resp.json()['accounts'][0]['name']
            sub_sub_acct_code = sub_sub_cost_act_resp.json()['accounts'][0]['code']
            child_sub_sub_acct_count = sub_sub_cost_act_resp.json()['accounts'][0]['SubAcctCounts']
            sub_sub_entity = sub_sub_cost_act_resp.json()['accounts'][0]['permission']['permissionByEntity']
            sub_sub_entity_value = sub_sub_cost_act_resp.json()['accounts'][0]['permission']['permissionByValue']
            sub_sub_parent_id = sub_sub_cost_act_resp.json()['accounts'][0]['parent']
            sub_sub_parent_name = sub_sub_cost_act_resp.json()['accounts'][0]['parentName']

            assert_that(created_sub_sub_acct_id, equal_to(sub_sub_acct_id))
            assert_that(sub_sub_acct_data[0], equal_to(sub_sub_acct_name))
            assert_that(sub_sub_acct_data[1], equal_to(sub_sub_acct_code))
            assert_that(0, equal_to(child_sub_sub_acct_count))
            assert_that(cost_acct_access_level, equal_to(sub_sub_entity))
            assert_that(entity_value, equal_to(sub_sub_entity_value))
            assert_that(sub_acct_id, equal_to(sub_sub_parent_id))
            assert_that(sub_acct_name, equal_to(sub_sub_parent_name))

        finally:

            # Validate that created account can be archived/deleted successfully and verify the status code
            archive_cost_acct_resp = resource['cost_acct_api'].archive_cost_account_api(acct_id=parent_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token)
            assert_that(self.validate_response_code(archive_cost_acct_resp, 200))

            time.sleep(wait_time)

            # Validate that error is obtained when archived cost account is fetched
            get_cost_acct_after_archive_resp = resource['cost_acct_api'] \
                .get_cost_account_by_acct_id_api(acct_id=parent_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token)

            assert_that(self.validate_response_code(get_cost_acct_after_archive_resp, 404))
            self.log.info(f'Deleted the created parent cost account - "{parent_acct_data[0]}" having access '
                          f'level "{cost_acct_access_level}" successfully!')

    @pytest.mark.cost_account_management_sp360commercial
    @pytest.mark.cost_account_management_sp360commercial_reg
    @pytest.mark.cost_account_management_sp360commercial_smoke
    @pytest.mark.cost_account_management_fedramp
    @pytest.mark.cost_account_management_fedramp_reg
    @pytest.mark.cost_account_management_fedramp_smoke
    @pytest.mark.parametrize('is_admin, cost_acct_access_level, cost_acct_update_level, user_access_level',
                             [(True, 'E', 'D', 'None'), (True, 'E', 'L', 'None'), (True, 'D', 'E', 'None'),
                              (True, 'D', 'L', 'None'), (True, 'L', 'D', 'None'), (True, 'L', 'E', 'None'),
                              (False, 'E', 'D', 'E'), (False, 'E', 'L', 'E'), (False, 'D', 'E', 'E'),
                              (False, 'D', 'L', 'E'), (False, 'L', 'D', 'E'), (False, 'L', 'E', 'E')
                              ])
    def test_02_add_parent_child_cost_account_update_their_access_level_and_delete_them(
            self, resource, is_admin, cost_acct_access_level, cost_acct_update_level, user_access_level):
        """
        This test method verifies the creation of parent, sub and sub-sub cost account at different access levels
        and update the created cost account access level to a different level and finally delete the created
        child and parent cost accounts using admin user and client users with different admin access levels.

        :param resource: The resource fixture used in the test.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses client user.
        :param cost_acct_access_level: The flag to determine the cost account access level.
        :param cost_acct_update_level: The flag to determine the new access level of cost account to be updated with.
        :param user_access_level: The flag to determine the client user's admin access level.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        wait_time = 10
        sub_id, email, pwd = resource['cost_acct_api'].get_sub_id_user_cred_from_cost_acct_file(
            user_type=user_access_level)
        ent_id, ent_name, divisions, loc_id, carrier_accounts, subs_role_ids = (
            resource['subs_api'].get_ent_div_loc_carrier_subs_details_from_sub_id(sub_id=sub_id))

        # Generate user access token
        user_token = None
        if not is_admin:
            user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        change_entity_value = None
        if cost_acct_update_level == 'E':
            change_entity_value = ent_id
        elif cost_acct_update_level == 'D':
            change_entity_value = divisions
        elif cost_acct_update_level == 'L':
            change_entity_value = [loc_id]

        # Create parent, sub and sub-sub cost account
        created_parent_acct_id, created_sub_acct_id, created_sub_sub_acct_id = (
            resource['cost_acct_api'].create_parent_child_cost_accounts(sub_id=sub_id, ent_id=ent_id,
                                                                        divisions=divisions, loc_id=loc_id,
                                                                        cost_acct_access_level=cost_acct_access_level,
                                                                        is_admin=is_admin, token=user_token))

        try:
            # verify cost account access level in parent, sub, and sub-sub
            (parent_acct_resp, extracted_account_data, parent_acct_access_lvl, sub_acct_access_lvl,
             sub_sub_acct_access_lvl) = (resource['cost_acct_api']
                                         .verify_cost_account_hierarchy_access_level_and_return_extracted_data(
                parent_acct_id=created_parent_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token))

            parent_name = parent_acct_resp.json().get('name', '')
            parent_code = parent_acct_resp.json().get('code', '')
            parent_billable = parent_acct_resp.json().get('billable', '')
            parent_desc = parent_acct_resp.json().get('description', '')
            parent_entity = parent_acct_resp.json().get('permission').get('permissionByEntity', '')
            parent_entity_value = parent_acct_resp.json().get('permission').get('permissionByValue', [])
            parent_acct_id = parent_acct_resp.json().get('accountID', '')
            parent_pwd_enabled = parent_acct_resp.json().get('passwordEnabled', '')
            parent_pwd_code = parent_acct_resp.json().get('passwordCode', '')
            parent_status = parent_acct_resp.json().get('status', '')
            parent_budget_amt = parent_acct_resp.json().get('budgetAmount', '')
            parent_acct_list_ids = parent_acct_resp.json().get('acctListIDs', [])

            time.sleep(wait_time)

            # Update cost account access level
            self.log.info(f'Updating parent cost account access level from "{cost_acct_access_level}" '
                          f'to "{cost_acct_update_level}"')
            update_cost_acct_resp = (
                resource['cost_acct_api'].put_update_cost_account_api(
                    acct_id=parent_acct_id, code=parent_code, name=parent_name, desc=parent_desc, status=parent_status,
                    billable=parent_billable, prmsn_by_entity=cost_acct_update_level, prmsn_by_value=change_entity_value,
                    pwd_enabled=parent_pwd_enabled, pwd_code=parent_pwd_code, budget_amt=parent_budget_amt, sub_id=sub_id,
                    acct_list_ids=parent_acct_list_ids, is_admin=is_admin, token=user_token))
            assert_that(self.validate_response_code(update_cost_acct_resp, 200))

            # verify the updated parent cost account access level is also updated to its child accounts
            (updtd_parent_acct_resp, updtd_extracted_account_data, updtd_parent_acct_access_lvl, updtd_sub_acct_access_lvl,
             updtd_sub_sub_acct_access_lvl) = (
                resource['cost_acct_api'].verify_cost_account_hierarchy_access_level_and_return_extracted_data(
                    parent_acct_id=parent_acct_id, sub_id=sub_id, is_admin=is_admin, token=user_token))

            updtd_parent_name = updtd_parent_acct_resp.json().get('name', '')
            updtd_parent_code = updtd_parent_acct_resp.json().get('code', '')
            updtd_parent_billable = updtd_parent_acct_resp.json().get('billable', '')
            updtd_parent_desc = updtd_parent_acct_resp.json().get('description', '')
            updtd_parent_entity = updtd_parent_acct_resp.json().get('permission').get('permissionByEntity', '')
            updtd_parent_entity_value = updtd_parent_acct_resp.json().get('permission').get('permissionByValue', [])
            updtd_parent_acct_id = updtd_parent_acct_resp.json().get('accountID', '')
            updtd_parent_pwd_enabled = updtd_parent_acct_resp.json().get('passwordEnabled', '')
            updtd_parent_pwd_code = updtd_parent_acct_resp.json().get('passwordCode', '')
            updtd_parent_status = updtd_parent_acct_resp.json().get('status', '')
            updtd_parent_budget_amt = updtd_parent_acct_resp.json().get('budgetAmount', '')
            updtd_parent_acct_list_ids = updtd_parent_acct_resp.json().get('acctListIDs', [])

            assert_that(parent_name, equal_to(updtd_parent_name))
            assert_that(parent_code, equal_to(updtd_parent_code))
            assert_that(parent_billable, equal_to(updtd_parent_billable))
            assert_that(parent_desc, equal_to(updtd_parent_desc))
            assert_that(parent_acct_id, equal_to(updtd_parent_acct_id))
            assert_that(parent_pwd_enabled, equal_to(updtd_parent_pwd_enabled))
            assert_that(parent_pwd_code, equal_to(updtd_parent_pwd_code))
            assert_that(parent_status, equal_to(updtd_parent_status))
            assert_that(parent_budget_amt, equal_to(updtd_parent_budget_amt))
            assert_that(parent_acct_list_ids, equal_to(updtd_parent_acct_list_ids))

            assert_that(cost_acct_update_level, equal_to(updtd_parent_entity))
            assert_that(change_entity_value, equal_to(updtd_parent_entity_value))

            assert_that(parent_acct_access_lvl, is_not(equal_to(updtd_parent_acct_access_lvl)))
            assert_that(sub_acct_access_lvl, is_not(equal_to(updtd_sub_acct_access_lvl)))
            assert_that(sub_sub_acct_access_lvl, is_not(equal_to(updtd_sub_sub_acct_access_lvl)))

            self.log.info(f'Updated parent cost account access level and its child accounts '
                          f'from "{cost_acct_access_level}" to "{cost_acct_update_level}" successfully!')

        finally:

            # Validate that created account can be archived/deleted successfully and verify the status code
            archive_cost_acct_resp = (resource['cost_acct_api']
                                      .archive_cost_account_api(acct_id=created_parent_acct_id, sub_id=sub_id,
                                                                is_admin=is_admin, token=user_token))
            assert_that(self.validate_response_code(archive_cost_acct_resp, 200))

            time.sleep(wait_time)

            # Validate that error is obtained when archived cost account is fetched
            get_cost_acct_after_archive_resp = resource['cost_acct_api'] \
                .get_cost_account_by_acct_id_api(acct_id=created_parent_acct_id, sub_id=sub_id, is_admin=is_admin,
                                                 token=user_token)

            assert_that(self.validate_response_code(get_cost_acct_after_archive_resp, 404))
            self.log.info(f'Deleted the created parent cost account successfully!')
