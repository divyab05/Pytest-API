import sys
import random
import pytest

from APIObjects.lockers_services.ilp_service.lookup_apis import LookUPAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    locker_api = {'app_config': app_config,
                  'locker_api': LookUPAPI(app_config, client_token),
                  'data_reader': DataReader(app_config),
                  'get_product_name': get_product_name}
    yield locker_api


@pytest.mark.usefixtures('initialize')
class TestLockerBankApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Locker_Lookup"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_list_banks_api(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks(context['tenantID'], context['siteID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_list_banks_api_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks(context['tenantID'], context['siteID'], "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_list_banks_api_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks(context['tenantID'], context['siteID'], "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_list_banks_api_with_invalid_tenantID(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks("XX", context['siteID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_list_banks_api_with_invalid_siteID(self, rp_logger, resource, context):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks(context['tenantID'], "XX", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True

    # ------------------------------Look ups api DETAILS------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_lookUp_bank(context["tenantID"], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api_with_siteID(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        addSiteEndpoint = context["tenantID"] + "&siteID=" + context["siteID"]
        res, status_code = resource['locker_api'].verify_lookUp_bank(addSiteEndpoint, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api_with_invalid_access_token(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_lookUp_bank(context["tenantID"], "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api_with_invalid_resource(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_lookUp_bank(context["tenantID"], "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api_with_invalid_tenantID(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_lookUp_bank("XX", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lookups_api_with_invalid_siteID(self, context, rp_logger, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        addSiteEndpoint = context["tenantID"] + "&siteID=XX"
        res, status_code = resource['locker_api'].verify_lookUp_bank(addSiteEndpoint, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True

    # ------------------------------SITES AVAILABLE BASED ON TENANT ID DETAILS------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_sites_available_basedon_tenantID(self, rp_logger, context, resource):
        """
        This test validates sites available on basis of tenantID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_sites_basedon_tenantID(context['tenantID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_sites_available_basedon_tenantID_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates sites available on basis of tenantID with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_sites_basedon_tenantID(context['tenantID'], "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_sites_available_basedon_tenantID_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates sites available on basis of tenantID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_sites_basedon_tenantID(context['tenantID'], "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_sites_available_basedon_tenantID_with_invalid_tenantID(self, rp_logger, context, resource):
        """
        This test validates sites available on basis of tenantID with invalid tenantID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_sites_basedon_tenantID("invalidTenantID", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------GET SITE FROM TENANT ID------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_list_banks_for_site(self, rp_logger, context, resource):
        """
        This test validates list of banks from site (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks_for_site(context['siteID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_list_banks_for_site_with_invalid_token(self, rp_logger, context, resource):
        """
        This test validates list of banks from site (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks_for_site(context['siteID'], "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_list_banks_for_site_with_invalidResource(self, rp_logger, context, resource):
        """
        This test validates list of banks from site (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks_for_site(context['siteID'], "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_list_banks_for_site_with_invalid_site(self, rp_logger, context, resource):
        """
        This test validates list of banks from site (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks_for_site("invalidSiteID", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_list_banks_for_site_with_no_site(self, rp_logger, context, resource):
        """
        This test validates list of banks from site (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_list_banks_for_site("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------GET Lockers FROM ManID ID------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers(self, rp_logger, context, resource):
        """
        This test validates get Lockers (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_lockers(context['manufacturerID'], "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_invalid_token(self, rp_logger, context, resource):
        """
        This test validates get Lockers (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_lockers(context['manufacturerID'], "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_invalidResource(self, rp_logger, context, resource):
        """
        This test validates get Lockers (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_lockers(context['manufacturerID'], "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_invalid_lockerID(self, rp_logger, context, resource):
        """
        This test validates get Lockers (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_lockers("invalidLockerID", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_no_lockerID(self, rp_logger, context, resource):
        """
        This test validates get Lockers (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_lockers("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # ------------------------------GET Locker unit FROM ManID ID------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_get_locker_unit(self, rp_logger, context, resource):
        """
        This test validates get Locker unit (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(random.randint(1, 100))

        res, status_code = resource['locker_api'].verify_get_locker_unit(context['manufacturerID'], locker_unit, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_locker_unit_with_invalid_token(self, rp_logger, context, resource):
        """
        This test validates get Locker unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(random.randint(1, 100))

        res, status_code = resource['locker_api'].verify_get_locker_unit(context['manufacturerID'], locker_unit, "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_locker_unit_with_invalidResource(self, rp_logger, context, resource):
        """
        This test validates get Locker unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(random.randint(1, 100))

        res, status_code = resource['locker_api'].verify_get_locker_unit(context['manufacturerID'], locker_unit, "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_locker_unit_with_invalid_lockerID(self, rp_logger, context, resource):
        """
        This test validates get Locker unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(random.randint(1, 100))

        res, status_code = resource['locker_api'].verify_get_locker_unit("invalidManID", locker_unit, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_no_lockerID(self, rp_logger, context, resource):
        """
        This test validates get Lockers (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_unit = str(random.randint(1, 100))

        res, status_code = resource['locker_api'].verify_get_locker_unit("", locker_unit, "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_get_lockers_with_invalid_locker_unit(self, rp_logger, context, resource):
        """
        This test validates get Locker unit (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['locker_api'].verify_get_locker_unit(context['manufacturerID'], "XXX", "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True
