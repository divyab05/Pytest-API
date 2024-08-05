import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.Get_Orders_Payload import Generate_Orders_Payload
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_Orders_Payload(general_config, app_config, custom_logger)
    yield req


class Test_magento1_get_order_api(common_utils):

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(4)
    def test_get_order_api_without_wh_flg(self, resource, get_integrator_id, generate_access_token, context):
        resp = resource.send_get_orders_request(get_integrator_id, context['record_id'],
                                                'valid_token', generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        res = self.validate_json_schema_validations(resp['response_body']['orders'][0],
                                                    self.read_json_file('Orders_wh_false_magento1.json',
                                                                        'ecommerce_services/Magento'))

        # resource.store_order_info(resp['response_body'], context)

        # if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                   "message {arg}".format(arg=res['error_message']))
        #
        # del resp['response_body']['orders']
        #
        # res_order_keys = self.validate_json_schema_validations(resp['response_body'],
        #                                                        self.read_json_file('GetOrdersKeys.json',
        #                                                                            'ecommerce_services'))
        #
        # if not res_order_keys['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                              "message {arg}".format(arg=res_order_keys['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(17)
    def test_get_order_api_with_expired_token(self, resource, get_integrator_id, generate_access_token, context):
        resp = resource.send_get_orders_request(get_integrator_id, context['record_id'],
                                                'invalid_token', generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(18)
    def test_get_order_with_invalid_order_id(self, resource, get_integrator_id, generate_access_token):

        order_id = generate_random_alphanumeric_string()
        resp = resource.send_get_orders_request(get_integrator_id, order_id,
                                                'valid_token', generate_access_token, None,"magento")

        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))

        res = self.validate_json_schema_validations(resp['response_body'],
                                                    self.read_json_file('Error_Schema.json', 'ecommerce_services'))

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))
