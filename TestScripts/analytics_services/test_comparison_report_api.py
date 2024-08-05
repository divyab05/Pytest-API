""" This module contains all test cases."""
import json
import sys, random
import time

import allure
import pytest

from APIObjects.analytics_services.comparison_report_api import ComparisonReportAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, generate_access_token):
    comparison_report_api = {}
    comparison_report_api['app_config'] = app_config
    comparison_report_api['comparison_report_api'] = ComparisonReportAPI(app_config, generate_access_token)
    comparison_report_api['data_reader'] = DataReader(app_config)
    yield comparison_report_api


@pytest.mark.usefixtures('initialize')
class TestComparisonReportAPI(common_utils):

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
        self.configparameter = "COMPARISON_REPORT_API_MGMT"

        if resource['data_reader'].get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_01_verify_comparison_report_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        if type(res)!=str:
            self.Failures.append("There is a failure in api, response type is not string")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_02_verify_comparison_report_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api returning success or not for response schema (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        #print(res)


        if len(res)<1:
            self.Failures.append("There is a failure in api, response is empty")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_03_verify_comparison_report_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_expired_token(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_authorisation(et)

        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_04_verify_comparison_report_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_invalid_header (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_header('Image/jpeg')

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_05_verify_comparison_report_getstatus_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        # print(res)
        res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_response(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_06_verify_comparison_report_getstatus_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api returning desired response schema (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        # print(res)
        res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_response(res)

        expected_responses=['Report_id not correct','Done','Started']

        if str(res) in expected_responses:
            self.Failures.append("There is a failure in api response schema, Recieved  " + str(res))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_07_verify_comparison_report_getStatus_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_expired_token(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()
        res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_authorisation(et,res)

        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_08_verify_comparison_report_generatePresignedUrl_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        # print(res)
        res, status_code = resource['comparison_report_api'].verify_comparison_report_generatePresignedUrl_api_response(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_09_verify_comparison_report_generatePresignedUrl_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api returning desired response schema or not (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()

        # print(res)
        res, status_code = resource['comparison_report_api'].verify_comparison_report_generatePresignedUrl_api_response(res)

        if len(res)<1:
            self.Failures.append("There is a failure in api response schema, Recieved  " + str(res))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_10_verify_comparison_report_generatePresignedUrl_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_expired_token(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()
        res, status_code = resource['comparison_report_api'].verify_comparison_report_generatePresignedUrl_api_authorisation(et,
                                                                                                                  res)

        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_11_verify_comparison_report_getstatus_api_response_with_invalid_reportID(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_invalid_reportID (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        reportID='123'

        # print(res)
        res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_response(reportID)

        expected_responses = ['"Report_id not correct"']
        if str(res) not in expected_responses:
            self.Failures.append("There is a failure in api response schema Expected:Report_id not correct, Recieved  " + str(res))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_12_verify_comparison_report_getstatus_api_response_schema_with_valid_report_id(self, rp_logger, resource):
        """
        test validates that api returning desired response schema  (positive scenario)
        :return: return test status, response body
    
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()
        reportID=res
        reportID=reportID[1:len(reportID)-1]



        # print(res)
        result=False
        for seconds in range(10):
            res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_response(reportID)

            if res=='"Started"':
                result=True
                break
            time.sleep(3)

        if result==False:
            self.Failures.append("There is a failure in api response schema, Expected:Started, Recieved  " + str(res))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.comparison
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_13_verify_comparison_report_getstatus_api_response_schema_for_status_Done(self, rp_logger, resource):
        """
        test description
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['comparison_report_api'].verify_comparison_report_api_response()
        reportID = res
        reportID = reportID[1:len(reportID) - 1]

        # print(res)
        result = False
        for seconds in range(20):
            res, status_code = resource['comparison_report_api'].verify_comparison_report_getStatus_api_response(
                reportID)

            if res == '"Done"':
                result = True
                break
            time.sleep(3)

        if result == False:
            self.Failures.append("There is a failure in api response schema, Expected:Done, Recieved  " + str(res))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''