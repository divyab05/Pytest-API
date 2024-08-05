import pytest
from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string, generate_random_number
from body_jsons.ecommerce_services.OrderFullFillment.items import items
from body_jsons.ecommerce_services.OrderFullFillment.order_fullfilment_request import \
    order_fullfillment_request
from body_jsons.ecommerce_services.OrderFullFillment.trackingNumbers import trackingNumbers


class Generate_Order_FullFillment:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def generate_post_request_payload(self, context, store_key, others):
        lst_obj_items = []
        lst_obj_trackingNum = []

        if others == "invalid_store_key":
            store_key = generate_random_alphanumeric_string()
        elif others == "blank_store_key":
            store_key = ""
        else:
            store_key = store_key

        if others == "invalid_order_id":
            order_id = generate_random_number(8)
        elif others == "blank_order_id":
            order_id = ""
        else:
            order_id = context['order_id']

        if others == "invalid_product_id":
            order_product_id = generate_random_number(8)
        elif others == "blank_product_id":
            order_product_id = ""
        else:
            order_product_id = context['order_product_id']

        if others == "blank_carrier_id":
            carrier_id = ""
        else:
            carrier_id = self.general_config.get("Common_Variables", "carrierid")

        lst_obj_items.append(items(order_product_id, 1))
        tracking_no = generate_random_number(5)
        obj_tracking_numbers = trackingNumbers(carrier_id, tracking_no)
        lst_obj_trackingNum.append(obj_tracking_numbers)
        obj_order_fullfillment = order_fullfillment_request(store_key, order_id
                                                            , lst_obj_items, lst_obj_trackingNum)
        req_payload = common_utils.convert_object_to_json(obj_order_fullfillment)
        return req_payload

    def send_order_fullfilment_post_request(self, integratorid, access_token, token_type, context,
                                            invalid_resource_path, store_key, others,connector):

        req_payload = self.generate_post_request_payload(context, store_key, others)

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.orderfullfillment) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.orderfullfillment)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)

        self.custom_logger.info("Send post request to Fullfill order"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)

        self.custom_logger.info("Response payload for order fullfillment api"
                                "is {arg1}".format(arg1=response))
        return response

    def validate_success_message_response_msg(self, msg):
        if msg.__contains__("Shipment added successfully"):
            return True
        else:
            return False

    def validate_error_messages(self, expected_msg, actual_msg):
        if actual_msg.__contains__(expected_msg):
            return True
        else:
            pytest.fail("Expected message {arg1} does not contain in actual text message "
                        "{arg2}".format(arg1=expected_msg, arg2=actual_msg))
