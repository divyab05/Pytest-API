import pytest
import logging

from APIObjects.sendtech_apps.device_rate_api import DevicePostRateAPI
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
        'deviceRateAPI': DevicePostRateAPI(app_config, context['cseries_okta_token']),
        'subscription': Subscription(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class TestRateAPI(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture
    def getCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()
        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "usps" not in carrierProfileArray:
            pytest.skip("Skip USPS Cases due to not having carrier added in this account")
        self.uspsCarrierProfileId = carrierProfileArray['usps']['carrierProfiles'][0]['id']

    @pytest.fixture
    def getUKCarrierProfileIdFromCustomerContextAPI(self, resource):
        res = resource['subscription'].get_customer_context()
        carrierProfileArray = res.json()['carrierProfilesSummaries']

        if "usps" not in carrierProfileArray:
            pytest.skip("Skip USPS Cases due to not having carrier added in this account")
        self.UKCarrierProfileId = carrierProfileArray['usps']['carrierProfiles'][0]['id']


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "RateAPITestData.xlsx",
                                                                "usps"))
    def test_usps_post_rate_api(self, resource,test_data,getCarrierProfileIdFromCustomerContextAPI):

        resp = resource['deviceRateAPI'].post_rateAPI("usps",test_data,self.uspsCarrierProfileId)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')



        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "RateAPITestData.xlsx",
                                                                "rmg"))
    def test_post_rate_api_UK_RMG(self, resource, test_data,getUKCarrierProfileIdFromCustomerContextAPI):
        resp = resource['deviceRateAPI'].post_rateAPI("rmg", test_data,self.UKCarrierProfileId)
        print("response of UK Rate api ",resp)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "RateAPITestData.xlsx",
                                                                "pfw"))
    def test_post_rate_api_UK_PFW(self, resource, test_data,getUKCarrierProfileIdFromCustomerContextAPI):
        resp = resource['deviceRateAPI'].post_rateAPI("pfw", test_data,self.UKCarrierProfileId)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True




