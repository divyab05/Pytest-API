from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from body_jsons.devicehub_services.save_envelope_coordinates import envelope_payload


class Get_Envelope_Print_Coordinates:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_devicehub_save_envelope_coordinates(self, token_type, access_token, is_peripheral_id_blank,
                                                     is_serial_no_blank):

        base_uri = str(
            self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.get_coordinate)
        if token_type == "invalid_token":
            headers = common_utils.set_devicehub_request_headers(self.app_config, False, access_token)
        else:
            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

        request_params = self.get_request_parmas(is_peripheral_id_blank, is_serial_no_blank)

        self.custom_logger.info("Send Get request to check save co-ordinates for Envelope"
                                "for base uri is {arg2}".format(arg2=base_uri))
        response = request_utils.send_request_based_on_http_method(base_uri, request_params, headers, None, "get",
                                                                   None)
        self.custom_logger.info("Response payload for save coordinates against serial number and peripheral id"
                                "is {arg1}".format(arg1=response))
        return response

    def get_request_parmas(self, is_peripheral_id_blank, is_serial_no_blank):
        if is_peripheral_id_blank:
            request_params = {"peripheralId": "",
                              "serialNumber": envelope_payload["serialNumber"]}
        elif is_serial_no_blank:
            request_params = {"peripheralId": "",
                              "serialNumber": envelope_payload["serialNumber"]}
        elif is_serial_no_blank and is_peripheral_id_blank:
            request_params = {"peripheralId": "",
                              "serialNumber": ""}
        else:
            request_params = {"peripheralId": envelope_payload['peripheralId'],
                              "serialNumber": envelope_payload["serialNumber"]}

        return request_params
