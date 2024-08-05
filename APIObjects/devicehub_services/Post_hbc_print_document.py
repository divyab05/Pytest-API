import os

import pytest

from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string
from body_jsons.devicehub_services.hbc_base64_4x6 import body_base64_4x6
from body_jsons.devicehub_services.hbc_base64_8x11 import body_base64_8x11
from body_jsons.devicehub_services.hbc_print_document import hbc_print_document
from body_jsons.devicehub_services.printv2_body import printv2_body


class Post_hbc_print_document:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def generate_print_payload_request(self, test_data):

        if test_data['documentType'] == "pdf" and test_data['dataType'] == "base64" and test_data['formName'] == "8x11":
            hbc_print_document['data'] = body_base64_8x11['data']
        elif test_data['documentType'] == "pdf" and test_data['dataType'] == "base64" and test_data[
            'formName'] == "4x6":
            hbc_print_document['data'] = body_base64_4x6['data']
        else:
            hbc_print_document['data'] = self.check_none_type_and_return_blank(test_data['data'])
        hbc_print_document['documentType'] = self.check_none_type_and_return_blank(test_data['documentType'])
        hbc_print_document['dataType'] = self.check_none_type_and_return_blank(test_data['dataType'])
        hbc_print_document['formName'] = self.check_none_type_and_return_blank(test_data['formName'])
        hbc_print_document['printerAliasName'] = self.check_none_type_and_return_blank(test_data['printerAliasName'])

        req_paylod = common_utils.convert_object_to_json(hbc_print_document)
        return req_paylod

    def send_hbc_post_print_document_request(self, hbc_token, invalid_resource_path, test_data):

        if type(invalid_resource_path) == str:
            base_uri = str(
                self.app_config.env_cfg['hbc_shipping_api'] + device_hub_resource_path.hbc_print_document) + \
                       "/" + generate_random_alphanumeric_string()
        else:
            base_uri = str(self.app_config.env_cfg['hbc_shipping_api'] + device_hub_resource_path.hbc_print_document)

        headers = {"Authorization": "{arg1}{arg2}".format(arg1="Bearer ", arg2=hbc_token)}

        req_payload = self.generate_print_payload_request(test_data)

        response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                   invalid_resource_path)
        self.custom_logger.info("Response payload for print document for hbc api"
                                "is {arg1}".format(arg1=response))

        return response

    def check_none_type_and_return_blank(self, excel_data):
        if excel_data != "None":
            return excel_data
        else:
            return ""

    def read_txt_file(self, file_name):
        file_path = os.getcwd() + "/TestData/{arg1}/{arg2}".format(arg1="devicehub_services", arg2=file_name)
        with open(file_path) as f:
            contents = f.read()
        return contents

    def send_printv2_post_request(self, access_token, invalid_resource_path, test_data):
        if test_data['is_Runnable'] == "True":

            if type(invalid_resource_path) == str:
                base_uri = str(
                    self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.printv2_request) + \
                           "/" + generate_random_alphanumeric_string()
            else:
                base_uri = str(self.app_config.env_cfg['base_uri_devicehub'] + device_hub_resource_path.printv2_request)

            headers = common_utils.set_devicehub_request_headers(self.app_config, True, access_token)

            self.custom_logger.info("Send Post request to print"
                                    "for base uri is {arg2}".format(arg2=base_uri))
            req_payload = self.generate_printv2_payload_request(test_data)
            print(req_payload)

            response = request_utils.send_request_based_on_http_method(base_uri, None, headers, req_payload, "post",
                                                                       invalid_resource_path)
            self.custom_logger.info("Response payload for print v2 api"
                                    "is {arg1} for test scenario {arg2}".format(arg1=response,
                                                                                arg2=test_data['TC_Scenario']))

            return response
        else:
            pytest.skip("Test case runnable is set to false in test_data_sheet for scenario "
                        "{arg1}".format(arg1=test_data['TC_Scenario']))

    def generate_printv2_payload_request(self, test_data):

        printv2_body['payload'][0]['data'] = self.check_none_type_and_return_blank(test_data['data'])
        printv2_body['payload'][0]['documentType'] = self.check_none_type_and_return_blank(test_data['documentType'])
        printv2_body['payload'][0]['dataType'] = self.check_none_type_and_return_blank(test_data['dataType'])
        printv2_body['payload'][0]['formName'] = self.check_none_type_and_return_blank(test_data['formName'])
        printv2_body['payload'][0]['printType'] = self.check_none_type_and_return_blank(test_data['printType'])
        printv2_body['payload'][0]['name'] = generate_random_alphanumeric_string()
        printv2_body['payload'][0]['printerName'] = self.check_none_type_and_return_blank(test_data['printerName'])
        printv2_body['serialNumber'] = self.check_none_type_and_return_blank(test_data['serialNumber'])
        printv2_body['jobId'] = generate_random_alphanumeric_string()
        printv2_body['deviceInfo'][0]['serialNumber'] = self.check_none_type_and_return_blank(test_data['serialNumber'])
        printv2_body['deviceInfo'][0]['printerName'][0] = self.check_none_type_and_return_blank(test_data['printerName'])
        req_paylod = common_utils.convert_object_to_json(printv2_body)
        return req_paylod
