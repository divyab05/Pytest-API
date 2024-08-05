from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import request_utils


class Get_DeviceHub_By_UserID:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_devicehub_by_userid_request(self, token_type, access_token):

        base_uri = str(
            self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.getDeviceHubByUserID) + "/" + \
                   self.app_config.env_cfg['GetuserId']

        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Get request to check devicehub by user id"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   None)
        return response
