import random
import sys
import pytest

from APIObjects.lockers_services.ilp_service.locker_onboarding import lockerOnboarding
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token):
    onboarding = {'app_config': app_config,
                  'onboardingAPI': lockerOnboarding(app_config, generate_access_token),
                  'basicflow': LockerAPI(app_config, generate_access_token),
                  'data_reader': DataReader(app_config)}
    yield onboarding


@pytest.mark.usefixtures('initialize')
class TestConfigurationApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_locker_Onboarding"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @pytest.mark.onboarding
    def test_get_pcn(self, rp_logger, resource):
        """
        This test validates the get pcn of an environment(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['onboardingAPI'].verify_get_pcn_configuration("valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.onboarding
    def test_verify_the_upload_PCN_data(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        PCN = 'AutomationPCN_' + str(random.randint(1, 100))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_upload_the_PCN_data(token_type="valid", PCN=PCN)
        assert self.validate_response_code(res, 200) is True
        resource['onboardingAPI'].db_pcn_get(PCN)
        print("Get complete")
        resource['onboardingAPI'].db_pcn_delete(PCN)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_verify_add_locker_bank_without_serial_ids(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        MID = "AutomationLockerBank_" + str(random.randint(1, 100000))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=None,
                                                               wagoSerial=None, deviceSerial=None,
                                                               description="Bank without serial",
                                                               units=None)
        assert self.validate_response_code(res, 200) is True

        res, status_code = resource['basicflow'].verify_Lockerbank_details(MID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        resource['onboardingAPI'].db_delete_lockerbank(MID)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_verify_add_locker_bank_with_serial_ids(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        MID = "AutomationLockerBank_" + str(random.randint(1, 100000))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=MID,
                                                               wagoSerial=MID, deviceSerial=MID,
                                                               description="Bank with serial",
                                                               units=None)
        assert self.validate_response_code(res, 200) is True

        res, status_code = resource['basicflow'].verify_Lockerbank_details(MID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        resource['onboardingAPI'].db_delete_lockerbank(MID)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_verify_add_config_without_serial_ids(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        MID = "AutomationLockerBank_" + str(random.randint(1, 100000))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=None,
                                                               wagoSerial=None, deviceSerial=None,
                                                               description="Bank without serial",
                                                               units=None)
        assert self.validate_response_code(res, 200) is True

        res = resource['onboardingAPI'].verify_add_config_locker_bank(lockerBank=MID, manHardwareID=None,
                                                                      wagoSerial=None,
                                                                      deviceSerial=None)
        assert self.validate_response_code(res, 200) is True

        res = resource['onboardingAPI'].verify_get_config_lockerbank(lockerBank=MID)
        assert self.validate_response_code(res, 200) is True

        resource['onboardingAPI'].db_delete_lockerbank(MID)
        resource['onboardingAPI'].db_delete_config_lockerbank(MID)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_verify_add_config_with_serial_ids(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        MID = "AutomationLockerBank_" + str(random.randint(1, 100000))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=MID,
                                                               wagoSerial=MID, deviceSerial=MID,
                                                               description="Bank with serial",
                                                               units=None)
        assert self.validate_response_code(res, 200) is True

        res = resource['onboardingAPI'].verify_add_config_locker_bank(lockerBank=MID, manHardwareID=MID,
                                                                      wagoSerial=MID,
                                                                      deviceSerial=None)
        assert self.validate_response_code(res, 200) is True

        res = resource['onboardingAPI'].verify_get_config_lockerbank(lockerBank=MID)
        assert self.validate_response_code(res, 200) is True
        print(res)

        resource['onboardingAPI'].db_delete_lockerbank(MID)
        resource['onboardingAPI'].db_delete_config_lockerbank(MID)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_verify_add_units_to_lockerbank(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        MID = "AutomationLockerBank_" + str(random.randint(1, 100000))
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=MID,
                                                               wagoSerial=MID, deviceSerial=MID,
                                                               description="Bank with serial",
                                                               units=None)
        assert self.validate_response_code(res, 200) is True

        res = resource['onboardingAPI'].verify_add_config_locker_bank(lockerBank=MID, manHardwareID=MID,
                                                                      wagoSerial=MID,
                                                                      deviceSerial=None)
        assert self.validate_response_code(res, 200) is True

        response = res.json()
        units = response['columns'][0]['units']

        res = resource['onboardingAPI'].verify_add_locker_bank(bankName=MID, manufacturerID=MID, manHardwareID=MID,
                                                               wagoSerial=MID, deviceSerial=MID,
                                                               description="Bank with serial",
                                                               units=units)
        assert self.validate_response_code(res, 200) is True

        res, status_code = resource['basicflow'].verify_Lockerbank_details(MID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        resource['onboardingAPI'].db_delete_lockerbank(MID)
        resource['onboardingAPI'].db_delete_config_lockerbank(MID)
        print("Delete complete")

    @pytest.mark.onboarding
    def test_delete_asset(self, rp_logger, resource):
        """
        This test validates the upload the PCN data(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        for x in range(1):
            resource['onboardingAPI'].db_delete_asset()

        print("Delete complete")
