import pytest
from hamcrest import assert_that

from APIObjects.devicehub_services.Print_DeviceHub import Print_DeviceHub
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Print_DeviceHub(general_config, app_config, custom_logger)
    yield req


class Test_post_print_request(common_utils):

    @pytest.mark.device_hub_sp360
    @pytest.mark.device_hub_spong
    @pytest.mark.order(14)
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("devicehub_services",
                                                                "DeviceHubTestData.xlsx",
                                                                "StampRoll"))
    def test_post_stamp_print_request_2X1_stamps(self, resource, generate_access_token, test_data,
                                                 custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, None, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

        expected_schema = self.read_json_file('Print_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['jobs'][0]['jobStatus'] == "PRINTING"
        assert resp['response_body']['jobs'][0]['fileName'] == ""

    @pytest.mark.dh_printing
    @pytest.mark.device_hub_spong
    @pytest.mark.order(15)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "LabelPrinter4X6"))
    def test_post_label_print_request_4X6_label(self, resource, generate_access_token, test_data,
                                                custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, None, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

        expected_schema = self.read_json_file('Print_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['jobs'][0]['jobStatus'] == "PRINTING"
        assert resp['response_body']['jobs'][0]['fileName'] == ""

    @pytest.mark.dh_printing
    @pytest.mark.order(16)
    @pytest.mark.device_hub_spong
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "LabelPRinter8.5X11"))
    def test_post_label_print_request_8X11_label(self, resource, generate_access_token, test_data,
                                                 custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, None, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

        expected_schema = self.read_json_file('Print_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['jobs'][0]['fileName'] == ""
        assert resp['response_body']['jobs'][0]['jobStatus'] == "PRINTING"

    @pytest.mark.dh_printing
    @pytest.mark.device_hub_spong
    @pytest.mark.order(17)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "SheetPrint"))
    def test_post_label_print_request_Sheet(self, resource, generate_access_token, test_data,
                                            custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, None, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

        expected_schema = self.read_json_file('Print_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['jobs'][0]['fileName'] == ""
        assert resp['response_body']['jobs'][0]['jobStatus'] == "PRINTING"

    @pytest.mark.dh_printing_envelope9
    @pytest.mark.device_hub_spong
    @pytest.mark.order(18)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "Envelope"))
    def test_post_stamp_print_envelope_request(self, resource, generate_access_token, test_data,
                                                custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, None, None, test_data)

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

        expected_schema = self.read_json_file('Print_Response.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['jobs'][0]['fileName'] == ""
        assert resp['response_body']['jobs'][0]['jobStatus'] == "PRINTING"

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_spong
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.order(19)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "StampRoll"))
    def test_post_print_request_with_invalid_path(self, resource, generate_access_token, test_data, custom_logger):
        resp = resource.send_post_print_request("valid", generate_access_token, "invalid_path", None, test_data)

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(
                        arg1=resp['response_code']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    @pytest.mark.device_hub_spong
    @pytest.mark.order(20)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("devicehub_services",
                                                                             "DeviceHubTestData.xlsx",
                                                                             "StampRoll"))
    def test_post_print_request_by_passing_expired_token(self, resource, generate_access_token, test_data,
                                                         custom_logger):
        resp = resource.send_post_print_request("invalid_token", generate_access_token, None, None, test_data)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))