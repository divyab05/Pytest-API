
import json

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities import generic_utils
from body_jsons.cseries_services.planner_requestbody import PlannerRequestBody
from body_jsons.cseries_services.uk_services_requestbody import UKServicesRequestBody


class DevicePlanner:

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
        self.planner_request_endpoint=self.baseUri +"/planner"


    def generate_planner_request(self,test_data,uspsCarrierProfileID):

        PlannerRequestBody['carriersInfo'][0]["carrierProfileId"] = uspsCarrierProfileID

        PlannerRequestBody['initialCarrierSelection'] = test_data['carrierSelection']
        PlannerRequestBody['recipient']['isoCountry'] = test_data['recipientCountry']
        PlannerRequestBody['recipient']['city'] = test_data['recipientCity']
        PlannerRequestBody['recipient']['state'] = test_data['recipientState']
        PlannerRequestBody['recipient']['postalCode'] = test_data['recipientPostalCode']

        print("Get Current timestamp ",generic_utils.get_current_timestamp() )
        
        PlannerRequestBody['dateOfShipment'] =generic_utils.get_current_timestamp()

        PlannerRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        PlannerRequestBody['sender']['city'] = test_data['senderCity']
        PlannerRequestBody['sender']['state'] = test_data['senderState']
        PlannerRequestBody['sender']['postalCode'] = test_data['senderPostalCode']

        # recipient details
        PlannerRequestBody['packageDetails']['packageId'] = test_data['packageId']
        PlannerRequestBody['packageDetails']['packageDisplayId'] = test_data['packageDisplayId']

        PlannerRequestBody['packageDetails']['lengthMeters'] = float(test_data['lengthMeter'])
        PlannerRequestBody['packageDetails']['widthMeters'] = float(test_data['widthMeter'])
        PlannerRequestBody['packageDetails']['heightMeters'] = float(test_data['heightMeter'])
        PlannerRequestBody['packageDetails']['weightKilos'] = float(test_data['weightKilos'])

        lst=[]
        lst.append(test_data['serviceOptions'])
        PlannerRequestBody['serviceOptions'] = lst
        PlannerRequestBody['inductionPostalCode'] = test_data['inductionPostalCode']
        PlannerRequestBody['cultureCode'] = test_data['cultureCode']
        PlannerRequestBody['dimensionUnits'] = test_data['dimensionUnits']



        req_paylod = common_utils.convert_object_to_json(PlannerRequestBody)

        return req_paylod

    def generate_services_api_request(self, test_data):

        UKServicesRequestBody['carrierProfileId']= test_data['carrierProfileId']

        UKServicesRequestBody['cultureCode'] = test_data['cultureCode']
        UKServicesRequestBody['dimensionUnits'] = test_data['dimensionUnits']
        UKServicesRequestBody['inductionPostalCode']= test_data['inductionPostalCode']

        UKServicesRequestBody['packageDetails']['lengthMeters'] = float(test_data['lengthMeters'])
        UKServicesRequestBody['packageDetails']['widthMeters'] = float(test_data['widthMeters'])
        UKServicesRequestBody['packageDetails']['heightMeters'] = float(test_data['heightMeters'])
        UKServicesRequestBody['packageDetails']['weightKilos'] = float(test_data['weightKilos'])
        UKServicesRequestBody['packageDetails']['packageId'] = test_data['packageId']

        # Current timestamp
        UKServicesRequestBody['dateOfShipment'] = generic_utils.get_current_timestamp()

        UKServicesRequestBody['recipient']['isoCountry'] = test_data['reciCountry']
        UKServicesRequestBody['recipient']['city'] = test_data['reciCity']
        UKServicesRequestBody['recipient']['postalCode'] = test_data['reciPostalCode']
        UKServicesRequestBody['recipient']['state'] = test_data['reciState']


        UKServicesRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        UKServicesRequestBody['sender']['city'] = test_data['senderCity']
        UKServicesRequestBody['sender']['state'] = test_data['senderState']
        UKServicesRequestBody['sender']['postalCode'] = test_data['senderPostalCode']

        # recipient details
        lst = []
        lst.append(test_data['serviceOptions'])
        UKServicesRequestBody['serviceOptions']= lst
        UKServicesRequestBody['weightUnits'] = test_data['weightUnits']



        req_paylod = common_utils.convert_object_to_json(UKServicesRequestBody)

        return req_paylod



    def post_planner(self,test_data,uspsCarrierProfieID):
        requestBody = self.generate_planner_request(test_data,uspsCarrierProfieID)

        print("planner request body ",requestBody)
        print("planner end point is ",self.planner_request_endpoint)



        resp = request_utils.send_request_based_on_http_method(self.planner_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp


    def post_services(self,test_data):
        requestBody = self.generate_services_api_request(test_data)

        self.services_api_request_endpoint = self.baseUri + "/gbPostal/package/services?batch=false"

        print("request body ",requestBody)
        print("planner end point is ",self.services_api_request_endpoint)



        resp = request_utils.send_request_based_on_http_method(self.services_api_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp





