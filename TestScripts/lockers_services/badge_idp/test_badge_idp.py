import random
import sys
import pytest

from APIObjects.lockers_services.badge_idp.badge_idp import BadgeIDP
from APIObjects.lockers_services.device_token import generate_kiosk_token
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI


@pytest.fixture()
def resource(app_config, client_token, context):
    badgeapi = {'app_config': app_config,
                'badgeService': BadgeIDP(app_config, client_token),
                'locker_api': LockerAPI(app_config, client_token),
                'data_reader': DataReader(app_config)}
    context['basic_device_token'] = generate_kiosk_token(app_config).kiosk_token
    yield badgeapi


@pytest.mark.usefixtures('initialize')
class TestBadgeApis(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_badge_service"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
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

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_create_user_badge_for_onborded_user(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_Post_add_user_badge_for_user(token_type="valid",
                                                                                        resource_type="validResource")
        context["badgeID"] = res['badgeID']
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_create_user_badge_for_onborded_user_with_invalid_access_Token(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_Post_add_user_badge_for_user(token_type="invalid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_create_user_badge_for_onborded_user_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_Post_add_user_badge_for_user(token_type="valid",
                                                                                        resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_create_user_badge_for_for_already_created_user(self, rp_logger, resource):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_Post_add_user_badge_for_user(token_type="valid",
                                                                                        resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_generate_the_samal_token(self, rp_logger, resource, context):
        """
        This test generate the sample token for specifc user badge
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_samal_user_badge(context, token_type="valid",
                                                                                resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.ilp_kiosk
    @pytest.mark.regressioncheck_lockers
    def test_kiosk_saml_token_login(self, rp_logger, resource, context):
        """
        This test generate the sample token for specifc user badge
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_samal_user_badge(context, token_type="valid",
                                                                                resource_type="validResource", kioskToken=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_generate_the_samal_token_with_invalid_access_token(self, rp_logger, resource, context):
        """
        This test verifies the error response of generate samal token API with invalid access token
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_samal_user_badge(context, token_type="invalid",
                                                                                resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_generate_the_samal_token_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test verifies the error response of generate samal token API with resource Type
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_samal_user_badge(context, token_type="valid",
                                                                                resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_badge_details_for_recently_created_user(self, rp_logger, resource, context):
        """
        This test will validate the user badge details which is recently created by post user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_user_details(token_type="valid",
                                                                            resource_type="SpecificBadge",
                                                                            context=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_user_badge_details(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_user_details(token_type="valid",
                                                                            resource_type="validResource",
                                                                            context=context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        result = self.validate_json_schema_validations(res[0], self.read_json_file('get_user_badge_resp_schema.json',
                                                                                   'lockers_services/badge_idp'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_user_badge_details_with_invalid_token_type(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_user_details(token_type="invalid",
                                                                            resource_type="validResource",
                                                                            context=context)
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_user_badge_details_with_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_get_user_details(token_type="valid",
                                                                            resource_type="invalidResource",
                                                                            context=context)
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_edit_the_existing_user_badge_with_new(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        NewbadgeID = "Badge" + str(random.randint(1, 35000))
        Newjson = '{"newBadgeID":"abcdx"}'

        res, status_code = resource['badgeService'].verify_edit_user_badge_with_new_badge_ID(Newjson=Newjson,
                                                                                             context=context,
                                                                                             token_type="valid",
                                                                                             resource_type="validResource")
        context["NewbadgeID"] = "abcdx"
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_edit_the_existing_user_badge_with_new_using_invalid_access_token(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        NewbadgeID = "Badge" + str(random.randint(1, 35000))
        Newjson = '{"newBadgeID":"abcdx"}'

        res, status_code = resource['badgeService'].verify_edit_user_badge_with_new_badge_ID(Newjson=Newjson,
                                                                                             context=context,
                                                                                             token_type="invalid",
                                                                                             resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_edit_the_existing_user_badge_with_new_using_invalid_resource(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        NewbadgeID = "Badge" + str(random.randint(1, 35000))
        Newjson = '{"newBadgeID":"abcdx"}'

        res, status_code = resource['badgeService'].verify_edit_user_badge_with_new_badge_ID(Newjson=Newjson,
                                                                                             context=context,
                                                                                             token_type="valid",
                                                                                             resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_delete_user_badge_for_onborded_user(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_delete_user_badge_details(context, token_type="valid",
                                                                                     resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_delete_user_badge_for_onborded_user_with_invalid_access_Token(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_delete_user_badge_details(context, token_type="invalid",
                                                                                     resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(401, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_delete_user_badge_for_onborded_user_with_invalid_resource_type(self, rp_logger, resource, context):
        """
        This test validates the list of user badge enabled for user
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_delete_user_badge_details(context, token_type="valid",
                                                                                     resource_type="invalidResource")
        assert self.validate_expected_and_actual_response_code_with_msg(404, status_code, res) is True

    @pytest.mark.badge_idp_sp360commercial
    @pytest.mark.badge_idp_sp360commercial_smoke
    @pytest.mark.regressioncheck_lockers
    def test_delete_already_deleted_badge(self, rp_logger, resource, context):
        """
        This test validates the already deleted badges with error response
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")
        res, status_code = resource['badgeService'].verify_delete_user_badge_details(context, token_type="valid",
                                                                                     resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(400, status_code, res) is True
