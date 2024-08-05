""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.usage_api import UsageAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token):
    usage_api = {}
    usage_api['app_config'] = app_config
    usage_api['usage_api'] = UsageAPI(app_config, generate_access_token)
    usage_api['data_reader'] = DataReader(app_config)
    yield usage_api

@pytest.mark.usefixtures('initialize')
class TestUsageAPI(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, rp_logger, resource):
        exe_status.__init__()

        def cleanup():
            # data cleaning steps to be written here
            rp_logger.info('Cleaning Test Data.')

        yield
        cleanup()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, request,resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "USAGE_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")
        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_overall_spend_summary_usage_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not (positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Overall_Spend_Summary")
        # print(res)
        #print(len(res[0]))

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_details_usage_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not (positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_summary_usage_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not (positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Summary")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_overall_spend_summary_usage_api_response_with_expired_token(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_expired_token(negative scenario)
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
        res, status_code = resource['usage_api'].verify_usage_api_authorisation(startdate, enddate, et, divisionIds,
                                                                    api_type="Overall_Spend_Summary")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_details_usage_api_response_with_expired_token(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_expired_token(negative scenario)
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
        res, status_code = resource['usage_api'].verify_usage_api_authorisation(startdate, enddate, et, divisionIds,
                                                                    api_type="Details")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_summary_usage_api_response_with_expired_token(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_expired_token(negative scenario)
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
        res, status_code = resource['usage_api'].verify_usage_api_authorisation(startdate, enddate, et, divisionIds,
                                                                    api_type="Summary")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_overall_spend_summary_usage_api_response_schema(self, rp_logger, resource):
        """
        It verifies usage api overall Spend summary is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Overall_Spend_Summary")

        with open(
                'response_schema/analytics_services/usage_api/overall_spend_summary.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_details_usage_api_response_schema(self, rp_logger, resource):
        """
        It verifies usage api details is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Details")

        with open(
                'response_schema/analytics_services/usage_api/details.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_summary_usage_api_response_schema(self, rp_logger, resource):
        """
        It verifies usage api Summary is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type="Summary")

        with open(
                'response_schema/analytics_services/usage_api/summary.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status'] and len(res[0]) != 4:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_overall_spend_summary_usage_api_response_with_single_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_single_division_id (positive scenario)
                :return: return test status, response body
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Overall_Spend_Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.wip
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_details_usage_api_response_with_single_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_single_division_id(positive scenario)
                :return: return test status, response body
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Details")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp

    def test_12_verify_summary_usage_api_response_with_single_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_single_division_id (positive scenario)
                :return: return test status, response body
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Summary")

        #print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_overall_spend_summary_usage_api_response_with_no_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_division_id(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Overall_Spend_Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    '''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_details_usage_api_response_with_no_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_division_id(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Details")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_summary_usage_api_response_with_no_division_id(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_division_id(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_overall_spend_summary_usage_api_response_with_invalid_dates(self, rp_logger, resource):
        """
                This test validates that api returning success or not with inverse dates(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_details_usage_api_response_with_invalid_dates(self, rp_logger, resource):
        """
                This test validates that api returning success or not with inverse dates(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Details")

        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_summary_usage_api_response_with_invalid_dates(self, rp_logger, resource):
        """
                This test validates that api returning success or not with inverse dates(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                               api_type="Summary")
        # print(res)
        # print(status_code)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_overall_spend_summary_usage_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_header(startdate, enddate, 'Image/jpeg', divisionIds,
                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_details_usage_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_header(startdate, enddate, 'Image/jpeg', divisionIds,
                                                             api_type="Details")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_summary_usage_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_header(startdate, enddate, 'Image/jpeg', divisionIds,
                                                             api_type="Summary")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_overall_spend_summary_usage_api_response_with_orderby_value(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_orderby_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": ["product_id"]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_orderby_value(startdate, enddate, orderByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_summary_usage_api_response_with_orderby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not
                with_orderby_value (positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": ["product_id"]}
        res, status_code = resource['usage_api'].verify_usage_api_response_with_orderby_value(startdate, enddate, orderByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_details_usage_api_response_with_orderby_value(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_orderby_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": ["product_id"]}
        res, status_code = resource['usage_api'].verify_usage_api_response_with_orderby_value(startdate, enddate, orderByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Details")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_overall_spend_summary_usage_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["product_id"]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_details_usage_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["product_id"]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_summary_usage_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["product_id"]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_overall_spend_summary_usage_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": [""]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Overall_Spend_Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_details_usage_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": [""]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_summary_usage_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": [""]}

        res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate, groupByCriteria,
                                                                                  divisionIds,
                                                                                  api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_overall_spend_summary_usage_api_response_with_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = ["mailing"]

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_details_usage_api_response_with_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = ["mailing"]

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_summary_usage_api_response_with_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = ["mailing"]

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_overall_spend_summary_usage_api_response_with_empty_spendtype_value(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_empty_spendtype_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = []

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_details_usage_api_response_with_empty_spendtype_value(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_empty_spendtype_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = []

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.suspects
    def test_36_verify_summary_usage_api_response_with_empty_spendtype_value(self, rp_logger, resource):
        """
                This test validates subscription creation is failure or not with_empty_spendtype_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = []

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, spendtype, type,
                                                                                    divisionIds,
                                                                                    api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_overall_spend_summary_usage_api_response_with_cities_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_cities_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        cities = ['JACKSON']

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, cities, type,
                                                                                    divisionIds,
                                                                                    api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_details_usage_api_response_with_cities_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_cities_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        cities = ['JACKSON']

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, cities, type,
                                                                                    divisionIds,
                                                                                    api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_verify_summary_usage_api_response_with_cities_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_cities_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        cities = ['JACKSON']

        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_value(startdate, enddate, cities, type,
                                                                                    divisionIds,
                                                                                    api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_overall_spend_summary_usage_api_response_without_response_type(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not without_response_type(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response_without_response_type(startdate, enddate, divisionIds,

                                                                                     api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_details_usage_api_response_without_response_type(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not without_response_type(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response_without_response_type(startdate, enddate, divisionIds,
                                                                                     api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_42_summary_usage_api_response_without_response_type(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not without_response_type(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_api_response_without_response_type(startdate, enddate, divisionIds,
                                                                                     api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_overall_spend_summary_usage_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with_empty_selectQueryColumnsList(negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        selectQueryColumnsList = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_selectQueryColumnsList(startdate, enddate,
                                                                                           selectQueryColumnsList,
                                                                                           divisionIds,

                                                                                           api_type="Overall_Spend_Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_44_details_usage_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList (positive scenario)
        :return: return test status,response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        selectQueryColumnsList = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_selectQueryColumnsList(startdate, enddate,
                                                                                           selectQueryColumnsList,
                                                                                           divisionIds,
                                                                                           api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_45_summary_usage_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList(positive scenario)
        :return: return test status,response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        selectQueryColumnsList = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_selectQueryColumnsList(startdate, enddate,
                                                                                           selectQueryColumnsList,
                                                                                           divisionIds,
                                                                                           api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''#@pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    @pytest.mark.u
    def test_46_verify_details_usage_api_response_with_combination_of_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not (positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        combi = []

        def getCombinations(input, output):

            if len(input) == 0:
                if (len(output) > 0):
                    combi.append(output)
                return

            getCombinations(input[1:], output + [input[0]])

            getCombinations(input[1:], output)

        output = []
        input = ["spend_type", "division_name", "location_city"]

        getCombinations(input, output)

        for c in combi:
            groupByCriteria = {"groupByColumns": c}
            res, status_code = resource['usage_api'].verify_usage_api_response_with_groupby_value(startdate, enddate,
                                                                                      groupByCriteria,
                                                                                      divisionIds,
                                                                                      api_type="Details")
            # print(res)
            # print(status_code)

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
'''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_47_verify_overall_spend_summary_usage_api_response_with_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_spendType_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = ["mailing", "shipping"]
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_48_details_usage_api_response_with_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_spendType_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = ["mailing", "shipping"]
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_49_summary_usage_api_response_with_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_spendType_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = ["mailing", "shipping"]
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Summary")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_50_verify_overall_spend_summary_usage_api_response_with_empty_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_spendType_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_51_details_usage_api_response_with_empty_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_spendType_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.suspects
    def test_52_summary_usage_api_response_with_empty_spendType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_spendType_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Summary")
        # print(res)
        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_53_verify_overall_spend_summary_usage_api_response_with_empty_productIds_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_productIds_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_54_details_usage_api_response_with_empty_productIds_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not empty_productIds_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Details")
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_55_summary_usage_api_response_with_empty_productIds_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_productIds_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Summary")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_56_verify_overall_spend_summary_usage_api_response_with_empty_cities_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_cities_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_57_details_usage_api_response_with_empty_cities_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_cities_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_58_summary_usage_api_response_with_empty_cities_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_cities_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Summary")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_59_verify_overall_spend_summary_usage_api_response_with_empty_psdPcns_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_psdPcns_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'psdPcns'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Overall_Spend_Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_60_details_usage_api_response_with_empty_psdPcns_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_psdPcns_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'psdPcns'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_61_summary_usage_api_response_with_empty_psdPcns_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_psdPcns_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'psdPcns'
        val = []
        res, status_code = resource['usage_api'].verify_usage_api_response_with_subfilter_type_and_value(startdate, enddate, type,
                                                                                             val, divisionIds,
                                                                                             api_type="Summary")
        # print(res)
        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_62_verify_usage_export_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['usage_api'].verify_usage_export_api_response(
            startdate, enddate,
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_63_verify_usage_export_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token(negative scenario)
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
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_authorisation(startdate, enddate, et,
                                                                                divisionIds)

        if status_code_csv != 401:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:401 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 401:
            self.Failures.append(
                "There is a failure in api response of status_code_excell: Expected:401 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_64_usage_export_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['usage_api'].verify_usage_export_api_header(
            startdate, enddate,
            'Image/jpeg', divisionIds)

        # print(res)

        if status_code_csv != 415:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:415 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 415:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:415 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_65_verify_usage_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_groupByCriteria (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(startdate, enddate,
                                                                                              'groupByCriteria', {},
                                                                                              divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell: Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_66_verify_usage_export_api_response_without_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_groupByCriteria (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'groupByCriteria',
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_67_verify_usage_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_orderByCriteria (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'orderByCriteria', {},
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_68_verify_usage_export_api_response_without_orderByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_orderByCriteria (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'orderByCriteria',
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_69_verify_usage_export_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_subFilter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'subFilter', {},
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_70_verify_usage_export_api_response_without_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_subFilter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'subFilter',
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_71_verify_usage_export_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'selectQueryColumnsList', {},
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell: Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_72_verify_usage_export_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_selectQueryColumnsList (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'selectQueryColumnsList',
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_73_verify_usage_export_api_response_without_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_aggregationType (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'aggregationType',
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_74_verify_usage_export_api_response_with_empty_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'filter', {},
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_75_verify_usage_export_api_response_without_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_filter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'filter',
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_76_verify_usage_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_empty_reportColumns(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'reportColumns', {},
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_77_verify_usage_export_api_response_without_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_reportColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'reportColumns',
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_78_verify_usage_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_aggregationType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'usage_api'].verify_usage_export_api_response_with_key_and_value(
            startdate, enddate, 'aggregationType', {},
            divisionIds)

        # print(res)

        if status_code_csv != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_csv : Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 500:
            self.Failures.append(
                "There is a failure in api response of status_code_excell : Expected:500 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.pg
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_79_verify_details_usage_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api is working for pagination criteria or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['usage_api'].verify_usage_paginated_api_response(startdate,
                                                                                                      enddate,
                                                                                                      divisionIds,
                                                                                                      api_type="Details")

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        pagination = True
        if len(res) > 3 and res['noOfRecords'] != 0:
            if res['pagesAvailable'] + 1 != res['noOfRecords']:
                pagination = False

        if pagination == False:
            # pagination with one record per page
            self.Failures.append("There is a failure in pagination of api : ,Recieved  noOfRecords=" + str(
                res['noOfRecords']) + " pagesAvailable=" + str(res['pagesAvailable']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    def test_80_verify_usage_postage_spend(self, rp_logger, resource):
        """
        This test validates that api is working for pagination criteria or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res,status_code=resource['usage_api'].verify_usage_api_response(startdate,enddate,divisionIds,api_type='Details')

        #print(res)

        assert status_code==200

        _sum=0

        for i in res:
            _sum+=i['postage_spend']

        res_of_summary, status_code_of_summary = resource['usage_api'].verify_usage_api_response(startdate, enddate, divisionIds,
                                                                           api_type='Summary')

        #print(res_of_summary)
        if int(_sum)==int(res_of_summary[0]['postage_spend']):
            self.Failures.append("There is a failure in Summary API , : Expected Postage Spend  " + str(_sum) +'Received Postage Spend'+ str(res_of_summary[0]['postage_spend']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.usage
    def test_81_verify_usage_postage_spend_in_reports(self, rp_logger, resource):
        """
        This test validates that api is working for pagination criteria or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['usage_api'].verify_usage_api_reports_response(startdate, enddate, divisionIds,
                                                                           api_type='Details')

        # print(res)

        assert status_code == 200

        _sum = 0

        for i in res['pageItems']:
            _sum += i['postage_spend']

        res_of_summary, status_code_of_summary = resource['usage_api'].verify_usage_api_reports_response(startdate, enddate,
                                                                                                 divisionIds,
                                                                                                 api_type='Summary')

        # print(res_of_summary)
        if int(_sum) != int(res_of_summary[0]['postage_spend']):
            self.Failures.append("There is a failure in Summary API , : Expected Postage Spend  " + str(
                _sum) + 'Received Postage Spend' + str(res_of_summary[0]['postage_spend']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)








