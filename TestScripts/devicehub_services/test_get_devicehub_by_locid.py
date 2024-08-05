import os
import pytest
from hamcrest import assert_that, equal_to

from APIObjects.devicehub_services.Get_DeviceHub_By_Locid import Get_DeviceHub_By_Locid
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_DeviceHub_By_Locid(general_config, app_config, custom_logger)
    yield req


class Test_get_devicehub_by_locid(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(6)
    def test_get_devicehub_by_passing_loc_id(self, resource, generate_access_token, custom_logger):
        resp = resource.send_devicehub_by_locid_request("valid_token", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Get_DeviceHub_By_Locid.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'][0],
                                                    expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(3)
    def test_get_devicehub_after_adding_new_dh(self, resource, generate_access_token, custom_logger, context):
        resp = resource.send_devicehub_by_locid_request("valid_token", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body'][0]['serialNumber'],
                    equal_to(context['serial_number']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(6)
    def test_get_devicehub_after_saving_envelope_coordinates(self, resource, generate_access_token, custom_logger,
                                                             context):
        resp = resource.send_devicehub_by_locid_request("valid_token", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))
        assert_that(resp['response_body'][0]['printers'][0]['envelope']['ENV_OFF_IN']['top'], equal_to(0))
        assert_that(resp['response_body'][0]['printers'][0]['envelope']['ENV_OFF_IN']['right'], equal_to(0))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(10)
    def test_get_devicehub_by_locid_with_expired_token(self, resource, generate_access_token, custom_logger):
        resp = resource.send_devicehub_by_locid_request("invalid_token", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(11)
    def test_get_devicehub_by_locid_with_invalid_path(self, resource, generate_access_token, custom_logger):
        resp = resource.send_devicehub_by_locid_request("valid_token", generate_access_token, "invalid")

        assert self.validate_expected_and_actual_response_code(404, resp['response_code']) is True
