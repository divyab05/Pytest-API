import inspect
import json
import pytest
import logging

from hamcrest import assert_that, equal_to, has_length, is_, is_not, contains_string
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


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
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_all_users_expected_response_body')) as f1:
            self.sample_get_all_users_exp_resp = json.load(f1)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_add_user_expected_response_body')) as f2:
            self.sample_add_user_exp_resp = json.load(f2)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_admin_user_by_id_expected_response_body')) as f3a:
            self.sample_get_admin_user_by_id_exp_resp = json.load(f3a)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_by_id_expected_response_body')) as f3b:
            self.sample_get_user_by_id_exp_resp = json.load(f3b)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_account_claim_expected_response_body')) as f4:
            self.sample_account_claim_exp_resp = json.load(f4)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_user_login_expected_response_body')) as f5:
            self.sample_user_login_exp_resp = json.load(f5)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_by_id_response_body')) as f6:
            self.sample_get_user_profile_by_id_exp_resp = json.load(f6)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_invalid_error_resp_body')) as f7:
            self.sample_get_user_profile_invalid_error_exp_resp = json.load(f7)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_claim_response_body')) as f8:
            self.sample_get_user_profile_claim_exp_resp = json.load(f8)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_entity_response_body')) as f9:
            self.sample_get_user_profile_entity_exp_resp = json.load(f9)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_by_user_id_response_body')) as f10:
            self.sample_get_user_profile_by_user_id_exp_resp = json.load(f10)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_error_response_body')) as f11:
            self.sample_get_user_error_exp_resp = json.load(f11)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_properties_response_body')) as f12:
            self.sample_get_user_properties_exp_resp = json.load(f12)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_by_user_id_product_id_response_body')) as f13:
            self.sample_get_user_by_user_id_product_id_exp_resp = json.load(f13)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_admin_user_by_search_query_response_body')) as f14:
            self.sample_get_admin_user_by_search_query_exp_resp = json.load(f14)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_subscription_user_response_body')) as f15:
            self.sample_get_subscription_user_exp_resp = json.load(f15)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_subs_user_by_email_response_body')) as f16:
            self.sample_get_subs_user_by_email_exp_resp = json.load(f16)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_subs_user_by_search_query_response_body')) as f17:
            self.sample_get_subs_user_by_search_query_exp_resp = json.load(f17)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_subscription_ids')) as f18:
            self.sample_subscription_ids = json.load(f18)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_location_missing_error_response')) as f19:
            self.sample_location_missing_err_resp = json.load(f19)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_send_access_request_response_body')) as f20:
            self.sample_send_access_request_resp = json.load(f20)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_all_users_list_exp_response_body')) as f21:
            self.sample_get_all_users_list_exp_resp = json.load(f21)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_user_profile_id_exp_resp_body')) as f22:
            self.sample_get_user_profile_id_exp_resp = json.load(f22)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_enterprises_by_user_exp_response_body')) as f23:
            self.sample_get_enterprises_by_user_exp_resp = json.load(f23)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_admin_user_details_resp')) as f24:
            self.sample_admin_user_details_resp = json.load(f24)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_get_menu_items_resp_body')) as f25:
            self.sample_get_menu_items_resp = json.load(f25)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_subs_prop_exp_resp')) as f26:
            self.sample_subs_prop_exp_resp = json.load(f26)

        yield

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.active_active_ppd
    def test_01_get_users_api(self, resource):
        """
        This test validates that the existing users details are fetched from get_users api successfully and compares
        the actual vs expected response objects.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_all_admin_users_resp = resource['subscription_api'].get_users_api()
        assert_that(self.validate_response_template(get_all_admin_users_resp, self.sample_get_all_users_exp_resp, 200))
        assert_that(self.compare_response_objects(get_all_admin_users_resp.json()['users'][1],
                                                  self.sample_admin_user_details_resp))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_02_get_users_list_api(self, resource):
        """
        This test validates that the existing users details are fetched from get_all_users_list api successfully and
        verifies the api with limit query parameters by comparing the actual vs expected response objects.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        limit = "3"
        default_limit = "10"

        get_all_users_list_with_limit_resp = resource['subscription_api'].get_all_users_list_api(limit)
        assert_that(self.validate_response_template(get_all_users_list_with_limit_resp,
                                                    self.sample_get_all_users_list_exp_resp, 200))
        assert_that(get_all_users_list_with_limit_resp.json()['users'], has_length(int(limit)))

        get_all_users_list_resp = resource['subscription_api'].get_all_users_list_api()
        assert_that(self.validate_response_template(get_all_users_list_resp,
                                                    self.sample_get_all_users_list_exp_resp, 200))
        assert_that(get_all_users_list_resp.json()['users'], has_length(int(default_limit)))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_03_get_admin_user_error_message_when_invalid_user_id(self, resource):
        """
        This test validates the error message when invalid user id is passed in the get_admin_user api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        invalid_user_id = '00uyt65fx39Yt3Y3m0hh'
        error_resp = resource['subscription_api']\
            .set_user_id_in_error_response(user_id=invalid_user_id,
                                           file_path='sample_get_user_profile_invalid_error_resp_body')

        get_user_profile_invalid_resp = resource['subscription_api']\
            .get_admin_user_profile_by_user_id_api(invalid_user_id)
        assert_that(self.validate_response_template(get_user_profile_invalid_resp, error_resp, 404))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_04_get_user_error_message_when_invalid_user_id(self, resource):
        """
        This test validates the error message when invalid user id is passed in the get_user_by_user_id api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        invalid_user_id = '00uyt65fx39Yt3Y3m0hh'
        error_resp = resource['subscription_api']\
            .set_user_id_in_error_response(user_id=invalid_user_id,
                                           file_path='sample_get_user_profile_invalid_error_resp_body')

        get_user_profile_by_invalid_id_resp = resource['subscription_api'].get_user_by_user_id_api(invalid_user_id)
        assert_that(self.validate_response_template(get_user_profile_by_invalid_id_resp, error_resp, 404))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_05_get_admin_users_profile_api(self, resource):
        """
        This test validates admin user profile details are fetched from get_admin_users_profile api for the logged in
        admin user and its generated admin access token.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_admin_users_profile_resp = resource['subscription_api'].get_admin_users_profile_api()
        assert_that(self.validate_response_template(get_admin_users_profile_resp,
                                                    self.sample_get_user_profile_claim_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_06_get_admin_user_profile_by_user_id(self, resource):
        """
        This test validates that admin user profiles are fetched from user id successfully and compare the actual
        response object with the expected response object.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_id = resource['subscription_api'].get_active_admin_user_id()

        if user_id:
            get_user_profile_resp = resource['subscription_api'].get_admin_user_profile_by_user_id_api(user_id)
            assert_that(self.validate_response_template(get_user_profile_resp,
                                                        self.sample_get_user_profile_by_id_exp_resp, 200))
        else:
            pytest.fail("Active admin user not found within the search limit!")

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_07_get_user_profile_by_user_id_api(self, resource):
        """
        This test validates that user profile details are fetched using user_id in the get_user_profile api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_id = resource['subscription_api'].get_active_user_id()

        get_user_profile_by_user_id_resp = resource['subscription_api'].get_user_by_user_id_api(user_id)
        assert_that(self.validate_response_template(get_user_profile_by_user_id_resp,
                                                    self.sample_get_user_profile_id_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_08_get_user_by_email_api(self, resource):
        """
        This test validates that user profile details are fetched using email in the get_user_by_email api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        email = resource['subscription_api'].get_active_user_email()

        get_user_by_email_exp_resp = resource['subscription_api'].get_user_by_email_api(email)
        assert_that(self.validate_response_template(get_user_by_email_exp_resp,
                                                    self.sample_get_user_profile_id_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_09_get_user_error_message_when_invalid_email(self, resource):
        """
        This test validates the error message when invalid email is passed in the get_user_by_email api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        invalid_email = 'invalid_test@com.com'
        get_user_by_invalid_email_resp = resource['subscription_api'].get_user_by_email_api(invalid_email)
        assert_that(self.validate_response_template(get_user_by_invalid_email_resp,
                                                    self.sample_get_user_error_exp_resp, 404))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_10_get_user_properties_api(self, resource):
        """
        This test validates that user properties can be fetched from the get_user_properties api for the logged-in user
        and its generated access token.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_user_properties_resp = resource['subscription_api'].get_user_properties_api()
        assert_that(self.validate_response_template(get_user_properties_resp,
                                                    self.sample_get_user_properties_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_11_get_enterprises_by_user_api(self, resource):
        """
        This test validates that enterprises details can be fetched from get_enterprises_by_user api and the logged-in
        user and its generated access token.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_enterprises_by_user_resp = resource['subscription_api'].get_enterprises_by_user_api()
        assert_that(self.validate_response_template(get_enterprises_by_user_resp,
                                                    self.sample_get_enterprises_by_user_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_12_get_user_admin_entity_api(self, resource):
        """
        This test validates that subscription user's admin entity can be fetched from get_user_admin_entity api and the
        logged-in user and its generated access token.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        get_user_admin_entity_resp = resource['subscription_api'].get_user_admin_entity_api()
        assert_that(self.validate_response_template(get_user_admin_entity_resp,
                                                    self.sample_get_user_profile_entity_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_13_get_user_admin_entity_by_user_id_api(self, resource):
        """
        This test validates that subscription user's admin entity can be fetched using user id in the
        get_user_admin_entity api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_id = resource['subscription_api'].get_active_admin_user_id()

        get_user_admin_entity_by_user_id_resp = resource['subscription_api']\
            .get_user_admin_entity_by_user_id_api(user_id)
        assert_that(self.validate_response_template(get_user_admin_entity_by_user_id_resp,
                                                    self.sample_get_user_profile_entity_exp_resp, 200))

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.active_active_ppd
    def test_14_get_user_sub_location_by_user_id_and_prod_id_api(self, resource):
        """
        This test validates that users sub-location can be fetched using user id and product id in the
        by get_user_sub_location_by_user_id_and_prod_id api.

        :param resource: The resource required for the api requests.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_id, prod_id = resource['subscription_api'].get_active_user_id_product_id_from_properties()

        get_user_sub_location_resp = resource['subscription_api']\
            .get_user_sub_location_by_user_id_and_prod_id_api(user_id, prod_id)
        assert_that(self.validate_response_template(get_user_sub_location_resp,
                                                    self.sample_get_user_by_user_id_product_id_exp_resp, 200))
        assert_that(get_user_sub_location_resp.json()[0]['productID'], equal_to(prod_id))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('admin_type', ['PB_ADMIN', 'PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT',
                                            ['PB_OPERATOR', 'PB_SERVICE'],
                                            ['PB_OPERATOR', 'PB_SUPPORT'],
                                            ['PB_SERVICE', 'PB_SUPPORT'],
                                            ['PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT']])
    @pytest.mark.skip(reason="skipped as token is not received in the response")
    def test_15_add_and_delete_admin_user(self, resource, admin_type):
        """
        This test validates addition of a new admin user and deletion of admin user with different admin roles are
        successful. Also, compares each of the actual response objects to that of the expected response objects.

        :param resource: The resource required for the api requests.
        :param admin_type: The admin roles type test data.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        group_id, group_name, features = resource['product_metadata_api']\
            .get_admin_role_details_by_admin_type(admin_type=admin_type)

        self.log.info("group_id: {arg1}, admin_type: {arg2}".format(arg1=group_id, arg2=admin_type))

        # Add admin user
        fname, lname, mailid, dispname, password, created_user_id, group_id = resource['subscription_api'] \
            .create_active_admin_user(admin_type=admin_type)

        get_admin_user_by_search_query_resp = resource['subscription_api'] \
            .get_admin_user_by_search_query(query=lname)
        assert_that(self.validate_response_template(get_admin_user_by_search_query_resp,
                                                    self.sample_get_admin_user_by_search_query_exp_resp, 200))
        assert_that(get_admin_user_by_search_query_resp.json()['users'][0]['profile']['email'], equal_to(mailid))
        assert_that(get_admin_user_by_search_query_resp.json()['users'][0]['active'], is_(equal_to(True)))

        # Delete admin user
        get_delete_user_resp = resource['subscription_api'].delete_admin_user_api(user_id=created_user_id)
        assert_that(self.validate_response_code(get_delete_user_resp, 200))

        get_user_by_id_after_delete_resp = resource['subscription_api']\
            .get_user_by_user_id_api(user_id=created_user_id, is_admin=True)
        assert_that(get_user_by_id_after_delete_resp.json()['archive'], is_(equal_to(True)))

        resource['login_api'].check_user_login_status(mailid, password, login_success=False, admin=True)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('admin_type', ['PB_ADMIN', 'USER_ADMIN', ['PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT']])
    @pytest.mark.skip(reason="skipped as token is not received in the response")
    def test_16_change_admin_user_status(self, resource, admin_type):
        """
        This test validates addition of a new admin user, update (active to inactive and back to active) and deletion
        of admin user with different admin roles are successful. Also, compares each of the actual response objects
        to that of the expected response objects.

        :param resource: The resource required for the api requests.
        :param admin_type: The admin roles type test data.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        fname, lname, mailid, dispname, password, user_id, group_id = resource['subscription_api'] \
            .create_active_admin_user(admin_type=admin_type)

        # Update - change admin user status
        change_active_status_resp = resource['subscription_api'] \
            .change_active_status_for_admin_user_by_user_id_api(user_id=user_id, active_flag=False,
                                                                groupId=group_id, fname=fname, lname=lname,
                                                                disp_name=dispname, email=mailid)
        assert_that(self.validate_response_code(change_active_status_resp, 200))

        # If admin user is inactive then it is searchable when status=false
        get_admin_user_after_inactive_resp = resource['subscription_api'] \
            .get_admin_user_by_search_query(status='false', query=mailid)
        assert_that(get_admin_user_after_inactive_resp.json()['users'][0]['profile']['email'], equal_to(mailid))

        # Check login fails if the user is inactive
        resource['login_api'].check_user_login_status(mailid, password, login_success=False, admin=True)

        rechange_active_status_resp = resource['subscription_api'] \
            .change_active_status_for_admin_user_by_user_id_api(user_id=user_id, active_flag=True,
                                                                groupId=group_id, fname=fname, lname=lname,
                                                                disp_name=dispname, email=mailid)
        assert_that(self.validate_response_code(rechange_active_status_resp, 200))

        # If admin user is active then it is searchable when status=true
        get_admin_user_after_active_resp = resource['subscription_api'] \
            .get_admin_user_by_search_query(status='true', query=mailid)
        assert_that(get_admin_user_after_active_resp.json()['users'][0]['profile']['email'], equal_to(mailid))

        # Delete/Archive the created admin users
        resource['subscription_api'].delete_created_admin_users(query=fname)

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type, admin_level',
                             [('PITNEYSHIP_PRO', 'E'), ('PITNEYSHIP_PRO', 'D'), ('PITNEYSHIP_PRO', 'L'), ('PITNEYSHIP_PRO', 'User'),
                              ('PSP_APP', 'E'), ('PSP_APP', 'D'), ('PSP_APP', 'L'), ('PSP_APP', 'User'),
                              ('PITNEYSHIP', 'E'), ('PITNEYSHIP', 'D'), ('PITNEYSHIP', 'L'), ('PITNEYSHIP', 'User'),
                              ('PSP_CANADA', 'E'), ('PSP_CANADA', 'D'), ('PSP_CANADA', 'L'), ('PSP_CANADA', 'User'),
                              ('PSP_GLOBAL', 'E'), ('PSP_GLOBAL', 'D'), ('PSP_GLOBAL', 'L'), ('PSP_GLOBAL', 'User')])
    def test_17_add_and_delete_client_user(self, resource, sub_type, admin_level):
        """
        This test validates addition of a new subscription user, update (active to inactive and back to active) and
        deletion of subscription user with different subscription types and admin levels are successful.

        :param resource: The resource required for the api requests.
        :param sub_type: The subscription type test data.
        :param admin_level: The adminLevelAt attribute type test data.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level,
                                                                 del_existing_user=True)

        get_user_search_query_resp = resource['subscription_api'].get_user_by_search_query(query=mailid, sub_id=sub_id)
        assert_that(get_user_search_query_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['status'],
                    equal_to('ACTIVE'), "Subscription user is not active!")

        get_user_by_id_resp = resource['subscription_api'].get_user_by_user_id_api(user_id=user_id, is_admin=True)
        assert_that(self.validate_response_template(get_user_by_id_resp, self.sample_get_user_by_id_exp_resp, 200))

        get_subs_user_by_user_id_resp = resource['subscription_api']\
            .get_subscription_user_by_user_id_api(subId=sub_id, userId=user_id)
        assert_that(self.validate_response_template(get_subs_user_by_user_id_resp,
                                                    self.sample_get_subscription_user_exp_resp, 200))

        get_subs_user_by_email_resp = resource['subscription_api']\
            .get_subscription_user_by_email_api(sub_id=sub_id, email=mailid)
        assert_that(self.validate_response_template(get_subs_user_by_email_resp,
                                                    self.sample_get_subs_user_by_email_exp_resp, 200))
        if admin_level != 'User':
            assert_that(get_subs_user_by_email_resp.json()['usersDetailWithSubLocation'][0]['detail']['adminLevelAt'],
                        equal_to(admin_level), "The get_subs_user_by_email_resp adminLevelAt does not matches with the "
                                               "set admin_level!")
        assert_that(get_subs_user_by_email_resp.json()['usersDetailWithSubLocation'][0]['detail']['active'],
                    is_(equal_to(True)), "Subscription user is not active!")

        # Delete subscription user
        get_delete_user_resp = resource['subscription_api']\
            .delete_user_api(user_id=user_id, sub_id=sub_id, is_admin='y')
        assert_that(self.validate_response_code(get_delete_user_resp, 200))

        resource['login_api'].check_user_login_status(mailid, password, login_success=False)

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type, admin_level', [('PITNEYSHIP_PRO', 'E'), ('PSP_APP', 'E'), ('PITNEYSHIP', 'D'),
                                                       ('PSP_CANADA', 'L'), ('PSP_GLOBAL', 'User')])
    def test_18_change_client_user_status(self, resource, sub_type, admin_level):
        """
        This test validates addition of a new subscription user, update (active to inactive and back to active) and
        deletion of subscription user with different subscription types and admin levels are successful.

        :param resource: The resource required for the api requests.
        :param sub_type: The subscription type test data.
        :param admin_level: The adminLevelAt attribute type test data.
        :returns: The test execution status and results.
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level)

        # Update - change user status
        change_active_status_resp = resource['subscription_api'] \
            .change_active_status_for_subs_user_by_user_id_api(user_id=user_id, active_flag=False,
                                                               sub_id=sub_id, fname=fname, lname=lname,
                                                               disp_name=dispname, email=mailid)
        assert_that(self.validate_response_code(change_active_status_resp, 200))

        # If user is inactive then it is searchable when status=INACTIVE
        get_user_after_inactive_resp = resource['subscription_api'] \
            .get_user_by_search_query(status='INACTIVE', query=mailid, sub_id=sub_id)
        assert_that(get_user_after_inactive_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['email'],
                    equal_to(mailid), "The get_admin_user_after_inactive_resp email does not matches with the set "
                                      "mailid!")
        assert_that(get_user_after_inactive_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['status'],
                    equal_to('INACTIVE'), "Subscription user is active!")

        # Check login fails if the user is inactive
        resource['login_api'].check_user_login_status(mailid, password, login_success=False)

        rechange_active_status_resp = resource['subscription_api'] \
            .change_active_status_for_subs_user_by_user_id_api(user_id=user_id, active_flag=True,
                                                               sub_id=sub_id, fname=fname, lname=lname,
                                                               disp_name=dispname, email=mailid)
        assert_that(self.validate_response_code(rechange_active_status_resp, 200))

        # If user is active then it is searchable when status=ACTIVE
        get_user_after_active_resp = resource['subscription_api'] \
            .get_user_by_search_query(status='ACTIVE', query=mailid, sub_id=sub_id)
        assert_that(get_user_after_active_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['email'],
                    equal_to(mailid), "The get_admin_user_after_inactive_resp email does not matches with the set "
                                      "mailid!")
        assert_that(get_user_after_active_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['status'],
                    equal_to('ACTIVE'), "Subscription user is active!")

        # Delete subscription user
        resource['subscription_api'].delete_created_subs_users(sub_id=sub_id, query=mailid)

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type, admin_level', [('PITNEYSHIP_PRO', 'E'), ('PSP_APP', 'D')])
    def test_19_verify_error_message_when_add_by_user_email_without_location_api(self, resource, sub_type, admin_level):
        """
        This test validates that error is obtained when locationId is not provided while adding new user
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        fname, lname, mailid, dispname, password = resource['subscription_api'].generate_user_profile_data()
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'] \
            .get_ent_details_by_sub_id(sub_id)

        # Add subscription user with empty location
        add_user_by_email_resp = resource['subscription_api'] \
            .add_client_user_by_sub_id_email_api(fname=fname, lname=lname, email=mailid, disp_name=dispname,
                                                 sub_id=sub_id, loc_id='', admin_lvl=admin_level,
                                                 admn_lvl_entity=ent_id, subs_roles=subs_role_ids,
                                                 carriers=carrier_accounts)
        assert_that(self.validate_response_template(add_user_by_email_resp,
                                                    self.sample_location_missing_err_resp, 400))

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type, admin_level', [('PITNEYSHIP_PRO', 'E'), ('PSP_APP', 'D')])
    def test_20_verify_error_message_when_add_by_user_email_with_blank_location_api(self, resource, sub_type, admin_level):
        """
        This test validates that error is obtained when blank locationId is provided while adding new user
        """

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        fname, lname, mailid, dispname, password = resource['subscription_api'].generate_user_profile_data()
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        ent_id, loc_id, carrier_accounts, subs_role_ids = resource['subscription_api'] \
            .get_ent_details_by_sub_id(sub_id)

        # Add subscription user with spaces value in location
        add_user_by_email_resp = resource['subscription_api'] \
            .add_client_user_by_sub_id_email_api(fname=fname, lname=lname, email=mailid, disp_name=dispname,
                                                 sub_id=sub_id, loc_id=' ', admin_lvl=admin_level,
                                                 admn_lvl_entity=ent_id, subs_roles=subs_role_ids,
                                                 carriers=carrier_accounts)
        assert_that(self.validate_response_template(add_user_by_email_resp,
                                                    self.sample_location_missing_err_resp, 400))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.parametrize('sub_type, admin_level', [('PITNEYSHIP_PRO', 'E'),
                                                       ('PITNEYSHIP_PRO', 'D'),
                                                       ('PITNEYSHIP_PRO', 'L'),
                                                       ('PITNEYSHIP_PRO', 'User'),
                                                       ('PSP_APP', 'D')])
    def test_21_update_location_for_subscription_users(self, resource, sub_type, admin_level):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level)

        get_user_details_resp = resource['subscription_api'].get_user_subscription_details_by_user_id_api(user_id)
        current_loc_id = get_user_details_resp.json()[0]['locationID']

        get_enterprise_resp = resource['client_management_api'].get_enterprise_by_ent_id_api(ent_id[0])
        ent_name = get_enterprise_resp.json()['name']

        new_loc_id = resource['subscription_api'].retrieve_new_location_from_enterprise(current_loc_id, ent_id, sub_id)
        assert_that(current_loc_id, is_not(equal_to(new_loc_id)))

        resource['subscription_api']\
            .put_update_subs_user_details_by_user_id_api(user_id=user_id, fname=fname, lname=lname, email=mailid,
                                                         disp_name=dispname, sub_id=sub_id, loc_id=new_loc_id,
                                                         admin_lvl=admin_level, admn_lvl_entity=ent_id,
                                                         ent_name=ent_name,  subs_roles=subs_role_ids)

        get_user_after_update_resp = resource['subscription_api'].get_user_subscription_details_by_user_id_api(user_id)
        updated_loc_id = get_user_after_update_resp.json()[0]['locationID']

        assert_that(current_loc_id, is_not(equal_to(updated_loc_id)))

        # Delete/Archived the created subscription users
        resource['subscription_api'].delete_created_subs_users(sub_id=sub_id, query=mailid)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type', ['PITNEYSHIP_PRO', 'PSP_APP', 'PITNEYSHIP', 'PSP_CANADA'])
    def test_22_verify_update_subs_role_details_for_subs(self, resource, sub_type):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        role_id, role_name, features = resource['subscription_api'].get_non_default_subs_roles_details(sub_id=sub_id)
        set_role_name = 'SPSS test role'

        self.log.info(f'Role ID: {role_id[0]}, Role Name: {role_name[0]}, Features: {features[0]}')

        update_subs_roles_resp = resource['subscription_api']\
            .update_subscription_role_api(sub_id=sub_id, role_id=role_id[0], role_name=set_role_name)

        # PITNEYSHIP subscription roles features will be empty and roles are derived from subscription plans,
        # And it will throw 400 Bad request when updating its subscription roles
        if sub_type == 'PITNEYSHIP':
            assert_that(self.validate_response_code(update_subs_roles_resp, 400))
        else:
            assert_that(self.validate_response_code(update_subs_roles_resp, 200))

            updated_role_id, updated_role_name, updated_features = resource['subscription_api']\
                .get_non_default_subs_roles_details(sub_id=sub_id)

            self.log.info(f'Updated Role ID: {updated_role_id[0]}, Updated Role Name: {updated_role_name[0]}, '
                          f'Updated Features: {updated_features[0]}')

            assert_that(updated_role_id[0], is_(equal_to(role_id[0])))
            assert_that(updated_role_name[0], is_(equal_to(set_role_name)))

            # Resetting the subscription roles to their actual value
            reupdate_subs_roles_resp = resource['subscription_api'] \
                .update_subscription_role_api(sub_id=sub_id, role_id=role_id[0], role_name=role_name[0])

            assert_that(self.validate_response_code(reupdate_subs_roles_resp, 200))

            reupdated_role_id, reupdated_role_name, reupdated_features = resource['subscription_api']\
                .get_non_default_subs_roles_details(sub_id=sub_id)

            self.log.info(f'Re-updated Role ID: {reupdated_role_id[0]}, Re-updated Role Name: {reupdated_role_name[0]},'
                          f'Re-updated Features: {reupdated_features[0]}')

            assert_that(reupdated_role_id[0], is_(equal_to(role_id[0])))
            assert_that(reupdated_role_name[0], is_(equal_to(role_name[0])))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="need to check why it is failing in CICD")
    @pytest.mark.parametrize('sub_type, admin_level, change_admin_lvl', [('PITNEYSHIP_PRO', 'E', ['D', 'L', 'User']),
                                                                         ('PSP_APP', 'D', ['E', 'L', 'User'])])
    def test_23_update_admin_level_access_for_subscription_users(self, resource, sub_type, admin_level, change_admin_lvl):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level)

        user_id, admin_level_at, admin_level_entity, location_id, ent_name, subs_roles = \
            resource['subscription_api'].get_users_detail_with_sub_location(sub_id=sub_id, email=mailid,
                                                                            admin_level=admin_level, ent_id=ent_id)

        for i in range(len(change_admin_lvl)):
            update_user_details_resp = resource['subscription_api'] \
                .put_update_subs_user_details_by_user_id_api(user_id=user_id, fname=fname, lname=lname,
                                                             disp_name=dispname, sub_id=sub_id, loc_id=location_id,
                                                             admin_lvl=change_admin_lvl[i],
                                                             admn_lvl_entity=admin_level_entity,
                                                             ent_name=ent_name, subs_roles=subs_roles)
            assert_that(self.validate_response_code(update_user_details_resp, 200))

            updated_user_id, updated_admin_level_at, updated_admin_level_entity, updated_location_id, \
                updated_ent_name, updated_subs_roles_name = resource['subscription_api']\
                .get_users_detail_with_sub_location(sub_id=sub_id, email=mailid, ent_id=ent_id)

            assert_that(updated_admin_level_at, is_(equal_to(change_admin_lvl[i])))
            assert_that(updated_admin_level_at, is_not(equal_to(admin_level_at)))

        # Delete/Archived the created subscription users
        resource['subscription_api'].delete_created_subs_users(sub_id=sub_id, query=mailid)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type, admin_level', [('PITNEYSHIP_PRO', 'E'), ('PSP_APP', 'D')])
    def test_24_search_with_subscription_users_details(self, resource, sub_type, admin_level):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
            resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level)

        user_id, admin_level_at, admin_level_entity, location_id, ent_name, subs_roles = \
            resource['subscription_api'].get_users_detail_with_sub_location(sub_id=sub_id, email=mailid,
                                                                            admin_level=admin_level, ent_id=ent_id)

        # Search with first name
        fname_resp = resource['subscription_api'].get_user_by_search_query(query=fname, sub_id=sub_id)
        assert_that(fname_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['userID'],
                    equal_to(user_id))
        assert_that(fname_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['firstName'],
                    equal_to(fname))

        # Search with last name
        lname_resp = resource['subscription_api'].get_user_by_search_query(query=lname, sub_id=sub_id)
        assert_that(lname_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['userID'],
                    equal_to(user_id))
        assert_that(lname_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['lastName'],
                    equal_to(lname))

        # Search with disp name
        dispname_resp = resource['subscription_api'].get_user_by_search_query(query=dispname, sub_id=sub_id)
        assert_that(dispname_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['userID'],
                    equal_to(user_id))
        assert_that(dispname_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['displayName'],
                    equal_to(dispname))

        # Search with partial disp name
        partial_dispname = dispname[8:20]
        partial_dispname_resp = resource['subscription_api'] \
            .get_user_by_search_query(skip='0', limit='5', archive='false', query=partial_dispname, sub_id=sub_id)
        assert_that(partial_dispname_resp.json()['usersDetailWithSubLocation'][0]['subLocation']['userID'],
                    equal_to(user_id))
        assert_that(partial_dispname_resp.json()['usersDetailWithSubLocation'][0]['detail']['profile']['displayName'],
                    equal_to(dispname))

        # Delete/Archived the created subscription users
        resource['subscription_api'].delete_created_subs_users(sub_id=sub_id, query=mailid)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    @pytest.mark.skip(reason="skipped to due to sso on admin")
    @pytest.mark.parametrize('admin_type', ['PB_OPERATOR', 'PB_SERVICE', 'PB_SUPPORT'])
    def test_25_search_with_admin_users_details(self, resource, admin_type):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        fname, lname, mailid, dispname, password, user_id, group_id = resource['subscription_api']\
            .create_active_admin_user(admin_type=admin_type)

        # Search with first name
        fname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=fname)
        assert_that(fname_resp.json()['users'][0]['id'], equal_to(user_id))
        assert_that(fname_resp.json()['users'][0]['profile']['firstName'], equal_to(fname))

        # Search with last name
        lname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=lname)
        assert_that(lname_resp.json()['users'][0]['id'], equal_to(user_id))
        assert_that(lname_resp.json()['users'][0]['profile']['lastName'], equal_to(lname))

        # Search with disp name
        dispname_resp = resource['subscription_api'].get_admin_user_by_search_query(query=dispname)
        assert_that(dispname_resp.json()['users'][0]['id'], equal_to(user_id))
        assert_that(dispname_resp.json()['users'][0]['profile']['displayName'], equal_to(dispname))

        # Search with partial disp name
        partial_dispname = dispname[8:20]
        partial_dispname_resp = resource['subscription_api']\
            .get_admin_user_by_search_query(query=partial_dispname)
        assert_that(partial_dispname_resp.json()['users'][0]['id'], equal_to(user_id))
        assert_that(partial_dispname_resp.json()['users'][0]['profile']['displayName'], equal_to(dispname))

        # Delete/Archive the created admin users
        resource['subscription_api'].delete_created_admin_users(query='PyAuto')

    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="TO DO: Add IDP API to create user in okta only")
    def test_26_send_and_grant_access_request_for_admin_support_user(self, resource):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        # fname, lname, mailid, dispname, password, user_id = resource['subscription_api'] \
        #     .create_active_admin_user(admin_type='PB_SUPPORT')
        # TO DO: Create IDP user
        user_id=''
        mailid=''
        admin_level_at, group_ids = resource['subscription_api'].get_admin_user_details(user_id=user_id)

        send_access_request_resp = resource['subscription_api'].post_send_access_request(user_id=user_id, email=mailid)

        assert_that(self.validate_response_template(send_access_request_resp,
                                                    self.sample_send_access_request_resp, 201))

        status, comments = resource['subscription_api'].check_all_access_requests(user_id=user_id)
        assert_that(status, contains_string('Request Submitted'))

        grant_access_resp = resource['subscription_api'].post_grant_access_api(user_id=user_id, email=mailid)
        self.log.info("grant_access_resp: " + json.dumps(grant_access_resp.json()), grant_access_resp.status_code)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type', ['PITNEYSHIP_PRO'])
    def test_27_update_user_properties_by_subscription_owner_user(self, resource, sub_type):
        """
        This test validates that the user properties is updated by subscription owner user and client user tokens.

        :param resource: The resource required for the api requests.
        :param sub_type: Based on the subscription plan type, sub_id will be retrieved.
        :returns: The test execution status and results.
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        subs_details_resp = resource['subscription_api'].get_subscription_details_by_sub_id_api(sub_id=sub_id)
        assert_that(self.validate_response_code(subs_details_resp, 200))
        subs_owner = subs_details_resp.json()['primaryOwner']
        self.log.info(f'Subscription Owner is {subs_owner} for the subs ID: {sub_id}')

        token = resource['login_api'].get_access_token_for_user_credentials(username=subs_owner, password='Horizon#123')
        get_user_prop_resp = resource['subscription_api'].get_user_properties_api(token=token)
        assert_that(self.validate_response_template(get_user_prop_resp, self.sample_get_user_properties_exp_resp, 200))
        email_subject_tracking = get_user_prop_resp.json()[0]['properties']['emailSubjectForTrackingNumber']
        user_id = get_user_prop_resp.json()[0]['userID']

        update_email_subject = generate_random_string(char_count=40)

        update_user_prop_resp = resource['subscription_api']\
            .put_update_user_properties_for_user_id_sub_id_api(user_id=user_id, sub_id=sub_id, token=token,
                                                               emailSubjectForTrackingNumber=update_email_subject)
        assert_that(self.validate_response_code(update_user_prop_resp, 200))

        get_user_prop_after_update_resp = resource['subscription_api'].get_user_properties_api(token=token)
        assert_that(self.validate_response_code(get_user_prop_after_update_resp, 200))
        updated_email_subject_tracking = get_user_prop_after_update_resp.json()[0]['properties']['emailSubjectForTrackingNumber']
        assert_that(update_email_subject, equal_to(updated_email_subject_tracking))
        assert_that(email_subject_tracking, is_not(equal_to(updated_email_subject_tracking)))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.parametrize('sub_type', ['PITNEYSHIP_PRO'])
    def test_28_update_subs_properties_by_subscription_owner_user(self, resource, sub_type):
        """
        This test validates that the user properties is updated by subscription owner user and client user tokens.

        :param resource: The resource required for the api requests.
        :param sub_type: Based on the subscription plan type, sub_id will be retrieved.
        :returns: The test execution status and results.
        """
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        sub_id = resource['subscription_api'].get_sub_id_from_file(sub_type)

        subs_details_resp = resource['subscription_api'].get_subscription_details_by_sub_id_api(sub_id=sub_id)
        assert_that(self.validate_response_code(subs_details_resp, 200))
        subs_owner = subs_details_resp.json()['primaryOwner']
        self.log.info(f'Subscription Owner is {subs_owner} for the subs ID: {sub_id}')

        token = resource['login_api'].get_access_token_for_user_credentials(username=subs_owner, password='Horizon#123')
        get_subs_prop_resp = resource['subscription_api'].get_subscription_properties_api(token=token, sub_id=sub_id)
        assert_that(self.validate_response_template(get_subs_prop_resp, self.sample_subs_prop_exp_resp, 200))

        okta_group_id = get_subs_prop_resp.json()['oktaGroupID']
        cost_acct_status = get_subs_prop_resp.json()['costAccountsEnabled']

        if cost_acct_status:  # when it is True, updating it to False
            update_subs_prop_resp = resource['subscription_api'] \
                .put_update_subs_properties_for_user_id_sub_id_api(sub_id=sub_id, client_token=token, oktaGroupID=okta_group_id,
                                                                   costAccountsEnabled=False)
            assert_that(self.validate_response_code(update_subs_prop_resp, 200))
        else:  # when it is False, updating it to True
            update_subs_prop_resp = resource['subscription_api'] \
                .put_update_subs_properties_for_user_id_sub_id_api(sub_id=sub_id, client_token=token, oktaGroupID=okta_group_id,
                                                                   costAccountsEnabled=True)
            assert_that(self.validate_response_code(update_subs_prop_resp, 200))

        get_subs_prop_after_update_resp = resource['subscription_api'].get_subscription_properties_api(token=token, sub_id=sub_id)
        assert_that(self.validate_response_code(get_subs_prop_after_update_resp, 200))
        updated_cost_acct_status = get_subs_prop_after_update_resp.json()['costAccountsEnabled']
        assert_that(cost_acct_status, is_not(equal_to(updated_cost_acct_status)))

        # Resetting back with original value
        reset_subs_prop_resp = resource['subscription_api'] \
            .put_update_subs_properties_for_user_id_sub_id_api(sub_id=sub_id, client_token=token, oktaGroupID=okta_group_id,
                                                               costAccountsEnabled=cost_acct_status)
        assert_that(self.validate_response_code(reset_subs_prop_resp, 200))

