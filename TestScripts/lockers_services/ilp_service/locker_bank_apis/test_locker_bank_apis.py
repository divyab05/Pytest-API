import inspect
import pytest
import base64
from hamcrest import assert_that

from APIObjects.lockers_services.ilp_service.locker_bank_apis import LockerBankAPI
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.integration_api import IntegrationAPI
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string_locker, generate_random_number, \
    generate_random_string
from APIObjects.shared_services.login_api import LoginAPI


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    lockerbankapi = {'app_config': app_config,
                     'locker_api': LockerAPI(app_config, client_token),
                     'lockerbankapi': LockerBankAPI(app_config, client_token),
                     'integration_api': IntegrationAPI(app_config, client_token),
                     'cancel_reservation': CancelReservation(app_config, client_token),
                     'data_reader': DataReader(app_config),
                     'login_api': LoginAPI(app_config),
                     'get_product_name': get_product_name}
    yield lockerbankapi


@pytest.mark.usefixtures('initialize')
class TestLockerBankApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Locker_Bank"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    # ------------------------------LOCKER SIZE DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_sizes_details(self, resource):
        """
        This test validates on locker bank available sizes (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('lockers_sizes_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_sizes_details_with_invalid_resource(self, resource):
        """
        This test validates the lockerbank size details with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_sizes_details_with_invalid_access_token(self, resource):
        """
        This test validates the lockerbank size details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_sizes_details_with_invalid_lockerBank(self, resource):
        """
        This test validates the lockerbank size details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_sizes_details_with_no_lockerBank(self, resource):
        """
        This test validates the lockerbank size details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------LOCKERBANK DIMENSION DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_dimensions_oflockerbank(self, resource):
        """
        This test validates lockerbank dimensions details (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_lockerbank_Dimensions(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_dimensions_oflockerbank_with_invalid_resource(self, resource):
        """
        This test validates lockerbank dimensions details with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_lockerbank_Dimensions(locker_bank, "valid",
                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_dimensions_oflockerbank_with_invalid_access_token(self, resource):
        """
        This test validates lockerbank dimensions details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_lockerbank_Dimensions(locker_bank, "invalid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_dimensions_oflockerbank_with_invalid_lockerBank(self, resource):
        """
        This test validates lockerbank dimensions details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_lockerbank_Dimensions("invalidBank", "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_dimensions_oflockerbank_with_no_lockerBank(self, resource):
        """
        This test validates lockerbank dimensions details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_lockerbank_Dimensions("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------LOCKER BANK REFRIGERATION TYPES---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_refrigeration_types_oflockerbank(self, resource):
        """
        This test validates lockerbank refrigeration details (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types(locker_bank, "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('refrigeration_types_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_refrigeration_types_oflockerbank_with_invalid_resource(self, resource):
        """
        This test validates lockerbank refrigeration details with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types(locker_bank, "valid",
                                                                                             "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_refrigeration_types_oflockerbank_with_invalid_access_token(self, resource):
        """
        This test validates lockerbank refrigeration details with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types(locker_bank, "invalid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_bank_refrigeration_types_oflockerbank_with_invalid_lockerBank(self, resource):
        """
        This test validates lockerbank refrigeration details with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types("invalidBank", "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers88
    def test_verify_locker_bank_refrigeration_types_oflockerbank_with_no_lockerBank(self, resource):
        """
        This test validates lockerbank refrigeration details with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types("", "valid",
                                                                                             "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------STALE PACKAGES AT LOCKERBANK DETAILS---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_stale_packages_at_lockerBank(self, resource):
        """
        This test validates the stale packages at lockerbank (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_stale_packages_at_lockerBank(locker_bank, "valid",
                                                                                             "validResource")
        if status_code == 200 or status_code == 404:
            assert True
        else:
            assert False

    @pytest.mark.regressioncheck_lockers
    def test_verify_stale_packages_at_lockerBank_with_invalid_resource(self, resource):
        """
        This test validates the stale packages at lockerbank with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_stale_packages_at_lockerBank(locker_bank, "valid",
                                                                                             "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_stale_packages_at_lockerBank_with_invalid_access_token(self, resource):
        """
        This test validates the stale packages at lockerbank with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_stale_packages_at_lockerBank(locker_bank, "invalid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_stale_packages_at_lockerBank_with_invalid_locker_bank(self, resource):
        """
        This test validates the stale packages at lockerbank with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_stale_packages_at_lockerBank("invalidBank", "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_stale_packages_at_lockerBank_with_no_locker_bank(self, resource):
        """
        This test validates the stale packages at lockerbank with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_stale_packages_at_lockerBank("", "valid",
                                                                                             "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ---------------------------------------GET LOCKER BANK TIMEZONE--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_timezone(self, resource):
        """
        This test validates the locker bank timezone (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_timezone(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res,
                                                       self.read_json_file('get_lockerbank_timezone_res_schema.json',
                                                                           'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_timezone_with_invalid_resource(self, resource):
        """
        This test validates the locker bank timezone with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_timezone(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_timezone_with_invalid_access_token(self, resource):
        """
        This test validates the locker bank timezone with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_timezone(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_timezone_with_invalid_lockerbank(self, resource):
        """
        This test validates the locker bank timezone with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_timezone(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_timezone_with_no_lockerbank(self, resource):
        """
        This test validates the locker bank timezone with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_locker_timezone("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ---------------------------------GET QR CODE API-----------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_code(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context['qrCode'] = res["pairCode"]
        result = self.validate_json_schema_validations(res, self.read_json_file('get_qr_code_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_code_with_invalid_access_token(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_code_with_invalid_resource(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_code_with_invalidBank(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_code_with_no_bank(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ---------------------------------GET CONFIG FOR PAIRING-----------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "valid", "validResource")
        context['manHardwareID'] = res['manufacturerHardwareID']

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_invalid_access_token(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                context['manHardwareID'], "invalid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_invalid_resource(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_invalidBank(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api("invalidBank", context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_no_bank(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api("", context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_invalid_qrcode(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, "QRCODE",
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_used_qr(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_qr_configuration_with_invalid_MHID(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context['qrCode'] = res["pairCode"]

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                "TESTINGMHID", "valid",
                                                                                "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    # -------------------------------- Get Pair code-----------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_pair_code(self, context, resource):
        """
        This test validates the get pair code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api(context['manHardwareID'], "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('get_pair_code_MHID_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_pair_code_with_invalid_access_token(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api(locker_bank, "invalid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_pair_code_with_invalid_resource(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api(locker_bank, "valid",
                                                                                      "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_pair_code_with_invalidMHID(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api("invalidBank", "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_pair_code_with_no_bank(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # --------------------------------- DECODE API -----------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_decode_api(self, resource):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_alphanumeric_string_locker()
        sample_string_bytes = trackingID.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        encodedString = base64_bytes.decode("ascii")

        res, status_code = resource['lockerbankapi'].verify_decode_api(encodedString, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        decodedTrackingID = res['decoded'][0]['tracking_number']
        # result = self.validate_json_schema_validations(res, self.read_json_file('decode_api_res_schema.json', 'lockers_services'))
        # if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error message {arg}".format(arg=result['error_message']))
        if decodedTrackingID != trackingID:
            assert decodedTrackingID.upper() == trackingID.upper()

    @pytest.mark.regressioncheck_lockers
    def test_verify_decode_api_with_no_encoded_string(self, resource):
        """
        This test validates decode api when tracking is not sent decoded (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_number(6)

        res, status_code = resource['lockerbankapi'].verify_decode_api(trackingID, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_decode_api_with_no_trackingID(self, resource):
        """
        This test validates decode api when tracking is not sent (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_decode_api("", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_decode_api_with_invalid_access_token(self, resource):
        """
        This test validates decode api when access token is invalid (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_decode_api("", "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_decode_api_with_invalid_resource(self, resource):
        """
        This test validates decode api when url is invalid (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_decode_api("", "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # --------------------- Decode Variant V2 for rutgers for PitneyTrack ---------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_generate_user_token_for_decode_api(self, resource, context):
        """This test is for generating various user token for different Enterprise since
            decode API behaviours differs with FIREBALL_2.0_PLAN and TRACKING_PLAN
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        # SSTO 1.0 + Locker Plan
        EmailID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EmailID')
        password = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'password')
        context['ssto_locker_plan_user_token'] = resource['login_api'].get_access_token_for_user_credentials(
            username=EmailID, password=password)

    @pytest.mark.regressioncheck_lockers
    def test_verify_decodeV2_with_no_receive_and_reservation(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_string(uppercase=True, lowercase=False, digits=True, char_count=12)
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))
        response = decodeV2_response.json()
        if response['units'][0]['status'] != "UN-RESERVE":
            self.Failures.append("Status is incorrect")
        if len(response['units'][0]['assetsReserved']['recipient']) != 0:
            self.Failures.append("Recipient Object in assetsReserved")
        if len(response['units'][0]['recipient']) != 0:
            self.Failures.append("Recipient Object")
        if response['units'][0]['carrier']['tracking_number'] != trackingID:
            self.Failures.append("carrier has incorrect tracking ID")

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_decodeV2_with_receive_and_no_reservation(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_string(uppercase=True, lowercase=False, digits=True, char_count=12)
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        receivingSiteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receivingSiteID')

        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))

        # Receiving asset for same trackingID
        receiveAsset_response = resource['integration_api'].receiving_assets(trackingID=trackingID,
                                                                             recipientID=recipientID,
                                                                             receivingSiteID=receivingSiteID)
        assert_that(self.validate_response_code(receiveAsset_response, 201))

        # Decode V2 has recipient information now
        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))
        response = decodeV2_response.json()
        if response['units'][0]['status'] != "UN-RESERVE":
            self.Failures.append("Status is incorrect")
        if len(response['units'][0]['assetsReserved']['recipient']) != 0:
            self.Failures.append("Recipient Object in assetsReserved")
        if len(response['units'][0]['recipient']) == 0:
            self.Failures.append("Recipient Object missing")
        if response['units'][0]['carrier']['tracking_number'] != trackingID:
            self.Failures.append("carrier has incorrect tracking ID")

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_decodeV2_with_locker_reservation(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_string(uppercase=True, lowercase=False, digits=True, char_count=12)
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        # Reserve Locker for same trackingID
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank,
                                                                            size='extra small',
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=trackingID,
                                                                            EmailID='',
                                                                            recipientID=recipientID,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Decode V2 has recipient and locker information now
        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))
        response = decodeV2_response.json()
        if response['units'][0]['status'] != "RESERVE":
            self.Failures.append("Status is incorrect")
        if len(response['units'][0]['assetsReserved']['recipient']) == 0:
            self.Failures.append("Recipient Object in assetsReserved is missing")
        if len(response['units'][0]['recipient']) != 0:
            self.Failures.append("Recipient Object present")
        if response['units'][0]['carrier']['tracking_number'] != trackingID:
            self.Failures.append("carrier has incorrect tracking ID")

        # Cancel Reservation
        res, status_code = resource['cancel_reservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        # Decode V2 has only recipient information now
        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_decodeV2_with_deposit(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_string(uppercase=True, lowercase=False, digits=True, char_count=12)
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        # Reserve Locker for same trackingID
        res, status_code = resource['locker_api'].verify_reserve_locker_api(locker_bank=locker_bank,
                                                                            size='extra small',
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=trackingID,
                                                                            EmailID='',
                                                                            recipientID=recipientID,
                                                                            token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        # Deposit
        res, status_code = resource['locker_api'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                            "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        # Decode V2 should give 404
        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 404))

        res, status_code = resource['locker_api'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                           "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.regressioncheck_lockers
    def test_verify_decodeV2_with_multicarrier_tracking(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = '9314869904300103691999'
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        decodeV2_response = resource['lockerbankapi'].verify_decodeV2_api(locker_bank=locker_bank,
                                                                          trackingID=trackingID,
                                                                          encodedFlag='', token_type="valid",
                                                                          resource_type="validResource")
        assert_that(self.validate_response_code(decodeV2_response, 200))
        response = decodeV2_response.json()
        if len(response['units']) != 2:
            self.Failures.append(response['units'])
            self.Failures.append("Decode does not have multiple barcodes, actual = " + str(len(response['units'])))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # add dept and multicarrier receive and reservation and encoded

    # ------------------ Kiosk Token (Keep at the end of the file) ---------------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_Lockerbank_sizes_details(self, resource, context):
        """
        This test validates on locker bank available sizes (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_Lockerbank_sizes(locker_bank, "valid", "validResource",
                                                                             context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_locker_bank_refrigeration_types_oflockerbank(self, resource, context):
        """
        This test validates lockerbank refrigeration details (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_locker_refrigerated_locker_types(locker_bank, "valid",
                                                                                             "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_get_qr_configuration(self, context, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context['qrCode'] = res["pairCode"]

        res, status_code = resource['lockerbankapi'].verify_get_config_pair_api(locker_bank, context['qrCode'],
                                                                                context['manHardwareID'], "valid",
                                                                                "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_decode_api(self, resource, context):
        """
        This test validates the decode api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        trackingID = generate_random_alphanumeric_string_locker()
        sample_string_bytes = trackingID.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        encodedString = base64_bytes.decode("ascii")

        res, status_code = resource['lockerbankapi'].verify_decode_api(encodedString, "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        decodedTrackingID = res['decoded'][0]['tracking_number']
        if decodedTrackingID != trackingID:
            assert decodedTrackingID.upper() == trackingID.upper()

    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_get_pair_code(self, context, resource):
        """
        This test validates the get pair code api (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lockerbankapi'].verify_get_pair_code_by_MHID_api(context['manHardwareID'], "valid",
                                                                                      "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('get_pair_code_MHID_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))
