""" This module contains all test cases for email Notification.
emailSSTO - Runs tests for old notification
emailtest - Runs tests fot new notification
"""
import logging
import sys
import pytest

from APIObjects.lockers_services.ilp_service.locker_bank_apis import LockerBankAPI
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.reserve_with_pin import ReserveWithPin
from APIObjects.lockers_services.ilp_service.day_locker_apis import DayLocker
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.gmail_client import GmailClient
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.login_api import LoginAPI

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities import Crypt

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, client_token):
    pt_asset = {}
    pt_asset['app_config'] = app_config
    pt_asset['reserveWithPin'] = ReserveWithPin(app_config, client_token)
    pt_asset['lockerapi'] = LockerAPI(app_config, client_token)
    pt_asset['configuration'] = ConfigurationAPI(app_config, client_token)
    pt_asset['cancelreservation'] = CancelReservation(app_config, client_token)
    pt_asset['dept_api'] = DepartmentLockerAPI(app_config, client_token)
    pt_asset['data_reader'] = DataReader(app_config)
    pt_asset['login_api'] = LoginAPI(app_config)
    yield pt_asset


@pytest.mark.usefixtures('initialize')
class TestPTAsset(common_utils):
    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.configparameter = "PT_Asset_MGMT"
        self.Failures = []

    def test_reserve_asset_deliver(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        sample_json = '{"emailProvider":"PB_SSTO"}'

        res, status_code = resource['configuration'].verify_patch_email_configuration(locker_bank, sample_json, "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
