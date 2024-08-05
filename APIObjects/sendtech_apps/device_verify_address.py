import json

from FrameworkUtilities import request_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from body_jsons.cseries_services.verify_address import verify_address_payload
from body_jsons.cseries_services.add_address import AddAddressPayload
from body_jsons.cseries_services.update_address import UpdateAddressPayload




class VerifyAddress:

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.common = common_utils()

        self.admin_token = "Bearer " + access_token
        print("address token value is ", self.admin_token)

        if str(self.app_config.env_cfg['env']).lower()=="qa":
            self.headers = {"Authorization": self.admin_token}
        else:
            self.headers = {"Authorization": self.admin_token}
        self.baseUri = str(self.app_config.env_cfg['sending_legacy_api'])





    def generate_verify_address_request(self, test_data):

        verify_address_payload['address']['addressType'] = test_data['addressType']
        verify_address_payload['address']['isoCountry'] = test_data['Country']
        verify_address_payload['address']['contact']['fullName'] = test_data['FullName']
        verify_address_payload['address']['company'] = test_data['Company']
        verify_address_payload['address']['contact']['companyName'] = test_data['Company']

        verify_address_payload['address']['streetLine1'] = test_data['StreetLine-1']
        verify_address_payload['address']['streetLine2'] = test_data['StreetLine-2']
        verify_address_payload['address']['streetLine3'] = test_data['StreetLine-3']



        verify_address_payload['address']['postalCode'] = test_data['PostalCode']
        verify_address_payload['address']['city'] = test_data['City']
        verify_address_payload['address']['state'] = test_data['State']

        verify_address_payload['address']['contact']['primaryEmail'] = test_data['Email']
        verify_address_payload['address']['phone'] = test_data['Phone']

        req_paylod = common_utils.convert_object_to_json(verify_address_payload)


        return req_paylod




    def post_verify_address(self,carrier,test_data):
        # self.headers['Authorization'] = self.admin_token
        verifyAddress_request_endpoint = self.baseUri + "/" + carrier + "/verify-address"

        requestBody = self.generate_verify_address_request(test_data)


        resp = request_utils.send_request_based_on_http_method(verifyAddress_request_endpoint, None, self.headers,
                                                               requestBody, "post",
                                                               None)

        return resp

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
        print("response body ", resp['response_body'])

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


















