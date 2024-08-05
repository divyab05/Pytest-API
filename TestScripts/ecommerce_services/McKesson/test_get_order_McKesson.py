import pytest
from hamcrest import assert_that

from APIObjects.ecommerce_services.McKesson import Order_Details_Payload
from APIObjects.ecommerce_services.McKesson.Order_Details_Payload import Order_Details_McKesson_Payload
from FrameworkUtilities.common_utils import common_utils
from conftest import custom_logger


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Order_Details_McKesson_Payload(general_config, app_config, custom_logger)
    yield req


class Test_get_order_api(common_utils):

    # @pytest.mark.connector_mckesson_spe
    # @pytest.mark.order(5)
    # @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
    #                                                                          "McKessonTestData.xlsx",
    #                                                                          "Order_Info_Mckesson_Data"))
    # def test_get_order_api_mckesson(self, resource, test_data,get_integrator_id, generate_access_token, context):
    #     resp = resource.send_order_details_mckesson_post_request(test_data,get_integrator_id, context['store_key'],
    #                                             'valid_token', generate_access_token,"mckesson")
    #
    #     assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
    #                 "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        # expected_schema = self.read_json_file('order_info_mckesson_store_schema.json', 'ecommerce_services')
        #
        # res = self.validate_json_schema_validations(resp['response_body'],
        #                                             expected_schema)
        #
        # if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                   "message {arg}".format(arg=res['error_message']))
        #
        # resource.validate_mckesson_onboard_api_response_payload(test_data, resp['response_body'],
        #                                                         custom_logger)

    @pytest.mark.connector_mckesson_spe
    @pytest.mark.ecommerce_services_sp360commercial_smoke
    @pytest.mark.ecommerce_services_sp360commercial_reg
    @pytest.mark.ecommerce_services_sp360commercial
    @pytest.mark.order(34)
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ecommerce_services",
                                                                             "McKessonTestData.xlsx",
                                                                             "Order_Info_Mckesson_Data"))
    def test_get_order_mckesson_store_with_expired_token(self, resource, test_data, get_integrator_id,context):
        resp = resource.send_order_details_mckesson_post_request(test_data, get_integrator_id, context['store_key'],
                                                                 'invalid_token',None,"mckesson")

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))
        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
        if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                          "message {arg}".format(arg=res['error_message']))