import pytest
import logging

from APIObjects.sendtech_apps.device_customs_api import DeviceCustomsAPI
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, context):
    shippinglabel = {
        'app_config': app_config,
        'deviceCustomAPI': DeviceCustomsAPI(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class TestRateAPI(common_utils):
    log = log_utils.custom_logger(logging.INFO)


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "CustomAPITestData.xlsx",
                                                                "usps"))
    def test_usps_post_customs_api(self, resource,test_data):

        resp = resource['deviceCustomAPI'].post_customAPI("usps",test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')



        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "CustomAPITestData.xlsx",
                                                                "UK"))
    def test_post_customs_api_UK(self, resource, test_data):
        resp = resource['deviceCustomAPI'].post_customAPI("rmg", test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True





