import json
import allure
from ConfigFiles.ecommerce_services import API_Resource_Path
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.GetRegisteredCarts import GetRegisteredCarts
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.stores import stores
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.storeDetails import storedetails
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.store import store


class Get_Registered_Carts_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    @allure.step("Send Get Registered Carts API HTTP Request to get Registered carts")
    def send_get_registered_carts_request(self, integratorid, token_type, access_token, invalid_resource_path,connector):

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetRegisteredCarts) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetRegisteredCarts)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)

        self.custom_logger.info("Send Get request to Get Registered Carts"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Registered Carts"
                                "is {arg1}".format(arg1=response))
        return response

    def get_registered_carts_response_from_test_data(self, store_name):
        result_test_data = {}
        result_test_data_ls_store = []
        final_dict = {}

        results_store_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services",
                                                                               "MagentoTestData.xlsx",
                                                                               "GetRegisteredCarts_Store_detail",
                                                                               store_name)
        for index in range(0, len(results_store_details)):

            if results_store_details[index]['dimensionUnit'] is None:
                results_store_details[index]['dimensionUnit'] = ''
                results_store_details[index]['defaultWarehouseId'] = ''
                results_store_details[index]['weightUnit'] = ''

            result_test_data['store_details'] = results_store_details
            result_test_data_ls_store.append(result_test_data['store_details'])
        final_dict['store_details'] = result_test_data_ls_store

        return final_dict

    def generate_registered_carts_response(self, integrator_id, store_key, country_code, store_name, subscription_id):
        test_data = self.get_registered_carts_response_from_test_data(store_name)
        ls_store_Details = []
        ls_warehouse_details = None
        ls_store = []
        for index in range(0, len(test_data['store_details'])):
            obj_store_details = storedetails(test_data['store_details'][index][0])
            ls_store_Details.append(obj_store_details)
        obj_store = store("magento", store_key, country_code, ls_store_Details, ls_warehouse_details)
        ls_store.append(obj_store)
        obj_stores = stores(ls_store)
        obj_get_registered_carts = GetRegisteredCarts(integrator_id, subscription_id, obj_stores)
        resp_data = common_utils.convert_object_to_json(obj_get_registered_carts)
        return json.loads(resp_data)
