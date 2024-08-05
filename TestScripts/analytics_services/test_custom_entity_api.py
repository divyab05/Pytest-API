""" This module contains all test cases."""
import json
import sys,random
import allure
import pytest

from APIObjects.analytics_services.custom_entity_api import CustomEntityAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader


exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    custom_entity_api = {}
    custom_entity_api['app_config'] = app_config
    custom_entity_api['custom_entity_api'] = CustomEntityAPI(app_config, generate_access_token)
    custom_entity_api['data_reader'] = DataReader(app_config)
    yield custom_entity_api

@pytest.mark.usefixtures('initialize')
class Test_Custom_Entity_API(common_utils):

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
        self.configparameter = "CUSTOM_ENTITY_API_MGMT"


        if  resource['data_reader'].pd_get_data(self.configparameter,request.function.__name__, "Runmode")!= "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.custom_entity
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_custom_entity_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['custom_entity_api'].verify_custom_entity_api_status_code(Enterprise)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.custom_entity
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_custom_entity_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_expired_token (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        et = "yes"
        res, status_code = resource['custom_entity_api'].verify_custom_entity_api_response_authorisation(Enterprise,et)

        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.custom_entity
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_custom_entity_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['custom_entity_api'].verify_custom_entity_api_status_code(Enterprise)

        #print(res)

        with open(
                'response_schema/analytics_services/custom_entity_api/custom_entity.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
