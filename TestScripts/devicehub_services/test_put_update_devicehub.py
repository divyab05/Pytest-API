import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Put_Update_DeviceHub import Put_update_Devicehub
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Put_update_Devicehub(general_config, app_config, custom_logger)
    yield req


class Test_put_update_devicehub(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(7)
    def test_update_devicehub_by_passing_valid_sn(self, resource, generate_access_token, custom_logger, context):
        sn_no = context['serial_number']
        resp = resource.send_update_devicehub_request("valid_token", generate_access_token, None, sn_no, context)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['response'],
                    equal_to("DeviceHub[{arg1}] updated successfully!".format(arg1=context['serial_number'])))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_spong
    @pytest.mark.order(11)
    def test_update_devicehub_expired_token(self, resource, generate_access_token, custom_logger, context):
        sn_no = context['serial_number']
        resp = resource.send_update_devicehub_request("invalid_token", generate_access_token, None, sn_no, context)

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
    @pytest.mark.device_hub_spong
    @pytest.mark.order(12)
    def test_post_update_devicehub_invalid_path(self, resource, generate_access_token,
                                                custom_logger, context):
        sn_no = context['serial_number']
        resp = resource.send_update_devicehub_request("valid", generate_access_token, "invalid_path", sn_no, context)
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 405 is not match with actual {arg1}".format(arg1=resp['response_code']))
