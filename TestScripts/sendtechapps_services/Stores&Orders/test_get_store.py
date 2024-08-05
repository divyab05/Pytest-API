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



class TestGetStoreDetails(common_utils):
    log = log_utils.custom_logger(logging.INFO)
    storeKey,subId,subStoreId="","",""


    @pytest.mark.order(2)
    @pytest.mark.skip
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_get_all_store_details(self,resource):
        res = resource['store'].get_store_details()
        self.log.info(f'response json is: {res.json()}')
        if res.status_code == 200:
            TestGetStoreDetails.storeKey=res.json()["subStores"][0]["storeKey"]
            TestGetStoreDetails.subId = res.json()["subStores"][0]["subID"]
            TestGetStoreDetails.subStoreId = res.json()["subStores"][0]["subStoreID"]


    @pytest.mark.order(3)
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.skip
    def test_get_specific_store_details(self, resource):
        print("subid is",TestGetStoreDetails.subId )
        print("store key is ",TestGetStoreDetails.storeKey)
        res = resource['store'].get_specific_store_details(TestGetStoreDetails.storeKey,TestGetStoreDetails.subId)
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200

    @pytest.mark.order(4)
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_get_substore_details(self, resource):
        print("subStoreId is", TestGetStoreDetails.subStoreId)
        res = resource['store'].get_specific_substore_details(TestGetStoreDetails.subStoreId)
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200






















