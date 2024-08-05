from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from body_jsons.cseries_services.packages_requestbody import PackagesRequestBody
from body_jsons.cseries_services.packages_requestbody_UK import PackagesRequestBodyUK



class DevicePackages:

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



    def generate_package_request(self, test_data):
        PackagesRequestBody['recipient']['isoCountry'] = test_data['recipientCountry']
        PackagesRequestBody['recipient']['postalCode'] = test_data['recipientPostalCode']
        PackagesRequestBody['sender']['isoCountry'] = test_data['senderCountry']
        PackagesRequestBody['cultureCode'] = test_data['cultureCode']
        PackagesRequestBody['dimensionUnits']= test_data['dimensionUnits']
        PackagesRequestBody['weightUnits'] = test_data['weightUnits']



        req_paylod = common_utils.convert_object_to_json(PackagesRequestBody)

        return req_paylod

    def generate_package_request_UK(self, test_data):
        PackagesRequestBodyUK['recipient']['isoCountry'] = test_data['recipientCountry']
        PackagesRequestBodyUK['recipient']['postalCode'] = test_data['recipientPostalCode']
        PackagesRequestBodyUK['sender']['isoCountry'] = test_data['senderCountry']
        PackagesRequestBodyUK['cultureCode'] = test_data['cultureCode']
        PackagesRequestBodyUK['dimensionUnits']= test_data['dimensionUnits']
        PackagesRequestBodyUK['weightUnits'] = test_data['weightUnits']



        req_paylod = common_utils.convert_object_to_json(PackagesRequestBodyUK)

        return req_paylod


    def post_packages(self,carrier,isMilitaryAddress, test_data):
        self.packages_request_endpoint = self.baseUri + "/US/"+carrier+"/packages?militaryAddress="+str(isMilitaryAddress)+"&batch=false"
        requestBody = self.generate_package_request(test_data)

        print("request body ", requestBody)
        # print("planner end point is ", self.planner_request_endpoint)

        resp = request_utils.send_request_based_on_http_method(self.packages_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp

    def post_packages_UK(self,carrier,isMilitaryAddress, test_data):
        self.packages_request_endpoint = self.baseUri + "/GB/"+carrier+"/packages?militaryAddress="+str(isMilitaryAddress)+"&batch=false"
        requestBody = self.generate_package_request_UK(test_data)

        print("request body ", requestBody)
        # print("planner end point is ", self.planner_request_endpoint)

        resp = request_utils.send_request_based_on_http_method(self.packages_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp





