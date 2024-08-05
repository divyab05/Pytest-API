from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils
from FrameworkUtilities.generic_utils import *


class Delete_DeviceHub_By_Sn:
    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_delete_deviceHub_by_sn_request(self, token_type, access_token, invalid_resource_path, sn_no):

        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] +
                device_hub_resource_path.DeleteDeviceHubBySN).replace("{sn_no}",
                                                                      generate_random_alphanumeric_string()) + "/"
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] +
                           device_hub_resource_path.DeleteDeviceHubBySN).replace("{sn_no}", sn_no)

        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send delete request to unregister device"
                                "and base uri is {arg2}".format(arg2=base_uri)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "delete",
                                                                   others=None)
        self.custom_logger.info("Response payload for unregister device"
                                "is {arg1}".format(arg1=response))
        return response
