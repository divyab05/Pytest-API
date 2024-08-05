import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Save_Envelope_Print_Coordinate import Save_Envelope_Print_Coordinate
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Save_Envelope_Print_Coordinate(general_config, app_config, custom_logger)
    yield req


class Test_save_envelope_coordinates(common_utils):

    @pytest.mark.order(5)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinates_success(self, resource, generate_access_token,
                                               custom_logger, context):
        resp = resource.post_save_coordinates("valid", generate_access_token, None, context, is_sn_blank=False,
                                              is_peripheral_id=False)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['response'],
                    equal_to('Envelop offset is save successfully!'))

    @pytest.mark.order(19)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinate_with_blank_sn(self, resource, generate_access_token,
                                                    custom_logger, context):
        resp = resource.post_save_coordinates("valid", generate_access_token, None, context, is_sn_blank=True,
                                              is_peripheral_id=False)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("serialNumber - value missing"))

    @pytest.mark.order(20)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinate_with_blank_peripheral_id(self, resource, generate_access_token,
                                                               custom_logger, context):
        resp = resource.post_save_coordinates("valid", generate_access_token, None, context, is_sn_blank=False,
                                              is_peripheral_id=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("serialNumber - value missing"))
        assert_that(resp['response_body']['errors'][1]['errorDescription'],
                    equal_to("peripheralId - value missing"))

    @pytest.mark.order(23)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinate_with_blank_sn_and_peripheral(self, resource, generate_access_token,
                                                                   custom_logger, context):
        resp = resource.post_save_coordinates("valid", generate_access_token, None, context, is_sn_blank=True,
                                              is_peripheral_id=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("serialNumber - value missing"))
        assert_that(resp['response_body']['errors'][1]['errorDescription'],
                    equal_to("peripheralId - value missing"))

    @pytest.mark.order(24)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinates_with_invalid_path(self, resource, generate_access_token,
                                                         custom_logger, context):
        resp = resource.post_save_coordinates("valid", generate_access_token, "invalid_path", context,
                                              is_sn_blank=False,
                                              is_peripheral_id=False)
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.order(25)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_save_envelope_coordinates_with_expired_token(self, resource, generate_access_token, custom_logger,
                                                          context):
        resp = resource.post_save_coordinates("invalid_token", generate_access_token, None, context,
                                              is_sn_blank=False,
                                              is_peripheral_id=False)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
