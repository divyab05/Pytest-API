""" This module contains all test cases."""

import sys
import pytest

from APIObjects.lockers_services.ilp_service.dedicate_locker import DedicateLocker
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    dedicatedLocker = {'app_config': app_config,
                       'dedicatedLocker': DedicateLocker(app_config, client_token),
                       'data_reader': DataReader(app_config),
                       'get_product_name': get_product_name}
    yield dedicatedLocker


@pytest.mark.usefixtures('initialize')
class TestDedicatedLocker(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Dedicated_Locker_dept"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ----------------------DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_API_response_when_there_is_no_lockerunit_assigned_to_department(self, rp_logger, resource):
        """
       This test validates when no locker is assigned to department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, departmentID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_department(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag, departmentID, "valid", "validResource", Locker_unit)

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dedicate_lockerunit-recipi-resp.schm.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_department_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag, departmentID, "valid", "invalidResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_department_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a department with invalid token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag, departmentID, "invalid", "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_department_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a department with invalid locker Bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker("invalidBank", recipientFlag, departmentID, "valid", "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_department_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a department with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker("", recipientFlag, departmentID, "valid", "validResource", Locker_unit)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------DETAILS OF DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_department(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, departmentID, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('get_recpi_resp_schema.json',
                                                                           'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_department_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, departmentID, "valid",
                                                                                     "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_department_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, departmentID,
                                                                                     "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_department_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of department with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit("invalidBank", departmentID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_department_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of department with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit("", departmentID, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------UPDATE DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_department(self, rp_logger, context, resource):
        """
        This test validates the updation dedicated locker is assigned to a department  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag, departmentID, "valid", "validResource", Locker_unit)

        context["manufacturerLockerID1"] = res['units'][0]['manufacturerLockerID']
        context["manufacturerLockerID2"] = res['units'][1]['manufacturerLockerID']
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('upda_locker_unit_recipeint.res_schm.json',
                                                                           'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_department_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the updation dedicated locker is assigned to a department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag, departmentID, "valid", "invalidResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_department_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the updation dedicated locker is assigned to a department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag, departmentID, "invalid", "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_department_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the updation dedicated locker is assigned to a department with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker("invalidBank", recipientFlag, departmentID, "valid", "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_department_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the updation dedicated locker is assigned to a department with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker("", recipientFlag, departmentID, "valid", "validResource", Locker_unit)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ---------------------REMOVE DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_department(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a department  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, departmentID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('remove_dedocated_locker_unit_res_scham.json',
                                                                           'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_department_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a department with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, departmentID, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_department_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a department with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, departmentID, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_department_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a department with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context,  "invalidBank", departmentID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_department_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a department with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, "", departmentID, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_PUT_API_RESPONSE_WHEN_THERE_IS_NO_DDICATED_LOCKER_ASSIGNED_TO_department(self, rp_logger, context, resource):
        """
        This test validates when there is no locker assigned to department (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'departmentID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, departmentID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True
