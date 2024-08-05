""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.asset_details_api import AssestDetailsAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, generate_access_token):
    assest_details_api = {}
    assest_details_api['app_config'] = app_config
    assest_details_api['assest_details_api'] = AssestDetailsAPI(app_config, generate_access_token)
    assest_details_api['data_reader'] = DataReader(app_config)
    yield assest_details_api


@pytest.mark.usefixtures('initialize')
class TestAssestDetailAPI(common_utils):

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
        self.configparameter = "ASSEST_DETAILS_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_overall_summary_assest_detail_api_response(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_summary_assest_detail_api_response(self, rp_logger, resource):
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

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_overall_summary_assest_detail_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        with open(
                'response_schema/analytics_services/assest_details_api/overall_summary.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_summary_assest_detail_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not (positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        with open(
                'response_schema/analytics_services/assest_details_api/summary.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_overall_summary_assest_detail_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not  (positive scenario)
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_authorisation(startdate, enddate, et,
                                                                                                 divisionIds,
                                                                                                 api_type="Overall_Summary")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_summary_assest_detail_api_response_with_expired_token(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_authorisation(startdate, enddate, et,
                                                                                                 divisionIds,
                                                                                                 api_type="Summary")

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_overall_summary_assest_detail_api_response_with_all_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_all_division_id (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_summary_assest_detail_api_response_with_all_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_all_division_id(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_overall_summary_assest_detail_api_response_with_no_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_division_id (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_summary_assest_detail_api_response_with_no_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_division_id(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_overall_summary_assest_detail_api_response_with_invalid_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with end date is greater than start date (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_summary_assest_detail_api_response_with_invalid_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with end date is greater than start date (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_overall_summary_assest_detail_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates that api returning success or not
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_header(startdate, enddate,
                                                                                          'Image/jpeg', divisionIds,
                                                                                          api_type="Overall_Summary")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_summary_assest_detail_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates that api returning success or not
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_header(startdate, enddate,
                                                                                          'Image/jpeg', divisionIds,
                                                                                          api_type="Summary")

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.wip
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_overall_summary_assest_detail_api_response_with_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_orderby_value(
            startdate, enddate, orderByCriteria,
            divisionIds,
            api_type="Overall_Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_summary_assest_detail_api_response_with_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_orderby_value(
            startdate, enddate, orderByCriteria,
            divisionIds,
            api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_overall_summary_assest_detail_api_response_with_groupby_value(self, rp_logger, resource):
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
        groupByCriteria = {"groupByColumns": ["dim_day"]}

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_groupby_value(
            startdate, enddate, groupByCriteria,
            divisionIds,
            api_type="Overall_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_summary_assest_detail_api_response_with_groupby_value(self, rp_logger, resource):
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
        groupByCriteria = {"groupByColumns": ["product_id"]}

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_groupby_value(
            startdate, enddate, groupByCriteria,
            divisionIds,
            api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_overall_summary_assest_detail_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
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

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_groupby_value(
            startdate, enddate, groupByCriteria,
            divisionIds,
            api_type="Overall_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_summary_assest_detail_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
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

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_groupby_value(
            startdate, enddate, groupByCriteria,
            divisionIds,
            api_type="Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_overall_summary_assest_detail_api_response_with_no_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_orderby_value(
            startdate, enddate, orderByCriteria,
            divisionIds,
            api_type="Overall_Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_summary_assest_detail_api_response_with_no_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_orderby_value(
            startdate, enddate, orderByCriteria,
            divisionIds,
            api_type="Summary")

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_overall_summary_assest_detail_api_response_without_responsetype(self, rp_logger, resource):
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
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_without_response_type(
            startdate, enddate, divisionIds,
            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_verify_summary_assest_detail_api_response_without_responsetype(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        when invalid response type is passed(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_without_response_type(
            startdate, enddate, divisionIds, api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.wip
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_details_usage_api_response_with_derived_package_status_2_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_derived_package_status_2_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'derived_package_status_2'
        derived_package_status_2 = ['Created']

        res, status_code = resource['assest_details_api'].verify_assest_details_api_response_with_subfilter_value(
            startdate, enddate, derived_package_status_2, type,
            divisionIds,
            api_type="Overall_Summary")
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_overall_summary_assest_detail_api_response_with_empty_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with date is empty (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_summary_assest_detail_api_response_with_empty_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with date is empty (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Summary")
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_overall_summary_assest_detail_api_response_with_empty_payload(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with empty body json (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        body = 'empty_path'
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_payload(startdate,
                                                                                                         enddate, body,
                                                                                                         divisionIds,
                                                                                                         api_type="Overall_Summary")

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_summary_assest_detail_api_response_with_empty_payload(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        with empty body json (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        body = 'empty_path'
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_payload(startdate,
                                                                                                         enddate, body,
                                                                                                         divisionIds,
                                                                                                         api_type="Summary")
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_overall_summary_assest_detail_api_response_with_source_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_source_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        source_value = ["SSTO"]
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_source_value(startdate,
                                                                                                              enddate,
                                                                                                              source_value,
                                                                                                              divisionIds,
                                                                                                              api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_summary_assest_detail_api_response_with_source_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_source_value(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        source_value = ["SSTO"]
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_source_value(startdate,
                                                                                                              enddate,
                                                                                                              source_value,
                                                                                                              divisionIds,
                                                                                                              api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_overall_summary_assest_detail_api_response_with_empty_source_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_source_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        source_value = ["SSTO"]
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_source_value(startdate,
                                                                                                              enddate,
                                                                                                              source_value,
                                                                                                              divisionIds,
                                                                                                              api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_summary_assest_detail_api_response_with_empty_source_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_source_value(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        source_value = []
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_source_value(startdate,
                                                                                                              enddate,
                                                                                                              source_value,
                                                                                                              divisionIds,
                                                                                                              api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_overall_summary_assest_detail_api_response_with_qyeryType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_qyeryType_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        query = 'LATEST_DATA_QUERY'
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_queryType_value(
            startdate, enddate,
            query,
            divisionIds,
            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_summary_assest_detail_api_response_with_queryType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_queryType_value(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        query = 'HISTORIC_DATA_QUERY'
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_queryType_value(
            startdate, enddate,
            query,
            divisionIds,
            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_overall_summary_assest_detail_api_response_with_empty_qyeryType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_qyeryType_value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        query = ''
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_queryType_value(
            startdate,
            enddate,
            query,
            divisionIds,
            api_type="Overall_Summary")

        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_summary_assest_detail_api_response_with_empty_queryType_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_queryType_value(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        query = ''
        res, status_code = resource['assest_details_api'].verify_assest_detail_api_response_with_queryType_value(
            startdate,
            enddate,
            query,
            divisionIds,
            api_type="Summary")
        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_summary_assest_details_overall_summary_api_response_with_empty_filter_value(self, rp_logger,
                                                                                                   resource):
        """
        This test validates that api returning success or not with_empty_filter_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = {}
        res, status_code = resource['assest_details_api'].verify_assest_details_api_response_with_filter_value(filter,
                                                                                                               api_type="Overall_Summary")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_verify_summary_assest_details_summary_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter_value(negative scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = {}
        res, status_code = resource['assest_details_api'].verify_assest_details_api_response_with_filter_value(filter,
                                                                                                               api_type="Summary")
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_assest_detail_export_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['assest_details_api'].verify_assest_detail_export_api_response(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_verify_assest_detail_export_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_toke(negative scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_authorisation(startdate, enddate, et,
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_42_overall_assest_detail_export_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates that api returning success or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        status_code_csv, status_code_excell = resource['assest_details_api'].verify_assest_detail_export_api_header(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_assest_detail_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_groupByCriteria (positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(startdate, enddate,
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

    @pytest.mark.assest
    def test_44_verify_assest_detail_export_api_response_without_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_groupByCriteria (positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'groupByCriteria',
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_45_verify_assest_detail_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_46_verify_assest_detail_export_api_response_without_orderByCriteria(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_47_verify_assest_detail_export_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_empty_subFilter(positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_48_verify_assest_detail_export_api_response_without_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_subFilter (positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'subFilter',
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_49_verify_assest_detail_export_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList (positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_50_verify_assest_detail_export_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_51_verify_assest_detail_export_api_response_without_aggregationType(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_52_verify_assest_detail_export_api_response_with_empty_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_empty_filter(negative scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
            startdate, enddate, 'filter', {},
            divisionIds)

        # print(res)

        if status_code_csv != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:500 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:500 , Recieved  " + str(status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_53_verify_assest_detail_export_api_response_without_filter(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_54_verify_assest_detail_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_reportColumns(positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_55_verify_assest_detail_export_api_response_without_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_reportColumns(positive scenario)
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
            'assest_details_api'].verify_assest_detail_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.assest
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_56_verify_assest_detail_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
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
            'assest_details_api'].verify_assest_detail_export_api_response_with_key_and_value(
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
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_57_verify_overall_summary_assest_detail_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api is working for pagination or not (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['assest_details_api'].verify_assest_detail_paginated_api_response(startdate, enddate,
                                                                                            divisionIds,
                                                                                            api_type="Overall_Summary")

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        pagination = True
        if len(res)>3 and res['noOfRecords']!=0:
            if res['pagesAvailable']+1!=res['noOfRecords']:
                pagination=False

        if pagination==False:
            #pagination with one record per page
            self.Failures.append("There is a failure in pagination of api : ,Recieved  noOfRecords=" + str(res['noOfRecords']) +" pagesAvailable="+str(res['pagesAvailable']) )

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
