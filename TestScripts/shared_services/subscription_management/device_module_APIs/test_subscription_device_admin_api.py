""" This module contains all test cases."""

import inspect
import json
import pytest
import logging
from hamcrest import assert_that, is_not, equal_to
from APIObjects.shared_services.subscription_api import SubscriptionAPI
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    subscription_api = {'app_config': app_config,
                        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token)}
    yield subscription_api


@pytest.mark.usefixtures('initialize')
class TestSubscriptionDeviceAdminAPI(common_utils):
    """
    The test class to place all the tests of Subscription Management Product/Device Admin APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_device_details_exp_resp')) as f1:
            self.sample_device_details_exp_resp = json.load(f1)

        with open(self.prop.get('SUBSCRIPTION_MGMT', 'sample_single_device_details_exp_resp')) as f2:
            self.sample_single_device_details_exp_resp = json.load(f2)

        yield

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_smoke
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_smoke
    @pytest.mark.subscription_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_01_get_device_details(self, resource, is_admin):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_prop_resp = resource['subscription_api'].get_user_properties_api()
        sub_id = user_prop_resp.json()[0]['subID']

        get_devices_resp = resource['subscription_api'].get_devices_api(sub_id=sub_id, is_admin=is_admin)
        assert_that(self.validate_response_code(get_devices_resp, 200))
        assert_that(self.compare_response_objects(get_devices_resp.json()[0], self.sample_single_device_details_exp_resp))

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.subscription_management_fedramp
    @pytest.mark.subscription_management_fedramp_reg
    def test_02_update_integrator_id_for_existing_device(self, resource):

        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_prop_resp = resource['subscription_api'].get_user_properties_api()
        sub_id = user_prop_resp.json()[0]['subID']

        device_sn, existing_int_id = resource['subscription_api'].get_device_sn_integrator_id()
        self.log.info(f'Selected Device Serial Number: {device_sn} and Integrator ID: {existing_int_id}')

        # Update integrator id for the selected device serial number
        new_int_id = generate_random_string(lowercase=False)
        self.log.info(f'Updating existing integrator ID - {existing_int_id} with new integrator id - {new_int_id}')
        update_int_id_resp = resource['subscription_api']\
            .patch_update_integrator_id_in_product_api(sub_id=sub_id, device_sno=device_sn, int_id=new_int_id)

        assert_that(self.validate_response_code(update_int_id_resp, 200))
        assert_that(existing_int_id, is_not(equal_to(new_int_id)))

        # Verify integrator id is updated successfully or not
        get_devices_after_update_resp = resource['subscription_api'].get_devices_api()
        assert_that(self.validate_response_code(get_devices_after_update_resp, 200))

        nxt_device_sn, updated_int_id = resource['subscription_api'].get_device_sn_integrator_id()
        assert_that(new_int_id, equal_to(updated_int_id))
        self.log.info(f'Updated integrator id - {updated_int_id} for Device Serial Number: {device_sn}')
