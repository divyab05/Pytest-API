import pytest

from APIObjects.dataagent_services.Send_Line_Items_Post_Request import Send_Line_Items_Post_Request
from FrameworkUtilities.common_utils import common_utils
from hamcrest import *


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Send_Line_Items_Post_Request(general_config, app_config, custom_logger)
    yield req


class Test_line_items(common_utils):

    @pytest.mark.dataagent
    @pytest.mark.order(37)
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_line_items_unauthorized(self, resource, generate_access_token, get_env):
        resp = resource.Send_Line_Items_Post_Request('invalid_token', generate_access_token.strip(), None,
                                                     get_env)

        assert_that(self.validate_expected_and_actual_response_code(403, resp['response_code']),
                    "Expected Status code 403 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.dataagent
    @pytest.mark.order(38)
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_line_items_up(self, resource, generate_access_token, get_env):
        resp = resource.Send_Line_Items_Post_Request('valid_token', generate_access_token.strip(), None, get_env)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))
