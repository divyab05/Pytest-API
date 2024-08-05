from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string, generate_random_number


class Get_Sync_Order_Payload:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_sync_order_request(self, integratorid, token_type, access_token, invalid_resource_path, context,connector):

        if type(invalid_resource_path) == str:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.SyncOrder).replace("?wh=true"
                                ,"/{arg1}".format(arg1=generate_random_alphanumeric_string()))
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.SyncOrder)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)

        unique_no = generate_random_number(5)
        headers['X-PB-TransactionId'] = str(self.app_config.env_cfg['X-PB-TransactionId']).replace('{unique_no}',
                                                                                                   unique_no)
        context['X-PB-TransactionId'] = headers['X-PB-TransactionId']

        self.custom_logger.info("Send Get Sync Order Request "
                                "for base uri is {arg2}".format(arg2=base_uri))

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Sync Order Request"
                                "is {arg1}".format(arg1=response))
        return response
