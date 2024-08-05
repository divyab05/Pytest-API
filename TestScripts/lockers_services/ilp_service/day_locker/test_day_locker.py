""" This module contains all test cases for day locker."""

import random
import string
import sys
import pytest
import datetime

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.day_locker_apis import DayLocker
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.locker_bank_apis import LockerBankAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token):
    storage = {'app_config': app_config,
               'storage': DayLocker(app_config, client_token),
               'lockerapi': LockerAPI(app_config, client_token),
               'configuration': ConfigurationAPI(app_config, client_token),
               'cancelreservation': CancelReservation(app_config, client_token),
               'event_api': LockerBankAPI(app_config, client_token),
               'data_reader': DataReader(app_config)}
    yield storage


@pytest.mark.usefixtures('initialize')
class TestReserveStorage(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """

        self.configparameter = "LOCKERS_Day_Locker"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    # ----------------------------Enable Day Locker----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_enable_day_locker_feature_in_bank(self, rp_logger, resource):
        """
        This test validates enable of day locker in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        dayLockerSupport = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'dayLockerSupport')
        json = '{"dayLockerSupport":"%s"}' % dayLockerSupport

        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------------Set Flexible Timing for Day Locker---------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_enable_flexible_locker_setting(self, rp_logger, resource):
        """
        This test validates the flexible setting for locker bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        max_date = random.randint(1, 30)
        json = '{"dayLockerFlexibleTimeInDays":%s}' % max_date

        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ------------------------------Reserve Flexible Day Locker----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_flexible_dayLocker(self, rp_logger, resource):
        """
        This test validates the reservation of day locker with flexible end reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        now = datetime.datetime.utcnow() + datetime.timedelta(days=4)
        current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=current_time,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('reserve_day_locker_res_schema.json', 'lockers_services'))

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    # ----------------------------Set Fixed Timing for Day Locker----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_enable_fixed_locker_setting(self, rp_logger, resource):
        """
        This test validates the fixed setting for locker bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=4)
        current_time = now.strftime("%H:%M")
        json = '{"dayLockerFixedTime":"%s"}' % current_time

        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------Reserve Fixed Day Locker----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_fixed_dayLocker(self, rp_logger, resource):
        """
        This test validates the reservation of day locker in fixed setting(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('reserve_day_locker_res_schema.json',
                                                                               'lockers_services'))

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    #-------------------------------Authenticate Day Locker API--------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_authdaylocker_reserve_pid(self, rp_logger, resource):
        """
        This test validates authenticate day locker after reservation using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        recipient_pid = res['assetsReserved']['recipient']['personalID']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=recipient_pid, token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('authDL_reservation_schema.json', 'lockers_services'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_authdaylocker_reserve_otp(self, rp_logger, resource):
        """
        This test validates authenticate day locker after reservation using access code (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        access_code = res['assetsReserved']['depositor']['oneTimePin']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=access_code, token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('authDL_reservation_schema.json', 'lockers_services'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_authdaylocker_deposit_pid(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        recipient_pid = res['assetsReserved']['recipient']['personalID']
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=recipient_pid, token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('authDL_deposit_schema.json', 'lockers_services'))

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank, locker_unit=locker_unit,  token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank, "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_authdaylocker_deposit_otp(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using access code(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        access_code = res['assetsReserved']['depositor']['oneTimePin']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=access_code, token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('authDL_deposit_schema.json', 'lockers_services'))

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank, "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))

    #---------------------------------------GET UNIT MANAGEMENT API-------------------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_get_unit_management_api(self, rp_logger, resource):
        """
        This test validates the get unit management api (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['storage'].get_locker_management_unit_allocation(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('unit_management_res_schema.json', 'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))

    # ----------------------------------POST Unit MANAGEMENT API-------------------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_post_unit_management_api_with_requestedCount_higher_than_enabled(self, rp_logger, resource):
        """
        This test validates the post unit management api when requested count is more than the enabled count (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['storage'].get_locker_management_unit_allocation(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].post_locker_management_unit_allocation(locker_bank, res, 6, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ------------------------------------PRE RESERVATION API-------------------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_pre_reservation_for_employee(self, rp_logger, resource):
        """
        This test validates the reservation of day locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        Name = resource['data_reader'].pd_get_data(self.configparameter, test_name, "Name")
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "receiver")
        pid = 'new123'
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=Name, EmailID=EmailID,
                                                                          token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        visitorID = res["visitorID"]
        access_code = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if isVisitorFlag:
            self.Failures.append("Employee has visitor Flag as true")
        if visitorID != recipientID:
            self.Failures.append("Employee has different visitor ID")
        if not access_code.startswith("DAY", 0, 4):
            self.Failures.append("Personal ID is does not start with DAY")

        receiver = res['visitorID']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=access_code,
                                                                       token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=pid,
                                                                       token_type="valid",  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=access_code,
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank,
                                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_visitor_able_to_create_reservation_or_entry(self, rp_logger, resource):
        """
        This test validates the visitor record for day locker reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        personalID = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if not isVisitorFlag:
            self.Failures.append("Visitor Flag as false")
        if not personalID.startswith("VIS", 0, 4):
            self.Failures.append("Personal ID is does not start with VIS")

        receiver = res['visitorID']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=personalID,
                                                                       token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=personalID,
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_pre_reservation_api_with_invalid_emailID(self, rp_logger, resource):
        """
        This test validates the visitor when wrong emailID is  passed (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank,
                                                                          Name=username,
                                                                          EmailID="wrong@",
                                                                          token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_pre_reservation_api_with_No_emailID(self, rp_logger, resource):
        """
        This test validates the visitor when wrong emailID is  passed (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank,
                                                                          Name=username,
                                                                          EmailID="",
                                                                          token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_pre_reservation_api_with_No_UserName_passed(self, rp_logger, resource):
        """
        This test validates the visitor when wrong emailID is  passed (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank,
                                                                          Name="", EmailID=visitor,
                                                                          token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ----------------------------Disable Day Locker----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reservation_when_flag_off(self, rp_logger, resource):
        """
        This test validates reservation of day locker when setting is false (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"dayLockerSupport": "disabled"}'
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        json = '{"dayLockerSupport": "enabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_pre_reservation_when_flag_off(self, rp_logger, resource):
        """
        This test validates the pre reservation of day locker when setting is false (negative  scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"dayLockerSupport": "disabled"}'
        visitor_email = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))

        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        json = '{"dayLockerSupport": "enabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    #----------------------------------End to END---------------------------------------------

    """ Double Reservations for employee vs visitor """
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_employee_double_reservation(self, rp_logger, resource):
        """
        This test validates the double reservation of employee from reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_one = res['manufacturerLockerID']

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit_one, locker_bank,
                                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_visitor_double_reservation(self, rp_logger, resource):
        """
        This test validates the double reservation of visitor from pre reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        visitor_email = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        personalID = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if not isVisitorFlag:
            self.Failures.append("Visitor Flag as true")
        if not personalID.startswith("VIS", 0, 4):
            self.Failures.append("Personal ID is does not match with address book")

        receiver = res['visitorID']
        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=personalID,
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_one = res['manufacturerLockerID']

        # Creating a second reservation.
        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit_one, locker_bank,
                                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    # @pytest.mark.ilp_sp360commercial
    # @pytest.mark.ilp_fedramp
    @pytest.mark.skip(reason="need to check")
    def test_employee_double_reservation_using_pre_reserve(self, rp_logger, resource):
        """
        This test validates the double reservation of employee from pre reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        emailID = res['assetsReserved']['recipient']['email']
        locker_unit_one = res['manufacturerLockerID']

        res, status_code_pre = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name="Random",
                                                                          EmailID=emailID, token_type="valid",
                                                                          resource_type="validResource")
        if status_code_pre != 400:
            self.Failures.append("Failure in pre reserve api response : Expected:400 , Received  " + str(status_code_pre))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit_one, locker_bank,
                                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    """ Day Locker and delivery reservations can be for same recipient """
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_employee_reservation_for_delivery_and_daylocker(self, rp_logger, resource):
        """
        This test validates the reservation of day locker and delivery for same recipient having same access code feature ON (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        json = '{"personalPackageAllAtOnce": "enabled"}'

        res, status_code = resource['configuration'].verify_patch_dropoff_property(locker_bank, json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_one = res['manufacturerLockerID']
        day_access_code = res['assetsReserved']['depositor']['oneTimePin']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=day_access_code,
                                                                       token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_one, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Delivery Reservation
        trackingID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=receiver,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_two = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_two, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        delivery_access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_authenticate_Pickup_api(delivery_access_code, locker_bank,
                                                                                "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # pickup day locker and delivery
        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=day_access_code,
                                                                       token_type="valid", resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(day_access_code, locker_unit_one, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(delivery_access_code, locker_unit_two, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # day and delivery reservations along with auth
    # delivery and day reservations along with auth

    @pytest.mark.regressioncheck_lockers
    def test_expire_code_for_employee(self, rp_logger, resource):
        """
        This test validates the reservation of day locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        Name = resource['data_reader'].pd_get_data(self.configparameter, test_name, "Name")
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "receiver")
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=Name,
                                                                          EmailID=EmailID,
                                                                          token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        visitorID = res["visitorID"]
        access_code = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if isVisitorFlag:
            self.Failures.append("Employee has visitor Flag as true")
        if visitorID != recipientID:
            self.Failures.append("Employee has different visitor ID")
        if not access_code.startswith("DAY", 0, 4):
            self.Failures.append("Personal ID is does not start with DAY")

        receiver = res['visitorID']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=access_code,
                                                                       token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=access_code,
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=access_code, token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=access_code, token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_expire_code_for_visitor(self, rp_logger, resource):
        """
        This test validates the visitor record for day locker reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        personalID = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if not isVisitorFlag:
            self.Failures.append("Visitor Flag as false")
        if not personalID.startswith("VIS", 0, 4):
            self.Failures.append("Personal ID is does not start with VIS")

        receiver = res['visitorID']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank, access_code=personalID,
                                                                       token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=personalID,
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=access_code, token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=access_code, token_type="valid",
                                                                       resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------ Kiosk Token (Keep it at the end of file) ------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_pre_reservation(self, rp_logger, resource, context):
        """
        This test validates the visitor record for day locker reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource",
                                                                          kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        isVisitorFlag = res["isVisitor"]
        personalID = res["personalID"]
        manufacturerID = res["manufacturerID"]

        if manufacturerID != locker_bank:
            self.Failures.append("Response has incorrect manufacturerID")
        if not isVisitorFlag:
            self.Failures.append("Visitor Flag as false")
        if not personalID.startswith("VIS", 0, 4):
            self.Failures.append("Personal ID is does not start with VIS")

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_authdaylocker_deposit_pid(self, rp_logger, resource, context):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource",
                                                                         kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        recipient_pid = res['assetsReserved']['recipient']['personalID']
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['storage'].authenticate_day_locker(locker_bank=locker_bank,
                                                                       access_code=recipient_pid, token_type="valid",
                                                                       resource_type="validResource",
                                                                       kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource",
                                                                                   kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False, context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
