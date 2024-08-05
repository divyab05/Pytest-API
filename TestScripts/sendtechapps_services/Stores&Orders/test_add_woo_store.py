
import pytest
import logging

from APIObjects.sendtech_apps.device_stores_and_orders import Stores

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config,context):

    store = {
        'app_config': app_config,
        'store': Stores(app_config, context['cseries_okta_token'])

    }
    yield store



class TestAddWooStore(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def get_woocomerce_onboarding_screen(self):
        res = resource['store'].get_woocommerice_onboarding_screen()
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200




    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.skip
    def test_add_woo_store(self,resource):
        res = resource['store'].add_woo_store("cs_5a9d8043b142b8d67e02c94c263186157e79a1fd","https://44.242.163.32","ck_922ca146c83329d6a294642a445fa1fc1eb56d4c")
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200













