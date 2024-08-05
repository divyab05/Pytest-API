""" This module contains all test cases."""

import inspect
import json
import time

import pytest
from hamcrest import assert_that, equal_to
import logging
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    client_mgmt = {'app_config': app_config,
                   'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
                   'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
                   'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
                   'login_api': LoginAPI(app_config)}
    yield client_mgmt


@pytest.mark.usefixtures('initialize')
class TestClientManagementCommonAPI(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_division_expected_response_body')) as f1:
            self.sample_add_division_expected_response_body = json.load(f1)

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_location_expected_response_body')) as f2:
            self.sample_add_location_expected_response_body = json.load(f2)

        yield

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    def test_01_validate_account_list_id_created_for_newly_created_location_with_admin_user(self, resource):
        """
        This test validates account list is created when a new location is created using admin user.
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id = f'{loc_name}_loc_id'

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id, is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
        assert_that(self.validate_response_code(get_loc_by_id_res, 200))

        fetched_loc_id = get_loc_by_id_res.json()['locationID']
        fetched_loc_name = get_loc_by_id_res.json()['name']

        assert_that(fetched_loc_id, equal_to(loc_id))
        assert_that(fetched_loc_name, equal_to(loc_name))

        t = 5
        self.log.info(f"Awaiting for {t} secs to populate the account list id in the DB!")
        time.sleep(t)

        # validate whether account list id is created for the newly created location
        get_acct_list_id_resp = resource['account_mgmt'].get_account_lists(account_list_id=created_loc_id,
                                                                           is_admin=True)
        assert_that(self.validate_response_code(get_acct_list_id_resp, 200))

        fetched_acct_list_id = get_acct_list_id_resp.json()['acctListID']
        fetched_loc_id_from_acct_list = get_acct_list_id_resp.json()['locID']

        assert_that(created_loc_id, equal_to(fetched_acct_list_id))
        assert_that(created_loc_id, equal_to(fetched_loc_id_from_acct_list))

        # delete the created location and division
        self.log.info(f"Deleting the created location and division!")
        del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)
        assert_that(del_loc_res, equal_to(200))

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # fetch the deleted location and division
        self.log.info(f"Deleted location should not be available")
        get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id)
        assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('user_type', ['E', 'D', 'L'])
    def test_02_validate_account_list_id_created_for_newly_created_location_with_client_users(self, resource, user_type):
        """
        This test validates account list is created when a new location is created using different
        admin access level client users.
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sub_id, ent_id, email, pwd = resource['client_mgmt'].get_subs_user_details_from_test_data(user_type=user_type)

        # Generate user access token
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id = f'{loc_name}_loc_id'

        # Create new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=False, client_token=user_token)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=False, client_token=user_token)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        # fetch the created location
        get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id, is_admin=False, client_token=user_token)
        assert_that(self.validate_response_code(get_loc_by_id_res, 200))

        fetched_loc_id = get_loc_by_id_res.json()['locationID']
        fetched_loc_name = get_loc_by_id_res.json()['name']

        assert_that(fetched_loc_id, equal_to(loc_id))
        assert_that(fetched_loc_name, equal_to(loc_name))

        t = 5
        self.log.info(f"Awaiting for {t} secs to populate the account list id in the DB!")
        time.sleep(t)

        # validate whether account list id is created for the newly created location
        get_acct_list_id_resp = resource['account_mgmt'].get_account_lists(account_list_id=created_loc_id,
                                                                           is_admin=False, client_token=user_token)
        assert_that(self.validate_response_code(get_acct_list_id_resp, 200))

        fetched_acct_list_id = get_acct_list_id_resp.json()['acctListID']
        fetched_loc_id_from_acct_list = get_acct_list_id_resp.json()['locID']

        assert_that(created_loc_id, equal_to(fetched_acct_list_id))
        assert_that(created_loc_id, equal_to(fetched_loc_id_from_acct_list))

        # delete the created location and division
        self.log.info(f"Deleting the created location and division!")
        del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)
        assert_that(del_loc_res, equal_to(200))

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # fetch the deleted location
        self.log.info(f"Deleted location should not be available")
        get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id, is_admin=False, client_token=user_token)
        assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    def test_03_validate_user_login_when_same_custom_loc_id_exist_as_archived_and_active(self, resource):
        """
        This test validates account list is created when a new location is created using admin user.
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f"auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}"
        div_id = f"{div_name}_div_id"
        custom_loc_id = f"same_custom_loc_id_{generate_random_string(uppercase=False, char_count=4)}"
        loc1_name = f"loc1_auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}"
        loc2_name = f"loc2_auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}"

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc1_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=custom_loc_id,
                                                                  loc_name=loc1_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc1_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id_1 = add_loc1_res.json()['locationID']

        t = 5
        self.log.info(f"Awaiting for {t} secs to populate the account list id in the DB!")
        time.sleep(t)

        # delete loc1
        self.log.info(f"Deleting location from the division!")
        del_loc_from_div_res = resource['client_mgmt'] \
            .delete_location_v2_api(loc_id=created_loc_id_1, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(del_loc_from_div_res, 200))

        update_dev_resp = resource['client_mgmt'] \
            .put_update_division_with_loc_id_api(loc_id=created_loc_id_1, div_id=created_div_id)
        assert_that(self.validate_response_code(update_dev_resp, 200))

        self.log.info(f"Creating new location and using location id of deleted location id...")
        add_loc2_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=custom_loc_id,
                                                                   loc_name=loc2_name, ent_id=ent_id, sub_id=sub_id,
                                                                   is_admin=True)
        assert_that(self.validate_response_template(add_loc2_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id_2 = add_loc2_res.json()['locationID']

        # create user with same custom loc id
        self.log.info(f"Creating new user with newly created location")
        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            (resource['subscription_api']
             .create_active_subs_user(sub_id=sub_id, admin_level='E', division_id=created_div_id,
                                      location_id=created_loc_id_2, del_existing_user=True))

        resource['login_api'].check_user_login_status(mailid, password)
        self.log.info(f"Deleting created user - {mailid}")
        resource['subscription_api'].delete_created_subs_users(sub_id=sub_id, query=mailid)


