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
def resource(app_config, context):
    shippinglabel = {
        'app_config': app_config,
        'history': HistoryTransactions(app_config, context['cseries_okta_token']),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class Test_FedExHistoryActions(common_utils):
    log = log_utils.custom_logger(logging.INFO)
    transactionId, trackingId = "", ""

    @pytest.fixture
    def getCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()
        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "fedex" not in carrierProfileArray:
            pytest.skip("Skip UPS Cases due to not having carrier added in this account")
        self.carrierProfileId = carrierProfileArray['fedex']['carrierProfiles'][0]['id']

    @pytest.fixture
    def verifyPrintFedExLabel(self, resource, getCarrierProfileIdFromCustomerContextAPI):
        response = resource['history'].printFedExLabel(self.carrierProfileId)
        if response['response_code'] == 200:
            Test_FedExHistoryActions.transactionId = response['response_body']['transactionId']
            Test_FedExHistoryActions.trackingId = response['response_body']['packageTrackingId']

    @pytest.mark.order(2)
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_fedex_reprint(self, resource, verifyPrintFedExLabel, custom_logger):
        reprintRequestBody['originalPackageTrackingId'] = Test_FedExHistoryActions.trackingId
        reprintRequestBody['originalTransactionId'] = Test_FedExHistoryActions.transactionId
        resp = resource['history'].send_ReprintRequest("fedex", reprintRequestBody)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.order(3)
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_fedex_refund(self, resource, verifyPrintFedExLabel, custom_logger):
        refundRequestBody['originalPackageTrackingId'] = Test_FedExHistoryActions.trackingId
        refundRequestBody['originalTransactionId'] = Test_FedExHistoryActions.transactionId
        resp = resource['history'].send_RefundRequest("fedex", refundRequestBody)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True
