import random
import sys
import pytest

from APIObjects.lockers_services.device_token import generate_kiosk_token
from APIObjects.lockers_services.ilp_service.bank_unit_status_apis import StatusAPIs
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name, context):
    statusapi = {'app_config': app_config,
                 'statusapi': StatusAPIs(app_config, client_token),
                 'lockerapi': LockerAPI(app_config, client_token),
                 'cancelreservation': CancelReservation(app_config, client_token),
                 'data_reader': DataReader(app_config),
                 'get_product_name': get_product_name}
    context['basic_device_token'] = generate_kiosk_token(app_config).kiosk_token
    context['basic_integrator_token'] = generate_kiosk_token(app_config).integrator_token
    yield statusapi


@pytest.mark.usefixtures('initialize')
class TestStatusApi(common_utils):

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

    # ------------------------------UPDATE LOCKER BANK STATUS---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_bank_out_of_service(self, rp_logger, resource):
        """
        This test validates on locker bank out of service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "validResource")
        if status_code == 200:
            result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_outofservice_res.json',
                                                                                    'lockers_services'))
            if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                                 "message {arg}".format(arg=result['error_message']))
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, True, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.order(1)
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_sp360uk_smoke
    @pytest.mark.ilp_sp360global_smoke
    @pytest.mark.ilp_govcloud_smoke
    def test_verify_update_locker_bank_in_service(self, rp_logger, resource):
        """
        This test validates on locker bank in service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_inservice_res.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

        if status_code != 200:
            print(res)
        else:
            res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid",
                                                                                   "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
            bank = res['status']
            if bank != "ENABLED":
                print("Error occurred")

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_oos_when_reserved_unit(self, rp_logger, resource):
        """
        This test validates on locker bank status when reserved unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrackingID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        email = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="",
                                                                           refrigeration="", climate_type="",
                                                                           TrkgID=TrackingID,
                                                                           EmailID=email,
                                                                           recipientID="", token_type="valid",
                                                                           resource_type="validResource")
        if status_code != 200:
            print(res)
        else:
            locker_unit = res["manufacturerLockerID"]
            res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                      "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

            res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                     locker_bank,
                                                                                                     "valid",
                                                                                                     "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_oos_when_occupied_unit(self, rp_logger, context, resource):
        """
        This test validates on locker bank status when occupied unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrackingID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        email = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="",
                                                                           refrigeration="", climate_type="",
                                                                           TrkgID=TrackingID,
                                                                           EmailID=email,
                                                                           recipientID="", token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode']
        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_bank_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates on locker bank when invalid resource is passed(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_bank_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates on locker bank when invalid access token is passed(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "invalid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_bank_status_with_invalid_locker_bank(self, rp_logger, resource):
        """
        This test validates on locker bank when invalid locker bank is passed(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status("invalidBank", delivery, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_bank_status_with_no_locker_bank(self, rp_logger, resource):
        """
        This test validates on locker bank when no locker bank is passed(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status("", delivery, "valid",
                                                                                  "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------GET LOCKER BANK STATUS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_status(self, rp_logger, resource):
        """
        This test validates on locker bank current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_status_responce_sche.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates on locker bank current status with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates on locker bank current status with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_status_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker bank current status with invalid locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['statusapi'].verify_get_locker_bank_status("invalidBank", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_status_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker bank current status with no locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['statusapi'].verify_get_locker_bank_status("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------UPDATE LOCKER UNIT STATUS---------------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_out_of_service(self, rp_logger, resource):
        """
        This test validates on locker unit out of service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    def test_verify_update_locker_unit_in_service(self, rp_logger, resource):
        """
        This test validates on locker unit out of service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('unit_update_status_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerunit_oos_when_reserved_unit(self, rp_logger, resource):
        """
        This test validates on locker unit status when reserved unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrackingID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        email = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit=locker_unit,
                                                                                  size=locker_size, accessible="",
                                                                                  refrigeration="",
                                                                                  climate_type="", TrkgID=TrackingID,
                                                                                  EmailID=email,
                                                                                  recipientID="", token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        if status_code != 200:
            print(res)
        else:
            locker_unit = res["manufacturerLockerID"]
            res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                      "valid",
                                                                                      "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

            res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                     locker_bank,
                                                                                                     "valid",
                                                                                                     "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerunit_oos_when_occupied_unit(self, rp_logger, context, resource):
        """
        This test validates on locker unit status when occupied unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        TrackingID = test_name + str(random.randint(1, 35000))
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        email = resource['data_reader'].pd_get_data(self.configparameter, test_name, "EmailID")
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['lockerapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                  locker_unit=locker_unit,
                                                                                  size=locker_size, accessible="",
                                                                                  refrigeration="",
                                                                                  climate_type="", TrkgID=TrackingID,
                                                                                  EmailID=email,
                                                                                  recipientID="", token_type="valid",
                                                                                  resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        access_code = res['assetsDeposited']['accesscode']
        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_status_with_invalid_lockerunit(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid locker unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid",
                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "invalid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_status_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status("invalidBank", locker_unit, enabled,
                                                                                  "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_locker_unit_status_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status("", locker_unit, enabled, "valid",
                                                                                  "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------GET LOCKER UNIT STATUS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status(self, rp_logger, resource):
        """
        This test validates on locker unit current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status(locker_bank, locker_unit, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_status_responce_sche.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status_with_invalid_unit(self, rp_logger, resource):
        """
        This test validates on locker unit current status with invalid unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status(locker_bank, locker_unit, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates on locker unit current status with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status(locker_bank, locker_unit, "valid",
                                                                               "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates on locker unit current status with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status(locker_bank, locker_unit, "invalid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit current status with invalid locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status("invalidBank", locker_unit, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_locker_unit_status_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit current status with no locker bank(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))

        res, status_code = resource['statusapi'].verify_get_locker_unit_status("", locker_unit, "valid",
                                                                               "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------Enable and Disable LIST OF LOCKERS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_enable_list_of_locker(self, rp_logger, resource):
        """
        This test validates on locker unit current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('list_units_status_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_disable_list_of_locker(self, rp_logger, resource):
        """
        This test validates on locker unit current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, True, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.skip(reason="IL-8945")
    @pytest.mark.regressioncheck_lockers
    def test_verify_update_list_of_locker_with_invalid_unit(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid unit passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(500, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_list_of_locker_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid resource passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_list_of_locker_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid access token passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_list_of_locker_with_invalid_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid locker bank passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_update_list_of_locker_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates on locker unit with invalid locker bank passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')
        unit_one = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        unit_two = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'second_unit'))

        res, status_code = resource['statusapi'].verify_update_list_of_lockers("", enabled, unit_one, unit_two, "valid",
                                                                               "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(405, status_code, res) is True

    # ----------------------- Kiosk Token (Keep at the end of the file) -----------------------------
    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_update_locker_bank_in_service(self, rp_logger, resource, context):
        """
        This test validates on locker bank in service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'delivery')

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if status_code != 200:
            print(res)
        else:
            res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid",
                                                                                   "validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
            bank = res['status']
            if bank != "ENABLED":
                print("Error occurred")

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_Lockerbank_status(self, rp_logger, resource, context):
        """
        This test validates on locker bank current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid", "validResource",
                                                                               context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_kiosk
    def test_kiosk_update_locker_unit_in_service(self, rp_logger, resource, context):
        """
        This test validates on locker unit out of service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_unit'))
        enabled = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'enabled')

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid", "validResource", context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
