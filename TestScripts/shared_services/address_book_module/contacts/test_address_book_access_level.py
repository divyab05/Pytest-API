import inspect
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.data_generator import DataGenerator
from FrameworkUtilities.config_utility import ConfigUtility
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
from conftest import generate_access_token, client_token


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'data_generator': DataGenerator(app_config)
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestAddressbookAccessLevel(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.parametrize('user_type, sub_id', [('ent_user', 'subscription'), ('div_user', 'subscription'),
                                                   ('loc_user', 'subscription')])
    def test_01_get_address_search_by_sub_type_using_access_level_users(self, resource, user_type, sub_id):
        """
        This test validates that address can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        paramval = 'sort=name,asc&skip=0&limit=20&search='
        user_name = resource['addressbook_api'].get_user_access_details_from_file(user_type)
        subscription = resource['addressbook_api'].get_user_subscription(sub_id)
        token = resource['login_api'].get_access_token_for_user_credentials(username=user_name, password='Horizon#123')
        get_contact_detail_resp = resource['addressbook_api'].search_address_api(param_val=paramval, client_token=token)
        assert_that(self.validate_response_code(get_contact_detail_resp, 200))
        record_total = len(get_contact_detail_resp.json())
        if record_total == 0:
            pytest.fail("No record found for this user")
        else:
            for i in range(record_total):
                get_contact_type = str(get_contact_detail_resp.json()[i]['type'])
                if get_contact_type == 'S':
                    assert_that(subscription, equal_to(get_contact_detail_resp.json()[i]['subscriptionId']))
                elif get_contact_type == 'U':
                    assert_that(subscription, equal_to(get_contact_detail_resp.json()[i]['subscriptionId']))
                else:
                    pytest.fail("contact is not related to primary location")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.parametrize('user_type, user_division, sub_id', [('div_userD1L1', 'division1', 'div_subscriptionID'),
                                                                  ('div_userD2L2', 'division2', 'div_subscriptionID'),
                                                                  ('ent_userD1L1', 'division1', 'div_subscriptionID'),
                                                                  ('ent_userD2L2', 'division2', 'div_subscriptionID'),
                                                                  ('loc_userD1L1', 'division1', 'div_subscriptionID'),
                                                                  ('loc_userD2L2', 'division2', 'div_subscriptionID')])
    def test_02_get_address_by_contact_id_div_type_using_access_level_users(self, resource, user_type,
                                                                            user_division, sub_id):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        paramval = 'sort=name,desc'
        user_name = resource['addressbook_api'].get_user_access_details_from_file(user_type)
        division = resource['addressbook_api'].get_user_access_division(user_division)
        subscription = resource['addressbook_api'].get_user_subscription(sub_id)
        token = resource['login_api'].get_access_token_for_user_credentials(username=user_name, password='Horizon#123')
        get_contact_detail_resp = resource['addressbook_api'].search_address_api(param_val=paramval, client_token=token)
        assert_that(self.validate_response_code(get_contact_detail_resp, 200))
        record_total = len(get_contact_detail_resp.json())
        if record_total == 0:
            pytest.fail("No record found for this user")
        else:
            for i in range(record_total):
                get_contact_type = str(get_contact_detail_resp.json()[i]['type'])
                if get_contact_type == 'D':
                    assert_that(division, equal_to(get_contact_detail_resp.json()[i]['divisionId']))
                elif get_contact_type == 'U':
                    assert_that(subscription, equal_to(get_contact_detail_resp.json()[i]['subscriptionId']))
                else:
                    pytest.fail("contact is not related to primary location")

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.parametrize('user_type, user_location', [('lsub_entuserD1L1', 'location1'),
                                                          ('lsub_entuserD2L2', 'location2'),
                                                          ('lsub_divuserD1L1', 'location1'),
                                                          ('lsub_divuserD2L2', 'location2'),
                                                          ('lsub_locuserD1L1', 'location1'),
                                                          ('lsub_locuserD2L2', 'location2'),
                                                          ('lsub_userD1L1', 'location1'),
                                                          ('lsub_userD2L2', "location2")])
    def test_03_get_address_by_contact_id_loc_type_using_access_level_users(self, resource, user_type, user_location):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        paramval = 'sort=name,desc'
        user_name = resource['addressbook_api'].get_user_access_details_from_file(user_type)
        location = resource['addressbook_api'].get_user_access_location(user_location)
        token = resource['login_api'].get_access_token_for_user_credentials(username=user_name, password='Horizon#123')
        get_contact_detail_resp = resource['addressbook_api'].search_address_api(param_val=paramval, client_token=token)
        assert_that(self.validate_response_code(get_contact_detail_resp, 200))
        record_total = len(get_contact_detail_resp.json())
        if record_total == 0:
            pytest.fail("No record found for this user")
        else:
            for i in range(record_total):
                get_contact_type = str(get_contact_detail_resp.json()[i]['type'])
                if get_contact_type == 'L':
                    assert_that(location, equal_to(get_contact_detail_resp.json()[i]['locationId']))
                elif get_contact_type == 'U':
                    assert_that(location, equal_to(get_contact_detail_resp.json()[i]['locationId']))
                else:
                    pytest.fail("contact is not related to primary location")
