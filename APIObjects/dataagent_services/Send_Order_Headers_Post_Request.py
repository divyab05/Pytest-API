from ConfigFiles.dataagent_services import resources_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from body_jsons.dataagent_services.body_json_headers import body_json


class Send_Order_Headers_Post_Request:
    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def Send_Order_Headers_Post_Request(self, token_type, access_token,
                                        invalid_resource_path, get_env):
        new_data = common_utils.convert_object_to_json(body_json)
        # req_payload = self.generate_post_request_payload()
        base_uri = str(self.app_config.env_cfg['base_uri_headers'] + resources_path.order_headers)

        if token_type == "invalid_token":
            headers = \
                common_utils.set_request_headers_DA(self.app_config, False, access_token, get_env)
        else:
            headers = common_utils.set_request_headers_DA(self.app_config, True, access_token, get_env)

        self.custom_logger.info("Send post request to order header"
                                "and base uri is {arg2} and request_payload is {arg1}".format(arg2=base_uri,
                                                                                              arg1=new_data)
                                )
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, new_data, "post",
                                                                   invalid_resource_path)

        self.custom_logger.info("Response payload for order header api"
                                "is {arg1}".format(arg1=response))
        return response
