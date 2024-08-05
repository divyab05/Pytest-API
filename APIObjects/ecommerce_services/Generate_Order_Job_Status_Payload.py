import polling
from ConfigFiles.ecommerce_services import API_Resource_Path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils


class Generate_Order_Job_status:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_order_job_status_request(self,integratorid, transaction_id, token_type, access_token,
                                          invalid_resource_path,connector):
        base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetOrderJobStatus).replace(
            "{transaction_id}", transaction_id)

        if token_type == "invalid_token":
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False, access_token,connector,False)
        else:
            headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)

        self.custom_logger.info("Send Get request to Check Get Order Job Status API"
                                "for base uri is {arg2}".format(arg2=base_uri))

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Order Job Status API"
                                "is {arg1}".format(arg1=response))

        return response

    def validate_invalid_header_msg(self, msg):
        if msg.__contains__("X-PB-TransactionId"):
            return True
        else:
            return False

    def store_job_status(self, response, context, integratorid, transaction_id, token_type, access_token,
                         invalid_resource_path,connector):

        if response['jobStatus'] == 'completed':
            context['record_id'] = response['recordId']
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_ecomm'] + API_Resource_Path.GetOrderJobStatus).replace(
                "{transaction_id}", transaction_id)
            if token_type == "invalid_token":
                headers = common_utils.set_request_headers_connector(integratorid, self.app_config, False,
                                                           access_token,connector,False)
            else:
                headers = common_utils.set_request_headers_connector(integratorid, self.app_config, True, access_token,connector,False)

            result = polling.poll(
                lambda: request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                        invalid_resource_path),
                step=3,
                timeout=60, check_success=self.check_job_completion)
            print("Inside Polling")
            context['record_id'] = result['response_body']['recordId']

    def check_job_completion(self, response):
        if response['response_body']['jobStatus'] == 'completed':
            return True
        else:
            return False
