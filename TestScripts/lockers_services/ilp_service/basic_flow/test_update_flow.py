""" This module contains all test cases."""

import random
import sys

import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.update_flow import UpdateFlow
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    updateapi = {'app_config': app_config,
                 'updateapi': UpdateFlow(app_config, client_token),
                 'locker_api': LockerAPI(app_config, client_token),
                 'cancel_reservation': CancelReservation(app_config, client_token),
                 'data_reader': DataReader(app_config),
                 'get_product_name': get_product_name}
    yield updateapi


@pytest.mark.usefixtures('initialize')
class TestUpdateFlow(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Update_Flow"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # Create Reservation for other testcases to reduce API calls.
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_create_reservation_for_update_reservation_testcases(self, rp_logger, context, resource):
        """
        This function will create reservation to be used in other testcases
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_size')
        recipient = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipient,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context['update_reserve_trackingID'] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['locker_unit'] = res['manufacturerLockerID']

    # ------------------------------Update Reservation for LOCKER---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_no_trackingID(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with no tracking id (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'], "",
                                                                                         "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_invalid_unit(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with invalid unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank, "xx", trackingID,
                                                                                         "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_not_reserved_unit(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with no previous reserved unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(random.randint(1, 100))
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank, locker_unit,
                                                                                         trackingID,
                                                                                         "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_invalid_resource(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "invalid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit("invalidBank",
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit("", context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------------Update Reservation via Tracking ID-----------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_when_no_reservation(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with no previous reservation (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID(locker_bank, trackingID,
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_when_no_trackingID_provided(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with no tracking id provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID(locker_bank, context[
            'update_reserve_trackingID'],
                                                                                         "", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID(locker_bank, context[
            'update_reserve_trackingID'],
                                                                                         trackingID, "valid",
                                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID(locker_bank, context[
            'update_reserve_trackingID'],
                                                                                         trackingID, "invalid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID("invalidBank", context[
            'update_reserve_trackingID'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID("", context[
            'update_reserve_trackingID'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------------------Multi Deposit-------------------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_invalid_unit(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages at a single locker unit (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels(locker_bank, "xxx",
                                                                                 context['update_reserve_trackingID'],
                                                                                 trackingID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank, "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_for_no_trackingID(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages at a single locker unit  (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels(locker_bank, context['locker_unit'],
                                                                                 "", "", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank, "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages with invalid resource (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels(locker_bank, context['locker_unit'],
                                                                                 context['update_reserve_trackingID'],
                                                                                 trackingID, "valid",
                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_invalid_token(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages with invalid access token (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels(locker_bank, context['locker_unit'],
                                                                                 context['update_reserve_trackingID'],
                                                                                 trackingID, "invalid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages with invalid locker bank (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels("invalidBank", context['locker_unit'],
                                                                                 context['update_reserve_trackingID'],
                                                                                 trackingID, "valid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_multiple_package_deposit_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the deposit of multiple packages with no locker bank (negative scenario)
        :return: returns test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['updateapi'].verify_deposit_multiple_parcels("", context['locker_unit'],
                                                                                 context['update_reserve_trackingID'],
                                                                                 trackingID, "valid",
                                                                                 "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # Executing sanity tests below since last test need to end the reservation
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_based_on_unit(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_ID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         tracking_ID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(tracking_ID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_update_reservation_based_on_unit(self, rp_logger, context, resource):
        """
        This function validates the updation of reservation (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                         context['locker_unit'],
                                                                                         trackingID, "valid",
                                                                                         "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['cancel_reservation'].cancel_reservation_by_trackingID(trackingID,
                                                                                           context['locker_unit'],
                                                                                           locker_bank, "valid",
                                                                                           "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ------- Locker 36 has a reservation just check Update for Private post reservation ----------
    # @pytest.mark.regressioncheck_lockers
    # def test_update_reservation_based_unit_api_for_private_recipient(self, rp_logger, resource):
    #     """
    #     This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
    #     :return: return test status
    #     """
    #     test_name = sys._getframe().f_code.co_name
    #     rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
    #
    #     trackingID = test_name + str(random.randint(1, 35000))
    #     locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
    #     locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
    #
    #     res, status_code = resource['updateapi'].verify_update_reservation_based_on_unit(locker_bank, locker_unit,
    #                                                                                      trackingID, "valid",
    #                                                                                      "validResource")
    #     assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # Always keep this testcase last, since it will end the reservation
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_by_trackingID(self, rp_logger, context, resource):
        """
        This test validates the update reservation by Tracking ID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['updateapi'].verify_update_reservation_by_trackingID(locker_bank, context[
            'update_reserve_trackingID'],
                                                                                         trackingID, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        # end reservation for entire unit
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(
            context['locker_unit'], locker_bank,
            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

