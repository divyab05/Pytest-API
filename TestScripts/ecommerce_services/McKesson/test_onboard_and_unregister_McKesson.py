import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.McKesson.Generate_McKesson_Payload import Generate_McKesson_Payload
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Generate_McKesson_Payload(general_config, app_config, custom_logger)
    yield req


class Test_onboard_McKesson_api(common_utils):

    @pytest.mark.connector_mckesson_spe
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(31)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "McKessonTestData.xlsx",
                                                                             "Onboard_Mckesson_Data"))
    def test_onboard_mckesson_store_with_expired_token(self, resource, test_data, get_integrator_id):
        resp = resource.send_onboard_mckesson_post_request(test_data, get_integrator_id, None, "invalid_token", "mckesson")

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))
        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

    @pytest.mark.order(33)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "McKessonTestData.xlsx",
                                                                             "Onboard_Mckesson_Data"))
    @pytest.mark.connector_mckesson_spe
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_onboard_mckesson_store(self, resource, test_data, get_integrator_id, custom_logger,
                                    context, generate_access_token):
        resp = resource.send_onboard_mckesson_post_request(test_data, get_integrator_id, generate_access_token,
                                                           "valid_token","mckesson")

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))
        expected_schema = self.read_json_file('onboard_mckesson_store_schema.json', 'ecommerce_services')
        context['store_key'] = resp['response_body']['storeKey']
        context['cart_Id'] = resp['response_body']['cartId']

        res = self.validate_json_schema_validations(resp['response_body'],
                                                    expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))

        #  resource.validate_mckesson_onboard_api_response_payload(test_data, resp['response_body'],
        #                                                                  custom_logger)



    @pytest.mark.order(32)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "McKessonTestData.xlsx",
                                                                             "OnboardMckessonErrorValidation"))
    @pytest.mark.connector_mckesson_spe
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    def test_onboard_mckesson_store_with_invalid_request_payload(self, resource, test_data, get_integrator_id,
                                                                generate_access_token):

        resp = resource.send_onboard_mckesson_post_request(test_data, get_integrator_id, generate_access_token,
                                                          "valid_token","mckesson")

        assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))

        assert resp['response_body']['errors'][0]['errorDescription'] == test_data['Error_Message']

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')

        res = self.validate_json_schema_validations(resp['response_body'],
                                                    expected_schema)

        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))
