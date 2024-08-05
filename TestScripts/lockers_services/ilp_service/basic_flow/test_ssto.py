""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token):
    ssto = {'app_config': app_config,
            'locker_api': LockerAPI(app_config, client_token),
            'dept_api': DepartmentLockerAPI(app_config, client_token),
            'cancel_reservation': CancelReservation(app_config, client_token),
            'data_reader': DataReader(app_config)}
    yield ssto


@pytest.mark.usefixtures('initialize')
class TestSSTO(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """

        self.configparameter = "LOCKERS_SSTO_Cases"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ------------------------------SSTO Reservations------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_ssto_reserve_deposit_pickup_flow(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "SSTO" + str(random.randint(1, 35000))
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

        res, status_code = resource['locker_api'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_ssto_reserve_deposit_pickup_flow_by_unit(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "SSTO" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit, size="",
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="", TrkgID=TrkgID,
                                                                                   EmailID="",
                                                                                   recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_ssto_reserve_deposit_pickup_flow_for_dept(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "SSTO" + test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentMail")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentpickcode"))

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_ssto_reserve_deposit_pickup_flow_for_dept_using_unit(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "SSTO" + test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentMail")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentpickcode"))

        res, status_code = resource['dept_api'].verify_reservation_based_on_unit_for_dept(locker_bank, locker_unit, "",
                                                                                          TrkgID,
                                                                                          departmentMail, departmentID,
                                                                                          "valid",
                                                                                          "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # -------------------Fireball Reservations----------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_fireball_reserve_deposit_pickup_flow(self, rp_logger, resource):
        """
        This test validates happy flow of fireball for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "Fireball" + test_name + str(random.randint(1, 35000))
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

        res, status_code = resource['locker_api'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_fireball_reserve_deposit_pickup_flow_by_unit(self, rp_logger, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "Fireball" + test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['locker_api'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit, size="",
                                                                                   accessible="", refrigeration="",
                                                                                   climate_type="", TrkgID=TrkgID,
                                                                                   EmailID="",
                                                                                   recipientID=recipientID,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['locker_api'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_fireball_reserve_deposit_pickup_flow_for_dept(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "Fireball" + test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentMail")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentpickcode"))

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_fireball_reserve_deposit_pickup_flow_for_dept_using_unit(self, rp_logger, context, resource):
        """
        This test validates happy flow of ssto for reservation deposit and pickup (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "Fireball" + test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentMail")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentpickcode"))

        res, status_code = resource['dept_api'].verify_reservation_based_on_unit_for_dept(locker_bank, locker_unit, "",
                                                                                          TrkgID,
                                                                                          departmentMail, departmentID,
                                                                                          "valid",
                                                                                          "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
