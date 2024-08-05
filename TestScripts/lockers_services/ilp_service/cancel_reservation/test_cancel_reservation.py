""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    cancelreservation = {'app_config': app_config,
                         'cancelreservation': CancelReservation(app_config, client_token),
                         'locker_api': LockerAPI(app_config, client_token),
                         'data_reader': DataReader(app_config),
                         'get_product_name': get_product_name}
    yield cancelreservation


@pytest.mark.usefixtures('initialize')
class TestCancelReservation(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Cancel_Reservation"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # -----------------------------Cancel Reservation BY LOCKER UNIT ID--------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID(self, rp_logger, context, resource):
        """
        This test validates cancel reservation by providing locker unit (positive scenario)
        :return: return test status
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('cancel_reservation_unit_res_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_no_reserved_unit(self, rp_logger, resource):
        """
        This test validates cancel reservation for no reserved unit (negative scenario)
        :return: return test status
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_invalid_unit(self, rp_logger, resource):
        """
        This test validates cancel reservation for invalid unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates cancel reservation by providing invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates cancel reservation by providing invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "invalid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates cancel reservation by providing invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 "invalidBank", "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_lockerunitID_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates cancel reservation by providing no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit, "",
                                                                                                 "valid",
                                                                                                 "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------Cancel Reservation BY Tracking ID--------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_trackingID_and_lockerunitID(self, rp_logger, context, resource):
        """
        This test validates cancel reservation api by providing trackingID and Locker unit id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit,
                                                                                          locker_bank, "valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file(
            'cancel_reservation_by_tracking_res_schema.json', 'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_trackingID_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates cancel reservation by providing invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = TrkgID = '0'

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit,
                                                                                          locker_bank, "valid",
                                                                                          "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_trackingID_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates cancel reservation by providing invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = TrkgID = '0'

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit,
                                                                                          locker_bank, "invalid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_trackingID_with_invalid_lockerBank(self, rp_logger, resource, context):
        """
        This test validates cancel reservation by providing invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = TrkgID = '0'

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit,
                                                                                          "invalidBank", "valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_cancel_reservation_by_trackingID_with_no_lockerBank(self, rp_logger, resource, context):
        """
        This test validates cancel reservation by providing no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = TrkgID = '0'

        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit, "",
                                                                                          "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------------------Free List of UNITS-------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units(self, rp_logger, resource):
        """
        This test validates cancel reservation of units (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        unit_one = res['manufacturerLockerID']
        TrkgID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        unit_two = res['manufacturerLockerID']

        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, locker_bank,
                                                                                   "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('free_list_of_units_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_with_no_reserved_units(self, rp_logger, resource):
        """
        This test validates cancel reservation of units with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')

        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, locker_bank,
                                                                                   "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.skip(reason="IL-8945")
    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_with_invalid_units(self, rp_logger, resource):
        """
        This test validates cancel reservation of units with invalid units (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')

        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, locker_bank,
                                                                                   "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(500, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates cancel reservation of units with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')
        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, locker_bank,
                                                                                   "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates cancel reservation of units with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')
        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, locker_bank,
                                                                                   "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_invalid_locker_bank(self, rp_logger, context, resource):
        """
        This test validates cancel reservation of units with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')
        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, "invalidBank",
                                                                                   "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_free_list_of_units_no_locker_bank(self, rp_logger, context, resource):
        """
        This test validates cancel reservation of units with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        unit_one = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        unit_two = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit')
        res, status_code = resource['cancelreservation'].free_list_of_locker_units(unit_one, unit_two, "", "valid",
                                                                                   "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -------------------Kiosk Token (Keep at the end of file)----------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_cancel_reservation_by_trackingID_and_lockerunitID(self, rp_logger, context, resource):
        """
        This test validates cancel reservation api by providing trackingID and Locker unit id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource",
                                                                            kioskToken=context)

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_by_trackingID(TrkgID, locker_unit,
                                                                                          locker_bank, "valid",
                                                                                          "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file(
            'cancel_reservation_by_tracking_res_schema.json', 'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))
