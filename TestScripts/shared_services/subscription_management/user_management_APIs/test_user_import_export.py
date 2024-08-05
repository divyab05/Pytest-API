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
class TestUserImportExport(common_utils):
    """
    The test class to place all the tests of User Import and Export in the subscription management APIs.
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

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'advance_search_request')) as f2:
            self.advance_search_request = json.load(f2)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_adv_search_exp_resp')) as f3:
            self.sample_adv_search_exp_resp = json.load(f3)

        yield

    @pytest.mark.skip(reason="work in progress")
    @pytest.mark.parametrize('sub_type, is_admin', [('PITNEYSHIP_PRO', True)])
    def test_01_import_users_at_each_access_level(self, resource, sub_type, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)
        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'].get_ent_details_by_sub_id(
            sub_id)

        get_users_by_subs_resp = resource['subscription_api'].get_users_by_subscription_api()
        assert_that(self.validate_response_template(get_users_by_subs_resp, self.sample_adv_search_exp_resp, 200))
