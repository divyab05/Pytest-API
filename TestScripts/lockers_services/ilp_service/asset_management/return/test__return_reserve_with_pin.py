""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from APIObjects.lockers_services.ilp_service.update_flow import UpdateFlow
from APIObjects.lockers_services.ilp_service.reserve_with_pin import ReserveWithPin
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    reserveWithPin = {'app_config': app_config,
                      'return': ReserveWithPin(app_config, client_token),
                      'lockerapi': LockerAPI(app_config, client_token),
                      'dept_api': DepartmentLockerAPI(app_config, client_token),
                      'updateapi': UpdateFlow(app_config, client_token),
                      'cancelreservation': CancelReservation(app_config, client_token),
                      'data_reader': DataReader(app_config),
                      'get_product_name': get_product_name}
    yield reserveWithPin


@pytest.mark.usefixtures('initialize')
class TestReserveReturn(common_utils):

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
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_recipient_to_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------Recipient to Department Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_recipient_to_department(self, rp_logger, resource, context):
        """
        This test validates the reservation of return flow for recipient to department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "department"
        flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=True
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
    def test_reserveWithPin_recipient_to_department_when_departmentMail_false(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to department when recipient departmentMail false (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "department"
        flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ----------------------------Department to Recipient Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_department_to_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for Department to Recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "personal"
        flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=True
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
    def test_reserveWithPin_department_to_recipient_when_departmentMail_is_false(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for Department to Recipient when departmentMail is false (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = "personal"
        flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ----------------------------Department to Department Flow----------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_department_to_department(self, rp_logger, resource, context):
        """
        This test validates the reservation of return flow for Department to Department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
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
                                                                                    departmentMail,
                                                                                    receiver, departmentpickcode,
                                                                                    "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------------------------------------------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_for_accessible_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for accessible locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=True
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
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
    def test_reserveWithPin_for_dry_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for dry locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration=True,
                                                                                 climate_type="dry",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
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
    def test_reserveWithPin_for_ambient_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for ambient locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration=True,
                                                                                 climate_type="ambient",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
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
    def test_reserveWithPin_for_frozen_locker(self, rp_logger, resource):
        """
        This test validates the reserve with pin for frozen locker (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=''
                                                                                 , refrigeration=True,
                                                                                 climate_type="frozen",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
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

    # -----------------------------------------------------------------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_recipient_to_recipient_duplicate_case(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to same recipient (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_department_to_department_duplicate_case(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for department to same department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_recipient_to_recipient_with_no_recipient(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for no recipient (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver="", depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_recipient_to_recipient_with_no_depositor(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for no depositor (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor="",
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_then_update_reservation(self, rp_logger, resource):
        """
        This test validates the reservation of return flow and then update the reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible="",
                                                                                 refrigeration="", climate_type="",
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
    def test_reserveWithPin_for_duplicate_tracking_id(self, rp_logger, context, resource):
        """
        This test validates the reservation for duplicate tracking ID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
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
        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible="",
                                                                                 refrigeration="", climate_type="",
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
    def test_reserveWithPin_when_no_size_provided(self, rp_logger, resource):
        """
        This test validates the reservation when no size is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_no_reservationType_provided(self, rp_logger, resource):
        """
        This test validates the reservation when no reservation type is provided  (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="", accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_no_trackingID_provided(self, rp_logger, resource):
        """
        This test validates the reservation when no tracking ID is provided  (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="", accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID="",
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_no_climateType_provided(self, rp_logger, resource):
        """
        This test validates the reservation when no climate type is provided  (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="", accessible=""
                                                                                 , refrigeration=True, climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalidSize_provided(self, rp_logger, resource):
        """
        This test validates the reservation when invalid size is provided  (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalid_recipient_provided(self, rp_logger, resource):
        """
        This test validates the reservation when invalid recipient is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalid_department_provided(self, rp_logger, resource):
        """
        This test validates the reservation when invalid department is provided  (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=True
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalid_resource(self, rp_logger, resource):
        """
        This test validates the reservation when invalid resource is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the reservation when invalid access token is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="invalid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the reservation when invalid lockerbank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank="invalidBank",
                                                                                 size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserveWithPin_when_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the reservation when no lockerbank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['return'].verify_reserve_with_pin_locker_api(locker_bank="", size=locker_size,
                                                                                 reservation_type="return",
                                                                                 accessible=""
                                                                                 , refrigeration="", climate_type="",
                                                                                 TrackingID=trackingID,
                                                                                 receiver=receiver, depositor=depositor,
                                                                                 departmentMail=False
                                                                                 , flagRecipient=flagRecipient,
                                                                                 flagDepositor=flagDepositor,
                                                                                 token_type="valid",
                                                                                 resource_type="validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True
