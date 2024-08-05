from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from body_jsons.cseries_services.us_printlabel_domestic import domestic_print_payload


class HistoryTransactions:
    def __init__(self, app_config, access_token):
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



    def printUspsLabel(self,carrierProfieID):

        domestic_print_payload['carrierProfileId'] = carrierProfieID

        domestic_print_payload['packageDetails']['packageDisplayId'] = "PKG"
        domestic_print_payload['packageDetails']['packageId'] = "PKG"
        domestic_print_payload['packageDetails']['packageName'] = "Customer Packaging"

        # service details
        domestic_print_payload['displayMailClass'] = "Priority Mail Express™"
        domestic_print_payload['mailClass'] = "EM"

        # Dimension details
        domestic_print_payload['packageDetails']['lengthMeters'] = 0.304
        domestic_print_payload['packageDetails']['widthMeters'] = 0.304
        domestic_print_payload['packageDetails']['heightMeters'] = 0.304
        domestic_print_payload['packageDetails']['weightKilos'] = 5.00

        self.print_request_endpoint = self.baseUri + "/usps/shipping-label"
        requestBody = common_utils.convert_object_to_json(domestic_print_payload)
        # print("print api request body",requestBody)
        response = request_utils.send_request_based_on_http_method(self.print_request_endpoint, None, self.headers,
                                                                   requestBody, "post", None)

        return response

    def printUpsLabel(self,carrierProfileID):

        domestic_print_payload['carrierProfileId'] = carrierProfileID
        #package details
        domestic_print_payload['packageDetails']['packageDisplayId'] = "PKG"
        domestic_print_payload['packageDetails']['packageId'] = "PKG"
        domestic_print_payload['packageDetails']['packageName'] = "Customer Packaging"

        # service details
        domestic_print_payload['displayMailClass'] = "UPS Next Day Air® Early"
        domestic_print_payload['mailClass'] = "NDA_AM"

        # Dimension details
        domestic_print_payload['packageDetails']['lengthMeters'] = 0.2286
        domestic_print_payload['packageDetails']['widthMeters'] = 0.2286
        domestic_print_payload['packageDetails']['heightMeters'] = 0.2286
        domestic_print_payload['packageDetails']['weightKilos'] = 4.08

        self.print_request_endpoint = self.baseUri + "/ups/shipping-label"

        requestBody = common_utils.convert_object_to_json(domestic_print_payload)
        response = request_utils.send_request_based_on_http_method(self.print_request_endpoint, None, self.headers,
                                                                   requestBody, "post", None)

        return response

    def printFedExLabel(self,carrierProfileID):

        domestic_print_payload['carrierProfileId'] = carrierProfileID

        #packageDetails
        domestic_print_payload['packageDetails']['packageDisplayId'] = "PKG"
        domestic_print_payload['packageDetails']['packageId'] = "PKG"
        domestic_print_payload['packageDetails']['packageName'] = "Your Packaging"

        #service details
        domestic_print_payload['displayMailClass'] = "FedEx Express Saver®"
        domestic_print_payload['mailClass'] = "3DA"

        # Dimension details
        domestic_print_payload['packageDetails']['lengthMeters'] = 0.304
        domestic_print_payload['packageDetails']['widthMeters'] = 0.304
        domestic_print_payload['packageDetails']['heightMeters'] = 0.304
        domestic_print_payload['packageDetails']['weightKilos'] = 5.00

        self.print_request_endpoint = self.baseUri + "/fedex/shipping-label"

        requestBody = common_utils.convert_object_to_json(domestic_print_payload)
        response = request_utils.send_request_based_on_http_method(self.print_request_endpoint, None, self.headers,
                                                                   requestBody, "post", None)
        # print("print response ",response)
        return response

    def send_RefundRequest(self,carrier,requestBody):
       req_paylod = common_utils.convert_object_to_json(requestBody)
       self.refundUrl=self.baseUri+"/"+carrier.lower()+"/refund"
       print("refund url is ",self.refundUrl)
       response = request_utils.send_request_based_on_http_method(self.refundUrl, None, self.headers,
                                                                  req_paylod, "post", None)

       # print("response is ",response)

       return  response

    def send_ReprintRequest(self,carrier,requestBody):
       req_paylod = common_utils.convert_object_to_json(requestBody)
       self.reprintUrl=self.baseUri+"/"+carrier.lower()+"/reprint"
       print("reprint url is ",self.reprintUrl)
       response = request_utils.send_request_based_on_http_method(self.reprintUrl, None, self.headers,
                                                                  req_paylod, "post", None)

       # print("response is ",response)

       return  response




