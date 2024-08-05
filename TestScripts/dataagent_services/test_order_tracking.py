import pytest
from hamcrest import assert_that

from APIObjects.dataagent_services.Get_Tracking_Payload import Get_Tracking_Payload
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_Tracking_Payload(general_config, app_config, custom_logger)
    yield req


class Test_order_tracking(common_utils):
    @pytest.mark.dataagent
    @pytest.mark.order(39)
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_order_tracking_unauthorized(self, resource, generate_access_token, get_env):
        resp = resource.send_get_tracking_request('invalid_token', generate_access_token.strip(), None,
                                                  get_env)
        assert_that(self.validate_expected_and_actual_response_code(403, resp['response_code']),
                    "Expected Status code 403 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.dataagent
    @pytest.mark.order(40)
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_order_tracking_up(self, resource, generate_access_token, get_env):
        resp = resource.send_get_tracking_request('valid_token', generate_access_token.strip(), None, get_env)
        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

