
import pytest
import logging

from APIObjects.sendtech_apps.device_shipping_label import ShippingLabel
from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config,context):
    shippinglabel = {
        'app_config': app_config,
        'shippinglabel': ShippingLabel(app_config,context['cseries_okta_token'],"ups"),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel






class TestUpsPrintLabel(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture()
    def getCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()
        # self.log.info(f'customer context response json is: {res.json()}')
        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "ups" not in carrierProfileArray:
            pytest.skip("Skip UPS Cases due to not having carrier added in this account")

        self.carrierProfileId = carrierProfileArray['ups']['carrierProfiles'][0]['id']


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                  "PrintLabelTestData_US.xlsx",
                                                                "UpsDomLabelPrint"))
    def test_ups_print_request_domestic(self,resource,test_data,
                                                 custom_logger,getCarrierProfileIdFromCustomerContextAPI):
        resp = resource['shippinglabel'].send_print_request(test_data,"domestic",self.carrierProfileId)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True



    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PrintLabelTestData_US.xlsx",
                                                                "UpsIntLabelPrint"))
    def test_ups_print_request_int(self, resource, test_data,
                                custom_logger,getCarrierProfileIdFromCustomerContextAPI):
        resp = resource['shippinglabel'].send_print_request(test_data, "international",self.carrierProfileId)
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True





