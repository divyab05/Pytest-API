import pytest
import logging
import json

from hamcrest import assert_that

import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.enrich_token_api import EnrichTokenAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.execution_status_utility import ExecutionStatus

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestUserSubscriptionManagementAPI.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: Subscription_API object.
    """
    enrich_api = {
        'app_config': app_config,
        'enrich_api': EnrichTokenAPI(app_config),
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'login_api': LoginAPI(app_config)

    }
    yield enrich_api


@pytest.mark.usefixtures('initialize')
class TestEnrichTokenAPI(common_utils):
    """
    The test class to place all the tests of User subscription management APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestUserSubscriptionManagementAPI.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        exe_status.__init__()
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('ENRICH_API', 'exp_user_properties_resp')) as f2:
            self.sample_user_prop_exp_resp = json.load(f2)

    @pytest.mark.enrichtoken_sp360commercial
    @pytest.mark.enrichtoken_sp360commercial_smoke
    @pytest.mark.enrichtoken_sp360commercial_reg
    @pytest.mark.parametrize('user_type, scope', [('admin', 'pbadm,spa,anx'), ('client', 'adm,spa,anx')])
    def test_01_enrich_token_to_get_user(self, resource, user_type, scope):
        expected_response = 'exp_' + user_type + '_user_resp'
        with open(self.prop.get('ENRICH_API', expected_response)) as f1:
            self.sample_exp_user_resp = json.load(f1)

        email, password, user_id = resource['enrich_api'].get_user_details_from_file(user_type)
        enrich_user_resp = resource['enrich_api'].get_enrich_user_details_by_user_id_api(user_id=user_id, scope=scope)

        assert_that(self.validate_response_template(enrich_user_resp, self.sample_exp_user_resp, 200))

    @pytest.mark.enrichtoken_sp360commercial
    @pytest.mark.enrichtoken_sp360commercial_smoke
    @pytest.mark.enrichtoken_sp360commercial_reg
    @pytest.mark.enrichtoken_fedramp
    @pytest.mark.enrichtoken_fedramp_smoke
    @pytest.mark.enrichtoken_fedramp_reg
    def test_02_enrich_device_token_to_get_user_properties(self, resource):

        token = resource['login_api'].get_device_access_token()

        device_token = 'Bearer ' + token
        self.log.info(f'Device Token: {device_token}')

        get_user_properties_resp = resource['subscription_api'].get_user_properties_api(token=device_token)

        assert_that(self.validate_response_template(get_user_properties_resp, self.sample_user_prop_exp_resp, 200))

