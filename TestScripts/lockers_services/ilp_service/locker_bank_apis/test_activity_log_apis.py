import sys
import pytest
from datetime import datetime, timedelta

from APIObjects.lockers_services.ilp_service.activity_log_apis import ActivityAPI
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, get_product_name):
    activityapi = {'app_config': app_config,
                   'locker_api': LockerAPI(app_config, client_token),
                   'activityapi': ActivityAPI(app_config, client_token),
                   'data_reader': DataReader(app_config),
                   'get_product_name': get_product_name}
    yield activityapi


@pytest.mark.usefixtures('initialize')
class TestLockerBankApi(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Locker_Activity"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_Lockerbank_details(self, rp_logger, context, resource):
        """
        This test validates locker bank details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['locker_api'].verify_Lockerbank_details(locker_bank, "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        context["tenantID"] = res['tenantID']
        context["siteID"] = res['siteID']
        context["integratorID"] = res['integratorID']
        context["manufacturerID"] = res['manufacturerID']
        context["manufacturerHardwareID"] = res['manufacturerHardwareID']
        result = self.validate_json_schema_validations(res, self.read_json_file('lockerbank_detail_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    # ------------------------------DAILY ACTIVITY COUNT BASED ON TENANT ID DETAILS--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_tenantID(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of  tenantID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_tenantID(context['tenantID'], "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('daily_activity_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_tenantID_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of tenantID  with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_tenantID(context['tenantID'], "valid",
                                                                                           "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_tenantID_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of tenantID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_tenantID(context['tenantID'],
                                                                                           "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_tenantID_with_invalid_tenantID(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of tenantID with invalid tenantID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_tenantID("invalidTenantID", "valid",
                                                                                           "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------DAILY ACTIVITY COUNT BASED ON SITE ID DETAILS--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_siteID(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of site ID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_siteID(context['siteID'], "valid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('daily_activity_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail(
            "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_siteID_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of site ID with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_siteID(context['siteID'], "valid",
                                                                                         "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_siteID_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of site ID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_siteID(context['siteID'], "invalid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_daily_activitycount_basedon_siteID_with_invalid_siteID(self, rp_logger, resource, context):
        """
        This test validates daily activity count on basis of site ID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_daily_activitycount_siteID("invalidSiteID", "invalid",
                                                                                         "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------LOCKER BANK DETAILS AT SITE--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_detail_by_siteID(self, rp_logger, resource, context):
        """
        This test validates locker bank details by site ID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_detail_at_site(context['siteID'], "valid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        print(res)

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_detail_by_siteID_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates locker bank details by site ID with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_detail_at_site(context['siteID'], "valid",
                                                                                        "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_detail_by_siteID_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates locker bank details by site ID with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_detail_at_site(context['siteID'], "invalid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_detail_by_siteID_with_invalid_siteID(self, rp_logger, resource, context):
        """
        This test validates locker bank details by site ID with invalid tenantID (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_detail_at_site("invalidSiteID", "valid",
                                                                                        "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------DELETE ACTIVITY CACHE API--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_activity_cache(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_integrator_cache(context['integratorID'], "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('string_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_activity_cache_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_integrator_cache(context['integratorID'], "valid",
                                                                                      "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_activity_cache_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_integrator_cache(context['integratorID'],
                                                                                      "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_activity_cache_with_no_integrator(self, rp_logger, resource):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_integrator_cache("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    # -----------------------------DELETE LOCKER BANK CACHE API--------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_locker_bank_cache(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_lockerbank_cache(context['manufacturerID'],
                                                                                      "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('string_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_locker_bank_cache_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_lockerbank_cache(context['manufacturerID'],
                                                                                      "valid", "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_locker_bank_cache_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_lockerbank_cache(context['manufacturerID'],
                                                                                      "invalid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_delete_locker_bank_cache_with_no_lockerBank(self, rp_logger, resource):
        """
        This test validates deletion of cache (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_invalidate_lockerbank_cache("", "valid", "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(405, status_code, res) is True

    # ------------------------------LOCKER BANK ACTIVITY COUNT--------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_activity_count(self, rp_logger, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID="", siteID="",
                                                                                        manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_activity_count_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank activity count with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID="", siteID="",
                                                                                        manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_activity_count_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank activity count with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID="", siteID="",
                                                                                        manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="invalid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # ------------------------------LOCKER BANK ACTIVITY API--------------------------------------
    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_activity_with_invalid_resource(self, rp_logger, resource):
        """
        This test validates locker bank activity count with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID="", siteID="", manufacturerID="",
                                                                              activityCode="",
                                                                              transactionType="", recipientInfo="",
                                                                              trackingID="", manufacturerLockerID="",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockerbank_activity_with_invalid_access_token(self, rp_logger, resource):
        """
        This test validates locker bank activity count with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID="", siteID="", manufacturerID="",
                                                                              activityCode="",
                                                                              transactionType="", recipientInfo="",
                                                                              trackingID="", manufacturerLockerID="",
                                                                              startDate="", token_type="invalid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    # -------------------------------------QUERY PARAMETERS for activity and activity count api-------------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_tenantID(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'], siteID="",
                                                                              manufacturerID="", activityCode="",
                                                                              transactionType="", recipientInfo="",
                                                                              trackingID="", manufacturerLockerID="",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID="", manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_siteID(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                              siteID=context["siteID"],
                                                                              manufacturerID="", activityCode="",
                                                                              transactionType="", recipientInfo="",
                                                                              trackingID="", manufacturerLockerID="",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID=context["siteID"],
                                                                                        manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_manufacturerID(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                              siteID=context["siteID"],
                                                                              manufacturerID=context["manufacturerID"],
                                                                              activityCode="", transactionType="",
                                                                              recipientInfo="", trackingID="",
                                                                              manufacturerLockerID="",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID=context["siteID"],
                                                                                        manufacturerID=context[
                                                                                            "manufacturerID"],
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_activityCode(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        activityCodes = ["deposit", "bankstatechange", "lockerstatechange", "pickup", "reservation",
                         "cancelreservation", "updatereservation", "stalemailpickup", "openlocker"]

        for activity in activityCodes:
            res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                                  siteID=context["siteID"],
                                                                                  manufacturerID=context[
                                                                                      "manufacturerID"],
                                                                                  activityCode=activity,
                                                                                  transactionType="",
                                                                                  recipientInfo="", trackingID="",
                                                                                  manufacturerLockerID="", startDate="",
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

            res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(
                tenantID=context['tenantID'], siteID=context["siteID"],
                manufacturerID=context["manufacturerID"], activityCode=activity, transactionType="",
                recipientInfo="", trackingID="", manufacturerLockerID="", startDate="",
                token_type="valid", resource_type="validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
            assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_transactionType(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        transactionTypes = ["deliver", "return", "exchange"]

        for transaction in transactionTypes:
            res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                                  siteID=context["siteID"],
                                                                                  manufacturerID=context[
                                                                                      "manufacturerID"],
                                                                                  activityCode="",
                                                                                  transactionType=transaction,
                                                                                  recipientInfo="", trackingID="",
                                                                                  manufacturerLockerID="", startDate="",
                                                                                  token_type="valid",
                                                                                  resource_type="validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

            res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                            siteID=context["siteID"],
                                                                                            manufacturerID=context["manufacturerID"],
                                                                                            activityCode="", transactionType=transaction,
                                                                                            recipientInfo="", trackingID="",
                                                                                            manufacturerLockerID="", startDate="",
                                                                                            token_type="valid", resource_type="validResource")
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
            assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_activityCode_and_transactionType(self, rp_logger, context, resource):
        """
               This test validates locker bank activity count (positive scenario)
               :return: return test status
               """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        activityCodes = ["deposit", "pickup", "reservation", "cancelreservation", "updatereservation"]
        transactionTypes = ["deliver"]

        for activity in activityCodes:
            for transaction in transactionTypes:
                res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                                      siteID=context["siteID"],
                                                                                      manufacturerID=context[
                                                                                          "manufacturerID"],
                                                                                      activityCode=activity,
                                                                                      transactionType=transaction,
                                                                                      recipientInfo="", trackingID="",
                                                                                      manufacturerLockerID="",
                                                                                      startDate="", token_type="valid",
                                                                                      resource_type="validResource")
                assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

                res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(
                    tenantID=context['tenantID'], siteID=context["siteID"],
                    manufacturerID=context["manufacturerID"], activityCode=activity,
                    transactionType=transaction, recipientInfo="",
                    trackingID="", manufacturerLockerID="", startDate="",
                    token_type="valid", resource_type="validResource")
                assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
                assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_recipientInfo(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                              siteID=context["siteID"],
                                                                              manufacturerID=context["manufacturerID"],
                                                                              activityCode="", transactionType="",
                                                                              recipientInfo="pravin", trackingID="",
                                                                              manufacturerLockerID="",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID=context["siteID"],
                                                                                        manufacturerID=context[
                                                                                            "manufacturerID"],
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="pravin",
                                                                                        trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_trackingID(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                              siteID=context["siteID"],
                                                                              manufacturerID=context["manufacturerID"],
                                                                              activityCode="", transactionType="",
                                                                              recipientInfo="",
                                                                              trackingID=context['Res_trackID'],
                                                                              manufacturerLockerID="", startDate="",
                                                                              token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID=context["siteID"],
                                                                                        manufacturerID=context[
                                                                                            "manufacturerID"],
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="",
                                                                                        trackingID=context['Res_trackID'],
                                                                                        manufacturerLockerID="",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_manufacturerLockerID(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'],
                                                                              siteID=context["siteID"],
                                                                              manufacturerID=context["manufacturerID"],
                                                                              activityCode="", transactionType="",
                                                                              recipientInfo="", trackingID="",
                                                                              manufacturerLockerID="2",
                                                                              startDate="", token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID=context["siteID"],
                                                                                        manufacturerID=context[
                                                                                            "manufacturerID"],
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="", trackingID="",
                                                                                        manufacturerLockerID="2",
                                                                                        startDate="",
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_startDate_30days(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        today = datetime.today()
        thirty_days_ago = today - timedelta(days=30)
        startDate = thirty_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        startDate = startDate + "Z"

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'], siteID="",
                                                                              manufacturerID="", activityCode="",
                                                                              transactionType="",
                                                                              recipientInfo="", trackingID="",
                                                                              manufacturerLockerID="",
                                                                              startDate=startDate, token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID="", manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="",
                                                                                        trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate=startDate,
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_startDate_7days(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        today = datetime.today()
        thirty_days_ago = today - timedelta(days=7)
        startDate = thirty_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        startDate = startDate + "Z"

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'], siteID="",
                                                                              manufacturerID="", activityCode="",
                                                                              transactionType="",
                                                                              recipientInfo="", trackingID="",
                                                                              manufacturerLockerID="",
                                                                              startDate=startDate, token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID="", manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="",
                                                                                        trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate=startDate,
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    @pytest.mark.regressioncheck_lockers
    def test_verify_activity_with_startDate_today(self, rp_logger, context, resource):
        """
        This test validates locker bank activity count (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        today = datetime.today()
        thirty_days_ago = today - timedelta(days=1)
        startDate = thirty_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        startDate = startDate + "Z"

        res, status_code = resource['activityapi'].verify_locker_activity_api(tenantID=context['tenantID'], siteID="",
                                                                              manufacturerID="", activityCode="",
                                                                              transactionType="",
                                                                              recipientInfo="", trackingID="",
                                                                              manufacturerLockerID="",
                                                                              startDate=startDate, token_type="valid",
                                                                              resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['activityapi'].verify_get_lockerbank_activity_count(tenantID=context['tenantID'],
                                                                                        siteID="", manufacturerID="",
                                                                                        activityCode="",
                                                                                        transactionType="",
                                                                                        recipientInfo="",
                                                                                        trackingID="",
                                                                                        manufacturerLockerID="",
                                                                                        startDate=startDate,
                                                                                        token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        assert not res['count'] == 0

    # ------------------------------LOCKER COUNT AVAILABLE AT BANK DETAILS---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank(context["siteID"],
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res, self.read_json_file('locker_count_at_bank_res_schema.json',
                                                                                'lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank_with_invalid_resource(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site with invalid resource (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank(context["siteID"],
                                                                                                  locker_bank, "valid",
                                                                                                  "invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank_with_invalid_access_token(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site with invalid access token (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank(context["siteID"],
                                                                                                  locker_bank,
                                                                                                  "invalid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank_with_invalid_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank(context["siteID"],
                                                                                                  "invalidBank",
                                                                                                  "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank_with_no_lockerBank(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site with no locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank(context["siteID"], "",
                                                                                                  "valid",
                                                                                                  "validResource")
        if resource['get_product_name'] != 'fedramp':
            assert self.validate_expected_and_actual_response_code_with_msg(403, status_code, res) is True
        else:
            assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    def test_verify_lockercount_available_at_lockerbank_with_invalid_siteID(self, rp_logger, context, resource):
        """
        This test validates the available lockerbank and lockerunit count at site with invalid locker bank (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        res, status_code = resource['activityapi'].verify_get_lockercount_available_at_lockerbank("invalidSiteID",
                                                                                                  locker_bank, "valid",
                                                                                                  "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True
