import inspect
import json
import pytest
import logging
from hamcrest import assert_that, equal_to, is_
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


log = log_utils.custom_logger(logging.INFO)


@pytest.mark.usefixtures('initialize')
class TestInvitedAdminUsersAPI(common_utils):
    """
    The test class to place all the tests of User subscription management APIs.
    """

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

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_active_sso_admin_user_response_body')) as f1:
            self.sample_get_active_sso_admin_user_exp_resp = json.load(f1)

        yield

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    def test_01_search_active_sso_admin_user_using_non_sso_admin_user(self, resource):
        """
        This test validates search of an existing active SSO admin user when logged-in or searched with
        a Non-SSO admin user token.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sso_email = 'sohail.mohammed@pb.com'

        get_admin_user_by_email_resp = (resource['subscription_api']
                                        .get_admin_users_by_email_api(email=sso_email, user_type='SSO'))
        assert_that(self.validate_response_template(
            get_admin_user_by_email_resp, self.sample_get_active_sso_admin_user_exp_resp, 200))
        assert_that(get_admin_user_by_email_resp.json()['profile']['email'], equal_to(sso_email))
        assert_that(get_admin_user_by_email_resp.json()['id'], equal_to(f"pb.com_{sso_email}"))
        assert_that(get_admin_user_by_email_resp.json()['externalID'], equal_to(f"pb.com_{sso_email}"))
        assert_that(get_admin_user_by_email_resp.json()['active'], is_(equal_to(True)))



