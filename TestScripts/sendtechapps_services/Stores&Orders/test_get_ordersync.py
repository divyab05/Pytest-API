import json

import pytest
import logging
from hamcrest import assert_that

from APIObjects.sendtech_apps.device_stores_and_orders import Stores
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

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



class TestOrderSync(common_utils):
    log = log_utils.custom_logger(logging.INFO)




    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_get_ordersync(self,resource):
        res = resource['store'].get_order_sync()
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code==200




























