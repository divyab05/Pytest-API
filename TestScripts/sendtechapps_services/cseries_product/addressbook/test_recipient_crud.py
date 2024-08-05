import json

import pytest
import logging

from APIObjects.sendtech_apps.device_verify_address import VerifyAddress
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils


exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, context):

    shippinglabel = {
        'app_config': app_config,
        'verifyAddress': VerifyAddress(app_config, context['cseries_okta_token'])

    }
    yield shippinglabel


class Test_Addressbook(common_utils):
    log = log_utils.custom_logger(logging.INFO)
    addressIDList=[]

    @pytest.mark.order(2)
    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "AddressbookTestData.xlsx",
                                                                "address"))
    def test_create_address(self, resource, test_data, custom_logger):
        resp = resource['verifyAddress'].addAddress(test_data)
        assert resp['response_code'] == int(test_data['responseCode'])
        if resp['response_code']==200:
            Test_Addressbook.addressIDList.append(resp['response_body']['id'])


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.order(3)
    def test_update_address(self,resource, custom_logger):
        resp = resource['verifyAddress'].editAddress("Recipient",Test_Addressbook.addressIDList[0])
        print("edit add response ", resp.status_code)
        assert resp.status_code==200



    @pytest.mark.order(4)
    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_delete_recipient_address(self,resource, custom_logger):
        resource['verifyAddress'].deleteAddress(Test_Addressbook.addressIDList)



