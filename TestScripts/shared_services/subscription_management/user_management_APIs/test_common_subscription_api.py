import inspect
import json
import pytest
import logging
from hamcrest import assert_that
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestUserSubscriptionManagementAPI.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: Subscription_API object.
    """
    subscription_api = {
        'app_config': app_config,
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'product_metadata_api': ProductMetadata(app_config, generate_access_token, client_token),
        'client_management_api': ClientManagementAPI(app_config, generate_access_token, client_token)
    }
    yield subscription_api


@pytest.mark.usefixtures('initialize')
class TestUserSubscriptionManagementAPI(common_utils):
    """
    This test class includes common tests of the user subscription management.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestUserSubscriptionManagementAPI.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_all_users_expected_response_body')) as f1:
            self.sample_get_all_users_exp_resp = json.load(f1)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'advance_search_request')) as f2:
            self.advance_search_request = json.load(f2)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_adv_search_exp_resp')) as f3:
            self.sample_adv_search_exp_resp = json.load(f3)

        yield

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.active_active_ppd
    def test_01_get_users_by_subscription(self, resource):
        """
        This test validates that the get userBySubscription API using the client user token is working correctly.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_users_by_subs_resp = resource['subscription_api'].get_users_by_subscription_api()
        assert_that(self.validate_response_template(get_users_by_subs_resp, self.sample_adv_search_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.active_active_ppd
    @pytest.mark.parametrize('sub_type, is_admin, user_type',
                             [('PITNEYSHIP_PRO', True, 'E'), ('PSP_APP', True, 'E'), ('PSP_APP', False, 'E'),
                              ('PITNEYSHIP', True, 'E'), ('PITNEYSHIP', False, 'E')])
    def test_02_advance_search_and_get_users_api(self, resource, sub_type, is_admin, user_type):
        """
        This test validates that the get users advance search API and get users API using the both admin and client
        user token. In case of client user token, we are first retrieving the client user details of a subscription
        and generating its token and passing this info to the APIs and checking the responses.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)
        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'].get_ent_details_by_sub_id(sub_id)

        if is_admin:
            get_users_from_adv_search = resource['subscription_api'].users_advance_search_api(is_admin=is_admin,
                                                                                              sub_id=sub_id,
                                                                                              ent_id=ent_id[0])
            assert_that(self.validate_response_code(get_users_from_adv_search, 200))
            assert_that(
                self.validate_response_template(get_users_from_adv_search, self.sample_adv_search_exp_resp, 200))

            get_users_resp = resource['subscription_api'].get_users_api(is_admin=is_admin, sub_id=sub_id)
            assert_that(self.validate_response_code(get_users_resp, 200))
            assert_that(self.validate_response_template(get_users_resp, self.sample_adv_search_exp_resp, 200))
        else:
            user_id, email, pwd, user_access_token = resource['subscription_api'] \
                .get_client_user_and_its_access_token_from_ent(sub_id=sub_id, ent_id=ent_id[0], user_type=user_type)

            get_users_from_adv_search = resource['subscription_api']\
                .users_advance_search_api(is_admin=is_admin, sub_id=sub_id, ent_id=ent_id[0],
                                          client_token=user_access_token)

            assert_that(self.validate_response_code(get_users_from_adv_search, 200))
            assert_that(
                self.validate_response_template(get_users_from_adv_search, self.sample_adv_search_exp_resp, 200))

            get_users_resp = resource['subscription_api'].get_users_api(is_admin=is_admin, sub_id=sub_id,
                                                                        token=user_access_token)
            assert_that(self.validate_response_code(get_users_resp, 200))
            assert_that(self.validate_response_template(get_users_resp, self.sample_get_all_users_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.active_active_ppd
    @pytest.mark.parametrize('sub_type, is_admin', [('PITNEYSHIP_PRO', True), ('PSP_APP', True), ('PITNEYSHIP', True)])
    def test_03_update_cost_account_settings_with_admin_user(self, resource, sub_type, is_admin):
        """
        This test validates that the Admin user is able to manage/edit cost account settings.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)
        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'].get_ent_details_by_sub_id(sub_id)

        get_users_from_adv_search = resource['subscription_api']\
            .users_advance_search_api(is_admin=is_admin, sub_id=sub_id, ent_id=ent_id[0])
        assert_that(self.validate_response_code(get_users_from_adv_search, 200))

        cost_account_settings_payload = {
            "costAccountsEnabled": True,
            "costAccountsRequiredForShipments": True,
            "costAccountRequiredForAddShipRequest": True,
            "costAccountRequiredForERR": True,
            "costAccountRequiredForAddingPostage": True,
            "costAccountsRequiredForStamps": True,
            "costAccountRequiredForLocker": False,
            "costAccountRequiredForReceiving": False,
            "costAccountsHierarchyEnabled": False
        }
        update_cost_acct_settings_resp = resource['subscription_api']\
            .put_update_cost_account_settings_in_subs_prop_api(sub_id=sub_id, payload=cost_account_settings_payload,
                                                               is_admin=is_admin)
        assert_that(self.validate_response_code(update_cost_acct_settings_resp, 200))
        cost_account_settings_after_update = update_cost_acct_settings_resp.json()['costAccountSettings']
        assert_that(self.compare_response_objects(cost_account_settings_after_update, cost_account_settings_payload))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    @pytest.mark.parametrize('sub_type, user_type', [('PITNEYSHIP_PRO', 'E'), ('PITNEYSHIP_PRO', 'D'),
                                                     ('PITNEYSHIP_PRO', 'L'), ('PITNEYSHIP_PRO', 'User')])
    def test_04_update_cost_account_settings_with_client_user(self, resource, sub_type, user_type):
        """
        This test validates that the Enterprise user alone is able to manage/edit cost account settings.
        Please note: We have an open issue under discussion - https://pbapps.atlassian.net/browse/SPSS-6328, where
        div or loc or user access level users are also able to edit/manage cost account settings via API. Once this is
        resolved, we can update the test accordingly.

        Did not enable this test for Fedramp as client users password cannot be hardcoded.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)
        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'].get_ent_details_by_sub_id(sub_id)

        get_users_from_adv_search = resource['subscription_api']\
            .users_advance_search_api(is_admin=True, sub_id=sub_id, ent_id=ent_id[0])
        assert_that(self.validate_response_code(get_users_from_adv_search, 200))

        # with pytest.raises(Exception):
        user_id, email, pwd, user_access_token = resource['subscription_api'] \
            .get_client_user_and_its_access_token_from_ent(sub_id=sub_id, ent_id=ent_id[0], user_type=user_type)

        cost_account_settings_payload = {
            "costAccountsEnabled": True,
            "costAccountsRequiredForShipments": True,
            "costAccountRequiredForAddShipRequest": True,
            "costAccountRequiredForERR": True,
            "costAccountRequiredForAddingPostage": True,
            "costAccountsRequiredForStamps": True,
            "costAccountRequiredForLocker": False,
            "costAccountRequiredForReceiving": False,
            "costAccountsHierarchyEnabled": False
        }
        update_cost_acct_settings_resp = resource['subscription_api'] \
            .put_update_cost_account_settings_in_subs_prop_api(sub_id=sub_id, payload=cost_account_settings_payload,
                                                               client_token=user_access_token)
        assert_that(self.validate_response_code(update_cost_acct_settings_resp, 200))
        cost_account_settings_after_update = update_cost_acct_settings_resp.json()['costAccountSettings']
        assert_that(self.compare_response_objects(cost_account_settings_after_update, cost_account_settings_payload))
