import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.magento1.Generate_UnRegister_Payload import Generate_UnRegister_Payload
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import generic_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_UnRegister_Payload(general_config, app_config, custom_logger)
    yield req


class Test_unregister_magento1_store_api(common_utils):

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(6)
    def test_unregister_magento_store(self, resource, get_integrator_id, context,
                                      generate_access_token):
        resp = resource.send_unregister_magento_delete_request(get_integrator_id, context['store_key_magento'],
                                                               'valid_token', generate_access_token,"magento",context['id1'])

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert resp['response_body']['message'] == "Store deleted successfully"

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(7)
    def test_unregister_magento_store_with_expired_token(self, resource, get_integrator_id, context):
        resp = resource.send_unregister_magento_delete_request(get_integrator_id,
                                                               context['store_key_magento'], "invalid_token", None,"magento",context['id1'])

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
    @pytest.mark.order(8)
    def test_unregister_shopify_store_with_invalid_store_key(self, resource, get_integrator_id, generate_access_token,context):

        resp = resource.send_unregister_magento_delete_request(get_integrator_id, generic_utils.
                                                               generate_random_alphanumeric_string(), "valid_token",
                                                               generate_access_token,"magento",context['id1'])

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations( resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        assert resp['response_body']['errors'][0]['errorDescription'] == 'Invalid storekey'
