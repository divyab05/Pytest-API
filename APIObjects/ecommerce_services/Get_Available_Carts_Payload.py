import json
from ConfigFiles.ecommerce_services import API_Resource_Path
from APIObjects.ecommerce_services.response_objects.GetAvailableCarts.GetAvailableCarts import GetAvailableCarts
from APIObjects.ecommerce_services.response_objects.GetAvailableCarts.cartList import cartList
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *


class Get_Available_Carts_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_available_carts_request(self, integratorid, code, token_type, access_token,
                                         invalid_resource_path):

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetAvailableCarts) \
                           .replace("{country_code}", code) + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetAvailableCarts).replace(
                "{country_code}", code)
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)

        self.custom_logger.info("Send Get request to check Available Carts"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Available Carts"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_get_available_carts_response_from_test_data(self, countryCode, appId, integratorId):

        global country_Code, results
        if integratorId == "spog":
            country_Code = "GB"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetAvailableCartsGB")
        elif integratorId == "spe" or integratorId == "sp360" or integratorId == "spo":
            country_Code = "US"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetAvailableCartsUS")
        elif integratorId == "spong":
            country_Code = "US"
            print("SPONG inside")
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetAvailableCartsSPONG")


        list_cart_list_obj = []
        for index in range(0, len(results)):
            obj_cart_list = cartList(results[index])
            list_cart_list_obj.append(obj_cart_list)
        get_available_carts_obj = GetAvailableCarts(country_Code, appId, integratorId, list_cart_list_obj)
        json_data = common_utils.convert_object_to_json(get_available_carts_obj).replace("\\", "")
        resp_data = json.loads(json_data.replace('"["', '["').replace('"]"', '"]'))
        return resp_data

    def validate_invalid_country_code_requests(self, msg):
        if msg.__contains__("Marketplace carts not found"):
            return True
        else:
            return False
