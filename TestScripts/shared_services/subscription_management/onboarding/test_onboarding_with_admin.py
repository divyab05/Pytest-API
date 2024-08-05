import inspect
import pytest
import logging
from hamcrest import assert_that
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.carrier_account_management_api import CarrierAccountManagement
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    data_generator = {
        'app_config': app_config,
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'login_api': LoginAPI(app_config),
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
        'data_generator': DataGenerator(app_config),
        'carrier': CarrierAccountManagement(app_config, generate_access_token)
    }
    yield data_generator


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

    @pytest.mark.spss_data_generator
    @pytest.mark.bulk_user_onboarding
    #@pytest.mark.parametrize('admin_level', ['E', 'D', 'L', 'User'])
    @pytest.mark.parametrize('admin_level', ['E'])
    def test_create_enterprise_with_n_active_subs_users(self, resource, admin_level):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        k = 1
        for i in range(1, k+1):
            # generate enterprise name and Id
            ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

            # "Call add enterprise API and verify the response"
            add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
            assert_that(self.validate_response_code(add_enterprise_res, 201))

            created_ent_id = add_enterprise_res.json()['enterpriseID']

            create_subs_resp = resource['subscription_api'].create_subscription_api(ent_id=created_ent_id)
            assert_that(self.validate_response_code(create_subs_resp, 201))
            sub_id = create_subs_resp.json()['subID']

            # ent_name = 'Ent_Auto_6452'
            # ent_id = 'Ent_Id_6178'
            # sub_id = 'OGJzm5QbZK6'

            div_name = f'{ent_name}_div_name_{i}'
            div_id = f'{ent_id}_div_id_{i}'
            loc_name = f'{ent_name}_loc_name_{i}'
            loc_id = f'{ent_id}_loc_id_{i}'

            # "Call add division API and verify the response"
            add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, sub_id=sub_id, ent_id=ent_id, is_admin=True)
            assert_that(self.validate_response_code(add_div_res, 201))
            created_div_id = add_div_res.json()['divisionID']

            add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                      ent_id=ent_id, sub_id=sub_id, loc_name=loc_name,
                                                                      is_admin=True)
            assert_that(self.validate_response_code(add_loc_res, 201))
            created_loc_id = add_loc_res.json()['locationID']

            division_id = [created_div_id]
            location_id = created_loc_id

            sub_role_id = ['ADMIN']

            if admin_level == 'User':
                sub_role_id = ['USER']

            n = 1
            self.log.info(f'Creating {n} active users in the Ent - {ent_name}, sub_id - {sub_id}')

            for j in range(1, n+1):
                first_name = generate_random_string(uppercase=False, digits=False, char_count=5)
                last_name = generate_random_string(uppercase=False, digits=False, char_count=5)
                disp_name = str(first_name) + str(last_name)
                adm = str(admin_level).lower()
                email = f'{first_name}.{adm}{j}@yopmail.com'
                password = 'Horizon#123'

                resource['subscription_api'] \
                    .create_active_subs_user(sub_id=sub_id, admin_level=admin_level, fname=first_name, lname=last_name,
                                             dispname=disp_name, mailid=email, password=password, ent_name=ent_name,
                                             division_id=division_id, location_id=location_id, ent_id=[ent_id],
                                             subs_role_ids=sub_role_id)
                self.log.info(f'Created {j} active users in the Ent - {ent_name}, sub_id - {sub_id}!!!')

            #resource['carrier'].verify_create_subCarrier_api(subID=sub_id, accountNumber='', gcsPartnerID='')


