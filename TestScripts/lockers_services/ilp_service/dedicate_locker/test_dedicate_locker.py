""" This module contains all test cases."""

import sys
import pytest

from APIObjects.lockers_services.ilp_service.dedicate_locker import DedicateLocker
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils


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
    def initialize(self, request, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Dedicated_Locker"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ----------------------DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_enable_dedicated_status_in_bank(self, rp_logger, resource):
        """
        This test validates the enabling of dedicated locker in the bank (positive scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, status,
                                                                                             "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_recipient(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag,
                                                                                   recipientID, "valid",
                                                                                   "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('dedicate_lockerunit-recipi-resp.schm.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a recipient with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag,
                                                                                   recipientID, "valid",
                                                                                   "invalidResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a recipient with invalid token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag,
                                                                                   recipientID, "invalid",
                                                                                   "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a recipient with invalid locker Bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker("invalidBank", recipientFlag,
                                                                                   recipientID, "valid",
                                                                                   "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_locker_unit_assigned_to_a_recipient_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates dedicated locker is assigned to a recipient with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker("", recipientFlag, recipientID,
                                                                                   "valid", "validResource",
                                                                                   Locker_unit)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------DETAILS OF DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_recipient(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, recipientID,
                                                                                        "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('get_recpi_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_recipient_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of recipient with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, recipientID,
                                                                                        "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_recipient_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of recipient with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit(locker_bank, recipientID,
                                                                                        "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_recipient_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of recipient with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit("invalidBank", recipientID,
                                                                                        "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_locker_with_recipient_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the details for dedicated locker of recipient with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_unit("", recipientID, "valid",
                                                                                        "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------UPDATE DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_recipient(self, rp_logger, context, resource):
        """
        This test validates the updation dedicated locker is assigned to a recipient  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag,
                                                                                     recipientID, "valid",
                                                                                     "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        context["manufacturerLockerID1"] = res['units'][0]['manufacturerLockerID']
        context["manufacturerLockerID2"] = res['units'][1]['manufacturerLockerID']

        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('upda_locker_unit_recipeint.res_schm.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_resource(self, rp_logger,
                                                                                                resource):
        """
        This test validates the updation dedicated locker is assigned to a recipient with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag,
                                                                                     recipientID, "valid",
                                                                                     "invalidResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_access_token(self, rp_logger,
                                                                                                    resource):
        """
        This test validates the updation dedicated locker is assigned to a recipient with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker(locker_bank, recipientFlag,
                                                                                     recipientID, "invalid",
                                                                                     "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_lockerBank(self, rp_logger,
                                                                                                  resource):
        """
        This test validates the updation dedicated locker is assigned to a recipient with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker("invalidBank", recipientFlag,
                                                                                     recipientID, "valid",
                                                                                     "validResource", Locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_updated_dedicated_locker_unit_assigned_to_a_recipient_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the updation dedicated locker is assigned to a recipient with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        Locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicate_locker("", recipientFlag, recipientID,
                                                                                     "valid", "validResource",
                                                                                     Locker_unit)
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------REMOVE DEDICATED LOCKER UNIT ASSIGNED TO RECIPIENT--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_recipient(self, rp_logger, context, resource):
        """
        This test validates removal of dedicated locker is assigned to a recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file(
            'remove_dedocated_locker_unit_res_scham.json', 'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_resource(self, rp_logger, context,
                                                                                               resource):
        """
        This test validates removal of dedicated locker is assigned to a recipient with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                                     "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_access_token(self, rp_logger,
                                                                                                   context, resource):
        """
        This test validates removal of dedicated locker is assigned to a recipient with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                                     "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_recipient_with_invalid_lockerBank(self, rp_logger,
                                                                                                 context, resource):
        """
        This test validates removal of dedicated locker is assigned to a recipient with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, "invalidBank",
                                                                                     recipientID, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_remove_dedicated_locker_unit_assigned_to_a_recipient_with_no_lockerBank(self, rp_logger, context,
                                                                                            resource):
        """
        This test validates removal of dedicated locker is assigned to a recipient with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, "", recipientID, "valid",
                                                                                     "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_PUT_API_RESPONSE_WHEN_THERE_IS_NO_DDICATED_LOCKER_ASSIGNED_TO_RECIPIENT(self, rp_logger, context,
                                                                                            resource):
        """
        This test validates when there is no locker assigned to recipient (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        res, status_code = resource['dedicatedLocker'].verify_remove_dedicate_locker(context, locker_bank, recipientID,
                                                                                     "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # --------------------------------------UPDATE DEDICATED STATUS----------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_disable_dedicated_status_in_bank(self, rp_logger, resource):
        """
        This test validates the enabling of dedicated locker in the bank (positive scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, status,
                                                                                             "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, True, "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_disable_dedicated_locker_then_add_dedicated_unit(self, rp_logger, resource):
        """
        This test validates the adding of dedicated locker when status is false (negative scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')
        recipientFlag = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientFlag')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        locker_unit = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Locker_unit')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, status,
                                                                                             "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)

        res, status_code = resource['dedicatedLocker'].verify_add_dedicated_locker(locker_bank, recipientFlag,
                                                                                   recipientID, "valid",
                                                                                   "validResource", locker_unit)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res)

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, True, "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)

    #     remove dedicated

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the dedicated locker status with invalid resource (negative scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, status,
                                                                                             "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the dedicated locker status with invalid access token (negative scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status(locker_bank, status,
                                                                                             "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_status_with_invalid_lockerbank(self, rp_logger, resource):
        """
        This test validates the dedicated locker status with invalid lockerbank (negative scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status("invalidBank", status,
                                                                                             "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_dedicated_status_with_no_lockerbank(self, rp_logger, resource):
        """
        This test validates the dedicated locker status with no lockerbank (negative scenario)
        :return: returns the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')

        res, status_code = resource['dedicatedLocker'].verify_update_dedicated_locker_status("", status, "valid",
                                                                                             "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # --------------------------------------GET DEDICATED STATUS----------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_status(self, rp_logger, resource):
        """
        This test validates the dedicated status (positive scenario)
        :returns: return the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_status(locker_bank, "valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res)
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the dedicated status with invalid resource (negative scenario)
        :returns: return the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_status(locker_bank, "valid",
                                                                                          "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the dedicated status with invalid access token (negative scenario)
        :returns: return the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_status(locker_bank, "invalid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_status_with_invalid_bank(self, rp_logger, resource):
        """
        This test validates the dedicated status with invalid bank(negative scenario)
        :returns: return the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_status("invalidBank", "valid",
                                                                                          "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_dedicated_status_with_no_lockerbank(self, rp_logger, resource):
        """
        This test validates the dedicated status with no lockerbank (negative scenario)
        :returns: return the test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['dedicatedLocker'].verify_get_dedicated_locker_status("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True
