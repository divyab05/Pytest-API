import json

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from body_jsons.cseries_services.us_printlabel_domestic import domestic_print_payload
from body_jsons.cseries_services.us_printlabel_international import international_print_payload


class ShippingLabel:

    def __init__(self, app_config, access_token, carrier):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token

        if str(self.app_config.env_cfg['env'])=="QA":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}
        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])
        self.print_request_endpoint = self.baseUri + "/" + carrier + "/shipping-label"

    def generate_domestic_print_payload_request(self, test_data,carrierProfileId):

        domestic_print_payload['carrierProfileId'] = carrierProfileId

        # sender details

        domestic_print_payload['sender']['isoCountry'] = test_data['SenderCountry']
        domestic_print_payload['sender']['fullName'] = test_data['SenderFullName']
        domestic_print_payload['sender']['company'] = test_data['SenderCompany']
        domestic_print_payload['sender']['streetLine1'] = test_data['SenderStreetLine-1']
        # domestic_print_payload['sender']['streetLine2'] =test_data['SenderStreetLine-2']
        domestic_print_payload['sender']['postalCode'] = test_data['SenderPostalCode']
        domestic_print_payload['sender']['city'] = test_data['SenderCity']
        domestic_print_payload['sender']['state'] = test_data['SenderState']
        # print("Sendr Email check  ",self.checkNoneValue(test_data['SenderEmail']))

        domestic_print_payload['sender']['email'] = test_data['SenderEmail']
        domestic_print_payload['sender']['phone'] = test_data['SenderPhone']

        # recipient details
        domestic_print_payload['recipient']['isoCountry'] = test_data['RecipientCountry']
        domestic_print_payload['recipient']['fullName'] = test_data['RecipientFullName']
        domestic_print_payload['recipient']['company'] = test_data['RecipientCompany']
        domestic_print_payload['recipient']['streetLine1'] = test_data['RecipientStreetLine-1']
        domestic_print_payload['recipient']['streetLine2'] = test_data['RecipientStreetLine-2']
        domestic_print_payload['recipient']['postalCode'] = test_data['RecipientPostalCode']
        domestic_print_payload['recipient']['city'] = test_data['RecipientCity']
        domestic_print_payload['recipient']['state'] = test_data['RecipientState']
        domestic_print_payload['recipient']['email'] = test_data['RecipientEmail']
        domestic_print_payload['recipient']['phone'] = test_data['RecipientPhone']
        # domestic_print_payload['recipient']['militaryAddress'] =bool(test_data['IsRecipientMilitaryAddress'])

        # package details
        domestic_print_payload['packageDetails']['packageDisplayId'] = test_data['packageDisplayId']
        domestic_print_payload['packageDetails']['packageId'] = test_data['packageId']
        domestic_print_payload['packageDetails']['packageName'] = test_data['packageName']

        # Dimension details
        domestic_print_payload['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        domestic_print_payload['packageDetails']['widthMeters'] = float(test_data['widthMeters'])
        domestic_print_payload['packageDetails']['heightMeters'] = float(test_data['heightMeters'])
        domestic_print_payload['packageDetails']['weightKilos'] = float(test_data['weightKilos'])

        # Service Details
        domestic_print_payload['displayMailClass'] = test_data['displayMailClass']
        domestic_print_payload['mailClass'] = test_data['mailClass']

        req_paylod = common_utils.convert_object_to_json(domestic_print_payload)

        return req_paylod

    def generate_international_print_payload_request(self, test_data,carrierProfileId):

        international_print_payload['carrierProfileId'] = carrierProfileId

        # sender details
        international_print_payload['sender']['isoCountry'] = test_data['SenderCountry']
        international_print_payload['sender']['fullName'] = test_data['SenderFullName']
        international_print_payload['sender']['company'] = test_data['SenderCompany']
        international_print_payload['sender']['streetLine1'] = test_data['SenderStreetLine-1']
        # international_print_payload['sender']['streetLine2'] =test_data['SenderStreetLine-2']
        international_print_payload['sender']['postalCode'] = test_data['SenderPostalCode']
        international_print_payload['sender']['city'] = test_data['SenderCity']
        international_print_payload['sender']['state'] = test_data['SenderState']
        # print("Sendr Email check  ",self.checkNoneValue(test_data['SenderEmail']))

        international_print_payload['sender']['email'] = test_data['SenderEmail']
        international_print_payload['sender']['phone'] = test_data['SenderPhone']

        # recipient details
        international_print_payload['recipient']['isoCountry'] = test_data['RecipientCountry']
        international_print_payload['recipient']['fullName'] = test_data['RecipientFullName']
        international_print_payload['recipient']['company'] = test_data['RecipientCompany']
        international_print_payload['recipient']['streetLine1'] = test_data['RecipientStreetLine-1']
        international_print_payload['recipient']['streetLine2'] = test_data['RecipientStreetLine-2']
        international_print_payload['recipient']['postalCode'] = test_data['RecipientPostalCode']
        international_print_payload['recipient']['city'] = test_data['RecipientCity']
        international_print_payload['recipient']['state'] = test_data['RecipientState']
        international_print_payload['recipient']['email'] = test_data['RecipientEmail']
        international_print_payload['recipient']['phone'] = test_data['RecipientPhone']
        # international_print_payload['recipient']['militaryAddress'] =bool(test_data['IsRecipientMilitaryAddress'])

        # package details
        international_print_payload['packageDetails']['packageDisplayId'] = test_data['packageDisplayId']
        international_print_payload['packageDetails']['packageId'] = test_data['packageId']
        international_print_payload['packageDetails']['packageName'] = test_data['packageName']

        # Dimension details
        international_print_payload['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        international_print_payload['packageDetails']['widthMeters'] = float(test_data['widthMeters'])
        international_print_payload['packageDetails']['heightMeters'] = float(test_data['heightMeters'])
        international_print_payload['packageDetails']['weightKilos'] = float(test_data['weightKilos'])

        # Service Details
        international_print_payload['displayMailClass'] = test_data['displayMailClass']
        international_print_payload['mailClass'] = test_data['mailClass']

        # Custom details
        international_print_payload['customInfo']['eelpfc'] = test_data['customEelpfc']
        international_print_payload['customInfo']['exportReason'] = test_data['customExportReason']
        international_print_payload['packageContent'][0]['originCountry'] = test_data['packageOriginCountry']

        req_paylod = common_utils.convert_object_to_json(international_print_payload)

        return req_paylod

    def send_print_request(self, test_data, labelType,carrierProfileId):

        # print_request_endpoint=self.endpoint + "/usps/shipping-label"

        if labelType == "domestic":
            requestBody = self.generate_domestic_print_payload_request(test_data,carrierProfileId)
        else:
            requestBody = self.generate_international_print_payload_request(test_data,carrierProfileId)

        print("request Body is ", requestBody)
        print("request API is ", self.print_request_endpoint)
        # print("header is",self.headers)

        # resp = self.api.post_api_response(endpoint=print_request_endpoint, headers=self.headers, body=requestBody)

        resp = request_utils.send_request_based_on_http_method(self.print_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp
