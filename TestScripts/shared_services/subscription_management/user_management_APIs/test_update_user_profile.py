import inspect
import json
import pytest
import logging
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.ccbs_api import CCBSApi
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config):
    """
    The resource fixture used for the test class - TestUpdateUserProfile.

    :param app_config: The application configuration to get the environment and project name details.
    :returns: Subscription_API object.
    """
    ccbs_api = {
        'app_config': app_config,
        'ccbs_api': CCBSApi(app_config)
    }
    yield ccbs_api


log = log_utils.custom_logger(logging.INFO)


@pytest.mark.usefixtures('initialize')
class TestUpdateUserProfile(common_utils):
    """
    The test class to update the user profile email in the CCBS / Okta side for existing users in the
    selected environment based on the client users json file data.
    """

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestUpdateUserProfile.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('CCBS_USER_DATA', 'sample_subs_users_data')) as f1:
            self.sample_subs_users_data = json.load(f1)

        yield

    @pytest.mark.ccbs_users_reg
    def test_01_update_client_user_profile(self, resource):

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        domain = "@yopmail.net"
        new_domain = "@yopmail.com"

        for user in self.sample_subs_users_data:
            if "email" in user['detail']['profile'] and domain in user['detail']['profile']['login']:
                email = user['detail']['profile']['login']
                user_id = user['detail']['id']
                new_email = resource['ccbs_api'].replace_email_domain(email=email, new_domain=new_domain)
                log.info(f"User's existing email: {email} and updating to {new_email}")

                update_user_email_resp = resource['ccbs_api'].patch_update_user_email_api(email=email, new_email=new_email)
                assert_that(self.validate_response_code(update_user_email_resp, 200))
                updated_email = update_user_email_resp.json()['userInformation']['login']
                assert_that(new_email, equal_to(updated_email))
                log.info(f"Updated email for user - {updated_email}")

                get_user_info_resp = resource['ccbs_api'].get_user_profile_information_using_userid_api(user_id=user_id)
                assert_that(self.validate_response_code(get_user_info_resp, 200))
                username = get_user_info_resp.json()['user']['username']
                user_email = get_user_info_resp.json()['user']['email']

                assert_that(new_email, equal_to(username))
                assert_that(new_email, equal_to(user_email))
                log.info(f"Updated username and email - {username}, {user_email}")
