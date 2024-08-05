import inspect
import json
import logging
import time
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.federated_subscription_api import FederatedSubscriptionAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'fed_subs_api': FederatedSubscriptionAPI(app_config, generate_access_token, client_token),
        'subs_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
        'login_api': LoginAPI(app_config)
    }
    yield resource_instances


log = log_utils.custom_logger(logging.INFO)


@pytest.mark.usefixtures('initialize')
class TestFedrampSSOUser(common_utils):
    """
    This class includes Fedramp SSO/Federated user and TA Device user related API tests.
    """

    @pytest.fixture()
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestFedrampSSOUser.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('FEDRAMP_SUBSCRIPTION_MGMT', 'sample_add_federated_user_response_body')) as f1:
            self.sample_add_federated_user_exp_resp = json.load(f1)

        yield

    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.parametrize('sub_type, admin_level', [
        ('single-subs', 'E'), ('single-subs', 'D'), ('single-subs', 'L'), ('single-subs', 'User'),
        ('multi-subs', 'E'), ('multi-subs', 'D'), ('multi-subs', 'L'), ('multi-subs', 'User')])
    def test_01_add_delete_federated_user(self, resource, sub_type, admin_level):
        """
        This test verifies the addition and deletion of SSO users using "Add Federated User" option in the
        enterprises configured with Client IDP in a single subscription and with same Client IDP in Multiple
        subscriptions.

        :param sub_type: The subscription type either single-subs or multi-subs.
        :param admin_level: The admin access level defined/used while creating SSO/Federated users.
        """

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        wait_time = 5

        fname, lname, email, dispname, sec_id, login_id, password, ent_name, sub_id, domain = \
            (resource['fed_subs_api'].get_federated_user_profile_from_file(subs_type=sub_type, n=3))

        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['fed_subs_api']\
            .get_federated_subscription_user_details(sub_id=sub_id)

        cost_acct_data = resource['account_mgmt'].get_all_cost_accounts_using_sub_id(sub_id=sub_id, is_admin=True)
        cost_acct_id, cost_acct_name = (resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data))

        # Delete/Archived the created subscription users
        resource['subs_api'].delete_created_subs_users(sub_id=sub_id, query=email)
        resource['fed_subs_api'].delete_federated_and_ta_user(sec_id=sec_id, email=email)

        add_federated_user_resp = resource['fed_subs_api'].add_federated_user_by_sub_id_login_id_api(
            fname=fname, lname=lname, email=email, disp_name=dispname, sub_id=sub_id, loc_id=loc_id, login_id=login_id,
            admin_lvl=admin_level, admn_lvl_entity=ent_id, subs_roles=subs_role_ids, ent_name=ent_name,
            default_cost_acct=cost_acct_id)
        assert_that(self.validate_response_template(add_federated_user_resp,
                                                    self.sample_add_federated_user_exp_resp, 200))
        created_user_id = add_federated_user_resp.json()['userID']

        try:
            update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
                user_id=created_user_id, sub_id=sub_id, def_cost_acct_id=cost_acct_id, is_admin=True)
            assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
            log.info(f'Updated SSO/Federated user default cost account with - {cost_acct_id}, {cost_acct_name}')

            time.sleep(wait_time)

            get_user_profile_from_sso = resource['fed_subs_api'].get_user_profile_from_sso_api(sec_id=sec_id)
            assert_that(self.validate_response_code(get_user_profile_from_sso, 200))
            assert_that(get_user_profile_from_sso.json()['status'], equal_to('ACTIVE'))
            assert_that(email, equal_to(get_user_profile_from_sso.json().get('profile').get('email')))
            assert_that(sec_id, equal_to(get_user_profile_from_sso.json().get('profile').get('login')))
            log.info(f'Email: {email}, UserId: {created_user_id}, SubId: {sub_id}, Sec_id: {sec_id}, Login_id: {login_id}')

            # verify SSO/Federated user login is successful or not
            resource['login_api'].check_user_login_status(username=email, password=password, sso_flag=True)

            time.sleep(wait_time)

            (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
             user_access_lvl, user_admin_entities) = (
                resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id[0], email=email, is_admin=True))
            user_email = user_data.get('detail').get('profile').get('email')
            user_login_id = user_data.get('detail').get('profile').get('login')

            assert_that(email, equal_to(user_email))
            assert_that(sec_id, equal_to(user_login_id))
            assert_that(cost_acct_id, equal_to(user_cost_acct_id))

            if admin_level != 'User':
                assert_that(admin_level, equal_to(user_access_lvl))
            elif admin_level == 'User':
                assert_that(user_access_lvl, equal_to(None))

        finally:
            # Delete/Archived the created subscription and federated user
            resource['subs_api'].delete_created_subs_users(sub_id=sub_id, query=email)
            resource['fed_subs_api'].delete_federated_and_ta_user(sec_id=sec_id, email=email)

    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.parametrize('sub_type, admin_level', [
        ('single-subs', 'E'), ('single-subs', 'D'), ('single-subs', 'L'), ('single-subs', 'User')])
    def test_02_add_delete_federated_user_and_invite_ta_user(self, resource, sub_type, admin_level):
        """
        This test verifies the addition and deletion of SSO users and TA Device users using "Add Federated User"
        and "Add Non-SSO User" options respectively in the enterprise configured with Client IDP in a
        single subscription. TA Device users will be created with the same SSO user email.

        Note: TA Device user creation is not supported in Multiple-subscriptions.

        :param sub_type: The subscription type either single-subs or multi-subs.
        :param admin_level: The admin access level defined/used while creating SSO/Federated users.
        """

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        wait_time = 5

        fname, lname, email, dispname, sec_id, login_id, password, ent_name, sub_id, domain = \
            (resource['fed_subs_api'].get_federated_user_profile_from_file(subs_type=sub_type, n=3))

        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['fed_subs_api'] \
            .get_federated_subscription_user_details(sub_id=sub_id)

        cost_acct_data = resource['account_mgmt'].get_all_cost_accounts_using_sub_id(sub_id=sub_id, is_admin=True)
        cost_acct_id, cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data))

        # Delete/Archived the created subscription users
        resource['subs_api'].delete_created_subs_users(sub_id=sub_id, query=email)
        resource['fed_subs_api'].delete_federated_and_ta_user(sec_id=sec_id, email=email)

        add_federated_user_resp = resource['fed_subs_api'].add_federated_user_by_sub_id_login_id_api(
            fname=fname, lname=lname, email=email, disp_name=dispname, sub_id=sub_id, loc_id=loc_id, login_id=login_id,
            admin_lvl=admin_level, admn_lvl_entity=ent_id, subs_roles=subs_role_ids, ent_name=ent_name,
            default_cost_acct=cost_acct_id)
        assert_that(self.validate_response_template(add_federated_user_resp,
                                                    self.sample_add_federated_user_exp_resp, 200))
        created_user_id = add_federated_user_resp.json()['userID']

        try:
            update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
                user_id=created_user_id, sub_id=sub_id, def_cost_acct_id=cost_acct_id, is_admin=True)
            assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
            log.info(f'Updated SSO/Federated user default cost account with - {cost_acct_id}, {cost_acct_name}')

            time.sleep(wait_time)

            get_user_profile_from_sso = resource['fed_subs_api'].get_user_profile_from_sso_api(sec_id=sec_id)
            assert_that(self.validate_response_code(get_user_profile_from_sso, 200))
            assert_that(get_user_profile_from_sso.json()['status'], equal_to('ACTIVE'))
            assert_that(email, equal_to(get_user_profile_from_sso.json().get('profile').get('email')))
            assert_that(sec_id, equal_to(get_user_profile_from_sso.json().get('profile').get('login')))
            log.info(
                f'Email: {email}, UserId: {created_user_id}, SubId: {sub_id}, Sec_id: {sec_id}, Login_id: {login_id}')

            # verify SSO/Federated user login is successful or not
            resource['login_api'].check_user_login_status(username=email, password=password, sso_flag=True)

            time.sleep(wait_time)

            (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
             user_access_lvl, user_admin_entities) = (
                resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id[0], email=email,
                                                                   is_admin=True))
            user_email = user_data.get('detail').get('profile').get('email')
            user_login_id = user_data.get('detail').get('profile').get('login')

            assert_that(email, equal_to(user_email))
            assert_that(sec_id, equal_to(user_login_id))
            assert_that(cost_acct_id, equal_to(user_cost_acct_id))

            if admin_level != 'User':
                assert_that(admin_level, equal_to(user_access_lvl))
            elif admin_level == 'User':
                assert_that(user_access_lvl, equal_to(None))

            ta_cost_acct_id, ta_cost_acct_name = (
                resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data, excluded_acct_ids=cost_acct_id))

            add_ta_user_resp = resource['fed_subs_api']\
                .add_ta_user_by_sub_id_api(fname=fname, lname=lname, email=email, disp_name=dispname, sub_id=sub_id,
                                           loc_id=loc_id, admin_lvl=admin_level, admn_lvl_entity=ent_id,
                                           subs_roles=subs_role_ids, default_cost_acct=ta_cost_acct_id)
            assert_that(self.validate_response_code(add_ta_user_resp, 200))
            created_ta_user_id = add_ta_user_resp.json()['userID']
            log.info(f"Invited TA Device user with same SSO user - {email} successfully!")

            time.sleep(wait_time)

            update_ta_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
                user_id=created_ta_user_id, sub_id=sub_id, def_cost_acct_id=ta_cost_acct_id, is_admin=True)
            assert_that(self.validate_response_code(update_ta_user_sub_loc_prop_resp, 200))
            log.info(f'Updated SSO/Federated user default cost account with - {ta_cost_acct_id}, {ta_cost_acct_name}')

            time.sleep(wait_time)

            (ta_user_data, ta_user_loc_id, ta_user_role_id, ta_user_cost_acct_id, ta_uid, ta_user_firstname,
             ta_user_lastname, ta_username, ta_user_access_lvl, ta_user_admin_entities) = (
                resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id[0], email=email,
                                                                   user_type='NON-SSO', is_admin=True))
            ta_user_email = ta_user_data.get('detail').get('profile').get('email')
            ta_user_login_id = ta_user_data.get('detail').get('profile').get('login')

            assert_that(email, equal_to(ta_user_email))
            assert_that(email, equal_to(ta_user_login_id))  # login id will be email for TA device user
            assert_that(ta_cost_acct_id, equal_to(ta_user_cost_acct_id))

            if admin_level != 'User':
                assert_that(admin_level, equal_to(ta_user_access_lvl))
            elif admin_level == 'User':
                assert_that(ta_user_access_lvl, equal_to(None))

        finally:
            # Delete/Archived the created subscription and federated user
            resource['subs_api'].delete_created_subs_users(sub_id=sub_id, query=email)
            resource['fed_subs_api'].delete_federated_and_ta_user(sec_id=sec_id, email=email)
