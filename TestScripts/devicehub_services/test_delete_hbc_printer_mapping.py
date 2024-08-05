import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Delete_hbc_printer_mapping import Delete_hbc_printer_mapping
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = {'delete_obj': Delete_hbc_printer_mapping(general_config, app_config, custom_logger),
           'test_data': common_utils.read_excel_data_store("devicehub_services",
                                                           "DeviceHubTestData.xlsx",
                                                           "hbc_print_validation")
           }
    yield req


class Test_hbc_delete_printer_mapping(common_utils):

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(150)
    def test_hbc_delete_printer_mapping_success(self, resource, custom_logger, context):
        resp = resource['delete_obj'].send_delete_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                      alias_name=resource['test_data'][0]['alias_name'])

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(151)
    def test_hbc_delete_already_deleted_alias(self, resource, custom_logger, context):
        resp = resource['delete_obj'].send_delete_hbc_printer_mapping(context['hbc_access_token'], None,
                                                                      alias_name=resource['test_data'][0]['alias_name'])

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'], equal_to("Document not found"))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(152)
    def test_delete_hbc_printer_alias_mapping_validation_for_invalid_token(self, resource, custom_logger, context):
        resp = resource['delete_obj'].send_delete_hbc_printer_mapping("abjdddk", None,
                                                                      alias_name="automation_alias")
        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))
