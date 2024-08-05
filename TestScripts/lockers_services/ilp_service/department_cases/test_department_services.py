""" This module contains all test cases."""

import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.update_flow import UpdateFlow
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    dept_api = {'app_config': app_config,
                'dept_api': DepartmentLockerAPI(app_config, client_token),
                'locker_api': LockerAPI(app_config, client_token),
                'cancel_reservation': CancelReservation(app_config, client_token),
                'update_reservation': UpdateFlow(app_config, client_token),
                'data_reader': DataReader(app_config),
                'get_product_name': get_product_name}
    yield dept_api


@pytest.mark.usefixtures('initialize')
class TestDepartmentApis(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Department_Flow"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ------------------------------RESERVE LOCKER FOR DEPARTMENT---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_details(self, rp_logger, context, resource):
        """
        This test validates reservation for department is success or not  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["manufacturerLockerID_dept1"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        result = self.validate_json_schema_validations(res, self.read_json_file('reserve_dept_api_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_details_when_no_size_provided(self, rp_logger, context, resource):
        """
        This test validates reservation for department with no size provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, "", TrkgID, departmentMail,
                                                                               departmentID,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_details_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates reservation for department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID,
                                                                               "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_details_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates reservation for department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID,
                                                                               "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserv_locker_department_api_with_no_trackingID(self, rp_logger, context, resource):
        """
        This test validates reservation for department when no trackingID is provided (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, "",
                                                                               departmentMail, departmentID,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_with_invalid_lockerbank(self, rp_logger, resource):
        """
        This test validates locker bank details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api("invalidBank", locker_size, TrkgID,
                                                                               departmentMail,
                                                                               departmentID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_reserve_locker_department_api_with_no_lockerbank(self, rp_logger, resource):
        """
        This test validates locker bank details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api("", locker_size, TrkgID, departmentMail,
                                                                               departmentID, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------DEPOSIT IN LOCKER FOR DEPARTMENT---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api(self, rp_logger, context, resource):
        """
        This test validates the deposit API for department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dept_deposit_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the deposit API for department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the deposit API for department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "invalid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api_response_with_same_lockerUnit_usefor_deposit_which_is_already_deposited(
            self, rp_logger, context, resource):
        """
        This test validates the deposit API for department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the deposit API for department with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, "invalidBank", "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_deposit_locker_department_api_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the deposit API for department with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, "", "valid",
                                                                                     "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------PICKUP FOR DEPARTMENT---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_with_invalid_departmentID(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department with invalid department ID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dept_pickup_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "invalidResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department with invalid resource(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "invalid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_response_with_invalid_PID(self, rp_logger, context, resource):
        """
        TThis test validates the pickup APi for department with invalid PID(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    "123456", "valid", "validResource",
                                                                                    False)
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_response_with_invalid_ManufacturerID(self, rp_logger, context,
                                                                                      resource):
        """
        This test validates the pickup APi for department with invalid manufacturerID(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')
        context['manufacturerLockerID_dept'] = resource['data_reader'].pd_get_data(self.configparameter, test_name,
                                                                                   'InvalidManufacturerID')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department with invalid bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, "invalidBank",
                                                                                    departmentMail,
                                                                                    departmentID, departmentpickcode,
                                                                                    "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Pickup_locker_department_api_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the pickup APi for department with no bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, "", departmentMail,
                                                                                    departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------PERSONAL ID ASSOCIATED WITH DEPARTMENT DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_personalID_list_associated_with_department(self, rp_logger, resource):
        """
        This test validates the list of personalID associated with department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID'))
        siteID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID'))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('get_pid_for_dept_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_personalID_list_associated_with_department_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the list of personalID associated with department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID'))
        siteID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID'))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_personalID_list_associated_with_department_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the list of personalID associated with department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID'))
        siteID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID'))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_personalID_list_associated_with_department_with_invalid_siteID(self, rp_logger, context, resource):
        """
        This test validates the list of personalID associated with department with invalid siteID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID'))
        siteID = str(random.randint(1, 1000))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_personalID_list_associated_with_department_with_invalid_tenantID(self, rp_logger, context,
                                                                                     resource):
        """
        This test validates the list of personalID associated with department with invalid tenantID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(random.randint(1, 1000))
        siteID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID'))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # -----------------------------Get All DEPARTMENT AT Site DETAILS---------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_all_department_at_site_api_response(self, rp_logger, resource):
        """
        This test validates the list of available department at site
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, SiteID, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_all_department_at_site_api_response_with_invalid_resource(self, rp_logger, resource):
        """
        This test error response of get all department API When invalid resource is being passed
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, SiteID, "valid",
                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_all_department_at_site_api_response_with_invalid_tanentID(self, rp_logger, resource):
        """
        This test validates the error response of get all department at site with invalid tenant ID
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("####### TEST EXECUTION STARTED :: " + test_name + " ######")

        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site("InvalidTenantID", SiteID, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_all_department_at_site_api_response_with_invalid_access_Token(self, rp_logger, resource):
        """
        This test validates the error response of get all department at site with invalid tanant ID
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, SiteID, "invalid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_all_department_at_site_api_response_with_invalid_siteID(self, rp_logger, resource):
        """
        This test validates the error response of get all department at site with invalid site ID
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, "invalidsiteID", "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------Update department pid for single recipient---------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_department_PersonalID_for_single_recipient_for_walmart(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        PID = "updtPID" + str(random.randint(1, 35000))
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_Update_Department_PersonalID(PID, tenantID, SiteID, departmentID,
                                                                                    "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('update_personalID_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_department_PersonalID_for_single_recipient_for_walmart_with_no_PID(self, rp_logger,
                                                                                              resource):
        """
        This test validates the update information of personal ID associated with department in case of No PID is passed
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_Update_Department_PersonalID("", tenantID, SiteID, departmentID,
                                                                                    "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_department_PersonalID_for_single_recipient_for_walmart_invalid_access_Token(self, rp_logger,
                                                                                                       resource):
        """
        This test validates the update information of personal ID associated with department in case of invalid access token
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        PID = "updtPID" + str(random.randint(1, 35000))
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_Update_Department_PersonalID(PID, tenantID, SiteID, departmentID,
                                                                                    "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_department_PersonalID_for_single_recipient_for_walmart_invalid_resource_path(self, rp_logger,
                                                                                                        resource):
        """
        This test validates the update information of personal ID associated with department in case of invalid resource path
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        PID = "updtPID" + str(random.randint(1, 35000))
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_Update_Department_PersonalID(PID, tenantID, SiteID, departmentID,
                                                                                    "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_department_PersonalID_for_single_recipient_for_walmart_with_invalid_department(self,
                                                                                                          rp_logger,
                                                                                                          resource):
        """
        This test validates the update information of personal ID associated with department in case of invalid department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        PID = "updtPID" + str(random.randint(1, 35000))
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_Update_Department_PersonalID(PID, tenantID, SiteID, "invalidDept",
                                                                                    "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_keyContact_only_authorized_for_pickups(self, rp_logger, resource, context):
        """
        This test validates keycontact pickup scenario (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "size")
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentMail")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        keycontact_pid = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentpickcode"))
        normalcontact_pid = str(
            resource['data_reader'].pd_get_data(self.configparameter, test_name, "InvalidPID"))

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Invalid case (non key contact pickups)
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(normalcontact_pid, locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    normalcontact_pid, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        # valid case (key contact pickups)
        res, status_code = resource['locker_api'].verify_authenticate_Pickup_api(keycontact_pid, locker_bank,
                                                                                 "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    keycontact_pid, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_recipient_reference(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "RecipientReference" + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')

        res, status_code = resource['dept_api'].verify_recipient_reference(tenantID, recipientID, "valid",
                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('recipient_ref_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        beforeReserve = res['recipients'][0]['status']
        assert not beforeReserve != False

        # Reservation
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID, EmailID="",
                                                                            recipientID=recipientID,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['dept_api'].verify_recipient_reference(tenantID, recipientID, "valid",
                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        afterReserve = res['recipients'][0]['status']
        assert not afterReserve != True

        # Cancel Reservation
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['dept_api'].verify_recipient_reference(tenantID, recipientID, "valid",
                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        afterCancel = res['recipients'][0]['status']
        assert not afterCancel != False

    @pytest.mark.regressioncheck_lockers
    def test_verify_recipient_reference_with_invalid_token(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_recipient_reference(tenantID, recipientID, "invalid",
                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_recipient_reference_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_recipient_reference(tenantID, recipientID, "valid",
                                                                           "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_department_reference(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')

        res, status_code = resource['dept_api'].verify_department_reference(tenantID, departmentID, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('department_ref_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
        beforeReserve = res['departments'][0]['status']
        assert not beforeReserve != False

        # Reservation
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               'true', departmentID, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['dept_api'].verify_department_reference(tenantID, departmentID, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        afterReserve = res['departments'][0]['status']
        assert not afterReserve != True

        # Cancel Reservation
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['dept_api'].verify_department_reference(tenantID, departmentID, "valid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        afterCancel = res['departments'][0]['status']
        assert not afterCancel != False

    @pytest.mark.regressioncheck_lockers
    def test_verify_department_reference_with_invalid_token(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_department_reference(tenantID, departmentID, "invalid",
                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_department_reference_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_department_reference(tenantID, departmentID, "valid",
                                                                            "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_location_reference(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locationID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_location_reference(tenantID, locationID, "valid",
                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('location_ref_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
        lockerOnboard = res['locations'][0]['status']
        assert not lockerOnboard != True

    @pytest.mark.regressioncheck_lockers
    def test_verify_location_reference_with_invalid_token(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locationID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_location_reference(tenantID, locationID, "invalid",
                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_location_reference_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the update pID information related to department
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locationID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_location_reference(tenantID, locationID, "valid",
                                                                          "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # Department update reservation usecase
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_reservation_unit_for_department(self, rp_logger, context, resource):
        """
        This test validates reservation for department is success or not  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'size')
        departmentMail = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentMail')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        departmentpickcode = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentpickcode')

        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, trackingID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["manufacturerLockerID_dept1"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['update_reservation'].verify_update_reservation_based_on_unit(locker_bank,
                                                                                                  context['manufacturerLockerID_dept'],
                                                                                                  trackingID, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    #-------------------------------Departments at site testcases-----------------------------------------
    # create testdata for QA and fedramp
    @pytest.mark.regressioncheck_lockers
    def test_department_response(self, rp_logger, resource):
        """
        This test validates the list of available department at site
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, SiteID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        department_response = res['departments']
        for name in department_response:
            if name['departmentName'] == "No Contact":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 0
            elif name['departmentName'] == "Key Contact with no email":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == True and len(name["recipients"]) == 1
            elif name['departmentName'] == "No pid":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 1
            elif name['departmentName'] == "Key Contact with private only":
                assert name['hasPrivateRecipient'] == True and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 0
            elif name['departmentName'] == "Key Contact with Private and shared":
                assert name['hasPrivateRecipient'] == True and name['hasRecipientWithEmailAndPID'] == True and len(name["recipients"]) == 1
            elif name['departmentName'] == "no email":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == True and len(name["recipients"]) == 1
            # elif name['departmentName'] == "hasEmailAndPID":
            #     assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == True and len(name["recipients"]) == 2
            elif name['departmentName'] == "Key Contact with no pid":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 1
            elif name['departmentName'] == "private + shared":
                assert name['hasPrivateRecipient'] == True and name['hasRecipientWithEmailAndPID'] == True and len(name["recipients"]) == 1
            elif name['departmentName'] == "no email and PID":
                assert name['hasPrivateRecipient'] == False and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 1
            elif name['departmentName'] == "private only dept":
                assert name['hasPrivateRecipient'] == True and name['hasRecipientWithEmailAndPID'] == False and len(name["recipients"]) == 0

    # ----------------------- Kiosk Token (Keep at the end of the file) -----------------------------
    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_verify_personalID_list_associated_with_department(self, rp_logger, resource, context):
        """
        This test validates the list of personalID associated with department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        tenantID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID'))
        siteID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID'))

        res, status_code = resource['dept_api'].verify_get_PersonalID_for_department(tenantID, siteID, departmentID,
                                                                                     "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_get_all_department_at_site_api_response(self, rp_logger, resource, context):
        """
        This test validates the list of available department at site
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        SiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'SiteID')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')

        res, status_code = resource['dept_api'].verify_get_All_Department_at_site(tenantID, SiteID, "valid",
                                                                                  "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
