import json
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.storeDetails import storedetails
from APIObjects.ecommerce_services.response_objects.magento1.OnboardMagento1 import onboard_magento1
from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from body_jsons.ecommerce_services.OnboardMagentoStore.onboard_magento_store import Onboard_Magento_Store_RequestObject
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class Generate_Magento_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_onboard_magento_post_request(self, test_data, integratorid, access_token, token_type,
                                          invalid_resource_path, connector,context):
        if test_data['apiUrl'] == "None":
            apiUrl = ""
        else:
            apiUrl = test_data['apiUrl']

        if test_data['accessToken'] == "None":
            accessToken = ""
        else:
            accessToken = test_data['accessToken']

        onboard_obj = Onboard_Magento_Store_RequestObject(apiUrl, accessToken)
        req_payload = common_utils.convert_object_to_json(onboard_obj)

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OnBoardMagentoStore) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OnBoardMagentoStore)

        self.custom_logger.info("Request payload for the onboard_magento_post_request "
                                "api {arg1}".format(arg1=req_payload))
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,
                                                                 connector, False)
            self.custom_logger.info("Send post request to onboard Magento store"
                                    "and base uri is {arg2}".format(arg2=base_uri)
                                    )

        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,
                                                                 connector, False)

            self.custom_logger.info("Send post request to onboard Magento store"
                                    "and base uri is {arg2}".format(arg2=base_uri)
                                    )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                              invalid_resource_path)
        context['id1'] = headers['subscriptionId']
        if response['response_code'] == 409:
            headers1 = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,
                                                                  connector, True)
            self.custom_logger.info("Send post request to onboard Magento store"
                                    "and base uri is {arg2}".format(arg2=base_uri)
                                    )
            response = request_utils.send_request_based_on_http_method(base_uri, None, headers1, req_payload,
                                                                       "post",
                                                                       invalid_resource_path)
            context['id1'] = headers1['subscriptionId']
            self.custom_logger.info("Response payload for onboard magento store"
                                    "is {arg1}".format(arg1=response))
            return response

        return response

    def get_magento_onboard_test_data(self, store_name):
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

    def generate_onboard_response(self, apiUrl, accessToken, store_name, message):
        test_data = self.get_magento_onboard_test_data(store_name)
        ls_store_Details = []
        for index in range(0, len(test_data['store_details'])):
            obj_store_details = storedetails(test_data['store_details'][index][0])
            ls_store_Details.append(obj_store_details)
        onboard_obj = onboard_magento1(apiUrl, accessToken, ls_store_Details, None,
                                       message)
        resp_data = common_utils.convert_object_to_json(onboard_obj)
        return json.loads(resp_data)
