

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import generic_utils
from body_jsons.cseries_services.rate_requestbody import RateRequestBody


class DevicePostRateAPI:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token

        if str(self.app_config.env_cfg['env']) == "QA" and str(
                self.app_config.env_cfg['product_name']) == "sp360commercial":
            self.headers = {"Authorization": self.admin_token}
        elif str(self.app_config.env_cfg['env']) == "QA" and str(
                self.app_config.env_cfg['product_name']) == "sp360global":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}


        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])


    def generate_rate_api_request(self,test_data,carrierProfileID):

        RateRequestBody['carrierProfileId'] = carrierProfileID
        RateRequestBody['dimensionUnits'] = test_data['dimensionUnits']
        RateRequestBody['weightUnits'] = test_data['weightUnits']
        RateRequestBody['cultureCode'] = test_data['cultureCode']
        RateRequestBody['inductionPostalCode']= test_data['inductionPostalCode']
        RateRequestBody['mailClass']= test_data['mailClass']


        RateRequestBody['dateOfShipment'] =generic_utils.get_current_timestamp()

        #package details
        RateRequestBody['packageDetails']['packageId'] = test_data['packageId']
        RateRequestBody['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        RateRequestBody['packageDetails']['widthMeters'] = float(test_data['widthMeters'])
        RateRequestBody['packageDetails']['heightMeters'] = float(test_data['heightMeters'])
        RateRequestBody['packageDetails']['weightKilos'] = float(test_data['weightKilos'])

        # recipient details
        RateRequestBody['recipient']['isoCountry'] = test_data['recipientCountry']
        RateRequestBody['recipient']['postalCode'] = test_data['recipientPostalCode']
        RateRequestBody['recipient']['city'] = test_data['recipientCity']
        RateRequestBody['recipient']['state'] = test_data['recipientState']


        # sender details
        RateRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        RateRequestBody['sender']['city'] = test_data['senderCity']
        RateRequestBody['sender']['state'] = test_data['senderState']
        RateRequestBody['sender']['postalCode'] = test_data['senderPostalCode']


        #RateType
        RateRequestBody['rateType'] = test_data['rateType']


        req_paylod = common_utils.convert_object_to_json(RateRequestBody)

        return req_paylod



    def post_rateAPI(self,carrier,test_data,carrierProfileID):
        self.rate_request_endpoint = self.baseUri + "/" + carrier + "/rate?batch=false&rateSelector=false"
        print("rate endpoint ",self.rate_request_endpoint)

        requestBody = self.generate_rate_api_request(test_data,carrierProfileID)
        print("rate requestBody ", requestBody)



        print("request body ",requestBody)
        print("planner end point is ",self.rate_request_endpoint)



        resp = request_utils.send_request_based_on_http_method(self.rate_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)
        return resp

    # def post_rateAPI_UK(self, carrier, test_data):
    #     self.rate_request_endpoint = self.baseUri + "/" + carrier + "/rate"
    #
    #     requestBody = self.generate_rate_api_request(test_data)
    #
    #     print("request body ", requestBody)
    #     print("planner end point is ", self.rate_request_endpoint)
    #
    #     resp = request_utils.send_request_based_on_http_method(self.rate_request_endpoint, None, self.headers,
    #                                                            requestBody, "post",
    #                                                            None)
    #
    #     return resp

#      need to check rateType=commercial for US & UK


