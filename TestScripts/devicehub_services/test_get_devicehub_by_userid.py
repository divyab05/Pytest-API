import datetime

import pytest
from hamcrest import assert_that

from APIObjects.devicehub_services.Get_DeviceHub_By_UserID import Get_DeviceHub_By_UserID
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_DeviceHub_By_UserID(general_config, app_config, custom_logger)
    yield req


class Test_get_devicehub_by_userid(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.order(4)
    def test_get_devicehub_by_passing_valid_userId(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_by_userid_request("valid_token", generate_access_token)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Get_DeviceHub_By_Locid.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'][0],
                                                    expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.order(11)
    def test_get_devicehub_by_userid_with_expired_token(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_by_userid_request("invalid_token", generate_access_token)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))
