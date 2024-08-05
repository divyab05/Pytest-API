import json
import os

import pytest
from hamcrest import assert_that

from APIObjects.sendtech_apps.device_subscription import Subscription

from FrameworkUtilities.common_utils import common_utils
from conftest import app_config


@pytest.fixture()
def resource(app_config, context,get_env, get_username, get_password,custom_logger):

    subscription = {
        'app_config': app_config,
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield subscription


class TestAccounts(common_utils):

    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_verify_get_user_context(self, resource):
        res = resource['subscription'].get_user_profile()
        self.log.info(f'response json is: {res.json()}')
        assert res.status_code == 200

         # --------Schema Validation------------
        with open(r'./response_schema/cseries_services/get_user_context.json', 'r') as s:
            expected_schema = json.loads(s.read())

        assert_that(self.validate_response_template(res,
                                                    expected_schema, 200))


