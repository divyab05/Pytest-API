""" This module contains all test cases."""
import json
import sys, random
import allure
import pytest

from APIObjects.analytics_services.supplies_api import SuppliesAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader

exe_status = ExecutionStatus()




@pytest.fixture()
def resource(app_config, generate_access_token):
    supplies_api = {}
    supplies_api['app_config'] = app_config
    supplies_api['supplies_api'] = SuppliesAPI(app_config, generate_access_token)
    supplies_api['data_reader'] = DataReader(app_config)
    yield supplies_api


@pytest.mark.usefixtures('initialize')
class TestSuppliesAPI(common_utils):

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
        self.configparameter = "SUPPLIES_API_MGMT"

        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_verify_supplies_api_response(self, rp_logger, resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['supplies_api'].verify_supplies_api_response(startdate, enddate, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_02_verify_supplies_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates supplies api details is success or not with_expired_token  (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        et = "bearer yes"

        res, status_code = resource['supplies_api'].verify_supplies_api_authorization(startdate, enddate, et,
                                                                                      divisionIds)

        # print(res)

        if status_code != 403:
            self.Failures.append(
                "There is a failure in api response : Expected:403 , Recieved  " + str(status_code))

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_03_verify_supplies_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates supplies api details is success or not
        with invalid header value(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_header(startdate, enddate,
                                                                                             'Image/jpeg', divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append(
                "There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_verify_supplies_api_response_with_empty_division_id(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty division id(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['supplies_api'].verify_supplies_api_response(startdate, enddate, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_verify_supplies_api_response_with_empty_dates(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty dates (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['supplies_api'].verify_supplies_api_response(startdate, enddate, divisionIds)

        # print(res)

        if status_code != 400:
            self.Failures.append("There is a failure in api response : Expected:400 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_verify_supplies_api_response_with_inverse_dates(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with inverse dates (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['supplies_api'].verify_supplies_api_response(startdate, enddate, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_verify_supplies_api_response_with_groupByColumns(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with group by value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'groupByColumns'
        val = ["sales_document", "sales_document_item"]

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_groupByCriteria(startdate,
                                                                                                      enddate, type,
                                                                                                      val, divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_08_verify_supplies_api_response_with_empty_groupByColumns(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty group by columns value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'groupByColumns'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_groupByCriteria(startdate,
                                                                                                      enddate, type,
                                                                                                      val,
                                                                                                      divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_verify_supplies_api_response_with_orderByColumns(self, rp_logger, resource):
        """
        This test validates supplies api details is success or not
        with order by value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'orderByColumns'
        val = ["sales_document"]

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_orderByCriteria(startdate,
                                                                                                      enddate, type,
                                                                                                      val,
                                                                                                      divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_verify_supplies_api_response_with_empty_orderByColumns(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty order by value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'orderByColumns'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_orderByCriteria(startdate,
                                                                                                      enddate, type,
                                                                                                      val,
                                                                                                      divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_verify_supplies_api_response_with_empty_subfilter_spendType(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        empty spendtype value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_subFilter(startdate, enddate,
                                                                                                type, val,
                                                                                                divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_verify_supplies_api_response_with_empty_subfilter_productIds(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty product id value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_subFilter(startdate, enddate,
                                                                                                type, val,
                                                                                                divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_verify_supplies_api_response_with_empty_subfilter_cities(self, rp_logger, resource):
        """
        This test validates supplies api details is success or not
        with cities values (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'spendType'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_subFilter(startdate, enddate,
                                                                                                type, val,
                                                                                                divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_verify_supplies_api_response_with_empty_subfilter_psdPcns(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with psdpcns value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'productIds'
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_subFilter(startdate, enddate,
                                                                                                type, val,
                                                                                                divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_verify_supplies_api_response_with_country_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with country value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = 'country'
        val = 'US'

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_Filter(startdate, enddate, type,
                                                                                             val,
                                                                                             divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_verify_supplies_api_response_with_empty_country_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty country value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        type = ''
        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_Filter(startdate, enddate, type,
                                                                                             val,
                                                                                             divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_verify_supplies_api_response_with_empty_filtergroup_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty filter group value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        val = {}

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_Filtergroup_value(startdate,
                                                                                                        enddate, val,
                                                                                                        divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_verify_supplies_api_response_with_selectQueryColumnsList_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with select query column list value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        val = ["product_quantity", "adjusted_net_value"]

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_selectQueryColumnsList_value(
            startdate, enddate, val,
            divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_verify_supplies_api_response_with_empty_selectQueryColumnsList_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty select query column list value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        val = []

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_selectQueryColumnsList_value(
            startdate,
            enddate, val,
            divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_verify_supplies_api_response_with_responseType_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with response type value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')

        val = 'DETAILS'

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_responseType_value(startdate,
                                                                                                         enddate, val,
                                                                                                         divisionIds)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_verify_supplies_api_response_with_empty_responseType_value(self, rp_logger, resource):
        """
        This test validates supplies api details  is success or not
        with empty response type value (negative scenario)
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

        res, status_code = resource['supplies_api'].verify_supplies_api_response_with_responseType_value(startdate,
                                                                                                         enddate, val,
                                                                                                         divisionIds)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # Export
    '''
    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_verify_supplies_export_api_response(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['supplies_api'].verify_supplies_export_api_response(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_verify_supplies_export_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates that api is returning valid response or not with_expired_token(positive scenario)
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
            'supplies_api'].verify_supplies_export_api_authorisation(startdate, enddate, et,
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_supplies_export_api_response_with_invalid_header(self, rp_logger, resource):
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
        status_code_csv, status_code_excell = resource['supplies_api'].verify_supplies_export_api_header(
            startdate, enddate,
            'Image/jpeg', divisionIds)

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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_verify_supplies_export_api_response_with_empty_groupByCriteria(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(startdate, enddate,
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_26_verify_supplies_export_api_response_without_groupByCriteria(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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


    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_27_verify_supplies_export_api_response_with_empty_orderByCriteria(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_28_verify_supplies_export_api_response_without_orderByCriteria(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_29_verify_supplies_export_api_response_with_empty_subFilter(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_subFilter (positive scenario)
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_30_verify_supplies_export_api_response_without_subFilter(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_31_verify_supplies_export_api_response_with_empty_selectQueryColumnsList(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
            startdate, enddate, 'selectQueryColumnsList', {},
            divisionIds)

        # print(res)

        if status_code_csv != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:400 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 400:
            self.Failures.append(
                "There is a failure in api response of status_code_excell: Expected:400 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_32_verify_supplies_export_api_response_without_selectQueryColumnsList(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_33_verify_supplies_export_api_response_without_aggregationType(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_verify_supplies_export_api_response_with_empty_filter(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
            startdate, enddate, 'filter', {},
            divisionIds)

        # print(res)

        if status_code_csv != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:200 , Recieved  " + str(
                    status_code_csv))

        if status_code_excell != 200:
            self.Failures.append(
                "There is a failure in api response of status_code_csv: Expected:200 , Recieved  " + str(
                    status_code_excell))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_verify_supplies_export_api_response_without_filter(self, rp_logger, resource):
        """
        This test validates that api returning success or not response_without_filter (negative scenario)
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_36_verify_supplies_export_api_response_with_empty_reportColumns(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_37_verify_supplies_export_api_response_without_reportColumns(self, rp_logger, resource):
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
            'supplies_api'].verify_supplies_export_api_response_by_deleting_key_in_payload(
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

    @pytest.mark.supplies
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_38_verify_supplies_export_api_response_with_empty_aggregationType(self, rp_logger, resource):
        """
        This test validates that api returning success or not with_empty_aggregationType (negative scenario)
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
            'supplies_api'].verify_supplies_export_api_response_with_key_and_value(
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
    def test_39_verify_supplies_paginated_api_response(self, rp_logger, resource):
        """
        This test validates that api working for pagination criteria or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        startdate = resource['data_reader'].get_data(self.configparameter, test_name, 'StartDate')
        enddate = resource['data_reader'].get_data(self.configparameter, test_name, 'EndDate')
        strdivIds = resource['data_reader'].get_data(self.configparameter, test_name, 'DivisionIds')
        divisionIds = strdivIds.split(',')
        res, status_code = resource['supplies_api'].verify_supplies_paginated_api_response(startdate,
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

    '''