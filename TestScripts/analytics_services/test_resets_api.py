""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest
import jwt

from APIObjects.analytics_services.resets_api import ResetsAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, generate_access_token):
    resets_api = {}
    resets_api['app_config'] = app_config
    resets_api['resets_api'] = ResetsAPI(app_config, generate_access_token)
    resets_api['data_reader'] = DataReader(app_config)
    yield resets_api


@pytest.mark.usefixtures('initialize')
class TestResetsAPI(common_utils):

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
        self.configparameter = "RESETS_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")
        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_summary_resets_api_response(self, rp_logger, resource):
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
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_details_resets_api_response(self, rp_logger, resource):
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
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_summary_resets_api_response_schema(self, rp_logger, resource):
        """
        It verifies resets api overall Spend summary is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Summary")

        with open(
                'response_schema/analytics_services/resets_api/summary.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_details_resets_api_response_schema(self, rp_logger, resource):
        """
        It verifies resets api overall Spend summary is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Details")

        with open(
                'response_schema/analytics_services/resets_api/details.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_summary_resets_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['resets_api'].verify_resets_api_authorisation(startdate, enddate, et,
                                                                                  divisionIds,
                                                                                  api_type="Summary")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_details_resets_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['resets_api'].verify_resets_api_authorisation(startdate, enddate, et,
                                                                                  divisionIds,
                                                                                  api_type="Details")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_summary_resets_api_response_with_one_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with valid with_one_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_details_resets_api_response_with_one_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_one_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_summary_resets_api_response_without_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with valid without_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_details_resets_api_response_without_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_status_only(startdate, enddate,
                                                                                         divisionIds,
                                                                                         api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_summary_resets_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_header(startdate, enddate, 'Image/jpeg',
                                                                           divisionIds,
                                                                           api_type="Summary")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_details_resets_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_header(startdate, enddate, 'Image/jpeg',
                                                                           divisionIds,
                                                                           api_type="Details")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_summary_resets_api_response_with_orderby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_orderby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": ["product_id"]}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_orderby_value(startdate, enddate,
                                                                                                orderByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_details_resets_api_response_with_orderby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_orderby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": ["product_id"]}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_orderby_value(startdate, enddate,
                                                                                                orderByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Details")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_summary_resets_api_response_with_no_orderby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_orderby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": []}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_orderby_value(startdate, enddate,
                                                                                                orderByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_details_resets_api_response_with_no_orderby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_orderby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        orderByCriteria = {"orderByColumns": [""]}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_orderby_value(startdate, enddate,
                                                                                                orderByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Details")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_summary_resets_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["daily"]}

        res, status_code = resource['resets_api'].verify_resets_api_response_with_groupby_value(startdate, enddate,
                                                                                                groupByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_details_resets_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["daily"]}

        res, status_code = resource['resets_api'].verify_resets_api_response_with_groupby_value(startdate, enddate,
                                                                                                groupByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_summary_resets_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": []}

        res, status_code = resource['resets_api'].verify_resets_api_response_with_groupby_value(startdate, enddate,
                                                                                                groupByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_details_resets_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": []}

        res, status_code = resource['resets_api'].verify_resets_api_response_with_groupby_value(startdate, enddate,
                                                                                                groupByCriteria,
                                                                                                divisionIds,
                                                                                                api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_verify_summary_resets_api_response_without_response_type(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        when invalid response type is passed(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_without_response_type(startdate,
                                                                                                   enddate,
                                                                                                   divisionIds,
                                                                                                   api_type="Summary")

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_details_resets_api_response_without_response_type(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        when invalid response type is passed(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_without_response_type(startdate,
                                                                                                   enddate,
                                                                                                   divisionIds,
                                                                                                   api_type="Details")

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_summary_resets_api_response_with_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = ["mailing"]

        res, status_code = resource['resets_api'].verify_resets_api_response_with_subfilter_value(startdate,
                                                                                                          enddate,
                                                                                                          spendtype,
                                                                                                          type,
                                                                                                          divisionIds,
                                                                                                          api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_verify_details_resets_api_response_with_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = ["mailing"]

        res, status_code = resource['resets_api'].verify_resets_api_response_with_subfilter_value(startdate,
                                                                                                          enddate,
                                                                                                          spendtype,
                                                                                                          type,
                                                                                                          divisionIds,
                                                                                                          api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_summary_resets_api_response_without_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = [""]

        res, status_code = resource['resets_api'].verify_resets_api_response_with_subfilter_value(startdate,
                                                                                                          enddate,
                                                                                                          spendtype,
                                                                                                          type,
                                                                                                          divisionIds,
                                                                                                          api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_details_resets_api_response_without_spendtype_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_spendtype_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        spendtype = [""]

        res, status_code = resource['resets_api'].verify_resets_api_response_status_with_subfilter_value(
            startdate, enddate,
            spendtype, type,
            divisionIds,
            api_type="Details")
        # print(res)
        # print(status_code)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_summary_resets_api_response_with_invalid_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with inverse dates(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response(startdate, enddate, divisionIds,
                                                                             api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_details_resets_api_response_with_invalid_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with inverse dates(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_status_only(startdate, enddate,
                                                                                         divisionIds,
                                                                                         api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_summary_resets_api_response_with_no_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_dates(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_status_only(startdate, enddate,
                                                                                         divisionIds,
                                                                                         api_type="Summary")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_details_resets_api_response_with_no_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_dates(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_api_response_status_only(startdate, enddate,
                                                                                         divisionIds,
                                                                                         api_type="Details")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_summary_resets_api_response_with_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_country_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        country = 'US'
        res, status_code = resource['resets_api'].verify_resets_api_response_with_country_value(startdate, enddate,
                                                                                                country, divisionIds,
                                                                                                api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_details_resets_api_response_with_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_country_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        country = 'US'
        res, status_code = resource['resets_api'].verify_resets_api_response_with_country_value(startdate, enddate,
                                                                                                country, divisionIds,
                                                                                                api_type="Details")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_summary_resets_api_response_with_empty_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_country_value(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        country = ''
        res, status_code = resource['resets_api'].verify_resets_api_response_with_country_value(startdate, enddate,
                                                                                                country,
                                                                                                divisionIds,
                                                                                                api_type="Summary")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_details_resets_api_response_with_empty_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_country_value (positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        country = ''
        res, status_code = resource['resets_api'].verify_resets_api_response_with_country_value(startdate, enddate,
                                                                                                country,
                                                                                                divisionIds,
                                                                                                api_type="Details")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_summary_resets_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = {}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_filter_value(filter,
                                                                                               api_type="Summary")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_details_resets_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = {}
        res, status_code = resource['resets_api'].verify_resets_api_response_with_filter_value(filter,
                                                                                               api_type="Details")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # EXPORT

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_resets_export_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['resets_api'].verify_resets_export_api_response(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_resets_export_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token(negative scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_authorisation(startdate, enddate, et,
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_resets_export_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['resets_api'].verify_resets_export_api_header(
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


    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_resets_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_groupByCriteria (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(startdate, enddate,
                                                                               'groupByCriteria', {},
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_verify_resets_export_api_response_without_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_groupByCriteria (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
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


    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_42_verify_resets_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_orderByCriteria (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_resets_export_api_response_without_orderByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_orderByCriteria (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.wip
    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_44_verify_resets_export_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_subFilter(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
            startdate, enddate, 'subFilter', {},
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_45_verify_resets_export_api_response_without_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_subFilter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_46_verify_resets_export_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_47_verify_resets_export_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_selectQueryColumnsList (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_48_verify_resets_export_api_response_without_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_aggregationType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'aggregationType',
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_49_verify_resets_export_api_response_with_empty_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
            startdate, enddate, 'filter', {},
            divisionIds)

        # print(res)

        if status_code_csv != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:400 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:400 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_50_verify_resets_export_api_response_without_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_filter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_51_verify_resets_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_reportColumn (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_52_verify_resets_export_api_response_without_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_reportColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'reportColumns',
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

    @pytest.mark.resets
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_53_verify_resets_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_aggregationType (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource[
            'resets_api'].verify_resets_export_api_response_with_key_and_value(
            startdate, enddate, 'aggregationType', {},
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

    @pytest.mark.pg
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_54_verify_resets_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api is working well for pagination scenario (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['resets_api'].verify_resets_paginated_api_response(startdate, enddate,
                                                                                       divisionIds)

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
