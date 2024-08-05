import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.magento1.Get_Registered_Carts_Payload import Get_Registered_Carts_Payload
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_Registered_Carts_Payload(general_config, app_config, custom_logger)
    yield req


class Test_magento1_get_registered_carts_api(common_utils):

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(5)
    def test_get_registered_carts(self, resource, get_integrator_id, generate_access_token, custom_logger, app_config,
                                  context):
        resp = resource.send_get_registered_carts_request(get_integrator_id, 'valid_token', generate_access_token, None,"magento")

        expected_json_resp = resource.generate_registered_carts_response(get_integrator_id,
                                                                         context['store_key_magento'],
                                                                         app_config.env_cfg['country_code'],
                                                                         context['store_name_magento'],
                                                                         app_config.env_cfg['subscriptionid'])

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        # res = self.validate_json_schema_validations(resp['response_body'],
        #                                             self.read_json_file('Get_Registered_Carts_without_warehouse.json',
        #                                                                 'ecommerce_services'))
        #
        # if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                   "message {arg}".format(arg=res['error_message']))
        #
        # out_put = self.compare_object(expected_json_resp, resp['response_body'], custom_logger)
        # self.validate_expected_and_response_payload(expected_json_resp, resp['response_body'], out_put)

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(19)
    def test_get_registered_carts_with_expired_token(self, resource, get_integrator_id):

        resp = resource.send_get_registered_carts_request(get_integrator_id, 'invalid_token', None, None,"magento")

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
    @pytest.mark.order(20)
    def test_get_registered_carts_with_invalid_resource_path(self, resource, get_integrator_id, generate_access_token):

        resp = resource.send_get_registered_carts_request(get_integrator_id, "valid_token", generate_access_token,
                                                          "invalid","magento")

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

