from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from conftest import context


class Generate_UnRegister_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_unregister_magento_delete_request(self, integratorid, store_key, token_type, access_token,connector,id):

        base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.UnregisterStore).replace(
            "{storeKey}", store_key)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
            headers['subscriptionId'] = id
        else:

            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)
            headers['subscriptionId'] = id
        self.custom_logger.info("Send delete request to unregister magento store"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "delete",
                                                                   others=None)
        self.custom_logger.info("Response payload for unregister magento store"
                                "is {arg1}".format(arg1=response))
        return response
