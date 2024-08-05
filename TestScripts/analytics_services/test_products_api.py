""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.products_api import ProductsAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    products_api = {}
    products_api['app_config'] = app_config
    products_api['products_api'] = ProductsAPI(app_config, generate_access_token)
    products_api['data_reader'] = DataReader(app_config)
    yield products_api


@pytest.mark.usefixtures('initialize')
class TestProdutsAPI(common_utils):

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
        self.configparameter = "PRODUCTS_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_products_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise= resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response(Enterprise,divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)




    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_products_api_response_schema(self, rp_logger, resource):
        """
        This test validates that api is returning valid response schema or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response(Enterprise,
                                                                                            divisionIds)

        #print(res)

        with open(
                'response_schema/analytics_services/products_api/products.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_products_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        et = "yes"
        res, status_code = resource['products_api'].verify_products_api_authorisation(Enterprise, et,
                                                                                                 divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_overall_products_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with invalid header (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_header(Enterprise,'Image/jpeg', divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_products_api_response_with_no_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_division_id(positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response(Enterprise,
                                                                                            divisionIds)
        # print(res)

        if status_code != 200:
            self.Failures.append(
                "There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_products_api_response_with_empty_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')


        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'groupByCriteria',{},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_products_api_response_without_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource['products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'groupByCriteria',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_products_api_response_with_empty_orderByCriteria_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_orderByCriteria_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'orderByCriteria', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_products_api_response_without_orderByCriteria(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_orderByCriteria(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'orderByCriteria',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_products_api_response_with_empty_aggregationType_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_aggregationType_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'aggregationType', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_products_api_response_without_aggregationType(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_aggregationType(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'aggregationType',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_products_api_response_with_empty_filter_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_filter_value(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'filter', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_products_api_response_without_filter(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_filter(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')

        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'filter',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_products_api_response_with_empty_enterpriseID(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_enterpriseID (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response(Enterprise, divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_15_verify_products_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_subFilter(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'subFilter', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_products_api_response_without_subFilter(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_subFilter(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'subFilter',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_products_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_empty_selectQueryColumnsList(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource['products_api'].verify_products_api_response_with_key_and_value(
            Enterprise, 'selectQueryColumnsList', {},
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    def test_18_verify_products_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_selectQueryColumnsList(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'selectQueryColumnsList',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    '''
    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_products_api_response_without_filtersGroup(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_filtersGroup(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'filtersGroup',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
    '''

    @pytest.mark.products
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_products_api_response_without_responseType(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_responseType(negative scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        Enterprise = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EnterpriseID')
        res, status_code = resource[
            'products_api'].verify_products_api_response_with_deleting_keys_in_payload(
            Enterprise, 'responseType',
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
