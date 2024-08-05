""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.notification_api import NotificationAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    notification_api = {}
    notification_api['app_config'] = app_config
    notification_api['notification_api'] = NotificationAPI(app_config, generate_access_token)
    notification_api['data_reader'] = DataReader(app_config)
    yield notification_api


@pytest.mark.usefixtures('initialize')
class TestNotificationAPI(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, rp_logger, resource):
        exe_status.__init__()

        def cleanup():
            # data cleaning steps to be written here
            rp_logger.info('Cleaning Test Data.')

        yield
        cleanup()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, request, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "NOTIFICATION_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    # 8th test case and some more test cases are checking for failed schema


    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_01_verify_notification_search_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        resoponse_of_overall_search, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        if resoponse_of_overall_search == {}:
            res, status_code = resource[
                'notification_api'].function_for_crate_one_report()
        # Above Code runs when their is not any report on user, it create one report so that other test cases won't fail




        res, status_code = resource['notification_api'].verify_notification_search_api_response()

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_notification_search_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['notification_api'].verify_notification_search_api_response()

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_notification_search_api_response_with_pageindex(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not  with_pageindex(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'pageIndex', 4)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_notification_search_api_response_schema_without_pageindex(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_pageindex(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'pageIndex')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_notification_search_api_response_schema_with_pageSize(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_pageSize (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'pageSize', 10)

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_notification_search_api_response_schema_without_pageSize(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_pageSize (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'pageSize')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_notification_search_api_response_schema_with_orgId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'orgId', 'SP360US')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_notification_search_api_response_schema_without_orgId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'orgId')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_notification_search_api_response_schema_with_ownerDesc(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'ownerDesc', 'SP360USowner')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_notification_search_api_response_schema_without_ownerDesc(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'ownerDesc')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_notification_search_api_response_schema_with_ownerId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'ownerId', 'SP360USownerId')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_notification_search_api_response_schema_without_ownerId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'ownerId')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_notification_search_api_response_schema_with_objectType(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'objectType', 'ReportNotify')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_notification_search_api_response_schema_without_objectType(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'objectType')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_notification_search_api_response_schema_with_enabled_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_enabled_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'enabled', True)

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_notification_search_api_response_schema_without_enabled_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_enabled_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'enabled')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_notification_search_api_response_schema_with_isCompleted_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_isCompleted_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'isCompleted', True)

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_notification_search_api_response_schema_without_isCompleted_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_isCompleted_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'enabled')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_notification_search_api_response_schema_with_empty_sorts_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_sorts_value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'sorts', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_notification_search_api_response_schema_without_sorts_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_sorts_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'sorts')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_verify_notification_search_api_response_schema_with_empty_subscriptionID_value(self, rp_logger,
                                                                                               resource):
        """
        This test validates that api is returning valid response or not with_empty_subscriptionID_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'subscriptionID', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_notification_search_api_response_schema_without_subscriptionID_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_subscriptionID_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'subscriptionID')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_notification_search_api_response_schema_with_empty_event_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_event_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'event', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_verify_notification_search_api_response_schema_without_event_value(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_event_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'event')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_notification_search_api_response_schema_with_empty_subscriptionfields_value(self, rp_logger,
                                                                                                   resource):
        """
        This test validates that api is returning valid response or not with_empty_subscriptionfields_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'subscriptionfields', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_notification_search_api_response_schema_without_subscriptionfields_value(self, rp_logger,
                                                                                                resource):
        """
        This test validates that api is returning valid response or not without_subscriptionfields_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_deleting_keys_in_payload(
            'subscriptionfields')

        assert status_code == 200

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    
    '''
    '''
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_notification_search_api_response_schema_with_empty_orgId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'orgId', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if result['status']:
            self.Failures.append("Expected Schema is matching with Actual Schema and result"
                                 " {arg}".format(arg=result))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_notification_search_api_response_schema_with_empty_ownerDesc(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'ownerDesc', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_notification_search_api_response_schema_with_empty_ownerId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'ownerId', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_notification_search_api_response_schema_with_empty_objectType(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_search_api_response_with_custom_keys_and_values_in_payload(
            'objectType', '')

        assert status_code == 200
        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/search_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_notification_search_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['notification_api'].verify_notification_search_api_header('Image/jpeg')

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_notification_search_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['notification_api'].verify_notification_search_api_authorisation(et)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # -------------------------------------------scherep/subscription for creating and deleting report----------------------------------------
    '''
    '''
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_notification_subscription_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['notification_api'].verify_notification_subscription_api_response()
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)

        resource['notification_api'].verify_notification_delete_api_response(notSubID)
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_notification_subscription_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token(negative scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"
        res, status_code = resource['notification_api'].verify_notification_subscription_api_authorisation(et)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_notification_subscription_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['notification_api'].verify_notification_subscription_api_header('Image/jpeg')

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_notification_subscription_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['notification_api'].verify_notification_subscription_api_response()

        # print(res)

        with open(
                'response_schema/analytics_services/notification_api/subscription_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)

        resource['notification_api'].verify_notification_delete_api_response(notSubID)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_notification_subscription_api_response_schema_with_empty_orgId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'orgId', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is  created with empty orgId")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_notification_subscription_api_response_schema_without_orgId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'orgId')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without parameter orgId")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_verify_notification_subscription_api_response_schema_with_empty_ownerDesc(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'ownerDesc', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is  created with empty ownerDesc")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_notification_subscription_api_response_schema_without_ownerDesc(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'ownerDesc')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is  created without parameter ownerDesc")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_verify_notification_subscription_api_response_schema_with_empty_ownerId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'ownerId', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty ownerId")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_42_verify_notification_subscription_api_response_schema_without_ownerId(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'ownerId')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without parameter ownerId")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_notification_subscription_api_response_schema_with_empty_barcode(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_barcode (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'barcode', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty barcode")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_44_verify_notification_subscription_api_response_schema_without_barcode(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_barcode (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'barcode')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is  created without barcode")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_45_verify_notification_subscription_api_response_schema_with_empty_enabled(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_enabled (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'enabled', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created with empty enabled")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_46_verify_notification_subscription_api_response_schema_without_enabled(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_enabled (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'enabled')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created without enabled")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_47_verify_notification_subscription_api_response_schema_with_empty_events(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_events (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'events', [])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty events")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_48_verify_notification_subscription_api_response_schema_without_events(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_events (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'events')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without events")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_49_verify_notification_subscription_api_response_schema_with_ScheduledReportEvent_events_only(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_ScheduledReportEvent_events_only (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'events', ['ScheduledReportEvent'])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created with only ScheduledReportEvent value")
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_50_verify_notification_subscription_api_response_schema_with_EndSubscriptionEvent_events_only(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_EndSubscriptionEvent_events_only (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'events', ['EndSubscriptionEvent'])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created with only EndSubscriptionEvent value")
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_51_verify_notification_subscription_api_response_schema_without_isCompleted(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_isCompleted (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'isCompleted')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created without isCompleted")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_52_verify_notification_subscription_api_response_schema_without_kvp(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_kvp (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'kvp')

        assert status_code == 500

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without kvp")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_53_verify_notification_subscription_api_response_schema_with_empty_objectType(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_empty_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'objectType', [])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty objectType")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_54_verify_notification_subscription_api_response_schema_without_objectType(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'objectType')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without objectType")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_55_verify_notification_subscription_api_response_schema_with_empty_terminalEvents(self, rp_logger,
                                                                                               resource):
        """
        This test validates that api is returning valid response or not with_empty_terminalEvents (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'terminalEvents', [])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created with empty terminalEvents")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_56_verify_notification_subscription_api_response_schema_without_terminalEvents(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_terminalEvents (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'terminalEvents')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            self.Failures.append("Scheduled report is not created without terminalEvents")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_57_verify_notification_subscription_api_response_schema_with_empty_channels(self, rp_logger,
                                                                                         resource):
        """
        This test validates that api is returning valid response or not with_empty_channels (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'channels', [])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty channels")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_58_verify_notification_subscription_api_response_schema_without_channels(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not without_channels (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'channels')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created without channels")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # jfjgnjsgkdfjgslkjgklsgklsg
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_59_verify_notification_subscription_api_response_schema_with_empty_channels_type_value(self, rp_logger,
                                                                                                    resource):
        """
        This test validates that api is returning valid response or not with_empty_channels_type_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload_for_channels(
            'type', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is created with empty channels type value")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_60_verify_notification_subscription_api_response_schema_without_channels_type_value(self, rp_logger,
                                                                                                 resource):
        """
        This test validates that api is returning valid response or not without_channels_type_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload_for_channels(
            'type')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created without channels type value")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_61_verify_notification_subscription_api_response_schema_with_empty_channels_address_value(self, rp_logger,
                                                                                                       resource):
        """
        This test validates that api is returning valid response or not with_empty_channels_address_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload_for_channels(
            'address', '')

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with empty channels address value")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_62_verify_notification_subscription_api_response_schema_without_channels_address_value(self, rp_logger,
                                                                                                    resource):
        """
        This test validates that api is returning valid response or not without_channels_address_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload_for_channels(
            'address')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created without channels address value")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_63_verify_notification_subscription_api_response_schema_with_empty_subscriptionFields(self, rp_logger,
                                                                                                   resource):
        """
        This test validates that api is returning valid response or not with_empty_subscriptionFields (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_custom_keys_and_values_in_payload(
            'subscriptionFields', [])

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with empty subscriptionFields")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_64_verify_notification_subscription_api_response_schema_without_subscriptionFields(self, rp_logger,
                                                                                                resource):
        """
        This test validates that api is returning valid response or not without_subscriptionFields (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response_with_deleting_keys_in_payload(
            'subscriptionFields')

        assert status_code == 200

        # print(res)
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        # print(res)
        if (notSubID != ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created without subscriptionFields")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_65_verify_notification_delete_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token(negative scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"
        res, status_code = resource['notification_api'].verify_notification_delete_api_authorisation(et, 12)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_66_verify_notification_update_api_response_schema_with_updating_reportName(self, rp_logger,
                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_update_api_response_with_custom_keys_and_values_in_kvp_key_payload(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID)

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with updated report name")
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_67_verify_notification_update_api_response_schema_with_updating_fileFormat(self, rp_logger,
                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_fileFormat (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        UPDATED = False

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_update_api_response_with_custom_keys_and_values_in_kvp_key_payload(
            'fileFormat', 'CSV', notSubID)

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script' and i['kvp']['fileFormat'] == 'CSV':
                notSubIDupdate = i['sid']
                UPDATED = True

        # print(res)
        if (notSubIDupdate == '' or UPDATED == False):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with updated file format")
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_68_verify_notification_update_api_response_schema_with_updating_filterType_and_filterBy(self, rp_logger,
                                                                                                     resource):
        """
        This test validates that api is returning valid response or not with_updating_filterType_and_filterBy (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        UPDATED = False
        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_update_api_response_with_custom_keys_and_values_in_kvp_with_2_keys(
            'filterType', 'cityState', 'filterBy', 'City / State, 4 Divisions, All Location', notSubID)

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script' and i['kvp']['filterType'] == 'cityState' and \
                    i['kvp']['filterBy'] == 'City / State, 4 Divisions, All Location':
                notSubIDupdate = i['sid']
                UPDATED=True

        # print(res)
        if (notSubIDupdate == '' or UPDATED==False):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with updated filterType")
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    
    
    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_69_verify_notification_update_api_response_schema_with_updating_email_address(self, rp_logger,
                                                                                                     resource):
        """
        This test validates that api is returning valid response or not with_updating_email_address (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        UPDATED = False
        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        template={"type": "Email","address": "shreysah.sahu@pb.com"}

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_custom_keys_and_values_in_payload_for_channels(
            template, notSubID)

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                for j in i['channels']:
                    j['type']=template['type']
                    j['address']=template['address']
                    notSubIDupdate = i['sid']
                    UPDATED = True

        # print(res)
        if (notSubIDupdate == '' or UPDATED == False):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not created with updated email")
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_70_verify_notification_update_api_response_schema_with_updating_reportName_with_expired_token(self, rp_logger,
                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_expired_token (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_update_api_authorisation(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID,et)



        # print(res)
        if (status_code_update == 401):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Notification update api accessable with expired token")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_71_verify_notification_update_api_response_schema_with_updating_reportName_with_invalid_header(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_invalid_header (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_update_api_header(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'Image/jpeg')

        # print(res)
        if (status_code_update == 500):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Notification update api accessable with expired token")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)





    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_72_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_orgId(self, rp_logger,
                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID,'orgId','')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty orgId")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_73_verify_notification_update_api_response_schema_with_updating_reportName_without_orgId(self,
                                                                                                         rp_logger,
                                                                                                         resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_orgId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'orgId')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource['notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without OrgId")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)






    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_74_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_ownerId(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'ownerId', '')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty ownerId")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_75_verify_notification_update_api_response_schema_with_updating_reportName_without_ownerId(self,
                                                                                                        rp_logger,
                                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_ownerId (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'ownerId')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without ownerId")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)





    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_76_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_ownerDesc(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'ownerDesc', '')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty ownerDesc")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_77_verify_notification_update_api_response_schema_with_updating_reportName_without_ownerDesc(self,
                                                                                                        rp_logger,
                                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_ownerDesc (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'ownerDesc')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without ownerDesc")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_78_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_barcode(self,
                                                                                                             rp_logger,
                                                                                                             resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_barcode (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'barcode', '')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty barcode")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_79_verify_notification_update_api_response_schema_with_updating_reportName_without_barcode(self,
                                                                                                          rp_logger,
                                                                                                          resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_barcode (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'barcode')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without barcode")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)





    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_80_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_events(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_events (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'events', [])

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty events")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_81_verify_notification_update_api_response_schema_with_updating_reportName_without_events(self,
                                                                                                        rp_logger,
                                                                                                        resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_events(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'events')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without events")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_82_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_kvp(self,
                                                                                                          rp_logger,
                                                                                                          resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_kvp (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'kvp', {})

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()

        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        if status_code_update != 500:
            self.Failures.append("Scheduled report is updated without kvp")
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_83_verify_notification_update_api_response_schema_with_updating_reportName_without_kvp(self,
                                                                                                       rp_logger,
                                                                                                       resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_kvp (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'kvp')

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()

        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        if status_code_update != 500:
            self.Failures.append("Scheduled report is updated without kvp")
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_84_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_channels(self,
                                                                                                          rp_logger,
                                                                                                          resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_channels (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'channels', [])

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty channels")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_85_verify_notification_update_api_response_schema_with_updating_reportName_without_channels(self,
                                                                                                       rp_logger,
                                                                                                       resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_channels (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'channels')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without channels")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)





    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_86_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_objectType(self,
                                                                                                            rp_logger,
                                                                                                            resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'objectType', [])

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty objectType")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_87_verify_notification_update_api_response_schema_with_updating_reportName_without_objectType(self,
                                                                                                         rp_logger,
                                                                                                         resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_objectType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'objectType')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without objectType")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)








    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_88_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_subscriptionFields(self,
                                                                                                              rp_logger,
                                                                                                              resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_subscriptionFields (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'subscriptionFields', [])

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated with empty subscriptionFields")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_89_verify_notification_update_api_response_schema_with_updating_reportName_without_subscriptionFields(self,
                                                                                                           rp_logger,
                                                                                                           resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_subscriptionFields (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'subscriptionFields')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        else:
            self.Failures.append("Scheduled report is updated without subscriptionFields")
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)




    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_90_verify_notification_update_api_response_schema_with_updating_reportName_with_empty_terminalEvents(
            self,
            rp_logger,
            resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_with_empty_terminalEvents (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_passing_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'terminalEvents', [])

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not updated with empty terminalEvents")

        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.notification
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_91_verify_notification_update_api_response_schema_with_updating_reportName_without_terminalEvents(self,
                                                                                                                   rp_logger,
                                                                                                                   resource):
        """
        This test validates that api is returning valid response or not with_updating_reportName_without_terminalEvents (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        resoponse_of_overall_search, status_code = resource['notification_api'].verify_notification_search_api_response()
        if resoponse_of_overall_search=={}:
            res,status_code=resource[
                'notification_api'].function_for_crate_one_report()
        # Above Code runs when their is not any report on user, it create one report so that other test cases won't fail

        res, status_code = resource[
            'notification_api'].verify_notification_subscription_api_response()

        assert status_code == 200
        # print(res)

        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()

        notSubID = ''
        for i in resoponse_of_search['data']:
            if i['kvp']['reportName'] == 'Report_From_Automation_Script':
                notSubID = i['sid']

        assert notSubID != ''

        res_update, status_code_update = resource[
            'notification_api'].verify_notification_subscription_update_api_response_with_deleting_keys_in_payload_and_custom_keys_and_values_in_kvp_key(
            'reportName', 'Updated_Report_From_Automation_Script', notSubID, 'terminalEvents')

        assert status_code_update == 200

        resoponse_of_search_update, status_code = resource[
            'notification_api'].verify_notification_search_api_response()
        notSubIDupdate = ''
        for i in resoponse_of_search_update['data']:
            if i['kvp']['reportName'] == 'Updated_Report_From_Automation_Script':
                notSubIDupdate = i['sid']

        # print(res)
        if (notSubIDupdate == ''):
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            self.Failures.append("Scheduled report is not updated without terminalEvents")

        else:
            resource['notification_api'].verify_notification_delete_api_response(notSubID)
            resource['notification_api'].verify_notification_delete_api_response(notSubIDupdate)


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)




    #Delete All Reports
    @pytest.mark.deleteschrep
    def test_92_test_case_for_deleting_scheduled_report(self,rp_logger,resource):


        """
        This test case is made for deleting report from perticular user,
        just have to change the subscriptionfields key's value in the notification search payload
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        lst=[]
        resoponse_of_search, status_code = resource['notification_api'].verify_notification_search_api_response()
        for schrep in resoponse_of_search['data']:
            notSubID=schrep['sid']
            #lst.append(schrep['sid'])
            lst.append(schrep['kvp']['reportName'])
            resource['notification_api'].verify_notification_delete_api_response(notSubID)

        for i in lst:
            print(i)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    
    '''