
import pytest
import logging

from APIObjects.sendtech_apps.device_shipping_label import ShippingLabel
from APIObjects.sendtech_apps.device_subscription import Subscription

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, context):
        subscription = {
            'app_config': app_config,
            'subscription': Subscription(app_config, context['cseries_okta_token'])

        }
        yield subscription


class TestAutoRefill(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture
    def getCostAccountDetailsFromCostAccountAPI(self, resource):
        res = resource['subscription'].get_costaccounts()
        # self.log.info(f'customer context response json is: {res.json()}')
        self.costAccountId,self.costAccountName = res.json()['content'][0]['id'], res.json()['content'][0]['name']



    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_get_autorefill(self,resource):
        resp = resource['subscription'].get_autorefill()
        # self.log.info(f'response json is: {resp.json()}')
        assert resp.status_code == 200





    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_usps_autorefill_api(self, resource,custom_logger, getCostAccountDetailsFromCostAccountAPI):
        resp = resource['subscription'].verify_autorefill( self.costAccountId,self.costAccountName,postageAmount=100)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_enable_shipping_transaction_limit(self,resource):
        resp = resource['subscription'].shippingtransactions_limit(10.0)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_disable_shipping_transaction_limit(self, resource):
        resp = resource['subscription'].shippingtransactions_limit(0.0)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_enable_labelOptions_OnPrinting(self,resource):
        requestBody = "{\"alwaysShowLabelOptions\":true}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_disable_labelOptions_OnPrinting(self, resource):
        requestBody = "{\"alwaysShowLabelOptions\":false}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_set_4cross6_defaultLabelType(self, resource):
        requestBody = "{\"printShippingLabelSize\":\"s4*6\"}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_set_8cross11_defaultLabelType(self, resource):
        requestBody = "{\"printShippingLabelSize\":\"s8*11\"}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_set_printReceiptType(self, resource):
        requestBody = "{\"printReceiptShippingLabel\":true}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_set_printReceiptType(self, resource):
        requestBody="{\"printReceiptShippingLabel\":false}"
        resp = resource['subscription'].userPreferencesAPIPatch(requestBody)
        assert resp.status_code == 200

    # @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_verify_emailNotifications_preferences(self):
       pass







