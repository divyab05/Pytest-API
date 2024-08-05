import random
import string
import sys
import pytest

from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.report_a_problem import ReportProblem
from APIObjects.lockers_services.ilp_service.day_locker_apis import DayLocker
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation

from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    reportProblem = {'app_config': app_config,
                     'reportProblem': ReportProblem(app_config, client_token),
                     'storage': DayLocker(app_config, client_token),
                     'lockerapi': LockerAPI(app_config, client_token),
                     'cancelreservation': CancelReservation(app_config, client_token),
                     'data_reader': DataReader(app_config),
                     'get_product_name': get_product_name}
    yield reportProblem


@pytest.mark.usefixtures('initialize')
class TestReportProblemApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Report_Problem"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")
        self.Failures = []

    # ------------------------------VALIDATE API LOCKERBANK DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_for_recipient(self, rp_logger, resource):
        """
        this test validates the recipient if present at address book (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API Fail with Email ID: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('validate_for_recipient_res_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_for_operator(self, rp_logger, resource):
        """
        this test validates the operator if present at address book (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('validate_for_operator_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_for_invalid_emailID(self, rp_logger, resource):
        """
        this test validates the email ID if present at address book (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_for_recipient_with_invalid_resource(self, rp_logger, resource):
        """
        this test validates the api for invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid",
                                                                                            "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_for_recipient_with_invalid_access_token(self, rp_logger, resource):
        """
        this test validates the api for invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "invalid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_with_access_code(self, rp_logger, resource):
        """
        This test validates the access code (positive scenario)
        :return: test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        trackingID = test_name + str(random.randint(1, 35000))

        # Reserving a unit
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Deposit
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid",
                                                                           'validResource')
        # if status_code != 200:
        #     resource['failure_case'].cancel_reservation(self, locker_unit=locker_unit, locker_bank=locker_bank)
        #     self.Failures.append("Deposit Failed" + str(status_code))
        #     assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode']
        id = res['assetsDeposited']['accesscode']

        # Validate API-report a problem
        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, id, "valid",
                                                                                            "validResource")
        if status_code != 200:
            self.Failures.append("Validate API Fail with Access Code: Expected:200 , Received  " + str(status_code))

        # Pickup
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_with_pid(self, rp_logger, resource):
        """
        This test validates the access code (positive scenario)
        :return: test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        trackingID = test_name + str(random.randint(1, 35000))

        # Reserving a unit
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Deposit
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']
        id = res['assetsDeposited']['recipient']['personalID']

        # Validate API-report a problem
        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, id,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API Fail with Personal ID: Expected:200 , Received  " + str(status_code))

        # Pickup
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_validation_api_with_invalid_access_code(self, rp_logger, context, resource):
        """
        This test validates the access code which is invalid (negative scenario)
        :return: test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, "pb12",
                                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------ADD COMPLAINTS FOR OCCUPIED LOCKER-----------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_when_package_is_in_locker(self, rp_logger, context, resource):
        """
        This test validates the addition of complaints at locker when the recipient has a parcel
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank'))
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message'))
        recipientID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID'))
        TrackingID = test_name + str(random.randint(1, 35000))

        # Reserving a unit
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrackingID,
                                                                           EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Deposit
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, access_code,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using access code: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit=locker_unit,
                                                                                             accesscode=access_code,
                                                                                             trackingid=TrackingID,
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append(
                "Add Complaint API failure for occupied unit: Expected:200 , Received  " + str(status_code))

        # Pickup
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR PACKAGE MISSING-----------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_package_missing(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank for package missing (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email id: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("Post API Failure for recipient: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res, self.read_json_file('complaint_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR PACKAGE DAMAGED---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_package_damaged(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank for package damaged (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("Post API Failure for recipient: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res, self.read_json_file('complaint_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR LOCKER STUCK---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_locker_stuck(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank of locker stuck category (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("Post API Failure for recipient: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res, self.read_json_file('complaint_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR REOPEN lOCKER---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_reopen_locker(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank of reopen category (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("Post API Failure for recipient: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res, self.read_json_file('complaint_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR OTHER ALERTS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_other_alerts_with_details(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank of others category (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        details = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'details')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details=details,
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("Post API Failure for recipient: Expected:200 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res, self.read_json_file('complaint_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_other_alerts_without_details(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank of others category with no details given (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        details = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'details')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details=details,
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 400:
            self.Failures.append("Post API Failure for details: Expected:400 , Received  " + str(status_code))

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------ADD COMPLAINTS LOCKERBANK FOR INVALID CASES------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_no_message_ID(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank when no messageID is given (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using email ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID='',
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Received  " + str(status_code))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_no_EMAIL_ID(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank when no emailID is given (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail="",
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_invalid_resource(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=emailID,
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="invalidResource",
                                                                                             token_type="valid")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_complaints_at_lockerBank_for_invalid_access_token(self, rp_logger, resource):
        """
        this test validates the adding of complaints at locker bank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=emailID,
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="invalid")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    # ------------------------------GET COMPLAINTS LOCKERBANK DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_complaints_at_lockerBank(self, rp_logger, resource):
        """
        this test validates the complaints at lockerbank (positive scenario)
        :return: return test status
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_get_complaints_at_lockerBank(locker_bank, "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_complaints_at_lockerBank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the complaints at lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_get_complaints_at_lockerBank(locker_bank, "valid",
                                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_complaints_at_lockerBank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the get complaints at lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_get_complaints_at_lockerBank(locker_bank, "invalid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('error_res_schema.json', 'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    # ------------------------------EXPORT COMPLAINTS LOCKERBANK ---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_export_complaints_at_lockerBank(self, rp_logger, resource):
        """
        This test validates the export complaints at lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_export_complaints_at_lockerBank(locker_bank, "valid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_export_complaints_at_lockerBank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the export complaints at lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_export_complaints_at_lockerBank(locker_bank, "valid",
                                                                                            "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_export_complaints_at_lockerBank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the export complaints at lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reportProblem'].verify_export_complaints_at_lockerBank(locker_bank, "invalid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------Report A Problem For VISITOR--------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_validate_with_existing_visitor_email(self, rp_logger, resource):
        """
        This test validates the access code (positive scenario)
        :return: test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        # Validate API-report a problem
        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 404:
            self.Failures.append(
                "Validate API Fail with Existing Visitor Having no reservation Email: Expected:404 , Received  " + str(
                    status_code))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_validate_with_new_visitor_email(self, rp_logger, resource):
        """
        This test validates the access code (positive scenario)
        :return: test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        visitor_email = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Reserving a unit
        receiver = res['visitorID']
        personalID = res["personalID"]
        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="extra small",
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=personalID,
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, visitor_email,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API Fail with Email ID: Expected:200 , Received  " + str(status_code))

        # Deposit
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Validate API-report a problem
        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, personalID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append(
                "Validate API Fail with Visitor Personal ID: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, visitor_email,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API Fail with Email ID: Expected:200 , Received  " + str(status_code))

        # Pickup
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(personalID, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_verify_add_complaint_for_operator(self, rp_logger, context, resource):
        """
        This test validates the addition of complaints at locker when the recipient has a parcel
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank'))
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message'))
        emailID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID'))

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using operator email ID: Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details='',
                                                                                             recipientEmail="",
                                                                                             operatorEmail=res[
                                                                                                 'operator'],
                                                                                             visitorEmail="",
                                                                                             lockerunit='',
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("POST API failure using operator email ID: Received  " + str(status_code))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # @pytest.mark.ilp_sp360commercial
    # @pytest.mark.ilp_fedramp
    # @pytest.mark.regressioncheck_lockers
    # def test_verify_add_complaint_for_existing_visitor(self, rp_logger, context, resource):
    #     """
    #     This test validates the addition of complaints at locker when the recipient has a parcel
    #     :return: return test status
    #     """
    #     test_name = sys._getframe().f_code.co_name
    #     rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
    #
    #     locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
    #     messageID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID')
    #     message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
    #     emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
    #
    #     res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID, "valid", "validResource")
    #     if status_code != 200:
    #         self.Failures.append("Validate API failure using visitor email ID: Received  " + str(status_code))
    #
    #     res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank, messageID=messageID,
    #                                                                                          message=message, details='',  recipientEmail="",
    #                                                                                          operatorEmail="", visitorEmail=res['visitor'], lockerunit='',
    #                                                                                          accesscode='', trackingid='', resource_type="validResource",
    #                                                                                          token_type="valid")
    #     if status_code != 200:
    #         self.Failures.append("POST API failure using visitor email ID: Received  " + str(status_code))
    #
    #     exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_add_complaint_for_new_visitor(self, rp_logger, context, resource):
        """
        This test validates the addition of complaints at locker when the recipient has a parcel
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        visitor_email = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        personalID = res["personalID"]
        receiver = res['visitorID']

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="extra small",
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID=personalID,
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, visitor_email,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using visitor email ID: Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details='',
                                                                                             recipientEmail="",
                                                                                             operatorEmail="",
                                                                                             visitorEmail=res[
                                                                                                 'visitor'],
                                                                                             lockerunit=locker_unit,
                                                                                             accesscode='',
                                                                                             trackingid='',
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("POST API failure using visitor email ID: Received  " + str(status_code))

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        if status_code != 200:
            self.Failures.append("Cancel API failure,  Received  " + str(status_code))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_add_complaint_for_visitor_occupied_unit(self, rp_logger, context, resource):
        """
        This test validates the addition of complaints at locker when the recipient has a parcel
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message')
        visitor_email = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))
        trackingID = test_name + str(random.randint(1, 35000))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor_email, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        personalID = res["personalID"]
        receiver = res['visitorID']

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size="extra small",
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

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, personalID,
                                                                                            "valid", "validResource")
        if status_code != 200:
            self.Failures.append("Validate API failure using visitor personal ID: Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details='',
                                                                                             recipientEmail="",
                                                                                             operatorEmail="",
                                                                                             visitorEmail=res[
                                                                                                 'visitor'],
                                                                                             lockerunit=locker_unit,
                                                                                             accesscode=personalID,
                                                                                             trackingid=trackingID,
                                                                                             resource_type="validResource",
                                                                                             token_type="valid")
        if status_code != 200:
            self.Failures.append("POST API failure using visitor email ID: Received  " + str(status_code))

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(personalID, locker_unit, locker_bank, "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------------------------Private Contact email and PID--------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_validate_api_for_private_recipient_using_email(self, rp_logger, resource, context):
        """
        this test validates the recipient if present at address book (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, emailID,
                                                                                            "valid", "validResource",
                                                                                            context)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # add cases for pid and access code post deposit

    # ------------------ Kiosk Token (Keep at the end of file)-----------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_post_complaints_at_lockerBank_when_package_is_in_locker(self, rp_logger, context, resource):
        """
        This test validates the addition of complaints at locker when the recipient has a parcel
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank'))
        messageID = int(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'messageID'))
        message = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'message'))
        recipientID = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID'))
        TrackingID = test_name + str(random.randint(1, 35000))

        # Reserving a unit
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrackingID,
                                                                           EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource",
                                                                           kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Deposit
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['reportProblem'].verify_validate_api_for_report_problem(locker_bank, access_code,
                                                                                            "valid", "validResource",
                                                                                            context)
        if status_code != 200:
            self.Failures.append("Validate API failure using access code: Expected:200 , Received  " + str(status_code))

        res, status_code = resource['reportProblem'].verify_post_add_complaint_at_lockerbank(locker_bank=locker_bank,
                                                                                             messageID=messageID,
                                                                                             message=message,
                                                                                             details="",
                                                                                             recipientEmail=res[
                                                                                                 'recipient'],
                                                                                             operatorEmail="",
                                                                                             visitorEmail="",
                                                                                             lockerunit=locker_unit,
                                                                                             accesscode=access_code,
                                                                                             trackingid=TrackingID,
                                                                                             resource_type="validResource",
                                                                                             token_type="valid",
                                                                                             kioskToken=context)
        if status_code != 200:
            self.Failures.append(
                "Add Complaint API failure for occupied unit: Expected:200 , Received  " + str(status_code))

        # Pickup
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False, context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))
