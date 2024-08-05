""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.shipment_transactions import ShipmentTransactionsAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    shipment_transactions_api = {}
    shipment_transactions_api['app_config'] = app_config
    shipment_transactions_api['shipment_transactions_api'] = ShipmentTransactionsAPI(app_config, generate_access_token)
    shipment_transactions_api['data_reader'] = DataReader(app_config)
    yield shipment_transactions_api


@pytest.mark.usefixtures('initialize')
class TestShipmentTransactionsAPI(common_utils):

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
        self.configparameter = "SHIPMENT_TRANSACTIONS_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_shipment_transactions_api_response(self, rp_logger, resource):
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_shipment_transactions_api_response_schema(self, rp_logger, resource):
        """
        This test validates api returning valid response schema  or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)

        # print(res)

        with open(
                'response_schema/analytics_services/shipment_transaction_api/shipment_transactions_details.json',
                'r') as s:
            expected_schema = json.loads(s.read())

        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status'] and len(res) != 0:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_shipment_transactions_api_response_with_expired_token(self, rp_logger, resource):
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_authorisation(
            startdate, enddate, et,
            divisionIds)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_shipment_transactions_api_response_with_invalid_header(self, rp_logger, resource):
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_header(startdate,
                                                                                                        enddate,
                                                                                                        'Image/jpeg',
                                                                                                        divisionIds)

        # print(res)

        if status_code != 415:
            self.Failures.append("There is a failure in api response : Expected:415 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_shipment_transactions_api_response_without_responsetype(self, rp_logger, resource):
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

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_without_response_type(startdate,
                                                                                                         enddate,
                                                                                                         divisionIds)
        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_shipment_transactions_api_response_with_groupby_value(self, rp_logger, resource):
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

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_groupby_value(startdate,
                                                                                                      enddate,
                                                                                                      groupByCriteria,
                                                                                                      divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_shipment_transactions_api_response_with_no_groupby_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_groupby_value(positive scenario)
                :return: return test status
                """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        groupByCriteria = {"groupByColumns": []}

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_groupby_value(
            startdate, enddate,
            groupByCriteria,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_shipment_transactions_api_response_with_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource[
            'shipment_transactions_api'].verify_shipments_transactions_api_response_with_orderby_value(startdate,
                                                                                                       enddate,
                                                                                                       orderByCriteria,
                                                                                                       divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_shipment_transactions_api_response_with_no_orderby_value(self, rp_logger, resource):
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
        res, status_code = resource[
            'shipment_transactions_api'].verify_shipments_transactions_api_response_with_orderby_value(
            startdate, enddate,
            orderByCriteria,
            divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_shipment_transactions_api_response_with_spendtype_value(self, rp_logger, resource):
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

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_subfilter_value(startdate,
                                                                                                        enddate,
                                                                                                        spendtype, type,
                                                                                                        divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_shipment_transactions_api_response_with_invalid_dates(self, rp_logger, resource):
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_shipment_transactions_api_response_with_no_dates(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_dates(negative scenario)
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)
        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_shipment_transactions_api_response_with_single_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_single_division_id(positive scenario)
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)
        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_shipment_transactions_api_response_with_no_division_id(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_no_division_id(positive scenario)
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
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_api_response(startdate,
                                                                                                          enddate,
                                                                                                          divisionIds)
        # print(res)

        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_shipment_transactions_api_response_without_spendtype_value(self, rp_logger, resource):
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

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_subfilter_value(startdate,
                                                                                                        enddate,
                                                                                                        spendtype, type,
                                                                                                        divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_shipment_transactions_api_response_without_subfilter_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_subfilter_valu(positive scenario)
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

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_subfilter_value(
            startdate, enddate,
            spendtype, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_shipment_transactions_api_response_without_product_id_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not without_product_id_value(positive scenario)
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
        productIds = [""]

        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transactions_api_response_with_subfilter_value(
            startdate, enddate,
            productIds, type,
            divisionIds)
        # print(res)
        # print(status_code)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_shipment_transactions_api_response_with_no_filtersGroup_value(self, rp_logger, resource):
        """
                This test validates that api returning success or not with_no_filtersGroup_value(positive scenario)
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
        res, status_code = resource[
            'shipment_transactions_api'].verify_shipments_transactions_api_response_with_orderby_value(
            startdate, enddate,
            filtersGroup,
            divisionIds)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.shipments
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_shipment_transactions_api_response_without_country_value(self, rp_logger, resource):
        """
        This test validates that api returning success or not without_country_value (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource[
            'shipment_transactions_api'].verify_shipment_transaction_api_response_without_country_value(startdate,
                                                                                                        enddate,
                                                                                                        divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.pg
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    def test_20_verify_shipment_transactions_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api is working for pagination criteria or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['shipment_transactions_api'].verify_shipment_transaction_paginated_api_response(
            startdate,
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
