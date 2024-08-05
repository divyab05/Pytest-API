import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.Epic.Generate_Epic_Payload import Generate_Epic_Payload
from FrameworkUtilities.common_utils import common_utils
from conftest import generate_access_token


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_Epic_Payload(general_config, app_config, custom_logger)
    yield req


class Test_onboard_epic_store_api(common_utils):

    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "EpicTestData.xlsx",
                                                                             "Onboard_Epic_Data"))
    @pytest.mark.pharma_connector_epic
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(44)
    def test_onboard_epic_store(self, resource, test_data, get_integrator_id, custom_logger,
                                context, generate_access_token):
        # expected_payload = resource.generate_onboard_response(test_data['accessToken'], "epic",
        #                                                       test_data['name'], test_data['message'])

        resp = resource.send_onboard_epic_post_request(test_data, get_integrator_id, generate_access_token,
                                                       "valid_token", None, "epic")

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

    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "EpicTestData.xlsx",
                                                                             "Onboard_Epic_Data"))
    @pytest.mark.pharma_connector_epic
    @pytest.mark.order(43)
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_onboard_epic_store_with_expired_token(self, resource, test_data, get_integrator_id):

        resp = resource.send_onboard_epic_post_request(test_data, get_integrator_id, None, "invalid_token", None,
                                                       "epic")
        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema, )
        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "EpicTestData.xlsx",
                                                                             "Onboard_Epic_Error_Validat"))
    @pytest.mark.pharma_connector_epic
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(42)
    def test_onboard_epic_store_with_invalid_request_payload(self, resource, test_data, get_integrator_id,
                                                             generate_access_token):

        resp = resource.send_onboard_epic_post_request(test_data, get_integrator_id, generate_access_token,
                                                       "valid_token", None, "epic")
        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert resp['response_body']['errors'][0]['errorDescription'] == test_data['Error_Message']

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "EpicTestData.xlsx",
                                                                             "Onboard_Epic_Data"))
    @pytest.mark.pharma_connector_epic
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(41)
    def test_onboard_epic_with_invalid_path(self, test_data, resource, get_integrator_id, generate_access_token):
        resp = resource.send_onboard_epic_post_request(test_data, get_integrator_id, generate_access_token,
                                                       "valid_token", "invalid_path", "epic")
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(arg1=resp['response_code']))
