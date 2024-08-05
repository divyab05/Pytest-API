import pytest
from hamcrest import assert_that

from APIObjects.devicehub_services.Scale_Read import Scale_Read
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Scale_Read(general_config, app_config, custom_logger)
    yield req


class Test_post_scale_read(common_utils):

    @pytest.mark.device_hub_sp360
    @pytest.mark.device_hub_spong
    @pytest.mark.order(10)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "Scale_Test_Data"))
    def test_post_scale_read_request(self, resource, generate_access_token, custom_logger, test_data):
        resp = resource.send_post_scale_request("valid", generate_access_token, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True
        assert self.validate_expected_and_actual_response_code(200, resp['response_body']['statusCode']) is True

        expected_schema = self.read_json_file('Post_Scale_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_spong
    @pytest.mark.order(11)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "Scale_Test_Data"))
    def test_post_scale_read_request_invalid_path(self, resource, generate_access_token, custom_logger, test_data):
        resp = resource.send_post_scale_request("valid", generate_access_token, "invalid_path", test_data)

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(
                        arg1=resp['response_code']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_spong
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(12)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "Scale_Test_Data"))
    def test_post_scale_ready_request_by_passing_expired_token(self, resource, generate_access_token, custom_logger,
                                                               test_data):
        resp = resource.send_post_scale_request("invalid_token", generate_access_token, None, test_data)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
