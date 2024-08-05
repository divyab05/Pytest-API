"""This module contains all test cases for slider."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.reserve_with_pin import ReserveWithPin
from APIObjects.lockers_services.ilp_service.day_locker_apis import DayLocker
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.bank_unit_status_apis import StatusAPIs
from APIObjects.lockers_services.ilp_service.dedicate_locker import DedicateLocker
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token):
    sliders = {'app_config': app_config,
               'reserveWithPin': ReserveWithPin(app_config, client_token),
               'storage': DayLocker(app_config, client_token),
               'lockerapi': LockerAPI(app_config, client_token),
               'configuration': ConfigurationAPI(app_config, client_token),
               'statusapi': StatusAPIs(app_config, client_token),
               'cancelreservation': CancelReservation(app_config, client_token),
               'dedicated': DedicateLocker(app_config, client_token),
               'data_reader': DataReader(app_config)}
    yield sliders


@pytest.mark.usefixtures('initialize')
class TestSliders(common_utils):

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

    @staticmethod
    def set_value(refObj, locker_bank, units_req):
        """
        This method is used for setting value of slider by using get and post unit management api
        :return: nothing
        """
        res, status_code = refObj.get_locker_management_unit_allocation(locker_bank, "valid", "validResource")
        res, status_code = refObj.post_locker_management_unit_allocation(locker_bank, res, units_req, "valid",
                                                                         "validResource")

    @staticmethod
    def get_value(refObj, locker_bank):
        """
        This method is used for getting the value of the unit using the get locker bank api
        :return: status of units and counts
        """
        deliveryFlag1 = ''
        deliveryFlag2 = ''
        deliveryFlag3 = ''
        RequestedCount = 0
        CurrentCount = 0
        res, status_code = refObj.verify_Lockerbank_details(locker_bank, "valid", "validResource")
        deliveryFlag1 = res['units'][0]['deliveryUnit']
        deliveryFlag2 = res['units'][1]['deliveryUnit']
        deliveryFlag3 = res['units'][2]['deliveryUnit']
        RequestedCount = res['deliveryUnits'][0]['count']['countRequested']
        CurrentCount = res['deliveryUnits'][0]['count']['countCurrent']

        return deliveryFlag1, deliveryFlag2, deliveryFlag3, RequestedCount, CurrentCount

    def check_value(self, refObj, locker_bank, expectedFlag1, expectedFlag2, expectedFlag3, expectedRequestedCount,
                    expectedCurrentCount, customMessage, failures):
        """
        This method is used for validating the value of units and count
        if validation fails then appended to failures list along with customMessage
        :return: nothing
        """

        deliveryFlag1, deliveryFlag2, deliveryFlag3, RequestedCount, CurrentCount = self.get_value(refObj, locker_bank)

        if deliveryFlag1 != expectedFlag1:
            failures.append(customMessage + "Error with Unit 1 Flag, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedFlag1, arg2=deliveryFlag1))
        if deliveryFlag2 != expectedFlag2:
            failures.append(customMessage + "Error with Unit 2 Flag, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedFlag2, arg2=deliveryFlag2))
        if deliveryFlag3 != expectedFlag3:
            failures.append(customMessage + "Error with Unit 3 Flag, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedFlag3, arg2=deliveryFlag3))
        if RequestedCount != expectedRequestedCount:
            failures.append(customMessage + "Error with Requested Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedRequestedCount, arg2=RequestedCount))
        if CurrentCount != expectedCurrentCount:
            failures.append(customMessage + "Error with Current Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedCurrentCount, arg2=CurrentCount))

    @staticmethod
    def get_unit_allocation(refObj, locker_bank):
        """
        This method is used for getting the value of the count using the get unit allocation api
        :return: status of counts
        """
        EnabledCount = 0
        AvailableCount = 0
        RequestedCount = 0
        CurrentCount = 0
        res, status_code = refObj.get_locker_management_unit_allocation(locker_bank, "valid", "validResource")
        EnabledCount = res['deliveryUnits'][0]['count']['countEnabled']
        AvailableCount = res['deliveryUnits'][0]['count']['countAvailable']
        RequestedCount = res['deliveryUnits'][0]['count']['countRequested']
        CurrentCount = res['deliveryUnits'][0]['count']['countCurrent']

        return EnabledCount, AvailableCount, RequestedCount, CurrentCount

    def check_unit_allocation(self, refObj, locker_bank, expectedEnabledCount, expectedAvailableCount,
                              expectedRequestedCount, expectedCurrentCount, customMessage, failures):
        """
        This method is used for validating the value of count
        if validation fails then appended to failures list along with customMessage
        :return: nothing
        """

        EnabledCount, AvailableCount, RequestedCount, CurrentCount = self.get_unit_allocation(refObj, locker_bank)

        if EnabledCount != expectedEnabledCount:
            failures.append(customMessage + "Error with Enabled Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedEnabledCount, arg2=EnabledCount))
        if AvailableCount != expectedAvailableCount:
            failures.append(customMessage + "Error with Available Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedAvailableCount, arg2=AvailableCount))
        if RequestedCount != expectedRequestedCount:
            failures.append(customMessage + "Error with Requested Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedRequestedCount, arg2=RequestedCount))
        if CurrentCount != expectedCurrentCount:
            failures.append(customMessage + "Error with Current Count, Expected={arg1}/Received={arg2}".
                            format(arg1=expectedCurrentCount, arg2=CurrentCount))

    """TEST Reservation with flag false and true using reserve api"""

    # ----------------------------Have Reservations for 1.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_ssto_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for ssto 1.0 with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "SSTO" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_ssto_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates the reservation for ssto 1.0 with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "SSTO" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for 2.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_fireball_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for ssto 2.0 with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "Fireball" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_fireball_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates reservation for ssto 2.0 with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "Fireball" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for delivery---------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_delivery_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for delivery with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_delivery_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates the reservation for delivery with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for storage----------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_storage_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for storage with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="medium",
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=recipientID, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_storage_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates the reservation for storage with unit delivery flag as true (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="medium",
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=recipientID, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for return----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_return_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for return with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="return",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_return_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates the reservation for return with unit delivery flag as true (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="return",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for exchange----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_exchange_reservation_with_flag_false(self, rp_logger, resource):
        """
        This test validates the reservation for exchange with unit delivery flag as false (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="exchange",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_exchange_reservation_with_flag_true(self, rp_logger, resource):
        """
        This test validates the reservation for exchange with unit delivery flag as true (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="exchange",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """TEST Reservation with flag true using reserve with unit api"""

    # ----------------------------Have Reservations for 1.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_ssto_reservationUnit_with_flag_true(self, rp_logger, resource):
        """
        This test validates unit reservation for ssto 1.0 with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "SSTO" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit='3',
                                                                                  size="", accessible="",
                                                                                  refrigeration="",
                                                                                  climate_type="", TrkgID=trackingID,
                                                                                  EmailID="", recipientID=recipientID,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for 2.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_fireball_reservationUnit_with_flag_true(self, rp_logger, resource):
        """
        This test validates unit reservation for ssto 2.0 with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "Fireball" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit='3',
                                                                                  size="", accessible="",
                                                                                  refrigeration="",
                                                                                  climate_type="", TrkgID=trackingID,
                                                                                  EmailID="", recipientID=recipientID,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for delivery----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_delivery_reservationUnit_with_flag_true(self, rp_logger, resource):
        """
        This test validates unit reservation for delivery with unit delivery flag as true (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit='3',
                                                                                  size="", accessible="",
                                                                                  refrigeration="",
                                                                                  climate_type="", TrkgID=trackingID,
                                                                                  EmailID="", recipientID=recipientID,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for return----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_return_reservationUnit_with_flag_true(self, rp_logger, resource):
        """
        This test validates unit reservation for return with unit delivery flag as true (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                     locker_unit='3',
                                                                                     size="medium",
                                                                                     reservation_type="return",
                                                                                     accessible="", refrigeration="",
                                                                                     climate_type="",
                                                                                     TrackingID=trackingID,
                                                                                     receiver=recipientID,
                                                                                     depositor=depositor,
                                                                                     departmentMail=False,
                                                                                     flagRecipient=flagRecipient,
                                                                                     flagDepositor=flagDepositor,
                                                                                     token_type="valid",
                                                                                     resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ----------------------------Have Reservations for exchange----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_exchange_reservationUnit_with_flag_true(self, rp_logger, resource):
        """
        This test validates unit reservation for exchange with unit delivery flag as true (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                     locker_unit='3',
                                                                                     size="medium",
                                                                                     reservation_type="exchange",
                                                                                     accessible="", refrigeration="",
                                                                                     climate_type="",
                                                                                     TrackingID=trackingID,
                                                                                     receiver=recipientID,
                                                                                     depositor=depositor,
                                                                                     departmentMail=False,
                                                                                     flagRecipient=flagRecipient,
                                                                                     flagDepositor=flagDepositor,
                                                                                     token_type="valid",
                                                                                     resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # --------------------------CANCEL RESERVATION ------------------------
    """Test Cancel Reservation API's for requested count > current count
        1.Make some reservation for deliver.
        2.Make request for more than available.
        3.Cancel reservation for them.
        EXPECTED -  Unit would be assigned for delivery
    """

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_cancel_reservation_unit_requested_more(self, rp_logger, resource):
        """
        This test validates assignment of unit for delivery when unit reservation is cancelled (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_cancel_reservation_trackingID_requested_more(self, rp_logger, resource, context):
        """
        This test validates assignment of unit for delivery when unit reservation is cancelled (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(trackingID, locker_unit,
                                                                                          locker_bank,"valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """Test Cancel Reservation API's for requested count < current count.
        1. Assign units to delivery in settings page.
        2. Make reservations against those size for delivery .
        3. Go to the settings page and reduce the slider count.
        4. Cancel Reservation
        EXPECTED -  Unit would be unassigned for delivery
    """

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_cancel_reservation_unit_requested_less(self, rp_logger, resource):
        """
        This test validates un assigning of delivery unit if the count is decreased when unit is cancelled (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting less units after assignment : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_cancel_reservation_trackingID_requested_less(self, rp_logger, resource, context):
        """
        This test validates un assigning of delivery unit if the count is decreased when unit is cancelled (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting less units after assignment : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(trackingID, locker_unit,
                                                                                          locker_bank,"valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # --------------------------PICK UP RESERVATIONS------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_delivery_flow_with_flag_false(self, rp_logger, resource):
        """
        This test validates the enabling of day locker in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_delivery_flow_with_flag_true(self, rp_logger, resource):
        """
        This test validates the enabling of day locker in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """Test Pickup Reservation for requested count > current count
       1.Make some reservation for deliver.
       2.Make request for more than available.
       3.Deposit and pickup reservation for them.
       EXPECTED -  Unit would be assigned for delivery
    """

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_delivery_flow_with_requested_more(self, rp_logger, resource):
        """
        This test validates assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """Test Pickup Reservation for requested count < current count.
        1.Assign units to delivery in settings page.
        2. Make reservations for delivery and do a deposit for it.
        3. Go to the settings page and reduce the slider count.
        4. Go to Manage Lockers and pickup those package reservations.
        EXPECTED -  Unit would be unassigned for delivery
    """

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_delivery_flow_with_requested_less(self, rp_logger, resource):
        """
        This test validates un assigning of delivery unit if the count is decreased when unit is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting less units after assignment : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Pickup reservation for 1.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_ssto_flow_with_requested_more(self, rp_logger, resource):
        """
        This test validates assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "SSTO" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_ssto_flow_with_requested_less(self, rp_logger, resource):
        """
        This test validates un assigning of delivery unit if the count is decreased when unit is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "SSTO" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting less units after assignment : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Pickup reservation for 1.0----------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_fireball_flow_with_requested_more(self, rp_logger, resource):
        """
        This test validates assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "Fireball" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_fireball_flow_with_requested_less(self, rp_logger, resource):
        """
        This test validates un assigning of delivery unit if the count is decreased when unit is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = "Fireball" + test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting less units after assignment : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Pickup reservation for Storage---------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_daylocker_flow_with_requested_more(self, rp_logger, resource):
        """
        This test assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="medium",
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=recipientID, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Pickup reservation for Return---------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_return_flow_with_requested_more(self, rp_logger, resource):
        """
        This test assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="return",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Pickup reservation for Exchange---------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_exchange_flow_with_requested_more(self, rp_logger, resource):
        """
        This test validates assignment of unit for delivery when unit reservation is picked up (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')
        flagRecipient = flagDepositor = "personal"

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                  size="medium",
                                                                                  reservation_type="exchange",
                                                                                  accessible=""
                                                                                  , refrigeration="", climate_type="",
                                                                                  TrackingID=trackingID,
                                                                                  receiver=recipientID,
                                                                                  depositor=depositor,
                                                                                  departmentMail=False,
                                                                                  flagRecipient=flagRecipient,
                                                                                  flagDepositor=flagDepositor,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requesting more units than available : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # -------------------------Disabled / Enabled Units ---------------------------------------
    """Place bank oos the assigned lockers should be same"""

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_change_of_units_outofservice_bank_with_none_assign(self, rp_logger, resource):
        """
        This test validates when bank is out of service then assigned units and placed bank in service state remains same (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Bank Out Of Service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Bank In Service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_change_of_units_outofservice_bank_with_assign(self, rp_logger, resource):
        """
        This test validates when delivery unit assigned then bank is out of service then placed in service state remains same (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Bank Out Of Service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Bank In Service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """have 3 oss-> make reservation 1 -> assign 2 lockers req 2 curr 1 -> 3 in service req2 curr 2"""

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_oos_units_assigned_when_requested_more(self, rp_logger, resource):
        """
        This test validates the enabling of day locker in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "3", False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Set value to 2 : "
        self.set_value(resource['storage'], locker_bank, 2)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=False, expectedRequestedCount=2,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "3", True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Unit 3 In Service : "
        self.set_value(resource['storage'], locker_bank, 2)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=2,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation {}: ".format(locker_unit)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=2,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    """Made all units delivery-> made one unit oos-> unchanged count but changed flag -- count should also lessen - IL-6351"""

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_delivery_unit_made_outofservice(self, rp_logger, resource):
        """
        This test validates when delivery unit is out of service then placed in service state remains same(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "1", False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "2", False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Unit 1 and 2 out of service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "1", True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "2", True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Unit 1 and 2 in service : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ---------------------------Dedicated Units---------------------------------------
    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_dedicated_units_assigned_when_requested_more(self, rp_logger, resource, context):
        """
        This test validates assignment of unit for delivery when dedicated units are removed (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['dedicated'].verify_add_dedicated_locker(locker_bank=locker_bank,
                                                                             recipientFlag=True,
                                                                             recipientID=recipientID,
                                                                             token_type="valid",
                                                                             resource_type="validResource",
                                                                             Locker_unit='1')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dedicated'].verify_update_dedicate_locker(locker_bank=locker_bank,
                                                                               recipientFlag=True,
                                                                               recipientID=recipientID,
                                                                               token_type="valid",
                                                                               resource_type="validResource",
                                                                               Locker_unit='2')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID1"] = res['units'][0]['manufacturerLockerID']
        context["manufacturerLockerID2"] = res['units'][1]['manufacturerLockerID']

        customMessage = "After Dedicated : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['dedicated'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Unassigned Dedicated : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_dedicated_units_assigned_when_requested_less(self, rp_logger, resource, context):
        """
        This test validates un assignment of delivery unit for when dedicated units are removed (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0:
            customMessage = "Since Failure assign units to 0 : "
            self.set_value(resource['storage'], locker_bank, 0)
            self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                             expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                             expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
            pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['dedicated'].verify_add_dedicated_locker(locker_bank=locker_bank,
                                                                             recipientFlag=True,
                                                                             recipientID=recipientID,
                                                                             token_type="valid",
                                                                             resource_type="validResource",
                                                                             Locker_unit='1')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dedicated'].verify_update_dedicate_locker(locker_bank=locker_bank,
                                                                               recipientFlag=True,
                                                                               recipientID=recipientID,
                                                                               token_type="valid",
                                                                               resource_type="validResource",
                                                                               Locker_unit='2')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID1"] = res['units'][0]['manufacturerLockerID']
        context["manufacturerLockerID2"] = res['units'][1]['manufacturerLockerID']

        customMessage = "After Dedicated : "
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Requested less : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['dedicated'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Unassigned dedicated : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # --------------------------Test counts in unit allocation------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_enabled_count(self, rp_logger, resource):
        """
        This test validates the enabled count while having out of service units (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3,
                                   expectedRequestedCount=0, expectedCurrentCount=0, customMessage=customMessage,
                                   failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "3", False, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Made unit 3 out of service : "
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=2,
                                   expectedAvailableCount=2, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, "3", True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "Made unit 3 in service : "
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # reservation, deposit, dedicated
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_available_count_having_reservations(self, rp_logger, resource):
        """
        This test validates the available count while having reserved units (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=2, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Cancel Reservation for unit {}: ".format(locker_unit)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_available_count_having_deposit(self, rp_logger, resource):
        """
        This test validates the available count while having occupied units (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        customMessage = "After Reservation for unit {}: ".format(locker_unit)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=2, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Deposit for unit {}: ".format(locker_unit)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=2, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Pickup for unit {}: ".format(locker_unit)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_available_count_having_dedicated(self, rp_logger, resource, context):
        """
        This test validates the available count while having dedicated units (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        res, status_code = resource['dedicated'].verify_add_dedicated_locker(locker_bank=locker_bank,
                                                                             recipientFlag=True,
                                                                             recipientID=recipientID,
                                                                             token_type="valid",
                                                                             resource_type="validResource",
                                                                             Locker_unit='1')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dedicated'].verify_update_dedicate_locker(locker_bank=locker_bank,
                                                                               recipientFlag=True,
                                                                               recipientID=recipientID,
                                                                               token_type="valid",
                                                                               resource_type="validResource",
                                                                               Locker_unit='2')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID1"] = res['units'][0]['manufacturerLockerID']
        context["manufacturerLockerID2"] = res['units'][1]['manufacturerLockerID']

        customMessage = "After Dedicated : "
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=1, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        res, status_code = resource['dedicated'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        customMessage = "After Unassigned Dedicated : "
        self.check_unit_allocation(refObj=resource['storage'], locker_bank=locker_bank, expectedEnabledCount=3,
                                   expectedAvailableCount=3, expectedRequestedCount=0, expectedCurrentCount=0,
                                   customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # --------------------------Test Flags and Count------------------------
    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_increase_single_count(self, rp_logger, resource):
        """
        This test validates the count when increased by 1 (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Increase count to 1 : "
        self.set_value(resource['storage'], locker_bank, 1)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=1,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        customMessage = "Increase count to 2 : "
        self.set_value(resource['storage'], locker_bank, 2)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=False, expectedRequestedCount=2,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        customMessage = "Increase count to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_increase_double_count(self, rp_logger, resource):
        """
        This test validates the count when increased by 2 (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Increase count to 2 : "
        self.set_value(resource['storage'], locker_bank, 2)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=False, expectedRequestedCount=2,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        customMessage = "Increase count to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_decrease_single_count(self, rp_logger, resource):
        """
        This test validates the count when decreased by 1 (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Decrease count to 2 : "
        self.set_value(resource['storage'], locker_bank, 2)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=2,
                         expectedCurrentCount=2, customMessage=customMessage, failures=self.Failures)

        customMessage = "Decrease count to 1 : "
        self.set_value(resource['storage'], locker_bank, 1)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=True, expectedRequestedCount=1,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        customMessage = "Decrease count to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.daylocker
    @pytest.mark.regressioncheck_lockers
    def test_decrease_double_count(self, rp_logger, resource):
        """
        This test validates count when decreased by 2 (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        customMessage = "Set value to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Set value to 3 : "
        self.set_value(resource['storage'], locker_bank, 3)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=True,
                         expectedFlag2=True, expectedFlag3=True, expectedRequestedCount=3,
                         expectedCurrentCount=3, customMessage=customMessage, failures=self.Failures)
        if len(self.Failures) > 0: pytest.fail("Error encountered in Step 1. {arg}".format(arg=self.Failures))

        customMessage = "Decrease count to 1 : "
        self.set_value(resource['storage'], locker_bank, 1)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=True, expectedRequestedCount=1,
                         expectedCurrentCount=1, customMessage=customMessage, failures=self.Failures)

        customMessage = "Decrease count to 0 : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        customMessage = "Reset Slider : "
        self.set_value(resource['storage'], locker_bank, 0)
        self.check_value(refObj=resource['lockerapi'], locker_bank=locker_bank, expectedFlag1=False,
                         expectedFlag2=False, expectedFlag3=False, expectedRequestedCount=0,
                         expectedCurrentCount=0, customMessage=customMessage, failures=self.Failures)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))
