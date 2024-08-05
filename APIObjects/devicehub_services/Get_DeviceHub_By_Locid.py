from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *


class Get_DeviceHub_By_Locid:
    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_devicehub_by_locid_request(self, token_type, access_token, invalid_resource_path):
        if type(invalid_resource_path) == str:
            base_uri = (str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.getDeviceHubByLocId) + \
                       generate_random_alphanumeric_string() + "/").replace("v1", "v2")
        else:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.getDeviceHubByLocId)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Get request to check devicehub by loc id"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        return response

    def validate_device_name_exists_in_response_payload(self, response, device_name):
        results = {}
        dev_name = "{arg1}-{arg2}".format(arg1=device_name, arg2=str(self.app_config.env_cfg["env"]).lower())
        for index in range(0, len(response)):
            if str(response[index]['name']) == dev_name:

                if str(response[index]['status']) == "ONLINE":
                    results['status'] = True
                else:
                    results['status'] = False
                    results['error_msg'] = "Device Name {arg1} is offline".format(arg1=dev_name)
                return results
            else:
                results['status'] = False
                results['error_msg'] = "Device Name {arg1} is not present in the payload".format(arg1=dev_name)

        return results
