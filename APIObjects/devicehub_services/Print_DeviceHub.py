from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import generic_utils, request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.print_body import print_payload


class Print_DeviceHub:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def generate_print_payload_request(self, transaction_id_status, test_data):

        print_payload['deviceId'] = "{arg1}-{arg2}".format(arg1=test_data['deviceId'],
                                                           arg2=str(self.app_config.env_cfg["env"]).lower())
        print_payload['peripheralId'] = test_data['peripheralId']
        print_payload['dhaId'] = "{arg1}-{arg2}".format(arg1=test_data['dhaId'],
                                                        arg2=str(self.app_config.env_cfg["env"]).lower())
        print_payload['documetUrls'][0] = test_data['documetUrls']
        print_payload['transactionId'] = generic_utils.generate_random_alphanumeric_string()
        print_payload['format'] = test_data['format']
        if transaction_id_status == "existing_transaction_id":
            print_payload['transactionId'] = "randomtranscationid-138890"
        print_payload['documentInfo']['type'] = test_data['type']
        print_payload['documentInfo']['formName'] = test_data['formName']

        req_paylod = common_utils.convert_object_to_json(print_payload)

        return req_paylod

    def send_post_print_request(self, token_type, access_token, invalid_resource_path, transaction_id_status,
                                test_data):

        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.print_request) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.print_request)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Post request to print"
                                "for base uri is {arg2}".format(arg2=base_uri))

        req_payload = self.generate_print_payload_request(transaction_id_status, test_data)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for print request"
                                "is {arg1}".format(arg1=response))
        return response
