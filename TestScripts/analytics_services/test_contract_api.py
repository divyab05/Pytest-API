""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.contract_api import ContractAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    contract_api = {}
    contract_api['app_config'] = app_config
    contract_api['contract_api'] = ContractAPI(app_config, generate_access_token)
    contract_api['data_reader'] = DataReader(app_config)
    yield contract_api



@pytest.mark.usefixtures('initialize')
class TestContractAPI(common_utils):

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
        self.configparameter = "CONTRACT_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_contract_api_response(self, rp_logger, resource):
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
        res, status_code = resource['contract_api'].verify_contract_api_response(startdate, enddate, divisionIds)

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_contract_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['contract_api'].verify_contract_api_response(startdate, enddate, divisionIds)

        #print(res)

        with open(
                'response_schema/analytics_services/contract_api/get_contract.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_contract_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (negative scenario)
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
        res, status_code = resource['contract_api'].verify_contract_api_authorisation(startdate, enddate, et,
                                                                          divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_contract_api_response_with_invalid_content_type_header(self, rp_logger, resource):
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
        headerType = 'Content-Type'
        res, status_code = resource['contract_api'].verify_contract_api_header(startdate, enddate, headerType,
                                                                   'Image/jpeg',
                                                                   divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_contract_api_response_without_responsetype(self, rp_logger, resource):
        """
        This test validates that api returning success or not
        when invalid response type is passed(negative scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['contract_api'].verify_contract_api_response_without_response_type(
            startdate,
            enddate,
            divisionIds)
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_contract_api_response_with_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not (negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": ["product_id"]}

        res, status_code = resource['contract_api'].verify_contract_api_response_with_groupby_value(
            startdate, enddate,
            groupByCriteria,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_contract_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not (positive scenario)
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

        res, status_code = resource['contract_api'].verify_contract_api_response_with_groupby_value(
            startdate, enddate,
            groupByCriteria,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_contract_api_response_with_orderby_value(self, rp_logger, resource):
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
        orderByCriteria = {"orderByColumns": ["latest_psd_serial_number", "bpn", "latest_psd_model"]}
        res, status_code = resource['contract_api'].verify_contract_api_response_with_orderby_value(startdate, enddate,
                                                                                        orderByCriteria,
                                                                                        divisionIds)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_contract_api_response_with_invalid_dates_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_invalid_dates_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['contract_api'].verify_contract_api_response(
            startdate, enddate, divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_contract_api_response_with_no_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource['contract_api'].verify_contract_api_response_with_orderby_value(
            startdate, enddate,
            orderByCriteria,
            divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_contract_api_response_with_spendtype_value(self, rp_logger, resource):
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

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            spendtype, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_contract_api_response_with_no_dates_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_dates_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['contract_api'].verify_contract_api_response(
            startdate, enddate, divisionIds)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_contract_api_response_with_single_division_id_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_single_division_id_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['contract_api'].verify_contract_api_response(
            startdate, enddate, divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_contract_api_response_with_no_division_id_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_division_id_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['contract_api'].verify_contract_api_response(
            startdate, enddate, divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_contract_api_response_with_cities_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_cities_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        cities = ["Hickory"]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            cities, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_contract_api_response_with_spendtype_value(self, rp_logger, resource):
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
        spendtype = [""]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            spendtype, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_contract_api_response_without_subfilter_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_subfilter_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = ''
        spendtype = [""]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            spendtype, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_contract_api_response_with_no_filtersgroup_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_filtersgroup_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        filtersGroup = {"filtersGroup": []}
        res, status_code = resource['contract_api'].verify_contract_api_response_with_filtergroup_value(
            startdate, enddate,
            filtersGroup,
            divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_contract_api_response_with_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_country_value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        val = 'US'
        res, status_code = resource['contract_api'].verify_contract_api_response_with_filter_value(startdate, enddate, 'country',
                                                                                       val, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_contract_api_response_with_empty_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_country_value (negartive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        val = ''
        res, status_code = resource['contract_api'].verify_contract_api_response_with_filter_value(startdate, enddate, 'country',
                                                                                       val, divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_verify_contract_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_filter_value (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        filter = {}
        res, status_code = resource['contract_api'].verify_contract_api_response_with_whole_filter_value(filter)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Received  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_contract_api_response_with_selectquerycolumn_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_selectquerycolumn_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        selectquerycolumn = ["location_info", "bpn", "street1", "street2"]
        res, status_code = resource['contract_api'].verify_contract_api_response_with_selectquerycolumnlist_value(startdate,
                                                                                                      enddate,
                                                                                                      selectquerycolumn,
                                                                                                      divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_contract_api_response_with_empty_selectquerycolumn_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_selectquerycolumn_value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        selectquerycolumn = []
        res, status_code = resource['contract_api'].verify_contract_api_response_with_selectquerycolumnlist_value(startdate,
                                                                                                      enddate,
                                                                                                      selectquerycolumn,
                                                                                                      divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_verify_contract_api_response_with_empty_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {}

        res, status_code = resource['contract_api'].verify_contract_api_response_with_groupby_value(
            startdate, enddate,
            groupByCriteria,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_contract_api_response_with_empty_cities_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_cities_value (positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'cities'
        cities = []

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            cities, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_contract_api_response_with_empty_productIds_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_productIds_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        productIds = []

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            productIds, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_contract_api_response_with_empty_psdPcns_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_psdPcns_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'psdPcns'
        psdPcns = []

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            psdPcns, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_contract_api_response_with_productIds_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_productIds_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        productIds = ["1923910_1MEC", "3007604_1R0T", "3007992_1R0T", "1377729_1W00", "1384250_1W00", "1397507_1W00",
                      "0336977_4W00", "0339265_4W00", "0348623_4W00", "0349466_4W00", "0349578_4W00", "0357937_4W00",
                      "0365471_4W00", ]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            productIds, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_contract_api_response_with_spiStatus_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_spiStatus_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spiStatus'
        spiStatus = ["LEASE-BOOKED","LEASE-EVERGREEN","LEASE-TERMINATED","LEASE-EXPIRED","LEASE-PENDING","RENTAL-ACTIVE","RENTAL-DEACTIVE","RENTAL-PENDING"]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            spiStatus, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_contract_api_response_with_empty_spiStatus_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_spiStatus_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spiStatus'
        spiStatus = []

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            spiStatus, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_contract_api_response_with_contractType_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_contractType_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'contractType'
        contractType = ["lease","rental"]

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            contractType, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_contract_api_response_with_empty_contractType_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_contractType_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'contractType'
        contractType = []

        res, status_code = resource['contract_api'].verify_contract_api_response_with_contractSubFilter_value(
            startdate, enddate,
            contractType, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_contract_api_response_with_contractInputTypesEnum_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_contractInputTypesEnum_value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        val = 'SHIPTO'
        res, status_code = resource['contract_api'].verify_contract_api_response_with_filter_value(startdate, enddate, 'contractInputTypesEnum',
                                                                                       val, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_contract_api_response_with_empty_contractInputTypesEnum_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_contractInputTypesEnum_value (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        val = ''
        res, status_code = resource['contract_api'].verify_contract_api_response_with_filter_value(startdate, enddate,
                                                                                       'contractInputTypesEnum',
                                                                                       val, divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    #Exportwip
    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_contract_export_api_response(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['contract_api'].verify_contract_export_api_response(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_contract_export_api_response_with_expired_token(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_authorisation(startdate, enddate, et,
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_contract_export_api_response_with_invalid_header(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['contract_api'].verify_contract_export_api_header(
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



    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_contract_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(startdate, enddate,
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_39_verify_contract_export_api_response_without_groupByCriteria(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_40_verify_contract_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_41_verify_contract_export_api_response_without_orderByCriteria(self, rp_logger, resource):
        """
        This test validates that api returning success or not  without_orderByCriteria(positive scenario)
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
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


    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_42_verify_contract_export_api_response_with_empty_contractSubFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_contractSubFilter (positive scenario)
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
            startdate, enddate, 'contractSubFilter', {},
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_43_verify_contract_export_api_response_without_contractSubFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_contractSubFilter (negative scenario)
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'contractSubFilter',
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_44_verify_contract_export_api_response_with_empty_responseType(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_responseType (negative scenario)
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
            startdate, enddate, 'responseType', '',
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_45_verify_contract_export_api_response_without_responseType(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_responseType (negative scenario)
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
            startdate, enddate, 'responseType',
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_46_verify_contract_export_api_response_without_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_aggregationType (negative scenario)
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_47_verify_contract_export_api_response_with_empty_filter(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_48_verify_contract_export_api_response_without_filter(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_49_verify_contract_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_reportColumns (positive scenario)
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_50_verify_contract_export_api_response_without_reportColumns(self, rp_logger, resource):
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
            'contract_api'].verify_contract_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.contract
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_51_verify_contract_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not  with_empty_aggregationType(npositive scenario)
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
            'contract_api'].verify_contract_export_api_response_with_key_and_value(
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
    def test_52_verify_contract_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api is working well with pagination (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['contract_api'].verify_contract_paginated_api_response(startdate,
                                                                                                      enddate,
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
