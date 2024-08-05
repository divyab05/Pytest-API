""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.account_balance_api import AccountBalanceAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, generate_access_token):
    account_balance_api = {}
    account_balance_api['app_config'] = app_config
    account_balance_api['account_balance_api'] = AccountBalanceAPI(app_config, generate_access_token)
    account_balance_api['data_reader'] = DataReader(app_config)
    yield account_balance_api


@pytest.mark.usefixtures('initialize')
class TestAccountBalanceAPI(common_utils):

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
        self.configparameter = "ACCOUNT_BALANCE_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_account_balance_api_response(self, rp_logger, resource):
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
        res, status_code = resource['account_balance_api'].verify_account_balance_api_response(startdate, enddate,
                                                                                            divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_account_balance_api_response_schema(self, rp_logger, resource):
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
        res, status_code = resource['account_balance_api'].verify_account_balance_api_response(startdate, enddate,
                                                                                            divisionIds)

        #print(res)

        with open(
                'response_schema/analytics_services/account_balance_api/account_balance.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_account_balance_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not  (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "yes"
        res, status_code = resource['account_balance_api'].verify_account_balance_api_authorisation(startdate, enddate, et,
                                                                                                 divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_overall_account_balance_api_response_with_invalid_header(self, rp_logger, resource):
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
        res, status_code = resource['account_balance_api'].verify_account_balance_api_header(startdate, enddate,
                                                                                          'Image/jpeg', divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_account_balance_api_response_with_no_division_id(self, rp_logger, resource):
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

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response(startdate, enddate,
                                                                                            divisionIds)
        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_account_balance_api_response_with_inverse_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with end date is greater than start date (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['account_balance_api'].verify_account_balance_api_response(startdate, enddate,
                                                                                            divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_account_balance_api_response_with_empty_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty group by value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')


        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'groupByCriteria',{},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_account_balance_api_response_without_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_groupby_value (negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'groupByCriteria',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_account_balance_api_response_with_empty_orderByCriteria_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty orderByCriteria value (positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'orderByCriteria', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_account_balance_api_response_without_orderByCriteria(self, rp_logger, resource):
        """
                This test validates that api returning success or not without orderByCriteria (positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'orderByCriteria',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_account_balance_api_response_with_empty_aggregationType_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty aggregationType value (negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'aggregationType', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_account_balance_api_response_without_aggregationType(self, rp_logger, resource):
        """
                This test validates that api returning success or not without aggregationType(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'aggregationType',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_account_balance_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty filter value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'filter', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_account_balance_api_response_without_filter(self, rp_logger, resource):
        """
                This test validates that api returning success or not without filter(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'filter',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_account_balance_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty subFilter(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'subFilter', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_account_balance_api_response_without_subFilter(self, rp_logger, resource):
        """
                This test validates that api returning success or not without subFilter(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'subFilter',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_account_balance_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
                This test validates that api returning success or not with empty selectQueryColumnsList(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'selectQueryColumnsList', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_account_balance_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
        """
                This test validates that api returning success or not without selectQueryColumnsList(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'selectQueryColumnsList',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_account_balance_api_response_with_zero_batchSize(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_zero_batchSize(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value(
            startdate, enddate, 'batchSize', 0,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_account_balance_api_response_without_batchSize(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_batchSize(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'batchSize',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_verify_account_balance_api_response_without_filtersGroup(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_filtersGroup(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'filtersGroup',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_account_balance_api_response_without_responseType(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_responseType(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_keys_in_payload(
            startdate, enddate, 'responseType',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_account_balance_api_response_with_empty_subFilter_accountTypes(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_subFilter_accountTypes(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['account_balance_api'].verify_account_balance_api_response_with_key_and_value_in_subfilter(
            startdate, enddate, 'accountTypes', [],
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_verify_account_balance_api_response_without_subFilter_accountTypes(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_subFilter_accountTypes(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_deleting_key_in_subfilter(
            startdate, enddate, 'accountTypes',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_account_balance_api_response_with_subFilter_accountTypes_Trusted_account(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_subFilter_accountTypes_Trusted_account(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_key_and_value_in_subfilter(
            startdate, enddate, 'accountTypes', ["TR"],
            divisionIds)
        # print(res)
        # print(status_code)
        CheckAccountType=True
        if(res.get('pageItems')==True and len(res['pageItems'])!=0):
            for i in res['pageItems']:
                if i['account_type']!='TR':
                    CheckAccountType=False



        if CheckAccountType == False:
            self.Failures.append("There is a failure in api response : Subfilter for account type not working  ")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_account_balance_api_response_with_subFilter_accountTypes_Reserved_account(self, rp_logger,
                                                                                                resource):
        """
                This test validates that api returning success or not with_subFilter_accountTypes_Reserved_account(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource[
            'account_balance_api'].verify_account_balance_api_response_with_key_and_value_in_subfilter(
            startdate, enddate, 'accountTypes', ["RA"],
            divisionIds)
        # print(res)
        # print(status_code)
        CheckBalanceAvailable = True
        if (res.get('pageItems') and len(res['pageItems']) != 0):
            for i in res['pageItems']:
                if i['account_type']!='RA':
                    CheckBalanceAvailable = False

        if CheckBalanceAvailable == False:
            self.Failures.append("There is a failure in api response : Subfilter for account type RA not working")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    
    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_account_balance_export_api_response(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['account_balance_api'].verify_account_balance_export_api_response(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_account_balance_export_api_response_with_expired_token(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_authorisation(startdate, enddate, et,
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_account_balance_export_api_response_with_invalid_header(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['account_balance_api'].verify_account_balance_export_api_header(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_account_balance_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_groupByCriteria(negative scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(startdate, enddate,
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_account_balance_export_api_response_without_groupByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_groupByCriteria(negative scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_account_balance_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_account_balance_export_api_response_without_orderByCriteria(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_account_balance_export_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_subFilter (positive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_account_balance_export_api_response_without_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_subFilter (positive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_account_balance_export_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectQueryColumnsList(negative scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
            startdate, enddate, 'selectQueryColumnsList', [],
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_account_balance_export_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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




    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_account_balance_export_api_response_without_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_aggregationType (positive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_verify_account_balance_export_api_response_with_empty_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter (negetive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_account_balance_export_api_response_without_filter(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_verify_account_balance_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_reportColumns (positive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
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

    @pytest.mark.account_balance
    def test_42_verify_account_balance_export_api_response_without_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not  without_reportColumns(positive scenario)
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
            'account_balance_api'].verify_account_balance_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.account_balance
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_account_balance_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
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
            'account_balance_api'].verify_account_balance_export_api_response_with_key_and_value(
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

    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_44_verify_account_balance_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that pagination works or not for api(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['account_balance_api'].verify_account_balance_paginated_api_response(startdate,
                                                                                                      enddate,
                                                                                                      divisionIds)

        # print(res)

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
