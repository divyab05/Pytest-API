
import pytest
import logging

from APIObjects.sendtech_apps.device_planner import DevicePlanner
from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, context):

    shippinglabel = {
        'app_config': app_config,
        'devicePlanner': DevicePlanner(app_config, context['cseries_okta_token']),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class TestPlanner(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture
    def getCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()
        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "usps" not in carrierProfileArray:
            pytest.skip("Skip USPS Cases due to not having carrier added in this account")
        self.uspsCarrierProfileId = carrierProfileArray['usps']['carrierProfiles'][0]['id']


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PlannerAPITestData.xlsx",
                                                                "planner"))
    def test_post_planner_api(self, resource,test_data,getCarrierProfileIdFromCustomerContextAPI):

        resp = resource['devicePlanner'].post_planner(test_data,self.uspsCarrierProfileId)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')



        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "UKServicesAPITestData.xlsx",
                                                                "uk"))
    def test_post_service_api_UK(self, resource, test_data):
        resp = resource['devicePlanner'].post_services(test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True





