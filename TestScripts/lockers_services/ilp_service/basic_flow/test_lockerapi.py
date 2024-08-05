""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    locker_api = {'app_config': app_config,
                  'locker_api': LockerAPI(app_config, client_token),
                  'cancel_reservation': CancelReservation(app_config, client_token),
                  'configuration': ConfigurationAPI(app_config, client_token),
                  'data_reader': DataReader(app_config),
                  'get_product_name': get_product_name}
    yield locker_api


@pytest.mark.usefixtures('initialize')
class TestLockerApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """

        self.configparameter = "LOCKERS_Personal_Flow"
        self.Failures = []
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ------------------------------LOCKER BANK DETAILS---------------------------------------------
    @pytest.mark.order(2)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360canada
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_details(self, rp_logger, context, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        context["tenantID"] = res['tenantID']
        context["siteID"] = res['siteID']
        context["integratorID"] = res['integratorID']
        context["manufacturerID"] = res['manufacturerID']
        context["manufacturerHardwareID"] = res['manufacturerHardwareID']

        # result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_detail_schema.json',
        #                                                                         'lockers_services'))
        # if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
        #                                      "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_details_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank details with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_response_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_response_with_invalid_lockerbank(self, rp_logger, resource):
        """
        This test validates locker bank details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_Lockerbank_details("invalidbank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # --------------------------------------Reserve Locker---------------------------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_by_emailID(self, rp_logger, context, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('reserveapi_response_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        # Cancel Reservation
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.order(3)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_by_recipientID(self, rp_logger, context, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        context["manufacturerLockerID"] = res['manufacturerLockerID']
        context["Res_trackID"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID'] = recipientID

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('reserveapi_response_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_accessible_locker(self, rp_logger, context, resource):
        """
        This test validates reservation for accessible unit is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_accessible = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_accessible")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible=locker_accessible,
                                                                            refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Cancel Reservation
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_dry_locker_type(self, rp_logger, context, resource):
        """
        This test validates reservation for dry locker unit is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="",
                                                                            refrigeration=locker_refrigeration,
                                                                            climate_type=locker_type, TrkgID=TrkgID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Cancel Reservation
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_ambient_locker_type(self, rp_logger, context, resource):
        """
        This test validates reservation for dry locker unit is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="",
                                                                            refrigeration=locker_refrigeration,
                                                                            climate_type=locker_type, TrkgID=TrkgID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Cancel Reservation
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_frozen_locker_type(self, rp_logger, context, resource):
        """
        This test validates reservation for dry locker unit is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="",
                                                                            refrigeration=locker_refrigeration,
                                                                            climate_type=locker_type, TrkgID=TrkgID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Cancel Reservation
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_by_invalid_recipientID(self, rp_logger, context, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="",
                                                                            TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    def test_verify_reserve_locker_api_with_duplicate_trackingID(self, rp_logger, context, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Assertion for Duplicate TrackingID
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        # Cancel Reservation
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_API_response_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates reservation of locker with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_API_response_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="invalid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_API_response_with_invalid_lockerbank(self, rp_logger, resource):
        """
        This test validates locker bank with invalid locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank="invalidBank", size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_API_response_with_no_lockerbank(self, rp_logger, resource):
        """
        This test validates locker bank with no locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank="", size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_api_when_no_size_provided(self, rp_logger, resource):
        """
        This test validates reservation with no size (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_climate_locker_when_no_lockerType_provided(self, rp_logger, resource):
        """
        This test validates reservation with no size (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrkgID = test_name + str(random.randint(1, 35000))
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_accessible = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_accessible")
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible=locker_accessible,
                                                                            refrigeration=locker_refrigeration,
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_api_response_with_no_trackingID_provided(self, rp_logger, resource):
        """
        This test validates reservation with no tracking ID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID="", EmailID=EmailID,
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_api_response_with_no_emailID_provided(self, rp_logger, resource):
        """
        This test validates reservation with no email id provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # ------------------------------GET RESERVED LOCKER BASED ON TRACKING ID---------------------------------------------
    @pytest.mark.order(4)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('reserved_based_trackingID_res_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api_with_invalid_resource(self, rp_logger, context,
                                                                                      resource):
        """
        This function validates the reservation of locker unit when invalid resource is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 locker_bank, "valid",
                                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api_with_invalid_access_token(self, rp_logger, context,
                                                                                          resource):
        """
        This function validates the reservation of locker unit when invalid access token is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 locker_bank, "invalid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api_with_invalid_locker_bank(self, rp_logger, context,
                                                                                         resource):
        """
        This function validates the reservation of locker unit when invalid bank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 "invalidBank", "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api_with_no_locker_bank(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when no locker bank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 "", "valid",
                                                                                                 "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reserved_locker_based_on_trackingID_api_with_invalid_tracking_id(self, rp_logger, context,
                                                                                         resource):
        """
        This function validates the reservation of locker unit when invalid tracking ID is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID("INVALIDtrackingID",
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ---------------------------GET RESERVED V2 based on recipient id-----------------------------------
    @pytest.mark.order(5)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_V2(locker_bank, context['recipientID'], "valid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file(
            'reservedV2_singleUnit_reserve_res_schema.json', 'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker_with_invalid_resource(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when invalid resource is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_V2(locker_bank, context['recipientID'], "valid",
                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when invalid access token is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_V2(locker_bank, context['recipientID'], "invalid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker_with_invalid_locker_bank(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when invalid bank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_reserved_V2("invalidBank", context['recipientID'], "valid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker_no_locker_bank(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when no locker bank is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_reserved_V2("", context['recipientID'], "valid",
                                                                         "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_reservedV2_locker_invalid_recipient_id(self, rp_logger, context, resource):
        """
        This function validates the reservation of locker unit when invalid recipient ID is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_reserved_V2(locker_bank, "invalidRecipient", "valid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------DEPOSIT LOCKER---------------------------------------------
    @pytest.mark.order(6)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_api(self, rp_logger, context, resource):
        """
        This test validates the deposit APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code"] = res['assetsDeposited']['accesscode']
        result = self.validate_json_schema_validations(res, self.read_json_file('depositapi_responseschema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_API_response_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates deposit of locker with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_API_response_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates locker bank details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_API_response_with_invalid_lockerbank_is_passed(self, rp_logger, context, resource):
        """
        This test validates the deposit APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            "Invalid_locker_bank", "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_API_response_with_no_lockerbank_is_passed(self, rp_logger, context, resource):
        """
        This test validates the deposit APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'], "",
                                                                            "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------AUTHENTICATE PICKUP---------------------------------------------
    @pytest.mark.order(7)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_authenticate_pickup_locker_api(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('authenticationapi_response_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Authenticatepickup_locker_api_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup API with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Authenticatepickup_locker_api_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_invalid_access_code_is_passed_authenticate_api(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        context['pickup_code'] = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                     'InvalidAccessCode')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Authenticatepickup_locker_api_with_invalid_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], "invalidBank",
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Authenticatepickup_locker_api_with_no_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], "", "valid",
                                                                                 "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Authenticatepickup_locker_api_with_multiple_parcel_same_recipeint_diffrent_lockerunit(self,
                                                                                                          rp_logger,
                                                                                                          context,
                                                                                                          resource):
        """
        This test validates the Authentication of pickup API with multiple parcels for same recipeint with personalPackageAllAtOnce
        with diffrent units(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        # reservation1
        TrkgID = "firstpackage" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        context["manufacturerLockerID"] = res['manufacturerLockerID']
        context["Res_trackID"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID'] = recipientID
        # reservation2
        TrkgID = "second-package" + str(random.randint(1, 35000))
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        context["manufacturerLockerID1"] = res['manufacturerLockerID']
        context["Res_trackID1"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID1'] = recipientID
        # deposit1
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code"] = res['assetsDeposited']['accesscode']
        # deposit2
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID1'],
                                                                            context['manufacturerLockerID1'],
                                                                            locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code1"] = res['assetsDeposited']['accesscode']

        # authenticate
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        PID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'PID')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "validResource")
        record_total = len(res["authUnits"])
        if record_total != 2:
            self.Failures.append(
                "Multiple pickup bases on the allpackageat once setting  = " + str(record_total))
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(PID, locker_bank,
                                                                                 "valid", "validResource")
        record_total = len(res["authUnits"])
        if record_total != 2:
            self.Failures.append(
                "Multiple pickup bases on the allpackageat once setting  = " + str(record_total))
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('authenticationapi_response_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
        # Pickup
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code'],
                                                                           context['manufacturerLockerID'], locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code1'],
                                                                           context['manufacturerLockerID1'],
                                                                           locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------PICKUP FROM LOCKER---------------------------------------------
    @pytest.mark.order(8)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_pickup_locker_api(self, rp_logger, context, resource):
        """
        This test validates the pickup APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code'],
                                                                           context['manufacturerLockerID'], locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('PickupApi_response_Schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_API_response_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the pickup APi with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['manufacturerLockerID'],
                                                                           context['pickup_code'], locker_bank, "valid",
                                                                           "invalidResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_API_response_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the pickup APi with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['manufacturerLockerID'],
                                                                           context['pickup_code'], locker_bank,
                                                                           "invalid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_invalid_Pickup_code_is_pass_when_pickup_is_done(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code'],
                                                                           context['manufacturerLockerID'], locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickup_api_with_invalid_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the pickup APi with invalid locker bank passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['manufacturerLockerID'],
                                                                           context['pickup_code'], "invalidBank",
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickup_api_with_no_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the pickup APi with no locker bank passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['manufacturerLockerID'],
                                                                           context['pickup_code'], "", "valid",
                                                                           "validResource", False)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------RESERVATION BASED ON LOCKER UNIT----------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('reserveapi_response_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit when invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(random.randint(1, 100))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit when invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(random.randint(1, 100))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="", token_type="invalid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_with_invalid_bank(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit when invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(random.randint(1, 100))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank="invalidBank",
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="", token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_with_no_bank(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit when no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_unit = str(random.randint(1, 100))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank="",
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_dry_locker(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size="", accessible="",
                                                                                   refrigeration=locker_refrigeration,
                                                                                   climate_type=locker_type,
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID, EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        reserved_unit = res["manufacturerLockerID"]
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(reserved_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_ambient_locker(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size="", accessible="",
                                                                                   refrigeration=locker_refrigeration,
                                                                                   climate_type=locker_type,
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID, EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        reserved_unit = res["manufacturerLockerID"]
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(reserved_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_frozen_locker(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_refrigeration = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                   "locker_refrigeration")
        locker_type = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_type")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size="", accessible="",
                                                                                   refrigeration=locker_refrigeration,
                                                                                   climate_type=locker_type,
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID, EmailID="",
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        reserved_unit = res["manufacturerLockerID"]
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(reserved_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_based_unit_accessible_locker(self, rp_logger, resource):
        """
        This test validates the reservation of locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_accessible = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_accessible")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size="",
                                                                                   accessible=locker_accessible,
                                                                                   refrigeration="", climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   recipientID=recipientID,
                                                                                   EmailID="", token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        reserved_unit = res["manufacturerLockerID"]
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(reserved_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # -----------------------------UNIQUE TRACKING ID----------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_unique_tracking_id(self, rp_logger, resource):
        """
        This test validates the unique tracking id ( positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_unique_tracking_id(locker_bank, tracking_id, "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
        value = res['status']
        if value:
            print("Success")
        else:
            print("Error")

    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_duplicate_tracking_id(self, rp_logger, resource):
        """
        This test validates the unique tracking id with duplicate tracking id given(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        recipient = resource['data_reader'].pd_get_data(self.configparameter, test_name, "recipientID")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=tracking_id,
                                                                            EmailID="",
                                                                            recipientID=recipient,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['locker_api'].verify_get_unique_tracking_id(locker_bank, tracking_id, "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        value = res['status']
        if value == False:
            print("Success")

        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_unique_tracking_id_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the unique tracking id with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_unique_tracking_id(locker_bank, tracking_id, "valid",
                                                                                "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_unique_tracking_id_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the unique tracking id with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_get_unique_tracking_id(locker_bank, tracking_id, "invalid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_unique_tracking_id_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the unique tracking id with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))

        res, status_code = resource['locker_api'].verify_get_unique_tracking_id("invalidBank", tracking_id, "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_unique_tracking_id_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the unique tracking id with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tracking_id = test_name + str(random.randint(1, 35000))

        res, status_code = resource['locker_api'].verify_get_unique_tracking_id("", tracking_id, "valid",
                                                                                "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------Older APIS---------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    def test_old_happy_flow_recipient(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api_v1(access_code, locker_bank,
                                                                                    "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                                  "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_old_neg_flow_recipient_accesscode(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        actual_access_code = res['assetsDeposited']['accesscode']

        access_code = "invalid"
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(access_code, locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                                  "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(actual_access_code, locker_unit,
                                                                                  locker_bank,
                                                                                  "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_old_neg_flow_recipient_pid(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        actual_access_code = res['assetsDeposited']['accesscode']
        access_code = "invalid"
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(access_code, locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                                  "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(actual_access_code, locker_unit,
                                                                                  locker_bank, "valid", "validResource",
                                                                                  False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # -------------------Case Sensitive Authenticate/Pickup cases---------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    def test_case_sensitive_access_code_v2(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode'].lower()
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(access_code, locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_case_sensitive_access_code_v1(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode'].lower()
        # res, status_code = resource['locker_api'].verify_authenticate_Pickup_api_v1(access_code, locker_bank,
        #                                                                             "valid", "validResource")
        # assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_normal_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                                  "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------Disable delivery for Loose Coupling---------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    def test_disable_delivery_in_reserve(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        samplejson = '{"disableDeliverySupport":"enabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, samplejson,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        samplejson = '{"disableDeliverySupport":"disabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, samplejson,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_disable_delivery_in_reserve_unit(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_unit"))

        samplejson = '{"disableDeliverySupport":"enabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, samplejson,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="", TrkgID=TrkgID,
                                                                                   EmailID="",
                                                                                   recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        samplejson = '{"disableDeliverySupport":"disabled"}'
        res, status_code = resource['configuration'].verify_patch_pro_configuration_status(locker_bank, samplejson,
                                                                                           "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # -------------------Private Flow---------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_reserve_api_for_private_recipient(self, rp_logger, resource):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=trackingID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_api_for_private_recipient(self, rp_logger, resource):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size, accessible="",
                                                                                   refrigeration="",
                                                                                   climate_type="", TrkgID=trackingID,
                                                                                   EmailID="", recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_api_for_private_recipient_using_device_token(self, rp_logger, resource, context):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=trackingID,
                                                                            EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource",
                                                                            kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_reserve_by_unit_api_for_private_recipient_using_device_token(self, rp_logger, resource, context):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size, accessible="",
                                                                                   refrigeration="",
                                                                                   climate_type="", TrkgID=trackingID,
                                                                                   EmailID="", recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource",
                                                                                   kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    #   TO DO Deposit, Authenticate, pickup

    # -------------------Authenticate Pickup v2 -------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_locker_api(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        personal_id = resource['data_reader'].pd_get_data(self.configparameter, test_name, "PID")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        Res_trackID = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(Res_trackID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        context["access_code_auth_v2"] = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_auth_v2_api(context["access_code_auth_v2"], True, locker_bank,
                                                                     "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_auth_v2_api(personal_id, True, locker_bank, "valid",
                                                                     "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_api_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup API with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_auth_v2_api(context["access_code_auth_v2"], True, locker_bank,
                                                                     "valid", "invalidResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_api_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_auth_v2_api(context["access_code_auth_v2"], True, locker_bank,
                                                                     "invalid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_invalid_access_code_is_passed_auth_v2_api(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        code = context["access_code_auth_v2"]
        collect_code = ""
        for singleCode in code:
            res, status_code = resource['locker_api'].verify_auth_v2_api(singleCode, True, locker_bank, "valid",
                                                                         "validResource", context)
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True
            collect_code = collect_code + singleCode
            if len(collect_code) != 6:
                res, status_code = resource['locker_api'].verify_auth_v2_api(singleCode, True, locker_bank, "valid",
                                                                             "validResource", context)
                assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_api_with_invalid_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_auth_v2_api(context["access_code_auth_v2"], True,
                                                                     "invalidBank", "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_api_with_no_locker_bank(self, rp_logger, context, resource):
        """
        This test validates the Authentication of pickup APi with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_auth_v2_api(context["access_code_auth_v2"], True, "", "valid",
                                                                     "validResource", context)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    @pytest.mark.ilp_sp360commercial
    def test_case_sensitive_access_code_in_auth_v2(self, rp_logger, resource, context):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        personal_id = resource['data_reader'].pd_get_data(self.configparameter, test_name, "PID")

        access_code = context["access_code_auth_v2"].lower()
        res, status_code = resource['locker_api'].verify_auth_v2_api(access_code, True, locker_bank, "valid",
                                                                     "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        pid = personal_id.lower()
        res, status_code = resource['locker_api'].erify_auth_v2_api(pid, True, locker_bank, "valid", "validResource",
                                                                    context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers88
    def test_verify_auth_v2_api_with_multiple_parcel_same_recipient_diffrent_lockerunit(self, rp_logger, context,
                                                                                        resource):
        """
        This test validates the Authentication of pickup API with multiple parcels for same recipeint with personalPackageAllAtOnce
        with diffrent units(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        # reservation1
        TrkgID = "firstpackage" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        context["manufacturerLockerID"] = res['manufacturerLockerID']
        context["Res_trackID"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID'] = recipientID
        # reservation2
        TrkgID = "second-package" + str(random.randint(1, 35000))
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource")
        context["manufacturerLockerID1"] = res['manufacturerLockerID']
        context["Res_trackID1"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID1'] = recipientID
        # deposit1
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code"] = res['assetsDeposited']['accesscode']
        # deposit2
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID1'],
                                                                            context['manufacturerLockerID1'],
                                                                            locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code1"] = res['assetsDeposited']['accesscode']

        # authenticate
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        PID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'PID')

        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "validResource")
        record_total = len(res["authUnits"])
        if record_total != 2:
            self.Failures.append(
                "Multiple pickup bases on the allpackageat once setting  = " + str(record_total))
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(PID, locker_bank,
                                                                                 "valid", "validResource")
        record_total = len(res["authUnits"])
        if record_total != 2:
            self.Failures.append(
                "Multiple pickup bases on the allpackageat once setting  = " + str(record_total))
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('authenticationapi_response_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
        # Pickup
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code'],
                                                                           context['manufacturerLockerID'], locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code1'],
                                                                           context['manufacturerLockerID1'],
                                                                           locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # -------------------Kiosk Device Token E2E (Keep at end of file)---------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_Lockerbank_details(self, rp_logger, context, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "valid", "validResource",
                                                                            context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_delivery_flow(self, rp_logger, context, resource):
        """
               This test validates reservation is done or not (positive scenario)
               :return: return test status
               """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        # Reserve locker
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID, token_type="valid",
                                                                            resource_type="validResource",
                                                                            kioskToken=context)
        context["manufacturerLockerID"] = res['manufacturerLockerID']
        context["Res_trackID"] = res['assetsReserved']['assets'][0]['primaryTrackingID']
        context['recipientID'] = recipientID

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Get reserved locker
        res, status_code = resource['locker_api'].verify_get_reserved_locker_based_on_trackingID(context['Res_trackID'],
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource",
                                                                                                 context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # get reserved v2
        res, status_code = resource['locker_api'].verify_get_reserved_V2(locker_bank, context['recipientID'], "valid",
                                                                         "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # deposit
        res, status_code = resource['locker_api'].verify_deposit_locker_api(context['Res_trackID'],
                                                                            context['manufacturerLockerID'],
                                                                            locker_bank, "valid", "validResource",
                                                                            context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["pickup_code"] = res['assetsDeposited']['accesscode']

        # Authenticate
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(context['pickup_code'], locker_bank,
                                                                                 "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # pickup
        res, status_code = resource['locker_api'].verify_pickup_locker_api(context['pickup_code'],
                                                                           context['manufacturerLockerID'], locker_bank,
                                                                           "valid", "validResource", False, context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_delivery_flow_by_unit(self, rp_logger, context, resource):
        """
               This test validates reservation is done or not (positive scenario)
               :return: return test status
               """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_unit")

        # Reserve locker
        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   size=locker_size,
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="", TrkgID=TrkgID,
                                                                                   EmailID="",
                                                                                   recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource",
                                                                                   kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        reserved_unit = res["manufacturerLockerID"]

        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(reserved_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
