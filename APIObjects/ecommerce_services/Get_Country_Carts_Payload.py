import json
from APIObjects.ecommerce_services.response_objects.GetCountryCarts.GetCountryCarts import GetCountryCarts
from ConfigFiles.ecommerce_services import API_Resource_Path
from APIObjects.ecommerce_services.response_objects.GetAvailableCarts.cartList import cartList
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *


class Get_Country_Carts_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_country_carts_request(self, integratorid, code, token_type, access_token,
                                       invalid_resource_path):

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetCountryCarts) \
                           .replace("{country_code}", code) + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetCountryCarts).replace(
                "{country_code}", code)
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)

        self.custom_logger.info("Send Get Country Carts "
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Country Carts"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_get_country_carts_response_from_test_data(self, countryCode, integratorId):

        global country_Code, results
        if integratorId == "spog" and countryCode == "GB":
            country_Code = "GB"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetCountryCarts_GB")
        elif integratorId == "spog" and countryCode == "AU":
            country_Code = "AU"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetCountryCarts_AU")
        elif integratorId == "spe" or integratorId == "sp360" or integratorId == "spo":
            country_Code = "US"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetCountryCarts_US")
        elif integratorId == "spong" and countryCode == "US":
            country_Code = "US"
            results = common_utils.read_excel_data_store("ecommerce_services", "EcommConnectorTestData.xlsx",
                                                         "GetCountryCarts_US")

        list_cart_list_obj = []
        for index in range(0, len(results)):
            obj_cart_list = cartList(results[index])
            list_cart_list_obj.append(obj_cart_list)
        get_country_carts_obj = GetCountryCarts(country_Code, list_cart_list_obj)
        json_data = common_utils.convert_object_to_json(get_country_carts_obj).replace("\\", "")
        resp_data = json.loads(json_data.replace('"["', '["').replace('"]"', '"]'))
        return resp_data

    # def validate_invalid_country_code_requests(self, msg):
    #     if msg.__contains__("Marketplace carts not found"):
    #         return True
    #     else:
    #         return False
