import json

from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *
from body_jsons.devicehub_services.scale_read_body import scale_read_body


class Scale_Read:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_post_scale_request(self, token_type, access_token, invalid_resource_path, test_data):

        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.print_scale_request) + \
                         "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.print_scale_request)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Post request to print scale"
                                "for base uri is {arg2}".format(arg2=base_uri))

        req_payload = self.generate_post_payload_body_for_scale(test_data)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for print scale request"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_post_payload_body_for_scale(self, test_data):

        scale_read_obj = scale_read_body(test_data['version'], test_data['subscriptionId'],
                                         "{arg1}-{arg2}".format(arg1=test_data['dhaId'],
                                                                arg2=str(self.app_config.env_cfg["env"]).lower()),
                                         "{arg1}-{arg2}".format(arg1=test_data['deviceId'],
                                                                arg2=str(self.app_config.env_cfg["env"]).lower()),
                                         test_data['peripheralId'], test_data['zero'],
                                         test_data['type'])

        req_payload = common_utils.convert_object_to_json(scale_read_obj)

        return req_payload
