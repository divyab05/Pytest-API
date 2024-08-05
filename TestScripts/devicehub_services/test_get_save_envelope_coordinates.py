import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Get_Envelope_Print_Coordinates import Get_Envelope_Print_Coordinates
from FrameworkUtilities.common_utils import common_utils
from body_jsons.devicehub_services.save_envelope_coordinates import envelope_payload


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_Envelope_Print_Coordinates(general_config, app_config, custom_logger)
    yield req


class Test_get_save_envelope_coordinates(common_utils):

    @pytest.mark.order(6)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_envelope_coordinates_success(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_save_envelope_coordinates("valid_token", generate_access_token,
                                                                     is_peripheral_id_blank=False,
                                                                     is_serial_no_blank=False)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Get_Envelope_Coordinates.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'],
                                                    expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

        assert resp['response_body']['envelope']['ENV9'] == envelope_payload['envelope']['ENV9']
        assert resp['response_body']['envelope']['ENV10'] == envelope_payload['envelope']['ENV10']

    @pytest.mark.order(11)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_envelope_coordinates_blank_sn(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_save_envelope_coordinates("valid_token", generate_access_token,
                                                                     is_peripheral_id_blank=False,
                                                                     is_serial_no_blank=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("GetEnvelopOffset SerialNumber and peripheralId are required fields"))

    @pytest.mark.order(12)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_envelope_coordinates_blank_peripheral_id(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_save_envelope_coordinates("valid_token", generate_access_token,
                                                                     is_peripheral_id_blank=True,
                                                                     is_serial_no_blank=False)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("GetEnvelopOffset SerialNumber and peripheralId are required fields"))

    @pytest.mark.order(13)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_envelope_coordinates_with_blank_query_params(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_save_envelope_coordinates("valid_token", generate_access_token,
                                                                     is_peripheral_id_blank=True,
                                                                     is_serial_no_blank=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("GetEnvelopOffset SerialNumber and peripheralId are required fields"))

    @pytest.mark.order(14)
    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_envelope_coordinates_passing_expired_token(self, resource, generate_access_token, custom_logger):
            resp = resource.send_get_devicehub_save_envelope_coordinates("invalid_token", generate_access_token,
                                                                         is_peripheral_id_blank=False,
                                                                         is_serial_no_blank=False)

            assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                        "Expected Status code 401 is not matched with actual {arg1}".format(arg1=resp['response_code']))

            expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
            res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

            assert_that(res['status'],
                        "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                            arg=res['error_message']))


