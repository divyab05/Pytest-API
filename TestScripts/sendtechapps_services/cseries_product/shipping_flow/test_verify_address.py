import pytest
import logging
from hamcrest import assert_that

from APIObjects.sendtech_apps.device_verify_address import VerifyAddress
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config,context):
    shippinglabel = {
        'app_config': app_config,
        'verifyAddress': VerifyAddress(app_config,context['cseries_okta_token'])

    }
    yield shippinglabel



class TestAccounts(common_utils):
    log = log_utils.custom_logger(logging.INFO)



    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "VerifyAddressTestData_US.xlsx",
                                                                "usps"))

    def test_usps_verify_address(self, resource,test_data):



        res = resource['verifyAddress'].post_verify_address("usps",test_data)
        self.log.info(f'response json is: {res["response_body"]}')
        assert res['response_code'] == int(test_data['responseCode'])


        # ----------Schema Validation----------
        # with open(r'./response_schema/cseries_services/verify_recipient_address.json', 'r') as s:
        #     expected_schema = json.loads(s.read())
        #
        #
        # assert_that(self.validate_response_template(res,
        #                                             expected_schema, 200))


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "VerifyAddressTestData_US.xlsx",
                                                                "ups"))

    def test_ups_verify_address(self, resource, test_data):

        res = resource['verifyAddress'].post_verify_address("ups", test_data)
        self.log.info(f'response json is: {res["response_body"]}')
        assert res['response_code'] == int(test_data['responseCode'])

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "VerifyAddressTestData_US.xlsx",
                                                                "fedex"))
    def test_fedex_verify_address(self, resource, test_data):

        res = resource['verifyAddress'].post_verify_address("fedex", test_data)
        self.log.info(f'response json is: {res["response_body"]}')
        assert res['response_code'] == int(test_data['responseCode'])
