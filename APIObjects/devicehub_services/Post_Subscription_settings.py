from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.post_subscription_settings_body import post_subscription_settings_payload


class Post_Subscription_settings:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_post_subscription_settings_request(self, token_type, access_token, invalid_resource_path, auto_update_flg,
                                                error_condition):
        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.SubscriptionSettings) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.SubscriptionSettings)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Post request to print scale"
                                "for base uri is {arg2}".format(arg2=base_uri))

        if error_condition:
            if auto_update_flg is None:
                post_subscription_settings_payload["automaticUpdatesDisabled"] = ""
            else:
                post_subscription_settings_payload["automaticUpdatesDisabled"] = ""
                post_subscription_settings_payload["subscriptionId"] = ""
        else:
            post_subscription_settings_payload['automaticUpdatesDisabled'] = auto_update_flg
            post_subscription_settings_payload['subscriptionId'] = self.app_config.env_cfg['subscriptionId']

        req_payload = common_utils.convert_object_to_json(post_subscription_settings_payload)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for post subscription api request"
                                "is {arg1}".format(arg1=response))
        return response
