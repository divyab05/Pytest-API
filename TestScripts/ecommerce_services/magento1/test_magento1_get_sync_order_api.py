import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.Generate_Sync_Order_Payload import Get_Sync_Order_Payload
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_Sync_Order_Payload(general_config, app_config, custom_logger)
    yield req


class Test_magento1_get_sync_order_api(common_utils):

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(2)
    def test_sync_order_api_without_warehouse_flg(self, resource, get_integrator_id, generate_access_token, context):
        resp = resource.send_get_sync_order_request(get_integrator_id, 'valid_token', generate_access_token, None,
                                                    context,"magento")

        assert_that(self.validate_expected_and_actual_response_code(202, resp['response_code']),
                    "Expected Status code 202 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert resp['response_body']['response'] == "Request has been submitted successfully!"

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(12)
    def test_sync_order_api_with_expired_token(self, generate_access_token, resource, get_integrator_id, context):
        resp = resource.send_get_sync_order_request(get_integrator_id, 'invalid_token', generate_access_token, None,
                                                    context,"magento")

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(13)
    def test_sync_order_api_with_invalid_path(self, generate_access_token, resource, get_integrator_id,
                                              context):
        resp = resource.send_get_sync_order_request(get_integrator_id, 'valid_token', generate_access_token, 'invalid',
                                                    context,"magento")
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(14)
    def test_sync_order_api_with_invalid_header(self, generate_access_token, resource, get_integrator_id,
                                                context):
        resp = resource.send_get_sync_order_request(get_integrator_id, 'valid_token', generate_access_token, 'invalid',
                                                    context,"magento")

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

