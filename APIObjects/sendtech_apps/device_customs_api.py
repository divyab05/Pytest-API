

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import generic_utils
from body_jsons.cseries_services.customs_api_requestbody import CustomsAPIRequestBody


class DeviceCustomsAPI:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token

        if str(self.app_config.env_cfg['env'])=="QA" and str(self.app_config.env_cfg['product_name'])=="sp360commercial":
            self.headers = {"Authorization": self.admin_token}
        elif str(self.app_config.env_cfg['env'])=="QA" and str(self.app_config.env_cfg['product_name'])=="sp360global":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}

        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])


    def generate_customs_api_request(self,test_data):

        # package details
        CustomsAPIRequestBody['packageDetails']['lengthMeters'] = float(test_data['packageLengthMeter'])
        CustomsAPIRequestBody['packageDetails']['widthMeters'] = float(test_data['packageWidthMeter'])
        CustomsAPIRequestBody['packageDetails']['heightMeters'] = float(test_data['packageHeightMeter'])
        CustomsAPIRequestBody['packageDetails']['packageId']= test_data['packageId']
        CustomsAPIRequestBody['packageDetails']['weightKilos']= float(test_data['packageWeight'])

        # recipient details
        CustomsAPIRequestBody['recipient']['isoCountry'] = test_data['recipientCountry']
        CustomsAPIRequestBody['recipient']['fullName'] = test_data['recipientName']
        CustomsAPIRequestBody['recipient']['postalCode'] = test_data['recipientPostalCode']
        CustomsAPIRequestBody['recipient']['streetLine1'] = test_data['recipientStreetLine']
        CustomsAPIRequestBody['recipient']['city'] = test_data['recipientCity']
        CustomsAPIRequestBody['recipient']['state'] = test_data['recipientState']
        CustomsAPIRequestBody['recipient']['phone'] = test_data['recipientPhone']

        # sender details
        CustomsAPIRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        CustomsAPIRequestBody['sender']['fullName'] = test_data['senderName']
        CustomsAPIRequestBody['sender']['company'] = test_data['senderCompany']
        CustomsAPIRequestBody['sender']['postalCode'] = test_data['senderPostalCode']
        CustomsAPIRequestBody['sender']['streetLine1'] = test_data['senderStreetLine']
        CustomsAPIRequestBody['sender']['city'] = test_data['senderCity']
        CustomsAPIRequestBody['sender']['state'] = test_data['senderState']
        CustomsAPIRequestBody['sender']['phone'] = test_data['senderPhone']



        req_paylod = common_utils.convert_object_to_json(CustomsAPIRequestBody)

        return req_paylod



    def post_customAPI(self,carrier,test_data):
        self.customs_api_request_endpoint = self.baseUri + "/" + carrier + "/customs/requirements"

        requestBody = self.generate_customs_api_request(test_data)

        print("request body ",requestBody)
        print("planner end point is ",self.customs_api_request_endpoint)





        resp = request_utils.send_request_based_on_http_method(self.customs_api_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp




