
import pytest
from APIObjects.sendtech_apps.device_stores_and_orders import Stores
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(app_config, context):

    store = {
        'app_config': app_config,
        'store': Stores(app_config, context['cseries_okta_token'])

    }
    yield store


class TestShipRequest(common_utils):

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_verify_get_ship_request(self, resource):
        res = resource['store'].get_shiprequest()
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200






