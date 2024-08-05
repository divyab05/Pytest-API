import sys
import random
import pytest

from APIObjects.lockers_services.ilp_service.admin_apis import AdminAPI
from APIObjects.lockers_services.ilp_service.bank_unit_status_apis import StatusAPIs
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from APIObjects.lockers_services.ilp_service.locker_bank_apis import LockerBankAPI
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.lookup_apis import LookUPAPI
from APIObjects.lockers_services.ilp_service.update_flow import UpdateFlow
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, get_product_name):
    locker_api = {'app_config': app_config,
                  'lookupapi': LookUPAPI(app_config, generate_access_token),
                  'configurationapi': ConfigurationAPI(app_config, generate_access_token),
                  'lockerbankapi': LockerBankAPI(app_config, generate_access_token),
                  'reserveapi': LockerAPI(app_config, generate_access_token),
                  'updatereserve': UpdateFlow(app_config, generate_access_token),
                  'cancelreserve': CancelReservation(app_config, generate_access_token),
                  'statusapi': StatusAPIs(app_config, generate_access_token),
                  'departmentapi': DepartmentLockerAPI(app_config, generate_access_token),
                  'adminapi': AdminAPI(app_config, generate_access_token),
                  'data_reader': DataReader(app_config),
                  'get_product_name': get_product_name}
    yield locker_api


@pytest.mark.usefixtures('initialize')
class TestAdminTokenApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Admin_Token"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @pytest.mark.skip(reason="need to fix object class")
    def test_list_banks_api_admin(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lookupapi'].verify_list_banks(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_lookup_banks_api_admin(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['lookupapi'].verify_lookUp_bank(context["tenantID"], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_get_qr_code_admin(self, rp_logger, resource):
        """
        This test validates the get qr code api (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['lockerbankapi'].verify_get_qr_code_api(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_reserve_locker_by_emailID_admin(self, rp_logger, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reserveapi'].verify_reserve_locker_api(locker_bank=locker_bank, size="extra small",
                                                                            accessible="", refrigeration="",
                                                                            climate_type="", TrkgID=TrkgID,
                                                                            EmailID="manvi@yopmail.com",
                                                                            recipientID="", token_type="valid",
                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        newTrackingID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['updatereserve'].verify_update_reservation_based_on_unit(locker_bank, locker_unit,
                                                                                             newTrackingID, "valid",
                                                                                             "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['cancelreserve'].cancel_reservation_basedon_lockerunitID(locker_unit, locker_bank,
                                                                                             "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_reserve_unit_and_free_admin(self, rp_logger, resource):
        """
        This test validates reservation is done or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['reserveapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit="39",
                                                                                   size="extra small", accessible="",
                                                                                   refrigeration="", climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   EmailID="manvi@yopmail.com",
                                                                                   recipientID="", token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        unit_one = res['manufacturerLockerID']

        TrkgID = test_name + str(random.randint(1, 35000))
        res, status_code = resource['reserveapi'].verify_reservation_based_on_unit(locker_bank=locker_bank,
                                                                                   locker_unit="40",
                                                                                   size="extra small", accessible="",
                                                                                   refrigeration="", climate_type="",
                                                                                   TrkgID=TrkgID,
                                                                                   EmailID="manvi@yopmail.com",
                                                                                   recipientID="", token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        unit_two = res['manufacturerLockerID']

        res, status_code = resource['cancelreserve'].free_list_of_locker_units(unit_one, unit_two, locker_bank, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_bank_in_service_admin(self, rp_logger, resource):
        """
        This test validates on locker bank in service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        delivery = True

        res, status_code = resource['statusapi'].verify_update_locker_bank_status(locker_bank, delivery, "valid",
                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['statusapi'].verify_get_locker_bank_status(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_unit_in_service_admin(self, rp_logger, resource):
        """
        This test validates on locker unit out of service (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_unit = '41'
        enabled = True

        res, status_code = resource['statusapi'].verify_update_locker_unit_status(locker_bank, locker_unit, enabled,
                                                                                  "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['statusapi'].verify_get_locker_unit_status(locker_bank, locker_unit, "valid",
                                                                               "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_list_of_locker_in_service_admin(self, rp_logger, resource):
        """
        This test validates on locker unit current status (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        enabled = True
        unit_one = "41"
        unit_two = "42"

        res, status_code = resource['statusapi'].verify_update_list_of_lockers(locker_bank, enabled, unit_one, unit_two,
                                                                               "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.skip(reason="need to check")
    def test_list_department_at_site_admin(self, rp_logger, resource, context):
        """
        This test validates the list of available department at site
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['departmentapi'].verify_get_All_Department_at_site(context['tenantID'],
                                                                                       context['siteID'],
                                                                                       "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_lookup_activity_admin(self, rp_logger, resource, context):
        """
        This test validates the activity api for admin portal
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['adminapi'].verify_lookup_activity_admin(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_lookup_activity_count_admin(self, rp_logger, resource, context):
        """
        This test validates the activity api for admin portal
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['adminapi'].verify_lookup_activity_count_admin(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_activity_export_admin(self, rp_logger, resource, context):
        """
        This test validates the activity api for admin portal
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['adminapi'].verify_activity_export_admin(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    def test_get_sites_admin(self, rp_logger, resource, context):
        """
        This test validates the activity api for admin portal
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['adminapi'].verify_get_sites_admin(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # ----------------------------GET PCN---------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_get_pcn(self, rp_logger, resource):
        """
        This test validates the get pcn of an environment(positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['configurationapi'].verify_get_pcn_configuration("valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
