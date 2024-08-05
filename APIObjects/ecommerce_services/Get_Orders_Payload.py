import re

import pytest

from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils


class Generate_Orders_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_orders_request(self, integratorid, order_id, token_type, access_token, invalid_resource_path,connector):

        base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetOrder).replace(
            "{id}", order_id)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector( integratorid, self.app_config, True, access_token,connector,False)

        self.custom_logger.info("Send Get request to Check Get Order API"
                                "for base uri is {arg2}".format(arg2=base_uri))

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Order API is {arg1}".format(arg1=response))

        return response

    def store_order_info(self, response, context):

        context['order_id'] = response['orders'][0]['order_id']
        context['order_product_id'] = response['orders'][0]['order_products'][0]['order_product_id']
        context['order_count'] = response['orders_count']
        context['order_id_2'] = response['orders'][1]['order_id']


    def validate_date_format_in_orders(self, response):

        expected_date_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}T([0-9]+(:[0-9]+)+)"
        actual_created_date = response['create_at']['value']
        time_zone_actual_created_date = str(actual_created_date).split("+")[1]
        actual_modified_date = response['modified_at']['value']
        time_zone_actual_modified_date = str(actual_modified_date).split("+")[1]
        if re.match(expected_date_pattern, actual_created_date) and \
                re.match(expected_date_pattern, actual_modified_date):
            if time_zone_actual_created_date == "0530" and time_zone_actual_modified_date == "0530":
                return True
            else:
                pytest.fail("Actual create timezone {arg1} and actual modified date timezone does not match with "
                            "expected".format(arg1=time_zone_actual_created_date,
                                              arg2=time_zone_actual_modified_date))
        else:
            pytest.fail("Actual Create date {arg1} or modified date {arg2} does not match with expected date"
                        " pattern".format(arg1=actual_created_date, arg2=actual_modified_date))