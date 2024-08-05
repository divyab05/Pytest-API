import json

import pytest
import logging

from APIObjects.sendtech_apps.device_shipping_label import ShippingLabel
from APIObjects.sendtech_apps.device_subscription import Subscription

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, context):

    shippinglabel = {
        'app_config': app_config,
        'shippinglabel': ShippingLabel(app_config,context['cseries_okta_token'],"usps" ),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel



class TestUspsPrintLabel(common_utils):
    log = log_utils.custom_logger(logging.INFO)



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
        self.carrierProfileId = carrierProfileArray['usps']['carrierProfiles'][0]['id']









    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PrintLabelTestData_US.xlsx",
                                                                "UspsDomLabelPrint"))
    def test_usps_print_request_domestic(self,resource,test_data,
                                                 custom_logger,verifyShipmentAmount,getCarrierProfileIdFromCustomerContextAPI):
        resp = resource['shippinglabel'].send_print_request(test_data,"domestic",self.carrierProfileId)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PrintLabelTestData_US.xlsx",
                                                                "UspsIntLabelPrint"))
    def test_usps_print_request_int(self, resource, test_data,
                                custom_logger, verifyShipmentAmount,getCarrierProfileIdFromCustomerContextAPI):
        resp = resource['shippinglabel'].send_print_request(test_data, "international",self.carrierProfileId)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True





