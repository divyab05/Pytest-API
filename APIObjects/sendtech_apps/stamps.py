import json

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import generic_utils
from body_jsons.cseries_services.mailingCheckRates_requestbody import mailingCheckRatesRequestBody
from body_jsons.cseries_services.stampsheet_mailingRates_requestbody import stampsheetMailingRatesRequestBody



class DeviceStampsActions:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token

        if str(self.app_config.env_cfg['env']).lower()=="qa":

            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}

        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])


    def generate_mailngCheckRates_request(self,carrierProfileId,test_data):


        mailingCheckRatesRequestBody['carrierProfileId'] = carrierProfileId
        mailingCheckRatesRequestBody['inductionPostalCode'] = test_data['inductionPostalCode']

        # package details
        mailingCheckRatesRequestBody['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        mailingCheckRatesRequestBody['packageDetails']['widthMeters'] = float(test_data['widthMeters'])
        mailingCheckRatesRequestBody['packageDetails']['heightMeters'] = float(test_data['heightMeters'])
        mailingCheckRatesRequestBody['packageDetails']['weightKilos']= float(test_data['weightKilos'])
        mailingCheckRatesRequestBody['packageDetails']['packageId']= test_data['packageId']


        # recipient details
        mailingCheckRatesRequestBody['recipient']['countryCode'] = test_data['recipientCountryCode']
        mailingCheckRatesRequestBody['recipient']['postalCode'] = test_data['recipientPostalCode']

        mailingCheckRatesRequestBody['sender']['countryCode'] = test_data['senderCountry']
        mailingCheckRatesRequestBody['sender']['postalCode'] = test_data['senderPostalCode']

        serviceOptionList = []
        serviceOptionList.append(test_data['serviceOptions'])
        mailingCheckRatesRequestBody['serviceOptions'] = serviceOptionList




        req_paylod = common_utils.convert_object_to_json(mailingCheckRatesRequestBody)

        return req_paylod

    def generate_stampsheet_mailngRates_request(self,carrierProfileId,test_data):


        stampsheetMailingRatesRequestBody['carrier'] = test_data['carrier']
        stampsheetMailingRatesRequestBody['carrierProfileId'] = carrierProfileId
        stampsheetMailingRatesRequestBody['inductionPostalCode']= test_data['inductionPostalCode']
        stampsheetMailingRatesRequestBody['mailClass']= test_data['mailClass']

        # package details
        stampsheetMailingRatesRequestBody['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        stampsheetMailingRatesRequestBody['packageDetails']['widthMeters']= float(test_data['widthMeters'])
        stampsheetMailingRatesRequestBody['packageDetails']['heightMeters']= float(test_data['heightMeters'])
        stampsheetMailingRatesRequestBody['packageDetails']['weightKilos'] = float(test_data['weightKilos'])
        stampsheetMailingRatesRequestBody['packageDetails']['packageId'] = test_data['packageId']

        # recipient details
        stampsheetMailingRatesRequestBody['recipient']['isoCountry'] = test_data['reciCountry']
        stampsheetMailingRatesRequestBody['recipient']['countryCode'] = test_data['reciCountry']
        stampsheetMailingRatesRequestBody['recipient']['city'] = test_data['reciCity']
        stampsheetMailingRatesRequestBody['recipient']['postalCode'] = test_data['reciPostalCode']
        stampsheetMailingRatesRequestBody['recipient']['state'] = test_data['reciState']

        # sender details
        stampsheetMailingRatesRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        stampsheetMailingRatesRequestBody['sender']['countryCode'] = test_data['senderCountry']
        stampsheetMailingRatesRequestBody['sender']['city'] = test_data['senderCity']
        stampsheetMailingRatesRequestBody['sender']['postalCode'] = test_data['senderPostalCode']
        stampsheetMailingRatesRequestBody['sender']['state'] = test_data['senderState']

        serviceOptionList=[]
        serviceOptionList.append(test_data['serviceOptions'])
        stampsheetMailingRatesRequestBody['serviceOptions'] = serviceOptionList


        req_paylod = common_utils.convert_object_to_json(stampsheetMailingRatesRequestBody)

        return req_paylod



    def post_verify_mailing_checrates(self,carrierProfileId,test_data):
        mailing_checkrates_endPoint = self.baseUri + "/mailing/checkrates"

        requestBody = self.generate_mailngCheckRates_request(carrierProfileId,test_data)

        print("request body ",requestBody)
        print("planner end point is ",mailing_checkrates_endPoint)



        resp = request_utils.send_request_based_on_http_method(mailing_checkrates_endPoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp


    def post_verify_fusion_iot_event(self):
        iot_endpoint="https://fusion-device-api-qa.sendpro360.pitneycloud.com/api/v1/iot/event"
        requestBody="{\"emailId\":\"vertikacubetest17@yopmail.com\",\"errorMessage\":\"\",\"fileName\":\"\",\"jobId\":\"\",\"jobStatus\":\"\",\"message\":\"Splash: Token Fetched from login service\",\"name\":\"\",\"pcn\":\"\",\"platformType\":\"Android\",\"recover\":\"\",\"schemaVersion\":\"\",\"serialNumber\":\"\",\"status\":\"OFFLINE\",\"success\":\"true\",\"timeStamp\":\""+generic_utils.get_current_timestamp()+"\",\"transactionId\":\"\",\"type\":\"Authorization\"}"
        print("Before serialized iOT Event Request body ", requestBody)
        requestBody_str=json.dumps(requestBody)
        print("After serialized iOT Event Request body ",requestBody_str)
        resp = request_utils.send_request_based_on_http_method(iot_endpoint, None, self.headers,
                                                               requestBody_str, "post",
                                                               None)
        return resp


    def post_verify_stampsheet_mailing_rates(self,carrierProfileId,test_data):
        stampsheet_mailing_rates_endPoint = self.baseUri + "/stampsheet/mailing/rate"

        requestBody = self.generate_stampsheet_mailngRates_request(carrierProfileId,test_data)

        print("request body ",requestBody)
        print("planner end point is ",stampsheet_mailing_rates_endPoint)



        resp = request_utils.send_request_based_on_http_method(stampsheet_mailing_rates_endPoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp






