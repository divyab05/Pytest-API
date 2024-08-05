import pytest

from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.ecommerce_services.OrderStatus.orderIds import orderIds
from body_jsons.ecommerce_services.OrderStatus.order_status import order_status_request_objects


class Generate_Order_Status_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def generate_order_status_post_request_payload(self, context, store_key, others):
        list_obj_orderIds = []
        order_Ids = []
        if others == "invalid_orderid":
            order_Ids.append({"orderId": generate_random_alphanumeric_string()})
            order_Ids.append({"orderId": generate_random_alphanumeric_string()})
        else:
            order_Ids.append({"orderId": context['order_id']})
            order_Ids.append({"orderId": context['order_id_2']})

        if others == "invalid_store_key":
            store_key = generate_random_alphanumeric_string()
        elif others == "blank_store_key":
            store_key = ""
        else:
            store_key = store_key

        for index in range(0, len(order_Ids)):
            list_obj_orderIds.append(orderIds(order_Ids[index]))

        order_status = order_status_request_objects(store_key, list_obj_orderIds)

        req_payload = common_utils.convert_object_to_json(order_status)
        return req_payload

    def send_post_order_status_request(self, integratorid, access_token, token_type, context,
                                       invalid_resource_path, store_key, others):

        request_payload = self.generate_order_status_post_request_payload(context, store_key, others)

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OrderStatus) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OrderStatus)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)

        self.custom_logger.info("Send post request to check Order Status"
                                "and base uri is {arg2}".format(arg2=base_uri))

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, request_payload, "post",
                                                                   invalid_resource_path)

        self.custom_logger.info("Response payload for order Status api"
                                "is {arg1}".format(arg1=response))
        return response

    def validate_order_status(self, response, context, scenario):

        order_id_1 = response['order'][1]['orderId']
        order_id_1_status = response['order'][1]['status']
        order_id_2 = response['order'][0]['orderId']
        order_id_2_status = response['order'][0]['status']
        if scenario == "before":
            if order_id_1 == context['order_id'] and order_id_1_status == "open" and \
                    order_id_2 == context['order_id_2'] and order_id_2_status == "open":
                return True
            else:
                pytest.fail("Order id and status does not match with Actual response before order fulfillment")
        else:
            if order_id_1 == context['order_id'] and order_id_1_status == "closed" and \
                    order_id_2 == context['order_id_2'] and order_id_2_status == "open":
                return True
            else:
                pytest.fail("Order id and status does not match with Actual response after order fulfillment")



