import random
import secrets
import sys
import pytest

from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    configapi = {'app_config': app_config,
                 'configapi': ConfigurationAPI(app_config, client_token),
                 'lockerapi': LockerAPI(app_config, client_token),
                 'data_reader': DataReader(app_config),
                 'get_product_name': get_product_name}
    yield configapi


@pytest.mark.usefixtures('initialize')
class TestConfigurationApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Configuration"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ------------------------------SET HEARTBEAT FOR LOCKERBANK---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_set_heartbeat_for_locker_bank(self, rp_logger, resource):
        """
        This test validates the setup a heartbeat time stamp bases on lockerunit (positive scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank(locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('set_heartbeat_resp_schem.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_set_heartbeat_for_locker_bank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the setup a heartbeat time stamp bases on lockerunit with invalid resource (negative scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank(locker_bank, "invalid",
                                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_set_heartbeat_for_locker_bank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the setup a heartbeat time stamp bases on lockerunit with invalid access token (negative scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank(locker_bank, "invalid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_set_heartbeat_for_locker_bank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the setup a heartbeat time stamp bases on locker unit with invalid locker bank (negative scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank("invalidBank", "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_set_heartbeat_for_locker_bank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the setup a heartbeat time stamp bases on locker unit with no locker bank (negative scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank("", "valid",
                                                                                                 "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(405, status_code, res) is True

    # ------------------------------LOCKERBANK HEARTBEAT DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_heartbeat_details(self, rp_logger, resource):
        """
        This test validates locker bank heartbeat details (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_lockerbank_heartbeat(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('string_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_heartbeat_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank heartbeat details with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_lockerbank_heartbeat(locker_bank, "valid",
                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_heartbeat_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validate locker bank heartbeat details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_lockerbank_heartbeat(locker_bank, "invalid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_heartbeat_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank heartbeat details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_lockerbank_heartbeat("invalidBank", "valid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_heartbeat_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank heartbeat details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_lockerbank_heartbeat("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------POST DROPOFF PROPERTIES---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Dropoff_properties(self, rp_logger, resource):
        """
        This test validates the setup of dropoff properties post APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_dropoff_property(locker_bank, "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dropoff_prop_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Dropoff_properties_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the set of dropoff properties post APi with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_dropoff_property(locker_bank, "valid",
                                                                                             "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Dropoff_properties_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the setup of dropoff properties post APi with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_dropoff_property(locker_bank, "invalid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Dropoff_properties_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the setup of dropoff properties post APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_post_api_to_set_the_dropoff_property("invalidBank", "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Dropoff_properties_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the setup of dropoff properties post APi with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_post_api_to_set_the_dropoff_property("", "valid",
                                                                                             "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------LOCKERBANK DROPOFF DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_droppff_properties(self, rp_logger, resource):
        """
        This test validates locker bank dropoff details (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_dropoff_properties(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dropoff_prop_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_dropoff_properties_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank dropoff properties with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_dropoff_properties(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_dropoff_properties_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank dropoff details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_dropoff_properties(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_dropoff_properties_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank dropoff details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_dropoff_properties("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_dropoff_properties_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank dropoff details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_dropoff_properties("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------POST PICKUP PROPERTIES---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Pickup_properties(self, rp_logger, resource):
        """
        This test validates the setup of pickup properties post APi (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_pickup_property(locker_bank, "valid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('pickup_prop_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Pickup_properties_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the setup of pickup properties post APi with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_pickup_property(locker_bank, "valid",
                                                                                            "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Pickup_properties_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the setup of pickup properties post APi with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_post_api_to_set_the_pickup_property(locker_bank, "invalid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Pickup_properties_with_invalid_locker_bank(self, rp_logger, resource):
        """
        This test validates the setup of pickup properties post APi with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_post_api_to_set_the_pickup_property("invalidBank", "valid",
                                                                                            "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_API_to_test_Pickup_properties_with_no_locker_bank(self, rp_logger, resource):
        """
        This test validates the setup of pickup properties post APi with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_post_api_to_set_the_pickup_property("", "valid",
                                                                                            "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------LOCKERBANK PICKUP DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_pickup_properties(self, rp_logger, resource):
        """
        This test validates locker bank pickup properties (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pickup_properties(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('pickup_prop_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_pickup_properties_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank pickup properties with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pickup_properties(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_pickup_properties_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank pickup properties with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pickup_properties(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_pickup_properties_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank pickup properties with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_pickup_properties("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbanks_pickup_properties_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates locker bank pickup properties with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_pickup_properties("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Patch PROCONFIGURATION LOCKERBANK DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_post_proconfiguration_at_lockerbank(self, rp_logger, resource):
        """
          This test validates the proconfiguration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"badgeSupport": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('pro_config_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_proconfiguration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
          This test validates the proconfiguration status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"badgeSupport": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_proconfiguration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
          This test validates the proconfiguration status of lockerbank with invalid access_token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"badgeSupport": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "invalid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_proconfiguration_at_lockerbank_with_invalid_lockerbank(self, rp_logger, resource):
        """
          This test validates the proconfiguration status of lockerbank with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"badgeSupport": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pro_configuration_status("invalidBank", json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_proconfiguration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
          This test validates the proconfiguration status of lockerbank with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"badgeSupport": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pro_configuration_status("", json, "valid",
                                                                                       "invalidResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Get PROCONFIGURATION LOCKERBANK DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_proconfiguration_at_lockerbank(self, rp_logger, resource):
        """
        This test validates the proconfiguration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pro_configuration_status(locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('pro_config_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_proconfiguration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the proconfiguration status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pro_configuration_status(locker_bank, "valid",
                                                                                     "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_proconfiguration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the proconfiguration status of lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pro_configuration_status(locker_bank, "invalid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_proconfiguration_at_lockerbank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the proconfiguration status of lockerbank with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_pro_configuration_status("invalidBank", "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_proconfiguration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the proconfiguration status of lockerbank with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_pro_configuration_status("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------Update EMAIL CONFIGURATION STATUS---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_disable_email_configuration_status(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status(locker_bank, emailEnabled,
                                                                                          "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_enable_email_configuration_status(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status(locker_bank, emailEnabled,
                                                                                          "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('email_config_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_email_configuration_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status(locker_bank, emailEnabled,
                                                                                          "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_email_configuration_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status(locker_bank, emailEnabled,
                                                                                          "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_email_configuration_status_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status("invalidBank", emailEnabled,
                                                                                          "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_email_configuration_status_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with no lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        emailEnabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'emailEnabled')

        res, status_code = resource['configapi'].verify_update_email_configuration_status("", emailEnabled, "valid",
                                                                                          "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Get EMAIL CONFIGURATION STATUS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_email_configuration_status(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_email_configuration_status(locker_bank, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('email_config_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_email_configuration_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_email_configuration_status(locker_bank, "valid",
                                                                                       "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_email_configuration_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_email_configuration_status(locker_bank, "invalid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_email_configuration_status_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with invalid lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_email_configuration_status("invalidBank", "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_email_configuration_status_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the email configuration status of lockerbank with no lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_email_configuration_status("", "invalid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Update EVENT Q CONFIGURATION STATUS-------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_enable_eventQ_configuration_at_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status(locker_bank, eventQstatus,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_disable_eventQ_configuration_at_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status(locker_bank, eventQstatus,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_eventQ_configuration_at_lockerBank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status(locker_bank, eventQstatus,
                                                                                           "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_eventQ_configuration_at_lockerBank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status(locker_bank, eventQstatus,
                                                                                           "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_eventQ_configuration_at_lockerBank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status("invalidBank", eventQstatus,
                                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_eventQ_configuration_at_lockerBank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        eventQstatus = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'eventQstatus')

        res, status_code = resource['configapi'].verify_update_eventQ_configuration_status("", eventQstatus, "valid",
                                                                                           "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Get EVENT Q CONFIGURATION STATUS-------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_eventQ_configuration_at_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_eventQ_configuration_status(locker_bank, "valid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('status_boolean_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_eventQ_configuration_at_lockerBank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_eventQ_configuration_status(locker_bank, "valid",
                                                                                        "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_eventQ_configuration_at_lockerBank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_eventQ_configuration_status(locker_bank, "invalid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_eventQ_configuration_at_lockerBank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_eventQ_configuration_status("invalidBank", "valid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_eventQ_configuration_at_lockerBank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates eventQ configuration at locker bank level (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_get_eventQ_configuration_status("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------Update PICKAGE EXPIRE DURATION DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_pickage_expireduration_at_lockerbank(self, rp_logger, resource):
        """
        This test validates updation of pickage expire duration at locker bank level (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_update_pickage_expire_duration(locker_bank, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('pickage_expire_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_pickage_expireduration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates updation of pickage expire duration with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_update_pickage_expire_duration(locker_bank, "valid",
                                                                                       "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_pickage_expireduration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates update of pickage expire duration with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_update_pickage_expire_duration(locker_bank, "invalid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_pickage_expireduration_at_lockerbank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates updation of pickage expire duration with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_update_pickage_expire_duration("invalidBank", "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_pickage_expireduration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates updation of pickage expire duration with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_update_pickage_expire_duration("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------GET PICKAGE EXPIRE DURATION DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_pickage_expireduration_at_lockerbank(self, rp_logger, resource):
        """
        This test validates pickage expire duration at locker bank level (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_pickage_expireduration(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('get_pickage_expire_res_schema.json',
                                                                                'lockers_services'))

        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickage_expireduration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates pickage expire duration at locker bank level with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_pickage_expireduration(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickage_expireduration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates pickage expire duration at locker bank level with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_pickage_expireduration(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickage_expireduration_at_lockerbank_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates pickage expire duration at locker bank level with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_pickage_expireduration("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_pickage_expireduration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates pickage expire duration at locker bank level with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configapi'].verify_pickage_expireduration("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------Patch Pickup Properties-----------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_enable_pickup_patch_property(self, rp_logger, resource):
        """
        This test validates the enabling of pickup property in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"recipientPhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pickup_property(locker_bank, json, "valid",
                                                                              "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('pickup_prop_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_pickup_patch_property_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the patch pickup property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"recipientPhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pickup_property(locker_bank, json, "invalid",
                                                                              "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_pickup_patch_property_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the patch pickup property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"recipientPhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pickup_property(locker_bank, json, "valid",
                                                                              "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_pickup_patch_property_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the patch pickup property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"recipientPhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pickup_property("invalidBank", json, "valid",
                                                                              "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_pickup_patch_property_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the patch pickup property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"recipientPhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_pickup_property("", json, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------------Patch Dropoff Properties---------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_dropoff_property(self, rp_logger, resource):
        """
        This test validates the enabling of dropoff property in a bank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"packagePhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property(locker_bank, json, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('dropoff_prop_resp_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_dropoff_patch_property_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates the patch dropoff property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"packagePhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property(locker_bank, json, "invalid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_dropoff_patch_property_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates the patch dropoff property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"packagePhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property(locker_bank, json, "valid",
                                                                               "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_dropoff_patch_property_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates the patch dropoff property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"packagePhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property("invalidBank", json, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_dropoff_patch_property_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates the patch dropoff property api with invalid scenarios (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"packagePhotoRequired": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property("", json, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -------------------------------------Production Checks--------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_same_access_code_generation(self, rp_logger, resource):
        """
        This test validates the generation of same access code for a recipient with this setting (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        json = '{"personalPackageAllAtOnce": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property(locker_bank, json, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Reserve Deposit one package
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_one = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_one, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code_one = res['assetsDeposited']['accesscode']

        # Reserve Deposit second package
        trackingID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID=recipientID,
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_two = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_two, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code_two = res['assetsDeposited']['accesscode']

        # Pickup both
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code_one, locker_unit_one, locker_bank,
                                                                          "valid",
                                                                          "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code_two, locker_unit_two, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if access_code_one != access_code_two: pytest.fail("Both access code are different")

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_reservation_wo_recipient(self, rp_logger, resource):
        """
        This test validates the generation of same access code for a recipient with this setting (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        json = '{"reservationWORecipient": "enabled"}'
        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID="",
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(res['assetsDeposited']['accesscode'],
                                                                          locker_unit,
                                                                          locker_bank, "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        json = '{"reservationWORecipient": "disabled"}'
        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_same_access_code_generation_with_reservation_wo_recipient(self, rp_logger, resource):
        """
        This test validates the generation of same access code for a recipient with this setting (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        trackingID = test_name + str(random.randint(1, 35000))
        json = '{"personalPackageAllAtOnce": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_dropoff_property(locker_bank, json, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        json = '{"reservationWORecipient": "enabled"}'
        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Reserve Deposit one package
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID="",
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_one = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_one, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code_one = res['assetsDeposited']['accesscode']

        # Reserve Deposit second package
        trackingID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="medium",
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=trackingID,
                                                                           EmailID="", recipientID="",
                                                                           token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit_two = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit_two, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code_two = res['assetsDeposited']['accesscode']

        # Pickup both
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code_one, locker_unit_one, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code_two, locker_unit_two, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        json = '{"reservationWORecipient": "disabled"}'
        res, status_code = resource['configapi'].verify_patch_pro_configuration_status(locker_bank, json, "valid",
                                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if access_code_one == access_code_two: pytest.fail("Both access code are Same")

    # Patch Properties API
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_properties_at_lockerbank(self, rp_logger, resource,context):
        """
          This test validates the Properties status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"signatureCaptureEnabled": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_properties(locker_bank, json, "valid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context['properties'] = res
        print(context['properties'])
        result = self.validate_json_schema_validations(res, self.read_json_file('patch_properties_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_properties_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"signatureCaptureEnabled": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_properties(locker_bank, json, "valid",
                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_properties_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid access_token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"signatureCaptureEnabled": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_properties(locker_bank, json, "invalid",
                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_properties_at_lockerbank_with_invalid_lockerbank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"signatureCaptureEnabled": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_properties("invalidBank", json, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_properties_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"signatureCaptureEnabled": "enabled"}'

        res, status_code = resource['configapi'].verify_patch_properties("", json, "valid", "invalidResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # Put Properties API
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_verify_put_properties_at_lockerbank(self, rp_logger, resource, context):
        """
          This test validates the Properties status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_put_properties(locker_bank, context['properties'], "valid",
                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_put_properties_at_lockerbank_with_invalid_resource(self, rp_logger, resource, context):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_put_properties(locker_bank, context['properties'], "valid",
                                                                       "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_put_properties_at_lockerbank_with_invalid_access_token(self, rp_logger, resource, context):
        """
          This test validates the Properties status of lockerbank with invalid access_token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_put_properties(locker_bank, context['properties'], "invalid",
                                                                       "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_put_properties_at_lockerbank_with_invalid_lockerbank(self, rp_logger, resource, context):
        """
          This test validates the Properties status of lockerbank with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")


        res, status_code = resource['configapi'].verify_put_properties("invalidBank", context['properties'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_put_properties_at_lockerbank_with_no_lockerBank(self, rp_logger, resource, context):
        """
          This test validates the Properties status of lockerbank with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"accessible": true}'

        res, status_code = resource['configapi'].verify_put_properties("", json, "valid", "invalidResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # Patch Email Configuration API
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_patch_email_configuration(locker_bank, json, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_patch_email_configuration(locker_bank, json, "valid",
                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid access_token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_patch_email_configuration(locker_bank, json, "invalid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank_with_invalid_lockerbank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_patch_email_configuration("invalidBank", json, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_patch_email_configuration("", json, "valid", "invalidResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # Post Email Configuration API
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_patch_email_configuration_at_lockerbank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_post_email_configuration(locker_bank, json, "valid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_email_configuration_at_lockerbank_with_invalid_resource(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_post_email_configuration(locker_bank, json, "valid",
                                                                                 "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_email_configuration_at_lockerbank_with_invalid_access_token(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid access_token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_post_email_configuration(locker_bank, json, "invalid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_email_configuration_at_lockerbank_with_invalid_lockerbank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with invalid lockerbank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_post_email_configuration("invalidBank", json, "valid",
                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_post_email_configuration_at_lockerbank_with_no_lockerBank(self, rp_logger, resource):
        """
          This test validates the Properties status of lockerbank with no lockerBank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        json = '{"emailProvider": "PB_PLATFORM"}'

        res, status_code = resource['configapi'].verify_post_email_configuration("", json, "valid", "invalidResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ----------------------- Kiosk Token (keep at the end of the file) ------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_set_heartbeat_for_locker_bank(self, rp_logger, resource, context):
        """
        This test validates the setup a heartbeat time stamp bases on lockerunit (positive scenario)
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_set_heartbeat_properties_for_locker_bank(locker_bank, "valid",
                                                                                                 "validResource",
                                                                                                 context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_proconfiguration_at_lockerbank(self, rp_logger, resource, context):
        """
        This test validates the proconfiguration status of lockerbank (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['configapi'].verify_get_pro_configuration_status(locker_bank, "valid",
                                                                                     "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True