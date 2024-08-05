import pytest

from APIObjects.sendtech_apps.device_cost_account import CostAccount
from APIObjects.sendtech_apps.device_verify_address import VerifyAddress
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from FrameworkUtilities.common_utils import common_utils

@pytest.fixture()
def resource(app_config,context):

    costAccount = {
        'app_config': app_config,
        'costAccount': CostAccount(app_config, context['cseries_okta_token'])

    }
    yield costAccount

class TestCostAccount(common_utils):


    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_search_active_costaccount(self, resource, custom_logger):
        resp = resource['costAccount'].searchCostAccount(True)
        assert resp['response_code'] == 200


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_search_inactive_costaccount(self, resource, custom_logger):
        resp = resource['costAccount'].searchCostAccount(False)
        assert resp['response_code'] == 200



