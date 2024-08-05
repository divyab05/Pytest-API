import pytest
from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(app_config,context):
    subscription = {
        'app_config': app_config,
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield subscription


class TestStamps(common_utils):

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_verify_get_subscription_details(self, resource):

        res = resource['subscription'].get_enterprise_subscription_details()
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200

        #  --------Schema Validation------------
        # with open(r'./response_schema/cseries_services/get_accounts.json', 'r') as s:
        #     expected_schema = json.loads(s.read())

        #
        # assert_that(self.validate_response_template(res,
        #                                             expected_schema, 200))


