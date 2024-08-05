import re

from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from body_jsons.ecommerce_services.McKesson.Order_Details_McKesson import Order_Details_McKesson_Store_RequestObject
from body_jsons.ecommerce_services.McKesson.onboard_mckesson import Onboard_McKesson_Store_RequestObject


class Order_Details_McKesson_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_order_details_mckesson_post_request(self, test_data, integratorid, store_key, token_type, access_token,connector):

        if test_data['orderNumber'] == "None":
            orderNumber = ""
        else:
            orderNumber = test_data['orderNumber']
        if test_data['shipperId'] == "None":
            shipperId = ""
        else:
            shipperId = test_data['shipperId']

        onboard_obj = Order_Details_McKesson_Store_RequestObject(store_key, orderNumber, shipperId)
        req_payload = common_utils.convert_object_to_json(onboard_obj)

        self.custom_logger.info("Request payload for the onboard_shopify_post_request "
                                "api {arg1}".format(arg1=req_payload))
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False,
                                                                access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True,
                                                                access_token,connector,False)
        base_uri = self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OrderDetailsMckessonStore
        self.custom_logger.info("Send post request to McKesson store"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   others=None)
        self.custom_logger.info("Response payload for onboard McKesson store"
                                "is {arg1}".format(arg1=response))
        return response

    # def validate_mckesson_onboard_api_response_payload(self, test_data, response_json, custom_logger):
    #     results = []
    #     if re.match("^[A-Za-z0-9_-]*$", response_json['storeKey']):
    #         custom_logger.info('Actual response matches with expected response '
    #                            'for storeKey')
    #         results.append(response_json['storeKey'])
    #     assert str(response_json['cartId']) == str(test_data['cartId'])
    #     custom_logger.info('Actual response matches with expected response '
    #                        'for cartId')
    #     results.append(response_json['cartId'])
    #     assert str(response_json['message']) == str(test_data['message'])
    #     custom_logger.info('Actual response matches with expected response '
    #                        'for response message')
    #     results.append(response_json['message'])
    #     assert str(response_json['messageCode']) == str(test_data['messageCode'])
    #     custom_logger.info('Actual response matches with expected response '
    #                        'for messageCode')
    #     results.append(response_json['messageCode'])
    #     return results



