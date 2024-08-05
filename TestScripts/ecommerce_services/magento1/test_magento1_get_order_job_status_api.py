import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.Generate_Order_Job_Status_Payload import Generate_Order_Job_status
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_Order_Job_status(general_config, app_config, custom_logger)
    yield req


class Test_magento1_get_order_job_status_api(common_utils):

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(3)
    def test_get_order_job_status_api(self, resource, get_integrator_id, generate_access_token, context):
        resp = resource.send_get_order_job_status_request(get_integrator_id, context['X-PB-TransactionId'],
                                                          'valid_token', generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        res = self.validate_json_schema_validations(resp['response_body'],
                                                    self.read_json_file('GetOrderJobStatus'
                                                                        '.json', 'ecommerce_services'))

        resource.store_job_status(resp['response_body'], context, get_integrator_id, context['X-PB-TransactionId'],
                                  'valid_token', generate_access_token, None,"magento")

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(15)
    def test_get_order_job_status_with_invalid_header(self, resource, get_integrator_id, generate_access_token):

        transaction_id = generate_random_alphanumeric_string()
        resp = resource.send_get_order_job_status_request(get_integrator_id, transaction_id, 'valid_token',
                                                          generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        res = self.validate_json_schema_validations(resp['response_body'],
                                                    self.read_json_file('Error_Schema.json', 'ecommerce_services'))

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        resp_msg = resp['response_body']['errors'][0]['errorDescription']

        assert resource.validate_invalid_header_msg(resp_msg) is True

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(16)
    def test_order_job_status_with_expired_token(self, generate_access_token, resource, get_integrator_id, context):
        resp = resource.send_get_order_job_status_request(get_integrator_id, context['X-PB-TransactionId'],
                                                          'invalid_token', generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))
