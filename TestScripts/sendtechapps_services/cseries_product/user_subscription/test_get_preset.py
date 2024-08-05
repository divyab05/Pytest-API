import pytest


from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from conftest import app_config


@pytest.fixture()
def resource(app_config,context,get_env, get_username, get_password,custom_logger):

    subscription = {
        'app_config': app_config,
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield subscription


class TestAccounts(common_utils) :


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.skip(reason="get_added_preset function need to rewrite")
    def test_verify_getAccounts(self,resource):

        self.log.info("Test Execution Started")
        res=resource['subscription'].get_added_preset()
        assert res.status_code==200

        # -------Schema Validation ---------------
        # with open(r'./response_schema/cseries_services/accounts.json', 'r') as s :
        #     expected_schema=json.loads(s.read())
        #
        # assert_that(self.validate_response_template(res,
        #                                             expected_schema, 200))








