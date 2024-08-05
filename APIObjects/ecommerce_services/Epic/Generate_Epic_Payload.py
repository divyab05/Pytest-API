import json
from APIObjects.ecommerce_services.response_objects.GetRegisteredCarts.storeDetails import storedetails
from APIObjects.ecommerce_services.response_objects.magento1.OnboardMagento1 import onboard_magento1
from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from body_jsons.ecommerce_services.Epic.onboard_epic_store import Onboard_Epic_Store_RequestObject
from body_jsons.ecommerce_services.OnboardMagentoStore.onboard_magento_store import Onboard_Magento_Store_RequestObject
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class Generate_Epic_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_onboard_epic_post_request(self, test_data, integratorid, access_token, token_type,
                                       invalid_resource_path, connector):
        if test_data['TokenURL'] == "None":
            TokenURL = ""
        else:
            TokenURL = test_data['TokenURL']

        if test_data['WritebackURL'] == "None":
            WritebackURL = ""
        else:
            WritebackURL = test_data['WritebackURL']

        if test_data['clientId'] == "None":
            clientId = ""
        else:
            clientId = test_data['clientId']

        onboard_obj = Onboard_Epic_Store_RequestObject(TokenURL, WritebackURL, clientId)
        req_payload = common_utils.convert_object_to_json(onboard_obj)

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OnBoardEpicStore) \
                       + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.OnBoardEpicStore)

        self.custom_logger.info("Request payload for the onboard_epic_post_request "
                                "api {arg1}".format(arg1=req_payload))
        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,
                                                                 connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,
                                                                 connector,False)

        self.custom_logger.info("Send post request to onboard Epic store"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for onboard Epic store"
                                "is {arg1}".format(arg1=response))

        return response

    def get_epic_onboard_test_data(self, store_name):
        result_test_data = {}
        result_test_data_ls_store = []
        final_dict = {}

        results_store_details = common_utils.read_excel_data_store_by_col_name("ecommerce_services",
                                                                               "EpicTestData.xlsx",
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
        test_data = self.get_epic_onboard_test_data(store_name)
        ls_store_Details = []
        for index in range(0, len(test_data['store_details'])):
            obj_store_details = storedetails(test_data['store_details'][index][0])
            ls_store_Details.append(obj_store_details)
        onboard_obj = onboard_magento1(apiUrl, accessToken, ls_store_Details, None,
                                       message)
        resp_data = common_utils.convert_object_to_json(onboard_obj)
        return json.loads(resp_data)
