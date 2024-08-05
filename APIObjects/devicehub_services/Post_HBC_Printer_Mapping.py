from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils, generic_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.add_devicehub_body import add_devicehub_payload
from body_jsons.devicehub_services.print_mapping_body import printer_mapping


class Post_HBC_Printer_Mapping:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_post_hbc_printer_mapping(self, hbc_token, invalid_resource_path, serial_number, printer_name,
                                      alias_name):
        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['hbc_shipping_api'] + device_hub_resource_path.hbc_printer_mapping) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['hbc_shipping_api'] + device_hub_resource_path.hbc_printer_mapping)

        headers = {"Authorization": "{arg1}{arg2}".format(arg1="Bearer ", arg2=hbc_token)}

        req_payload = self.generate_printer_mapping_payload(serial_number, printer_name, alias_name)
        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for hbc printer api devicehub"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_printer_mapping_payload(self, serial_number, printer_name, alias_name):

        printer_mapping['serialNumber'] = serial_number
        printer_mapping['printerName'] = printer_name
        printer_mapping['alias'] = alias_name

        req_paylod = common_utils.convert_object_to_json(printer_mapping)
        return req_paylod
