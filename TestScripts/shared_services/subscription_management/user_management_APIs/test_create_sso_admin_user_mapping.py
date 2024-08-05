import inspect
import json
import pytest
import logging

from hamcrest import assert_that

from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestSSOAdminUserMapping.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: Subscription_API object.
    """
    subscription_api = {
        'app_config': app_config,
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token)
    }
    yield subscription_api


log = log_utils.custom_logger(logging.INFO)


@pytest.mark.usefixtures('initialize')
class TestSSOAdminUserMapping(common_utils):
    """
    The test class to add the SSO admin user mapping for existing users in the selected environment based on the
    admin user json file data.
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

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_admin_users_data')) as f1:
            self.sample_admin_users_data = json.load(f1)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'user_mapping_failed_records')) as f2:
            self.user_mapping_failed_records = json.load(f2)

        yield

    def test_01_create_sso_admin_user_mappings(self, resource):

        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        domain = "@pb.com"

        # token = "Bearer eyJraWQiOiJYbDJrSVFRe"

        for user in self.sample_admin_users_data:
            if "email" in user['profile'] and domain in user['profile']['login']:
                email = user['profile']['login']
                email = email.lower()
                user_id = f"pb.com_{email}"
                log.info(f"Picked user email: {email}")
                user_data = {
                    'adminLevelAt': user.get('adminLevelAt'),
                    'adminLevelEntity': user.get('adminLevelEntity'),
                    'groupIds': user.get('groupIds'),
                    'analyticsRollupBy': user.get('analyticsRollupBy'),
                    'rollupEntity': user.get('rollupEntity'),
                    'roles': user.get('roles')
                }

                create_sso_admin_mapping_resp = (
                    resource['subscription_api']
                    .create_sso_admin_users_mappings_api(admin_lvl_at=user_data['adminLevelAt'],
                                                         admin_lvl_entity=user_data['adminLevelEntity'],
                                                         group_id=user_data['groupIds'],
                                                         analytics_rollup_by=user_data['analyticsRollupBy'],
                                                         rollup_entity=user_data['rollupEntity'],
                                                         roles=user_data['roles'],
                                                         #admin_token=token,
                                                         user_id=user_id))

                log.info(f"{create_sso_admin_mapping_resp}")
                if create_sso_admin_mapping_resp.status_code == 201:
                    log.info(f"Created SSO Admin User Mapping for: {email}")
                else:
                    log.error(f"Create SSO Admin User Mapping Error! {create_sso_admin_mapping_resp.json()}")

    def test_02_retrieve_email_from_json_file(self, resource):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')
        domain = "@pb.com"
        for user in self.user_mapping_failed_records:
            if user['profile']:
                if domain in user['profile']['email']:
                    email = user['profile']['email']
                    print(email)

    def test_03_create_sso_admin_user_mappings_for_existing_users_with_no_roles(self, resource):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        token = "Bearer eyJraWQiOiI1cEtiTG5fVUtuUm9jdmtxQzBwNW85WDdCclV5djA5LUprYk1rOVoyOWlnIiwiYWxnIjoiUlMyNTYifQ"
        domain = "@pb.com"

        for user in self.user_mapping_failed_records:
            roles = []

            for group_id in user.get('groupIds', []):
                if group_id == '00gfow2omlVXIeHqv1t7':
                    log.warn(f"Client group id found.")
                    roles.append('CLIENT_GROUP_ID')
                if group_id == '00gkmn8prbizSfSig1t7':
                    roles.append('PB_SUPPORT_BASIC')
                elif group_id == '00gfow0xdp0bqlgEO1t7':
                    roles.append('PB_OPERATOR')
                elif group_id == '00gfow6su4gsSvOXZ1t7':
                    admin_level_entity = user.get('adminLevelEntity', [])
                    if admin_level_entity:
                        roles.append('PB_SERVICE')
                    else:
                        roles.append('PB_SERVICE_INSTALLER')

            # if 'CLIENT_GROUP_ID' in roles:
            #     log.warn(f"Client group id is found with this account - {user['profile']['login']} Skipping it!")
            if "email" in user['profile'] and domain in user['profile']['login']:
                email = user['profile']['login']
                user_id = f"pb.com_{email}"
                log.info(f"Picked user email: {email}")

                user_data = {
                    'adminLevelAt': user.get('adminLevelAt'),
                    'adminLevelEntity': user.get('adminLevelEntity'),
                    'groupIds': user.get('groupIds'),
                    'analyticsRollupBy': user.get('analyticsRollupBy'),
                    'rollupEntity': user.get('rollupEntity'),
                    'roles': roles
                }

                create_sso_admin_mapping_resp = (
                    resource['subscription_api']
                    .create_sso_admin_users_mappings_api(admin_lvl_at=user_data['adminLevelAt'],
                                                         admin_lvl_entity=user_data['adminLevelEntity'],
                                                         group_id=user_data['groupIds'],
                                                         analytics_rollup_by=user_data['analyticsRollupBy'],
                                                         rollup_entity=user_data['rollupEntity'],
                                                         roles=user_data['roles'],
                                                         user_id=user_id, admin_token=token))

                log.info(f"{create_sso_admin_mapping_resp}")
                if create_sso_admin_mapping_resp.status_code == 201:
                    log.info(f"Created SSO Admin User Mapping for: {email}")
                else:
                    log.error(f"Create SSO Admin User Mapping Error! {create_sso_admin_mapping_resp.json()}")

    def test_04_prepare_non_sso_admin_user(self, resource):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        users_data = []
        size = 1

        for i in range(size):
            admin_users = resource['subscription_api'].get_admin_user_by_search_query(skip=str(i), limit='100')
            users = admin_users.json().get('users', [])
            for user in users:
                profile = user.get('profile', {})
                email = profile.get('email', '')
                roles = user.get('roles', [])
                if 'LOCKER_VENDOR' not in roles:
                    if email and '@pb.com' not in email:
                        self.log.info(f"Adding {email}")
                        users_data.append(user)

        with open(self.prop.get('COMMON_SHARED_SERVICES', 'prepared_admin_users_list'), 'w') as file:
            json.dump(users_data, file, indent=4)

        self.log.info(f"Found and added users data object: {len(users_data)}")

    def test_05_delete_non_sso_admin_users_from_json_data(self, resource):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        with open(self.prop.get('COMMON_SHARED_SERVICES', 'prepared_admin_users_list')) as file:
            users_data = json.load(file)

        self.log.info(f"Total users available in the json file: {len(users_data)}")

        for user in users_data:
            profile = user.get('profile', {})
            email = profile.get('email', '')
            user_id = user.get('id', '')
            if email and '@pb.com' not in email:
                self.log.info(f"Deleting {email}")
                del_user_resp = resource['subscription_api'].delete_admin_user_api(user_id=user_id)
                assert_that(common_utils.validate_response_code(del_user_resp, 200))
                if del_user_resp.status_code == 200:
                    log.info(f"Deleted admin user with id - {user_id} and email - {email}")

    def test_06_retrieve_existing_non_sso_admin_user_with_pbcom(self, resource):
        log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        users_data = []
        size = 1

        # token = "Bearer eyJraWQiOiJYbDJrSVFRekFJNGs"

        for i in range(size):
            admin_users = resource['subscription_api'].get_admin_user_by_search_query(skip=str(i),
                                                                                      #admin_token=token,
                                                                                      limit='100')
            users = admin_users.json().get('users', [])
            for user in users:
                profile = user.get('profile', {})
                email = profile.get('email', '')
                if email and '@pb.com' in email:
                    self.log.info(f"Adding {email}")
                    users_data.append(user)

        with open(self.prop.get('COMMON_SHARED_SERVICES', 'retrieved_non_sso_admin_users_pbcom_list'), 'w') as file:
            json.dump(users_data, file, indent=4)

        self.log.info(f"Found and added users data object: {len(users_data)}")
