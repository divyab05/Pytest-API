from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils, generic_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.add_devicehub_body import add_devicehub_payload


class Post_Add_Devicehub:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_add_devicehub_request(self, token_type, access_token, invalid_resource_path, context, is_sn_blank,
                                   is_duplicate):
        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.Add_Devicehub) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.Add_Devicehub)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Post request to add devicehub"
                                "for base uri is {arg2}".format(arg2=base_uri))

        req_payload = self.generate_add_devicehub_payload(context, is_duplicate, is_sn_blank)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for add devicehub"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_add_devicehub_payload(self, context, is_duplicate, is_sn_blank):

        add_devicehub_payload['subscriptionId'] = self.app_config.env_cfg['subscriptionId']
        add_devicehub_payload['deviceHub'][0]['locId'] = self.app_config.env_cfg['locId']
        add_devicehub_payload['deviceHub'][0]['userId'] = self.app_config.env_cfg['userId']
        add_devicehub_payload['deviceHub'][0]['name'] = "{arg1}-{arg2}".format(arg1="Automation",
                                                                               arg2=generic_utils.generate_random_alphanumeric_string())

        if is_duplicate:
            add_devicehub_payload['deviceHub'][0]['serialNumber'] = context['serial_number']
        else:
            add_devicehub_payload['deviceHub'][0]['serialNumber'] = "{arg1}-{arg2}".format(arg1="Automation",
                                                                                           arg2=generic_utils.generate_random_alphanumeric_string())

        if is_sn_blank:
            add_devicehub_payload['deviceHub'][0]['serialNumber'] = ""

        context['serial_number'] = add_devicehub_payload['deviceHub'][0]['serialNumber']

        req_paylod = common_utils.convert_object_to_json(add_devicehub_payload)

        return req_paylod
