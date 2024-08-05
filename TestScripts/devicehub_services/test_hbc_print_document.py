import pytest
from hamcrest import assert_that, equal_to, is_not

from APIObjects.devicehub_services.Get_hbc_print_job_status import Get_HBC_Print_Job_Status
from APIObjects.devicehub_services.Post_hbc_print_document import Post_hbc_print_document
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req_obj = {"print_doc_obj": Post_hbc_print_document(general_config, app_config, custom_logger),
               "get_job_status_obj": Get_HBC_Print_Job_Status(general_config, app_config, custom_logger)}

    yield req_obj


class Test_post_print_request(common_utils):

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(109)
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("devicehub_services",
                                                                "DeviceHubTestData.xlsx",
                                                                "hbc_print_validation"))
    def test_post_hbc_print_document_blank_validations_check(self, resource, context, test_data,
                                                             custom_logger):
        resp = resource['print_doc_obj'].send_hbc_post_print_document_request(context['hbc_access_token'], None,
                                                                              test_data)

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('hbc_error_schema.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("{arg1}".format(arg1=test_data['errorDescription'])))
        assert_that(resp['response_body']['errors'][0]['additionalCode'],
                    equal_to("{arg1}".format(arg1=test_data['additionalCode'])))
        assert_that(resp['response_body']['errors'][0]['additionalInfo'],
                    equal_to("{arg1}".format(arg1=test_data['additionalInfo'])))

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(110)
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("devicehub_services",
                                                                "DeviceHubTestData.xlsx",
                                                                "hbc_print_scenarios"))
    def test_post_hbc_print_document_success_end_to_end(self, resource, context, test_data,
                                                        custom_logger):
        resp = resource['print_doc_obj'].send_hbc_post_print_document_request(context['hbc_access_token'], None,
                                                                              test_data)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['jobId'],
                    is_not(""))
        assert_that(resp['response_body']['originalTransactionId'],
                    is_not(""))

        resp_job = resource['get_job_status_obj'].send_get_print_job_status("HBC", context['hbc_access_token'], None,
                                                                            resp['response_body']['jobId'])

        assert_that(self.validate_expected_and_actual_response_code(200, resp_job['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp_job['response_body']['jobId'], equal_to(resp['response_body']['jobId']))

        expected_schema = self.read_json_file('HBC_Success_tx.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp_job['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp_job['response_body']['status'], equal_to("SUCCESS"))
        assert_that(resp_job['response_body']['printStatusTransaction'][0]['name'],
                    equal_to(resp['response_body']['jobId']))
        assert_that(resp_job['response_body']['printStatusTransaction'][0]['status'],
                    equal_to("COMPLETED"))

    @pytest.mark.device_hub_print_v2
    @pytest.mark.order(110)
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("devicehub_services",
                                                                "DeviceHubTestData.xlsx",
                                                                "PrintV2"))
    def test_post_print_v2_success_end_to_end(self, generate_access_token, resource, context, test_data,
                                              custom_logger):
        resp = resource['print_doc_obj'].send_printv2_post_request(generate_access_token, None,
                                                                   test_data)
        print(resp)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp['response_body']['jobId'],
                    is_not(""))
        assert_that(resp['response_body']['originalTransactionId'],
                    is_not(""))

        resp_job = resource['get_job_status_obj'].send_get_print_job_status("OKTA", generate_access_token, None,
                                                                            resp['response_body']['jobId'])

        assert_that(self.validate_expected_and_actual_response_code(200, resp_job['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert_that(resp_job['response_body']['jobId'], equal_to(resp['response_body']['jobId']))

        expected_schema = self.read_json_file('HBC_Success_tx.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp_job['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp_job['response_body']['status'], equal_to("SUCCESS"))
        assert_that(resp_job['response_body']['printStatusTransaction'][0]['status'],
                    equal_to("COMPLETED"))
