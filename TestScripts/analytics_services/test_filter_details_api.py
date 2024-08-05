""" This module contains all test cases."""
import json
import sys,random
import allure
import pytest

from APIObjects.analytics_services.filter_details import FilterDetailsAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader


exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token):
    filter_details_api = {}
    filter_details_api['app_config'] = app_config
    filter_details_api['filter_details_api'] = FilterDetailsAPI(app_config, generate_access_token)
    filter_details_api['data_reader'] = DataReader(app_config)
    yield filter_details_api


@pytest.mark.usefixtures('initialize')
class TestFilterDetailsAPI(common_utils):

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
        self.configparameter = "FILTER_DETAILS_API_MGMT"


        if  resource['data_reader'].pd_get_data(self.configparameter,request.function.__name__, "Runmode")!= "Y":
            pytest.skip("Excluded from current execution run.")
        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_filter_details_api_response(self, rp_logger, resource):
        """
        This function is validates if analytics filter details  api gets response or not (positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['filter_details_api'].verify_filter_details_api_response(filter, divisionIds,)

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        if len(res)!=0 and len(res[0]) != 12:
            self.Failures.append(
                "There is a missing parameters in usage api response : Expected::['bpn', 'cost_account_id', 'cost_account_name', 'carrier', 'clerk_name', 'enterprise_customer', 'enterprise_customer_name', 'customer_name', 'location_address', 'location_city', 'location_state', 'location_country'] , Recieved  " + ",".join(
                    list(res[0].keys())))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_filter_details_api_response_schema(self, rp_logger, resource):
        """
        It verifies filter details api is returning valid response schema.(positive scenario)
        :return: return test response body
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['filter_details_api'].verify_filter_details_api_response(filter, divisionIds )

        with open(
                'response_schema/analytics_services/filter_details_api/filter_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_filter_details_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that filter details api is returning valid response or not with_expired_token (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['filter_details_api'].verify_filter_details_api_authorisation(filter,et,divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_filter_details_api_response_with_one_division_id(self, rp_logger, resource):
        """
        This function is validates if analytics filter details  api gets response or not
        with_one_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['filter_details_api'].verify_filter_details_api_response(filter, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_filter_details_api_response_with_no_division_id(self, rp_logger, resource):
        """
        This function is validates if analytics filter details  api gets response or not
         with_no_division_id(positive scenario)
        :return: return test status
                 response data
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = ""
        res, status_code = resource['filter_details_api'].verify_filter_details_api_response(filter, divisionIds )

        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
        
    @pytest.mark.filter
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_filtr_details_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not
        with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Filter')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['filter_details_api'].verify_filter_details_api_header(filter,'Image/jpeg',divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



