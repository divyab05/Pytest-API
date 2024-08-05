from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class Get_hbc_printer_mapping:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_hbc_printer_mapping_request(self, hbc_token, invalid_resource_path, alias_name):
        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['hbc_shipping_api'] +
                device_hub_resource_path.get_hbc_printer_mapping).replace("{alias_name}",
                                                                          generate_random_alphanumeric_string()) + "/"
        else:
            base_uri = str(self.app_config.env_cfg['hbc_shipping_api'] +
                           device_hub_resource_path.get_hbc_printer_mapping).replace("{alias_name}", alias_name)

        headers = {"Authorization": "{arg1}{arg2}".format(arg1="Bearer ", arg2=hbc_token)}

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                   others=None)
        self.custom_logger.info("Response payload for get hbc printer mapping api devicehub"
                                "is {arg1}".format(arg1=response))
        print(response)
        return response
