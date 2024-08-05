import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.magento1.Generate_Magento_Payload import Generate_Magento_Payload
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_Magento_Payload(general_config, app_config, custom_logger)
    yield req


class Test_onboard_magento1_store_api(common_utils):

    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "MagentoTestData.xlsx",
                                                                             "Onboard_Magento_Data"))
    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(1)
    def test_onboard_magento_store(self, resource, test_data, get_integrator_id, custom_logger,
                                   context, generate_access_token):
        expected_payload = resource.generate_onboard_response(test_data['accessToken'], "magento",
                                                              test_data['name'], test_data['message'])

        resp = resource.send_onboard_magento_post_request(test_data, get_integrator_id, generate_access_token,
                                                          "valid_token", None,"magento",context)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        context['store_key_magento'] = resp['response_body']['storeKey']
        context['store_name_magento'] = resp['response_body']['cartId']

        # res = self.validate_json_schema_validations(resp['response_body'],
        #                                             self.read_json_file('onboard_magento_store.json',
        #                                                                 'ecommerce_services/Magento'))
        #
        # if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                   "message {arg}".format(arg=res['error_message']))
        #
        # out_put = self.compare_object(expected_payload, resp['response_body'], custom_logger)
        # self.validate_expected_and_response_payload(expected_payload, resp['response_body'], out_put)

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(9)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "MagentoTestData.xlsx",
                                                                             "Onboard_Magento_Data"))
    def test_onboard_magento_store_with_expired_token(self, resource, test_data, get_integrator_id,context):

        resp = resource.send_onboard_magento_post_request(test_data, get_integrator_id, None, "invalid_token", None,"magento",context)
        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations( resp['response_body'], expected_schema,)
        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(10)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "MagentoTestData.xlsx",
                                                                             "Onboard_Magento_Error_Validat"))
    def test_onboard_magento_store_with_invalid_request_payload(self, resource, test_data, get_integrator_id,
                                                                generate_access_token,context):

        resp = resource.send_onboard_magento_post_request(test_data, get_integrator_id, generate_access_token,
                                                          "valid_token", None,"magento",context)
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert resp['response_body']['errors'][0]['errorDescription'] == test_data['Error_Message']

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations( resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.ecommerce_services_magento
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(11)
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("ecommerce_services", "MagentoTestData.xlsx",
                                                                "Onboard_Magento_Error_Validat"))
    def test_onboard_magento_with_invalid_path(self, test_data, resource, get_integrator_id, generate_access_token,context):
        resp = resource.send_onboard_magento_post_request(test_data, get_integrator_id, generate_access_token,
                                                          "valid_token", "invalid_path","magento",context)
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))
