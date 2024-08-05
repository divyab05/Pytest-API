import json

import pytest
import logging

from APIObjects.sendtech_apps.device_history_transactions import HistoryTransactions
from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from body_jsons.cseries_services.refund_requestbody import refundRequestBody
from body_jsons.cseries_services.reprint_requestbody import reprintRequestBody


from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils


exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config,context):

    shippinglabel = {
        'app_config': app_config,
        'history': HistoryTransactions(app_config,context['cseries_okta_token']),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel



class Test_UspsHistoryActions(common_utils):
    log = log_utils.custom_logger(logging.INFO)
    transactionId,trackingId="",""



    @pytest.fixture
    def verifyShipmentAmount(self,resource):
        response = resource['subscription'].get_accounts()
        if response.status_code==200 :
            response_dict = json.loads(response.text)
            if int(response_dict['prepayBalance']) < 200 :
                res=resource['subscription'].post_add_fund(100)
                # add postage amount if postage balance is less than 200

    @pytest.fixture
    def getCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()

        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "usps" not in carrierProfileArray:
            pytest.skip("Skip USPS Cases due to not having carrier added in this account")
        # self.log.info(f'customer context response json is: {res.json()}')
        self.carrierProfileId = carrierProfileArray['usps']['carrierProfiles'][0]['id']



    @pytest.fixture
    def verifyPrintUspsLabel(self,verifyShipmentAmount,resource,getCarrierProfileIdFromCustomerContextAPI):
         response=resource['history'].printUspsLabel(self.carrierProfileId)
         # print("print response ",response['response_body'],response['response_code'])
         if response['response_code']==200:
             Test_UspsHistoryActions.transactionId=response['response_body']['transactionId']
             Test_UspsHistoryActions.trackingId = response['response_body']['packageTrackingId']



    @pytest.mark.order(2)
    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_usps_reprint(self, resource, verifyPrintUspsLabel, custom_logger):
        reprintRequestBody['originalPackageTrackingId'] = Test_UspsHistoryActions.trackingId
        reprintRequestBody['originalTransactionId'] = Test_UspsHistoryActions.transactionId
        print("reprint request body",reprintRequestBody)
        resp = resource['history'].send_ReprintRequest("usps", reprintRequestBody)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.order(3)
    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_usps_refund(self,resource,verifyPrintUspsLabel,custom_logger):
        refundRequestBody['originalPackageTrackingId']=Test_UspsHistoryActions.trackingId
        refundRequestBody['originalTransactionId']=Test_UspsHistoryActions.transactionId
        print("refund request body is",refundRequestBody)
        resp = resource['history'].send_RefundRequest("usps",refundRequestBody)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True


