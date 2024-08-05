import json
from ConfigFiles.ecommerce_services import API_Resource_Path
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.GetRegisteredCarts import GetRegisteredCarts
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.address import address
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.stores import stores
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.state import state
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.country import country
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.warehouses import warehouses
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.storeDetails import storedetails
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.store import store


class Get_Registered_Carts_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_registered_carts_request(self, integratorid, token_type, access_token, invalid_resource_path):

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetRegisteredCarts) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetRegisteredCarts)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)

        self.custom_logger.info("Send Get request to Get Registered Carts"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Registered Carts"
                                "is {arg1}".format(arg1=response))
        return response

    def get_registered_carts_response_from_test_data(self, store_name, file_name):
        result_test_data = {}
        result_test_data_ls_store = []
        result_test_data_ls_warehouse = []
        result_test_data_ls_address = []
        result_test_data_ls_country = []
        result_test_data_ls_state = []
        final_dict = {}

        if file_name == "MagentoTestData.xlsx":
            sheet_name = "GetRegisteredCart2_Store_detail"
        else:
            sheet_name = "GetRegisteredCarts_Store_detail"

        results_store_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services", file_name,
                                                                               sheet_name, store_name)
        for index in range(0, len(results_store_details)):

            if results_store_details[index]['dimensionUnit'] is None:
                results_store_details[index]['dimensionUnit'] = ''
            if results_store_details[index]['defaultWarehouseId'] is None:
                results_store_details[index]['defaultWarehouseId'] = ''
            result_test_data['store_details'] = results_store_details
            result_test_data_ls_store.append(result_test_data['store_details'])
        final_dict['store_details'] = result_test_data_ls_store

        results_warehouse_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services", file_name,
                                                                                   "GetRegisteredCarts_Warehouse",
                                                                                   store_name)

        for index in range(0, len(results_warehouse_details)):
            result_test_data['warehouses'] = results_warehouse_details[index]
            del result_test_data['warehouses']['store_name']
            result_test_data_ls_warehouse.append(result_test_data['warehouses'])

        final_dict['warehouses'] = result_test_data_ls_warehouse

        results_address_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services", file_name,
                                                                                 "GetRegisteredCarts_address"
                                                                                 , store_name)
        for index in range(0, len(results_address_details)):
            result_test_data['address_detail'] = results_address_details[index]
            del result_test_data['address_detail']['store_name']
            result_test_data_ls_address.append(result_test_data['address_detail'])
        final_dict['address_detail'] = result_test_data_ls_address

        result_country_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services", file_name,
                                                                                "GetRegisteredCarts_Country"
                                                                                , store_name)

        for index in range(0, len(result_country_details)):
            result_test_data['country_details'] = result_country_details[index]
            del result_test_data['country_details']['store_name']
            result_test_data_ls_country.append(result_test_data['country_details'])
        final_dict['country_details'] = result_test_data_ls_country

        result_state_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services", file_name,
                                                                              "GetRegisteredCarts_State",
                                                                              store_name)
        for index in range(0, len(result_state_details)):
            result_test_data['state_details'] = result_state_details[index]
            del result_test_data['state_details']['store_name']
            result_test_data_ls_state.append(result_test_data['state_details'])
        final_dict['state_details'] = result_test_data_ls_state

        return final_dict

    def generate_registered_carts_response(self, integrator_id, store_key, country_code, store_name, subscription_id,
                                           file_name, cart_name):
        test_data = self.get_registered_carts_response_from_test_data(store_name, file_name)
        ls_store_Details = []
        ls_warehouse_details = []
        ls_store = []
        obj_country = country(test_data['country_details'][0])
        obj_state = state(test_data['state_details'][0])
        obj_address = address(test_data['address_detail'][0], obj_country, obj_state,
                              test_data['address_detail'][0]['fax'], test_data['address_detail'][0]['website'])
        for ind in range(0, len(test_data['warehouses'])):
            obj_warehouse = warehouses(test_data['warehouses'][ind], obj_address)
            ls_warehouse_details.append(obj_warehouse)
        for index in range(0, len(test_data['store_details'])):
            obj_store_details = storedetails(test_data['store_details'][index][0])
            ls_store_Details.append(obj_store_details)
        obj_store = store(cart_name, store_key, country_code, ls_store_Details, ls_warehouse_details)
        ls_store.append(obj_store)
        obj_stores = stores(ls_store)
        obj_get_registered_carts = GetRegisteredCarts(integrator_id, subscription_id, obj_stores)
        resp_data = common_utils.convert_object_to_json(obj_get_registered_carts)
        return json.loads(resp_data)
