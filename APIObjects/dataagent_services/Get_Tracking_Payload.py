from ConfigFiles.dataagent_services import resources_path
from FrameworkUtilities import common_utils, request_utils


class Get_Tracking_Payload:
    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_tracking_request(self, token_type, access_token, invalid_resource_path, get_env):

        base_uri = str(self.app_config.env_cfg['base_uri_tracking'] + resources_path.track_order).replace(
            "{time}", self.app_config.env_cfg['updatedAt_gt'])

        if token_type == "invalid_token":

            headers = common_utils.common_utils.set_request_headers_DA(self.app_config, False, access_token, get_env)
        else:
            headers = common_utils.common_utils.set_request_headers_DA(self.app_config, True, access_token, get_env)

        self.custom_logger.info("Send Get request to Check Get Order Tracking  API"
                                "for base uri is {arg2}".format(arg2=base_uri))

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for Get Order API is {arg1}".format(arg1=response))

        return response
