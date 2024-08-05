""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from APIObjects.lockers_services.ilp_service.update_flow import UpdateFlow
from APIObjects.lockers_services.ilp_service.dedicate_locker import DedicateLocker
from APIObjects.lockers_services.ilp_service.reserve_with_pin import ReserveWithPin
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    reserveWithPin = {'app_config': app_config,
                      'exchangeUnit': ReserveWithPin(app_config, client_token),
                      'lockerapi': LockerAPI(app_config, client_token),
                      'dept_api': DepartmentLockerAPI(app_config, client_token),
                      'updateapi': UpdateFlow(app_config, client_token),
                      'cancelreservation': CancelReservation(app_config, client_token),
                      'dedicatedLocker': DedicateLocker(app_config, client_token),
                      'data_reader': DataReader(app_config),
                      'get_product_name': get_product_name}
    yield reserveWithPin


@pytest.mark.usefixtures('initialize')
class TestExchangeReserveByUnit(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_ReserveWithPin_Flow"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ----------------------------Recipient to Recipient Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------Recipient to Department Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_department(self, rp_logger, resource, context):
        """
        This test validates the reservation of exchange flow for recipient to department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "department"
        flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=True,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_department_when_departmentMail_false(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for recipient to department when recipient departmentMail false (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "department"
        flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ----------------------------Department to Recipient Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_department_to_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for Department to Recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "personal"
        flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=True,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_department_to_recipient_when_departmentMail_is_false(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for Department to Recipient when department flag is false (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "personal"
        flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ----------------------------Department to Department Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_department_to_department(self, rp_logger, resource, context):
        """
        This test validates the reservation of exchange flow for Department to Department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=True
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        departmentpickcode = "new123"
        departmentMail = True
        context['manufacturerLockerID_dept'] = locker_unit

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, receiver,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------------------------------------------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_accessible_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for accessible locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=True
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_dry_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for dry locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration=True,
                                                                                          climate_type="dry",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_ambient_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for ambient locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration=True,
                                                                                          climate_type="ambient",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_frozen_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for frozen locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=''
                                                                                          , refrigeration=True,
                                                                                          climate_type="frozen",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_dedicated_recipient_locker(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for dedicated locker to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank=locker_bank,
                                                                                   recipientFlag=True,
                                                                                   recipientID=receiver,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource",
                                                                                   Locker_unit=locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_dedicated_department_locker(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for dedicated locker to department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank=locker_bank,
                                                                                   recipientFlag=False,
                                                                                   recipientID=receiver,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource",
                                                                                   Locker_unit=locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=True,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # -----------------------------------------------------------------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_recipient_duplicate_case(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for recipient to same recipient (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_department_to_department_duplicate_case(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for department to same department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_recipient_with_no_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no recipient(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver="",
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_recipient_to_recipient_with_no_depositor(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no depositor (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor="",
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_then_update_reservation(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow and then update the reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res["manufacturerLockerID"]
        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank, locker_unit,
                                                                                         new_tracking_id="test123123",
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_duplicate_tracking_id(self, rp_logger, resource):
        """
        This test validates the reservation for duplicate tracking ID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        lockerUnit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="",
                                                                           TrkgID=trackingID, EmailID="",
                                                                           recipientID=receiver,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=lockerUnit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_for_already_reserved_unit(self, rp_logger, resource):
        """
        This test validates the reservation for already occupied unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit=locker_unit,
                                                                                  size=locker_size,
                                                                                  accessible="", refrigeration="",
                                                                                  climate_type="",
                                                                                  TrkgID=trackingID, EmailID="",
                                                                                  recipientID=receiver,
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        trackingID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_no_size_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no size provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_no_reservationType_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no reservation type provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_no_trackingID_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no tracking ID provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID="",
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_no_climateType_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no climate type provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="",
                                                                                          accessible=""
                                                                                          , refrigeration=True,
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_invalid_recipient_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for invalid recipient (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_invalid_department_provided(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for invalid department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=True
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_invalid_resource(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="invalidResource")

        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="invalid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank="invalidBank",
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_for_when_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank="",
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------Private Flow---------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_api_for_private_recipient_as_receiver(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_bank")
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_by_unit_api_for_private_recipient_as_depositor(self, rp_logger, resource):
        """
        This test validates the reservation of exchange flow for no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_bank")
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible=""
                                                                                          , refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False
                                                                                          , flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # --------------------Kiosk Token Flow (Keep it at end of the file)----------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_reserve_by_unit_for_recipient_to_recipient(self, rp_logger, resource, context):
        """
        This test validates the reservation of exchange flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['exchangeUnit'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                          locker_unit=locker_unit,
                                                                                          size=locker_size,
                                                                                          reservation_type="exchange",
                                                                                          accessible="",
                                                                                          refrigeration="",
                                                                                          climate_type="",
                                                                                          TrackingID=trackingID,
                                                                                          receiver=receiver,
                                                                                          depositor=depositor,
                                                                                          departmentMail=False,
                                                                                          flagRecipient=flagRecipient,
                                                                                          flagDepositor=flagDepositor,
                                                                                          token_type="valid",
                                                                                          resource_type="validResource",
                                                                                          kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource",
                                                                                                 context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
