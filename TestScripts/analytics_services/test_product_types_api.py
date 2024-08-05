'''
This module contains all test cases.
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.product_types_api import ProductTypesAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    product_types_api = {}
    product_types_api['app_config'] = app_config
    product_types_api['product_types_api'] = ProductTypesAPI(app_config, generate_access_token)
    product_types_api['data_reader'] = DataReader(app_config)
    yield product_types_api


@pytest.mark.usefixtures('initialize')
class TestProductTypesAPI(common_utils):

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
        self.configparameter = "PRODUCT_TYPES_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.product_types
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_product_types_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['product_types_api'].verify_product_types_api_response(divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.product_types
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_product_types_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['product_types_api'].verify_product_types_api_authorisation(et,divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.product_types
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_overall_product_types_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['product_types_api'].verify_product_types_api_header('Image/jpeg', divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.product_types
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_product_types_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['product_types_api'].verify_product_types_api_response(divisionIds)

        # print(res)

        with open(
                'response_schema/analytics_services/product_types_api/product_types.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.product_types
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_product_types_api_response_with_no_divisions(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_divisions (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['product_types_api'].verify_product_types_api_response(divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
'''