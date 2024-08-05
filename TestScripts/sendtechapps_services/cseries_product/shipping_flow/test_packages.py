import pytest
import logging

from APIObjects.sendtech_apps.device_packages import DevicePackages
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, context):
    shippinglabel = {
        'app_config': app_config,
        'packages': DevicePackages(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class TestPackages(common_utils):
    log = log_utils.custom_logger(logging.INFO)


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PostPackagesAPITestData.xlsx",
                                                                "usps"))
    def test_usps_post_packages_api(self, resource,test_data):

        resp = resource['packages'].post_packages("usps",False,test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')



        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PostPackagesAPITestData.xlsx",
                                                                "ups"))
    def test_ups_post_packages_api(self, resource, test_data):
        resp = resource['packages'].post_packages("ups",False, test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')



        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PostPackagesAPITestData.xlsx",
                                                                "fedex"))
    def test_fedex_post_packages_api(self, resource, test_data):
        resp = resource['packages'].post_packages("fedex",False, test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')


        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PostPackagesAPITestData.xlsx",
                                                                "uspsMilAddress"))
    def test_packages_api_withMilitaryAddress(self, resource, test_data):
        resp = resource['packages'].post_packages("usps",True,test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True


    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "PostPackagesAPITestData.xlsx",
                                                                "gbPostal"))
    def test_gbPostal_post_packages_api(self, resource, test_data):
        resp = resource['packages'].post_packages_UK("gbPostal", False, test_data)

        print("response code is ", resp['response_code'])
        print("response body is ", resp['response_body'])

        # self.log.info(f'response code is: {resp["response_code"]}')
        # self.log.info(f'response body is: {resp["response_body"]}')

        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

