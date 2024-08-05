import inspect
import time

import pytest
import logging
from hamcrest import assert_that, equal_to, is_not
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.jit_service_api import JitProvisioningAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestUpdateSSOUserDetailsViaJIT.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: resource instances.
    """
    resource_instances = {
        'app_config': app_config,
        'subs_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
        'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
        'jit_api': JitProvisioningAPI(app_config),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config)
    }
    yield resource_instances


log = log_utils.custom_logger(logging.INFO)
wait_time = 5

sso_data = [('saml', 'user3'), ('oidc', 'user3')]
# sso_data = [('saml', 'user3')]

# Define a global variable to cache the fixture
sso_user_details_cache = {}


@pytest.fixture(params=sso_data)
def get_sso_user_details(resource, request):
    global sso_user_details_cache

    protocol, sso_user = request.param

    # Check if the fixture is already cached
    # if 'sso_user_details' in sso_user_details_cache:
    #     return sso_user_details_cache['sso_user_details']

    # Check if the fixture is already cached for this protocol and user
    cache_key = f"{protocol}_{sso_user}"
    if cache_key in sso_user_details_cache:
        return sso_user_details_cache[cache_key]

    sub_id, ent_id, ent_name, domain, email, pwd, okta_id = (resource['subs_api']
                                                             .get_sso_user_details_from_sample_file(protocol=protocol,
                                                                                                    user_key=sso_user))

    loc_data = resource['client_mgmt'].get_all_loc_id_name_using_ent_id(ent_id=ent_id)
    role_data = resource['subs_api'].get_all_subs_roles_using_sub_id(sub_id=sub_id)
    cost_acct_data = resource['account_mgmt'].get_all_cost_accounts_using_sub_id(sub_id=sub_id, is_admin=True)
    log.info(f'Prepared get_sso_user_details fixture!')

    sso_user_details = sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data

    # Cache the fixture
    sso_user_details_cache['sso_user_details'] = sso_user_details
    return sso_user_details


@pytest.fixture()
def check_sso_setup_and_user(resource, get_sso_user_details):
    sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details

    # Ensure JIT update is allowed and custom attributes are updated
    fed_mapping_resp = resource['subs_api'].get_federation_mapping_api(ent_name=ent_name)
    assert_that(common_utils.validate_response_code(fed_mapping_resp, 200))
    jit_update = fed_mapping_resp.json()[0]['allowUpdate']

    if not jit_update:
        fed_id = fed_mapping_resp.json()[0]['fedMappingID']
        fed_mapping_update_resp = (resource['subs_api']
                                   .post_update_federation_mapping_api(fed_id=fed_id, sub_id=sub_id, ent_name=ent_name,
                                                                       domain=domain, jit_update=True))
        assert_that(common_utils.validate_response_code(fed_mapping_update_resp, 201))

        after_update_resp = resource['subs_api'].get_federation_mapping_api(ent_name=ent_name)
        assert_that(common_utils.validate_response_code(after_update_resp, 200))
        assert_that(after_update_resp.json()[0]['allowUpdate'], equal_to(True))

    (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
     user_access_lvl, user_admin_entities) = (
        resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))

    log.info(f'Prepared check_sso_setup_and_user fixture!')
    yield (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
           user_access_lvl, user_admin_entities)


@pytest.mark.usefixtures('initialize')
class TestUpdateSSOUserDetailsViaJIT(common_utils):
    """
    The test class to place all the tests of existing SSO users details updated via JIT.
    """

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_01_update_location_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                   check_sso_setup_and_user):

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_loc_id, update_loc_name = (resource['client_mgmt']
                                          .pick_random_loc_id_name(loc_data=loc_data, excluded_loc_ids=user_loc_id))
        log.info(f'Updating existing SSO user location with - {update_loc_id}, {update_loc_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, location=update_loc_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = \
            (resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_loc_id, is_not(equal_to(updtd_user_loc_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_02_update_role_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                               check_sso_setup_and_user):

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_role_id, update_role_name = (
            resource['subs_api'].pick_random_role_id_name(role_data=role_data, excluded_role_ids=user_role_id))
        log.info(f'Updating existing SSO user role with - {update_role_id}, {update_role_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, role=update_role_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_role_id, is_not(equal_to(updtd_user_role_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_03_update_cost_acct_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                    check_sso_setup_and_user):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_cost_acct_id, update_cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data, excluded_acct_ids=user_cost_acct_id))
        log.info(f'Updating existing SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, cost_center=update_cost_acct_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
            user_id=uid, sub_id=sub_id, def_cost_acct_id=update_cost_acct_id, is_admin=True)
        assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
        log.info(f'Updated SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        time.sleep(wait_time)

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_04_update_loc_role_cost_acct_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                             check_sso_setup_and_user):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_loc_id, update_loc_name = (resource['client_mgmt']
                                          .pick_random_loc_id_name(loc_data=loc_data, excluded_loc_ids=user_loc_id))
        log.info(f'Updating existing SSO user location with - {update_loc_id}, {update_loc_name}')

        update_role_id, update_role_name = (
            resource['subs_api'].pick_random_role_id_name(role_data=role_data, excluded_role_ids=user_role_id))
        log.info(f'Updating existing SSO user role with - {update_role_id}, {update_role_name}')

        update_cost_acct_id, update_cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data,
                                                                   excluded_acct_ids=user_cost_acct_id))
        log.info(f'Updating existing SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, location=update_loc_name,
                                                                      role=update_role_name,
                                                                      cost_center=update_cost_acct_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
            user_id=uid, sub_id=sub_id, def_cost_acct_id=update_cost_acct_id, is_admin=True)
        assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
        log.info(f'Updated SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        time.sleep(wait_time)

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_loc_id, is_not(equal_to(updtd_user_loc_id)))
        assert_that(user_role_id, is_not(equal_to(updtd_user_role_id)))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_05_update_loc_and_role_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                       check_sso_setup_and_user):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_loc_id, update_loc_name = (resource['client_mgmt']
                                          .pick_random_loc_id_name(loc_data=loc_data, excluded_loc_ids=user_loc_id))
        log.info(f'Updating existing SSO user location with - {update_loc_id}, {update_loc_name}')

        update_role_id, update_role_name = (
            resource['subs_api'].pick_random_role_id_name(role_data=role_data, excluded_role_ids=user_role_id))
        log.info(f'Updating existing SSO user role with - {update_role_id}, {update_role_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, location=update_loc_name,
                                                                      role=update_role_name, idp=domain,
                                                                      username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_loc_id, is_not(equal_to(updtd_user_loc_id)))
        assert_that(user_role_id, is_not(equal_to(updtd_user_role_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_06_update_role_and_cost_acct_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                             check_sso_setup_and_user):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_role_id, update_role_name = (
            resource['subs_api'].pick_random_role_id_name(role_data=role_data, excluded_role_ids=user_role_id))
        log.info(f'Updating existing SSO user role with - {update_role_id}, {update_role_name}')

        update_cost_acct_id, update_cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data,
                                                                   excluded_acct_ids=user_cost_acct_id))
        log.info(
            f'Updating existing SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, role=update_role_name,
                                                                      cost_center=update_cost_acct_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
            user_id=uid, sub_id=sub_id, def_cost_acct_id=update_cost_acct_id, is_admin=True)
        assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
        log.info(f'Updated SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        time.sleep(wait_time)

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_role_id, is_not(equal_to(updtd_user_role_id)))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    def test_07_update_loc_and_cost_acct_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                            check_sso_setup_and_user):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        update_loc_id, update_loc_name = (resource['client_mgmt']
                                          .pick_random_loc_id_name(loc_data=loc_data, excluded_loc_ids=user_loc_id))
        log.info(f'Updating existing SSO user location with - {update_loc_id}, {update_loc_name}')

        update_cost_acct_id, update_cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data,
                                                                   excluded_acct_ids=user_cost_acct_id))
        log.info(
            f'Updating existing SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, location=update_loc_name,
                                                                      cost_center=update_cost_acct_name,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
            user_id=uid, sub_id=sub_id, def_cost_acct_id=update_cost_acct_id, is_admin=True)
        assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
        log.info(f'Updated SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        time.sleep(wait_time)

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_loc_id, is_not(equal_to(updtd_user_loc_id)))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    @pytest.mark.parametrize('hierarchy_lvl', [0, 1, 2])
    def test_08_update_parent_sub_cost_acct_for_existing_saml_sso_user_via_jit(self, resource, get_sso_user_details,
                                                                               check_sso_setup_and_user, hierarchy_lvl):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        log.info(f'Retrieved sso user details are: \nSub ID: {sub_id}, Ent ID: {ent_id}, Ent name: {ent_name},\n'
                 f'Domain: {domain}, SSO Email: {email}, Pwd: {pwd}')

        log.info(f'SSO user existing with location - {user_loc_id}, role - {user_role_id}, '
                 f'cost account - {user_cost_acct_id}')

        cost_acct_id, cost_acct_name, cost_acct_hierarchy = (
            resource['account_mgmt'].get_cost_account_hierarchy_based_on_level(sub_id=sub_id, hierarchy_lvl=hierarchy_lvl, is_admin=True))

        log.info(f'Updating existing SSO user default cost account with cost account hierarchy - {cost_acct_hierarchy}')

        user_jit_update_resp = (resource['jit_api']
                                .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname,
                                                                      family_name=user_lastname, email=email,
                                                                      user_id=uid, cost_center=cost_acct_hierarchy,
                                                                      idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, user_access_lvl, user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

    @pytest.mark.jit_provisioning_sp360commercial
    @pytest.mark.jit_provisioning_sp360commercial_reg
    @pytest.mark.parametrize('div_count', [1, 3])
    def test_09_update_loc_belonging_to_diff_div_for_existing_saml_sso_user_via_jit(self, resource,
                                                                                    get_sso_user_details,
                                                                                    check_sso_setup_and_user, div_count):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        sub_id, ent_id, ent_name, domain, email, pwd, okta_id, loc_data, role_data, cost_acct_data = get_sso_user_details
        (user_data, user_loc_id, user_role_id, user_cost_acct_id, uid, user_firstname, user_lastname, username,
         user_access_lvl, user_admin_entities) = check_sso_setup_and_user

        updated_divs, update_loc_id, update_loc_name = (
            resource['subs_api']
            .update_user_admin_access_level_to_division(no_of_req_div=div_count, ent_id=ent_id, ent_name=ent_name,
                                                        sub_id=sub_id, email=email, exclude_divs=user_admin_entities))
        log.info(f'Updating existing SSO user location with - {update_loc_id}, {update_loc_name}')

        update_role_id, update_role_name, update_access_lvl = (
            resource['subs_api'].pick_random_role_id_name_with_access_level(role_data=role_data, excluded_role_ids=user_role_id, access_lvl='D'))
        log.info(f'Updating existing SSO user role with - {update_role_id}, {update_role_name}, {update_access_lvl}')

        update_cost_acct_id, update_cost_acct_name = (
            resource['account_mgmt'].pick_random_cost_acct_id_name(cost_acct_data=cost_acct_data, excluded_acct_ids=user_cost_acct_id))
        log.info(f'Updating existing SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        user_jit_update_resp = (
            resource['jit_api']
            .post_update_user_details_via_jit_api(unique_id=email, given_name=user_firstname, family_name=user_lastname,
                                                  email=email, user_id=uid, location=update_loc_name,
                                                  role=update_role_name, cost_center=update_cost_acct_name,
                                                  idp=domain, username=username))
        assert_that(self.validate_response_code(user_jit_update_resp, 200))

        update_user_sub_loc_prop_resp = resource['subs_api'].put_update_user_sub_location_properties_api(
            user_id=uid, sub_id=sub_id, def_cost_acct_id=update_cost_acct_id, is_admin=True)
        assert_that(self.validate_response_code(update_user_sub_loc_prop_resp, 200))
        log.info(f'Updated SSO user default cost account with - {update_cost_acct_id}, {update_cost_acct_name}')

        time.sleep(wait_time)

        (updtd_user_data, updtd_user_loc_id, updtd_user_role_id, updtd_user_cost_acct_id, updtd_uid,
         updtd_user_firstname, updtd_user_lastname, updtd_username, updtd_user_access_lvl, updtd_user_admin_entities) = (
            resource['subs_api'].get_sso_user_specific_details(sub_id=sub_id, ent_id=ent_id, email=email, is_admin=True))

        assert_that(user_loc_id, is_not(equal_to(updtd_user_loc_id)))
        assert_that(user_role_id, is_not(equal_to(updtd_user_role_id)))
        assert_that(user_cost_acct_id, is_not(equal_to(updtd_user_cost_acct_id)))
        assert_that(updtd_user_access_lvl, equal_to(update_access_lvl))

        if div_count == 1:
            assert_that(updated_divs, equal_to(updtd_user_admin_entities))
        else:
            assert any(entity == updtd_user_admin_entities[0] for entity in updated_divs)

        log.info(f'Updated SSO user with location - {updtd_user_loc_id}, role - {updtd_user_role_id}, '
                 f'cost account - {updtd_user_cost_acct_id}')

