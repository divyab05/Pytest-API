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

admin_type_data = ['PB_ADMIN', 'PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT', ['PB_OPERATOR', 'PB_SERVICE'],
                   ['PB_OPERATOR', 'PB_SUPPORT'], ['PB_SERVICE', 'PB_SUPPORT'],
                   ['PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT']]


@pytest.fixture(params=admin_type_data)
def create_invited_admin_user(resource, request):
    admin_type = request.param

    group_id, group_name, features = (resource['product_metadata_api']
                                      .get_admin_role_details_by_admin_type(admin_type=admin_type))

    # Add invited admin user
    fname, lname, mailid, dispname, password, created_user_id, group_id = resource['subscription_api'] \
        .create_invited_admin_user(admin_type=admin_type, group_id=group_id)

    yield group_id, group_name, features, fname, lname, mailid, dispname, password, created_user_id

    log.info(f"Created invited admin user :: Email: {mailid}, UserId: {created_user_id}, AdminType: {admin_type}")

    # Delete created admin users after test execution
    get_delete_user_resp = resource['subscription_api'].delete_admin_user_api(user_id=created_user_id)
    assert_that(common_utils.validate_response_code(get_delete_user_resp, 200))
    if get_delete_user_resp.status_code == 200:
        log.info(f"Deleted invited admin user with id - {created_user_id} and email - {mailid}")


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

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_admin_user_by_search_query_response_body')) as f1:
            self.sample_get_admin_user_by_search_query_exp_resp = json.load(f1)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_invited_admin_user_response_body')) as f2:
            self.sample_get_invited_admin_user_exp_resp = json.load(f2)

        yield

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.active_active_ppd
    @pytest.mark.skip(reason="need to fix for fedramp, not required for commercial")
    def test_01_add_search_invited_admin_user(self, resource, create_invited_admin_user):
        """
        This test validates addition of a new invited admin user and deletion of admin user with different admin roles
        are successful. Also, compares each of the actual response objects to that of the expected response objects.

        :param resource: The resource required for the api requests.
        :param create_invited_admin_user: The created invited admin user serves as parameterized test data.
        :returns: The test execution status and results.
        """

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        (group_id, group_name, features, fname, lname, mailid, dispname, password,
         created_user_id) = create_invited_admin_user

        get_admin_user_by_email_resp = resource['subscription_api'].get_admin_users_by_email_api(email=mailid)
        assert_that(self.validate_response_template(
            get_admin_user_by_email_resp, self.sample_get_invited_admin_user_exp_resp, 200))
        assert_that(get_admin_user_by_email_resp.json()['profile']['email'], equal_to(mailid))
        assert_that(get_admin_user_by_email_resp.json()['active'], is_(equal_to(True)))

        # Search with first name
        fname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=fname)
        assert_that(self.validate_response_template(
            fname_resp, self.sample_get_admin_user_by_search_query_exp_resp, 200))
        assert_that(fname_resp.json()['users'][0]['id'], equal_to(created_user_id))
        assert_that(fname_resp.json()['users'][0]['profile']['firstName'], equal_to(fname))

        # Search with last name
        lname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=lname)
        assert_that(self.validate_response_template(
            lname_resp, self.sample_get_admin_user_by_search_query_exp_resp, 200))
        assert_that(lname_resp.json()['users'][0]['id'], equal_to(created_user_id))
        assert_that(lname_resp.json()['users'][0]['profile']['lastName'], equal_to(lname))

        # Search with disp name
        dispname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=dispname)
        assert_that(self.validate_response_template(
            dispname_resp, self.sample_get_admin_user_by_search_query_exp_resp, 200))
        assert_that(dispname_resp.json()['users'][0]['id'], equal_to(created_user_id))
        assert_that(dispname_resp.json()['users'][0]['profile']['displayName'], equal_to(dispname))

        # Search with partial disp name
        partial_dispname = dispname[8:20]
        partial_dispname_resp = resource['subscription_api'] \
            .get_admin_user_by_search_query(query=partial_dispname)
        assert_that(self.validate_response_template(
            partial_dispname_resp, self.sample_get_admin_user_by_search_query_exp_resp, 200))
        assert_that(partial_dispname_resp.json()['users'][0]['id'], equal_to(created_user_id))
        assert_that(partial_dispname_resp.json()['users'][0]['profile']['displayName'], equal_to(dispname))
