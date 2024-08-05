from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.save_envelope_coordinates import envelope_payload


class Save_Envelope_Print_Coordinate:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def post_save_coordinates(self, token_type, access_token, invalid_resource_path, context, is_sn_blank,
                              is_peripheral_id):
        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.save_coordinate) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.save_coordinate)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        self.custom_logger.info("Send Post request to save envelope co-ordinates"
                                "for base uri is {arg2}".format(arg2=base_uri))

        req_payload = self.generate_save_coordinate_payload(context, is_sn_blank,  is_peripheral_id)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for add devicehub"
                                "is {arg1}".format(arg1=response))
        return response

    def generate_save_coordinate_payload(self, context, is_sn_blank,  is_peripheral_id):

        if is_sn_blank:
            envelope_payload['serialNumber'] = ""
        else:
            envelope_payload['serialNumber'] = context['serial_number']

        if is_peripheral_id:
            envelope_payload["peripheralId"] = ""

        if is_peripheral_id and is_sn_blank:
            envelope_payload['serialNumber'] = ""
            envelope_payload["peripheralId"] = ""

        req_paylod = common_utils.convert_object_to_json(envelope_payload)
        return req_paylod
