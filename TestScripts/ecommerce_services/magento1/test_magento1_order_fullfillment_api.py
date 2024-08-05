# import pytest
# from hamcrest import assert_that
#
# from APIObjects.ecommerce_services.Generate_Order_FullFilment import Generate_Order_FullFillment
# from FrameworkUtilities.common_utils import common_utils
#
#
# @pytest.fixture()
# def resource(general_config, app_config, custom_logger):
#     reqs = Generate_Order_FullFillment(general_config, app_config, custom_logger)
#     yield reqs
#
#
# class Test_magento1_order_fullfillment_api(common_utils):
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(51)
#     def test_order_fullfiment_api_end_to_end(self, resource, get_integrator_id, generate_access_token, context):
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             None,"magento")
#         assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
#                     "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         assert resource.validate_success_message_response_msg(resp['response_body']['message']) is True
#
#         context['shipmentId'] = resp['response_body']['shipmentId']
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(56)
#     def test_order_fullfiment_with_expired_token(self, resource, get_integrator_id, generate_access_token, context):
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'invalid_token', context, None,
#                                                             context['store_key_magento'], None,"magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
#                     "Expected Status code 401 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(57)
#     def test_order_fullfiment_with_invalid_path(self, resource, get_integrator_id, generate_access_token, context):
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, "invalid", context['store_key_magento']
#                                                             , None)
#         assert self.validate_expected_and_actual_response_code(404, resp['response_code']) is True
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(58)
#     def test_order_fullfiment_with_invalid_store_key(self, resource, get_integrator_id, generate_access_token, context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "invalid_store_key","magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#
#         resource.validate_error_messages("Invalid storeKey", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(59)
#     def test_order_fullfiment_with_invalid_order_id(self, resource, get_integrator_id, generate_access_token, context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "invalid_order_id","magento")
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#         resource.validate_error_messages("not found", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(60)
#     def test_order_fullfiment_with_invalid_order_product_id(self, resource, get_integrator_id, generate_access_token,
#                                                             context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "invalid_product_id","magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#         resource.validate_error_messages("not found", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(61)
#     def test_order_fullfiment_with_blank_store_key(self, resource, get_integrator_id, generate_access_token,
#                                                    context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "blank_store_key","magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#
#         resource.validate_error_messages("Invalid storeKey", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(62)
#     def test_order_fullfiment_with_blank_order_id(self, resource, get_integrator_id, generate_access_token,
#                                                   context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "blank_order_id","magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations( resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#
#         resource.validate_error_messages("The value of parameter 'orderId' can not be empty.", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(63)
#     def test_order_fullfiment_with_blank_order_product_id_key(self, resource, get_integrator_id, generate_access_token,
#                                                               context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "blank_product_id","magento")
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#
#         resource.validate_error_messages("The value of parameter 'orderProductId' can not be empty.", resp_msg)
#
#     @pytest.mark.ecommerce_services_magento
#     @pytest.mark.order(64)
#     def test_order_fullfiment_with_blank_carrier_id(self, resource, get_integrator_id, generate_access_token,
#                                                     context):
#
#         resp = resource.send_order_fullfilment_post_request(get_integrator_id, generate_access_token,
#                                                             'valid', context, None, context['store_key_magento'],
#                                                             "blank_carrier_id","magento")
#
#         assert_that(self.validate_expected_and_actual_response_code(400, resp['response_code']),
#                     "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp['response_code']))
#
#         expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
#         res = self.validate_json_schema_validations(resp['response_body'], expected_schema)
#
#         if not res['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error"
#                                           "message {arg}".format(arg=res['error_message']))
#
#         resp_msg = resp['response_body']['errors'][0]['errorDescription']
#
#         resource.validate_error_messages("The value of parameter 'carrierId' can not be empty.", resp_msg)
