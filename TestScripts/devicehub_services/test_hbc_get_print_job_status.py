import pytest
from hamcrest import assert_that, equal_to, is_not
from APIObjects.devicehub_services.Get_hbc_print_job_status import Get_HBC_Print_Job_Status
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    get_job_status_obj = Get_HBC_Print_Job_Status(general_config, app_config, custom_logger)

    yield get_job_status_obj


class Test_hbc_get_print_job_status(common_utils):

    @pytest.mark.device_hub_hbc_flow
    @pytest.mark.order(111)
    def test_get_print_job_status_invalid_job_id(self, resource, context,
                                                 custom_logger):
        resp = resource.send_get_print_job_status("HBC", context['hbc_access_token'], None, "invalid_job_id")

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))

        assert_that(resp['response_body']['errors'][0]['errorDescription'],
                    equal_to("jobId [{arg1}] not found!".format(arg1="invalid_job_id")))

    # @pytest.mark.device_hub_hbc_flow
    # @pytest.mark.order(112)
    # def test_get_print_job_status_invalid_access_token(self, resource, context,
    #                                                    custom_logger):
    #     resp = resource.send_get_print_job_status("invalid_token", None, "jdhekhdej494jj4")
    #
    #     assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
    #                 "Expected Status code 403 is not match with actual {arg1}".format(arg1=resp['response_code']))
