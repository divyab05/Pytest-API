import pytest
from hamcrest import assert_that, equal_to, is_not
from APIObjects.devicehub_services.Post_HBC_Printer_Mapping import Post_HBC_Printer_Mapping
from APIObjects.devicehub_services.generate_hbc_token import generate_hbc_token
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(app_config, custom_logger, general_config):
    printer_mapping_obj = {'hbc_obj': generate_hbc_token(app_config),
                           'printer_mapping_obj': Post_HBC_Printer_Mapping(general_config, app_config, custom_logger),
                           'test_data': common_utils.read_excel_data_store("devicehub_services",
                                                                           "DeviceHubTestData.xlsx",
                                                                           "hbc_print_validation")}
    yield printer_mapping_obj


class Test_hbc_post_printer_mapping(common_utils):

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(100)
    def test_login_hbc(self, resource, custom_logger, context):
        resp = resource['hbc_obj'].generate_hbc_access_token()
        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))
        context['hbc_access_token'] = resp['token']

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(101)
    def test_hbc_printer_mapping_validation_passing_blank_payload(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number="",
                                                                             printer_name="", alias_name="")
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("serialNumber is required field"))
        assert_that(resp['response_body']['errors'][0]['additionalCode'], equal_to("DH_VA_10002"))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'], equal_to("Please provide the serialNumber"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(102)
    def test_hbc_printer_mapping_validation_passing_blank_serial_number(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number="",
                                                                             printer_name="printer_dummy",
                                                                             alias_name="automation_alias")
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("serialNumber is required field"))
        assert_that(resp['response_body']['errors'][0]['additionalCode'], equal_to("DH_VA_10002"))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'], equal_to("Please provide the serialNumber"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(103)
    def test_hbc_printer_mapping_validation_passing_blank_printer_name(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number=resource['test_data'][0][
                                                                                 'serial_number'],
                                                                             printer_name="",
                                                                             alias_name="automation_alias")
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("printerName is required field"))
        assert_that(resp['response_body']['errors'][0]['additionalCode'], equal_to("DH_VA_10003"))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'], equal_to("Please provide the printer name"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(104)
    def test_hbc_printer_mapping_validation_passing_blank_alias_name(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number=resource['test_data'][0][
                                                                                 'serial_number'],
                                                                             printer_name="printer_dummy",
                                                                             alias_name="")
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("alias is required field"))
        assert_that(resp['response_body']['errors'][0]['additionalCode'], equal_to("DH_VA_10001"))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'], equal_to("Please provide the alias name"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(105)
    def test_hbc_printer_mapping_success(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number=resource['test_data'][0][
                                                                                 'serial_number'],
                                                                             printer_name=resource['test_data'][0][
                                                                                 'printer_name'],
                                                                             alias_name=resource['test_data'][0][
                                                                                 'alias_name'])
        assert_that(self.validate_expected_and_actual_response_code(201, resp['response_code']),
                    "Expected Status code 201 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']["id"], is_not(""))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(106)
    def test_hbc_printer_alias_name_already_exists(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                             serial_number=resource['test_data'][0][
                                                                                 'serial_number'],
                                                                             printer_name=resource['test_data'][0][
                                                                                 'printer_name'],
                                                                             alias_name=resource['test_data'][0][
                                                                                 'alias_name'])
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("alias mapping [{arg1}] already present".format(arg1=resource['test_data'][0][
                        'alias_name'])))
        assert_that(resp['response_body']['errors'][0]['additionalCode'], equal_to("DH_AE_30001"))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'],
                    equal_to("Alias name already present, Please enter the unique name for alias"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(107)
    def test_hbc_printer_alias_mapping_validation_for_invalid_token(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping("abcderfff", None,
                                                                             serial_number=resource['test_data'][0]['serial_number'],
                                                                             printer_name="printer_dummy",
                                                                             alias_name="automation_alias")
        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(108)
    def test_hbc_printer_alias_mapping_validation_for_invalid_path(self, resource, custom_logger, context):
        resp = resource['printer_mapping_obj'].send_post_hbc_printer_mapping(context['hbc_access_token'],
                                                                             "invalid_path",
                                                                             serial_number=resource['test_data'][0]['serial_number'],
                                                                             printer_name="printer_dummy",
                                                                             alias_name="automation_alias")
        assert_that(self.validate_expected_and_actual_response_code(403, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
