from ConfigFiles.ecommerce_services import API_Resource_Path
from APIObjects.ecommerce_services.response_objects.OnboardShopifyDataBucket import *
from FrameworkUtilities.common_utils import common_utils
from body_jsons.ecommerce_services.onboard_shopify_store import Onboard_Shopify_Store_RequestObject
from FrameworkUtilities import request_utils


class Generate_Shopify_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_onboard_shopify_post_request(self, test_data, integratorid, access_token, token_type):

        if test_data['storeUrl'] == "None":
            store_url = ""
        else:
            store_url = test_data['storeUrl']

        if test_data['apIkey'] == "None":
            api_key = ""
        else:
            api_key = test_data['apIkey']

        if test_data['apiPassword'] == "None":
            api_password = ""
        else:
            api_password = test_data['apiPassword']

        if test_data['sharedSecret'] == "None":
            shared_secret = ""
        else:
            shared_secret = test_data['sharedSecret']

        onboard_obj = Onboard_Shopify_Store_RequestObject(store_url, api_key,
                                                          api_password, shared_secret)
        req_payload = common_utils.convert_object_to_json(onboard_obj)

        self.custom_logger.info("Request payload for the onboard_shopify_post_request "
                                "api {arg1}".format(arg1=req_payload))
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)
        base_uri = self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OnBoardShopifyStore
        self.custom_logger.info("Send post request to onboard shopify store"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   others=None)
        self.custom_logger.info("Response payload for onboard shopify store"
                                "is {arg1}".format(arg1=response))
        return response

    def send_unregister_shopify_delete_request(self, integratorid, store_key, token_type, access_token):

        base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.UnregisterStore).replace(
            "{storeKey}", store_key)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, False, access_token)
        else:
            headers = common_utils.set_request_headers("shopify", integratorid, self.app_config, True, access_token)

        self.custom_logger.info("Send delete request to unregister shopify store"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "delete",
                                                                   others=None)
        self.custom_logger.info("Response payload for unregister shopify store"
                                "is {arg1}".format(arg1=response))
        return response

    def validate_shopify_onboard_api_response_payload(self, test_data, response_json, custom_logger):
        results = []
        results.append(self.get_store_details_results(test_data, response_json, custom_logger))
        results.append(self.get_warehouse_details_results(test_data, response_json, custom_logger))
        response_address_details = common_utils.parse_json_and_return_data_based_on_parent_key(response_json,
                                                                                               'warehouses', 'address')
        results.append(self.get_address_details_results(test_data, response_address_details, custom_logger))

        response_country_details = common_utils.parse_json_and_return_data_based_on_key(response_address_details,
                                                                                        'country')
        country_details = country_data_bucket(test_data)
        results_country_details = common_utils.compare_expected_actual_response(country_details['country']
                                                                                , response_country_details
                                                                                , custom_logger)
        results.append(results_country_details)

        response_state_details = common_utils.parse_json_and_return_data_based_on_key(response_address_details,
                                                                                      'state')
        state_details = state_data_bucket(test_data)
        results_state_details = common_utils.compare_expected_actual_response(state_details['state']
                                                                              , response_state_details
                                                                              , custom_logger)
        results.append(results_state_details)
        final_results = common_utils.remove_null_values_dict(results)

        return final_results

    def get_store_details_results(self, test_data, response_json, custom_logger):

        response_store_details = common_utils.parse_json_and_return_data_based_on_key(response_json, 'storesDetails')
        store_details = store_details_data_bucket(test_data)
        results_store_details = common_utils.compare_expected_actual_response(
            store_details['storesDetails'],
            response_store_details[0], custom_logger)
        return results_store_details

    def get_warehouse_details_results(self, test_data, response_json, custom_logger):
        response_ware_house_details = common_utils.parse_json_and_return_data_based_on_key(response_json, 'warehouses')
        ware_house_details = ware_house_details_data_bucket(test_data)
        results_ware_house_details = common_utils.compare_expected_actual_response(
            ware_house_details['warehouses'],
            response_ware_house_details[0], custom_logger)
        return results_ware_house_details

    def get_address_details_results(self, test_data, response_address_details, custom_logger):
        address_details = address_data_bucket(test_data)
        results_address_details = common_utils.compare_expected_actual_response(
            address_details['address'],
            response_address_details, custom_logger)
        return results_address_details
