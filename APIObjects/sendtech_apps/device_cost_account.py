import json

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from body_jsons.cseries_services.create_subCostAccount_requestBody import createSubCostAccount
from body_jsons.cseries_services.create_costAccount_requestBody import createCostAccount
from body_jsons.cseries_services.verify_address import verify_address_payload
from body_jsons.cseries_services.add_address import AddAddressPayload
from body_jsons.cseries_services.update_address import UpdateAddressPayload
from FrameworkUtilities.generic_utils import *





class CostAccount:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token
        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])

        if str(self.app_config.env_cfg['env']).lower()=="qa":
            self.headers = {"Authorization": self.admin_token}
            # self.headers = {"Authorization": self.admin_token, "X-PB-AUTH-ISSUER": "legacy"}
        else:
            self.headers = {"Authorization": self.admin_token}




    def searchCostAccount(self,costAccountStatus,query=None):
        searchCostAccountEndPoint= self.baseUri +"/costAccounts/advanceSearch?status="+str(costAccountStatus)+"&skip=0&limit=10&query=&searchInAllLevels=false"

        print("cost-account end point",searchCostAccountEndPoint)

        resp = request_utils.send_request_based_on_http_method(searchCostAccountEndPoint, None, self.headers,
                                                               json.dumps({}), "post",
                                                               None)

        # print("response",resp)

        # print("response body ", resp['response_body'])

        return resp


    def createCostAccount(self,test_data,enterpriseID,subID):
        createCostAccountEndPoint= self.baseUri +"/costaccounts"

        print("cost-account end point",createCostAccountEndPoint)

        requestBody = self.generate_create_costaccount_request(test_data,enterpriseID,subID)

        resp = request_utils.send_request_based_on_http_method(createCostAccountEndPoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        # print("response",resp)
        #
        # print("response body ", resp['response_body'])

        return resp

    def createSubCostAccount(self, enterpriseID, subID,parentCostAccountID,costAccountStatus):
        createSubCostAccountEndPoint = self.baseUri + "/costaccounts"

        print("sub-cost-account end point", createSubCostAccountEndPoint)

        requestBody = self.generate_create_subcostaccount_request(enterpriseID, subID,parentCostAccountID,costAccountStatus)

        resp = request_utils.send_request_based_on_http_method(createSubCostAccountEndPoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        # print("response", resp)
        #
        # print("response body ", resp['response_body'])

        return resp

    def getSubCostAccount(self, parentCostAccountID):
        getSubCostAccountEndPoint = self.baseUri + "/costAccounts/"+parentCostAccountID+"/subAccounts?status=true&skip=0&size=10&query="

        print("get sub-cost-account end point", getSubCostAccountEndPoint)

        # requestBody = self.generate_create_subcostaccount_request(enterpriseID, subID,parentCostAccountID,costAccountStatus)

        resp = request_utils.send_request_based_on_http_method(getSubCostAccountEndPoint, None, self.headers,
                                                               None, "get",
                                                               None)

        # print("response", resp)
        #
        # print("response body ", resp['response_body'])

        return resp

    def generate_create_costaccount_request(self, test_data,enterpriseID,subID):

        randomString=generate_random_string(char_count=6)
        createCostAccount['name'] = randomString
        createCostAccount['code'] = randomString
        createCostAccount['costAccountStatus'] = test_data['costAccountStatus']
        createCostAccount['isDefaultCostAccount'] = bool(test_data['isDefaultCostAccount'])

        createCostAccount['passwordCode'] = test_data['passwordCode']
        createCostAccount['passwordEnabled'] = bool(test_data['passwordEnabled'])

        createCostAccount['permission']['permissionByEntity'] = test_data['permissionByEntity']

        createCostAccount['subID'] = subID

        tempList=[]
        tempList.append(enterpriseID)
        createCostAccount['permission']['permissionByValue'] = tempList




        req_paylod = common_utils.convert_object_to_json(createCostAccount)





        print("request body is ", req_paylod)

        return req_paylod

    def generate_create_subcostaccount_request(self,enterpriseID, subID,parentCostAccID,costAccountStatus):
        randomString=generate_random_string(char_count=6)

        createSubCostAccount['name'] = randomString
        createSubCostAccount['code'] = randomString
        createSubCostAccount['costAccountStatus'] = costAccountStatus
        createSubCostAccount['parentCostAccount'] = parentCostAccID
        createSubCostAccount['isDefaultCostAccount'] = bool(False)


        createSubCostAccount['passwordEnabled'] = bool(False)

        createSubCostAccount['permission']['permissionByEntity'] = 'E'

        createSubCostAccount['subID'] = subID

        tempList = []
        tempList.append(enterpriseID)
        createSubCostAccount['permission']['permissionByValue'] = tempList




        req_paylod = common_utils.convert_object_to_json(createSubCostAccount)

        print("request body is ", req_paylod)

        return req_paylod

    def generate_add_address_request(self, test_data):
        AddAddressPayload['addressType'] = test_data['addressType']
        AddAddressPayload['isoCountry'] = test_data['isoCountry']
        AddAddressPayload['contact']['fullName'] = test_data['fullName']
        AddAddressPayload['contact']['companyName'] = test_data['postalCode']

        AddAddressPayload['streetLine1'] = test_data['streetLine1']
        AddAddressPayload['streetLine2'] = test_data['streetLine2']


        AddAddressPayload['city'] = test_data['city']
        AddAddressPayload['state'] = test_data['state']

        AddAddressPayload['contact']['primaryEmail'] = test_data['email']
        AddAddressPayload['homePhone'] = test_data['phone']

        req_paylod = common_utils.convert_object_to_json(AddAddressPayload)

        print("request body is ",req_paylod)

        return req_paylod


    def addAddress(self,test_data):
        # self.headers['Authorization'] = self.admin_token
        addAddress_endpoint = self.baseUri  + "/addressbooks/addresses"

        requestBody = self.generate_add_address_request(test_data)


        resp = request_utils.send_request_based_on_http_method(addAddress_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)
        # print("response body ", resp['response_body'])

        return resp

    def deleteAddress(self, lst):
        print("address id list ",lst)
        for id in lst:
            deleteAddress_endpoint = self.baseUri + "/addresses?ids="+id

            # resp = request_utils.send_request_based_on_http_method(deleteAddress_endpoint, None, self.headers,
            #                                                        None, "delete",
            #                                                        None)
            resp=self.api.delete_api_response(deleteAddress_endpoint,self.headers)

            assert resp.status_code==204



    def editAddress(self,addressType,id):
        editAddress_endpoint=self.baseUri + "/addressbooks/addresses/"+id
        UpdateAddressPayload["id"]=id
        UpdateAddressPayload["addressType"] = addressType

        # resp = request_utils.send_request_based_on_http_method(editAddress_endpoint, None, self.headers,
        #                                                        AddAddressPayload, "put",
        #                                                        None)
        req_paylod = common_utils.convert_object_to_json(UpdateAddressPayload)
        resp = self.api.put_api_response(editAddress_endpoint, self.headers,req_paylod)
        return resp

    def get_enterprise_subscription_details(self):
        # self.headers['Authorization'] = self.admin_token
        get_enterprise_subscriptions_endpoint = self.baseUri + "/enterprises/subscriptions?getPaymentStatus=true"
        print("enterprise url", get_enterprise_subscriptions_endpoint)
        resp = self.api.get_api_response(endpoint=get_enterprise_subscriptions_endpoint, headers=self.headers)
        return resp


















