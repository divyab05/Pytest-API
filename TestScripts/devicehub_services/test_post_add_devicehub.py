import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Post_Add_Devicehub import Post_Add_Devicehub
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Post_Add_Devicehub(general_config, app_config, custom_logger)
    yield req


class Test_post_add_devicehub(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(1)
    def test_post_add_devicehub(self, resource, generate_access_token,
                                custom_logger, context):
        resp = resource.send_add_devicehub_request("valid", generate_access_token, None, context,
                                                   is_sn_blank=False,
                                                   is_duplicate=False)

        assert_that(self.validate_expected_and_actual_response_code(201, resp['response_code']),
                    "Expected Status code 201 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['response'],
                    equal_to("DeviceHub [{arg1}]] added successfully!".format(arg1=context['serial_number'])))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(2)
    def test_post_add_devicehub_duplicate_validation(self, resource, generate_access_token,
                                                     custom_logger, context):
        resp = resource.send_add_devicehub_request("valid", generate_access_token, None, context,
                                                   is_sn_blank=False,
                                                   is_duplicate=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("Invalid Request: Device type [DVH] with Device Serial Number [{arg1}] "
                             "already exists.".format(arg1=context['serial_number'])))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_fedramp
    @pytest.mark.order(12)
    def test_post_add_devicehub_expired_token(self, resource, generate_access_token, custom_logger, context):
        resp = resource.send_add_devicehub_request("invalid_token", generate_access_token, None, context,
                                                   is_sn_blank=False,
                                                   is_duplicate=False)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_fedramp
    @pytest.mark.order(13)
    def test_post_add_devicehub_invalid_path(self, resource, generate_access_token,
                                             custom_logger, context):
        resp = resource.send_add_devicehub_request("valid", generate_access_token, "invalid_path", context,
                                                   is_sn_blank=False,
                                                   is_duplicate=False)
        assert_that(self.validate_expected_and_actual_response_code(405, resp['response_code']),
                    "Expected Status code 405 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_fedramp
    @pytest.mark.order(14)
    def test_post_add_devicehub_with_blank_sn(self, resource, generate_access_token,
                                              custom_logger, context):
        resp = resource.send_add_devicehub_request("valid", generate_access_token, None, context,
                                                   is_sn_blank=True,
                                                   is_duplicate=False)
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("serialNumber - value missing"))
