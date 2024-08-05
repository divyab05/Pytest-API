""" This module contains all test cases."""
import json
import sys,random
import allure
import pytest

from APIObjects.analytics_services.favourite_report_api import FavouriteReportAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.data_reader_utility import DataReader


exe_status = ExecutionStatus()



@pytest.fixture()
def resource(app_config, generate_access_token):
    favourite_report_api = {}
    favourite_report_api['app_config'] = app_config
    favourite_report_api['favourite_report_api'] = FavouriteReportAPI(app_config, generate_access_token)
    favourite_report_api['data_reader'] = DataReader(app_config)
    yield favourite_report_api


@pytest.mark.usefixtures('initialize')
class TestFavouriteReportAPI(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, rp_logger,resource):
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
        self.configparameter = "FAVOURITE_REPORT_API_MGMT"


        if  resource['data_reader'].pd_get_data(self.configparameter,request.function.__name__, "Runmode")!= "Y":
            pytest.skip("Excluded from current execution run.")


        self.Failures = []

    @pytest.fixture()
    def setUp(self):
        self.Failures = []

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_01_favourite_report_get_api_response(self, rp_logger,resource):
        """
        This test validates that api returning success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")


        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))



        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.suspects
    def test_02_favourite_report_get_api_response_schema(self, rp_logger,resource):
        """
        This test validates response schema is matching or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()

        #print(res)

        with open(
                'response_schema/analytics_services/favourite_report_api/get_favourite_reports.json',
                'r') as s:
            expected_schema = json.loads(s.read())
        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status'] and len(res)!=0:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp

    def test_03_favourite_report_create_api_response_with_existing_report_name(self, rp_logger,resource):
        """
        This test report creation is success or not
        with already existing report  (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name='qwe'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res,status_code= resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)

        #print(res)

        if status_code != 409:
            self.Failures.append("There is a failure in api response : Expected:409 , Received  " + str(status_code))

        if status_code == 200:
            resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_04_favourite_report_get_api_response_with_header(self, rp_logger,resource):
        """
        This test validates favourite get report  is success or not  (positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        headerType="Content-Type"
        headerVal="application/json"
        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response_with_header(headerType,headerVal)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:2000 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_05_favourite_report_get_api_response_with_expired_token(self, rp_logger,resource):
        """
        This test validates favourite get report  is success or not
        with expired access token(negative scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        et = "yes"

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_authorization(et)

        # print(res)

        if status_code != 401:
            self.Failures.append(
                "There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_06_favourite_report_get_api_response_with_other_userid(self, rp_logger,resource):
        """
        This test validates favourite get report  is success or not
        with other userId (positive scenario)
        :return: return test status

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        headerType = "X-UserId"
        headerVal = "123456"
        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response_with_header(headerType,
                                                                                                     headerVal)

        #print(res)

        if status_code != 401:
            self.Failures.append(
                "There is a failure in api response : Expected 401 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

#---------------------------TC's for create report--------------------------

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_07_favourite_report_create_api_response(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))
        
        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        
        flag=False
        for i in res:
            if i['name']==name:
                flag=True
        if flag==False:
            self.Failures.append("There is a failure in api response : Report not created ")
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    def test_08_favourite_report_create_api_response_without_report_name(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        without report name (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = ''

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        
        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)




        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_09_favourite_report_create_api_response_with_empty_templateInfo(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with empty templateInfo (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'

        value={}

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_templateinfo_and_val(name,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_10_favourite_report_create_api_response_with_groupByHierarchy(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with groupByHierarchy value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'groupByHierarchy'
        value = {"field1":"location"}


        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_11_favourite_report_create_api_response_with_empty_groupByHierarchy(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty groupByHierarchy value(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'groupByHierarchy'
        value = {}

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_12_favourite_report_create_api_response_with_aggregatedColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with aggregatedColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'aggregatedColumns'
        value = ["name","postage_spend","piece_count","avg_spend","postage_saving","last_transaction_date"]




        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_13_favourite_report_create_api_response_with_empty_aggregatedColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with aggregatedColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'aggregatedColumns'
        value=[]

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_14_favourite_report_create_api_response_with_columnNames(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with columnNames value (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'

        property = 'columnNames'
        value={"name":"Location","postage_spend":"Total Amount","piece_count":"Piece Count"}



        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_15_favourite_report_create_api_response_with_empty_columnNames(self, rp_logger,resource):
        """
        This test validates that api returning success or not
        empty with columnNames (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'columnNames'
        value ={}



        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(name,property,value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_16_favourite_report_create_api_response_with_context(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with context (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'context'
        value = "sending|summary|{\"summary\":\"/usage?isShippingUsageRequired=false&locale=en_US\",\"records\":\"/usage/paginated?isShippingUsageRequired=false&locale=en_US\",\"favouriteReportCreate\":\"/favourite/report/template\"}|mailing,shipping|true|true|false|[{\"label\":\"mailing\",\"value\":\"mailing\"},{\"label\":\"shipping\",\"value\":\"shipping\"}]|\"/usage/custom/export?locale=en_US&fileFormat=CSV&exportType=CUSTOM_REPORT\"|\"/usage/custom/export?locale=en_US&fileFormat=XLSX&exportType=CUSTOM_REPORT\""

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_17_favourite_report_create_api_response_with_empty_context(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with context (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'context'
        value = ""

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_18_favourite_report_create_api_response_with_defaultColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with defaultColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'defaultColumns'
        value = "bpn"

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_19_favourite_report_create_api_response_with_empty_defaultColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with defaultColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'defaultColumns'
        value = ""

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_20_favourite_report_create_api_response_with_groupingColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with groupingColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'groupingColumns'
        value = ["location_city","location_state"]

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")


        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_21_favourite_report_create_api_response_with_empty_groupingColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with groupingColumns (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'groupingColumns'
        value = []

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_22_favourite_report_create_api_response_with_sortingColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with_sortingColumns(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'sortingColumns'
        value = ["piece_count","postage_spend","postage_saving","avg_spend","last_transaction_date","base_rate","fee_amount","surcharges_amount","mailing_piece_count","shipping_piece_count","transaction_end_time"]

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_23_favourite_report_create_api_response_with_empty_sortingColumns(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with_sortingColumns(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'sortingColumns'
        value = []

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_24_favourite_report_create_api_response_with_columnOrder(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        with_columnOrder(positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'columnOrder'
        value = ["bpn"]

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.wip
    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_25_favourite_report_create_api_response_with_empty_columnOrder(self, rp_logger,resource):
        """
        This test validates favourite report creation is success or not
        empty with_columnOrder (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        property = 'columnOrder'
        value = []

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response_with_property_and_val(
            name, property, value)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        flag = False
        for i in res:
            if i.get('name') and i['name'] == name:
                flag = True
        if flag == False:
            self.Failures.append("There is a failure in api response : Report not created ")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


#---------------------------TC's for delete report--------------------------

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp

    def test_26_favourite_report_delete_api_response(self, rp_logger,resource):
        """
        This test validates favourite report delete is success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'


        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code=resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_27_favourite_report_delete_api_response_for_deleted_report(self, rp_logger,resource):
        """
        This test validates favourite report delete is success or not
        with already deleted report (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'

        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_28_favourite_report_delete_api_response_with_empty_name(self, rp_logger,resource):
        """
        This test validates favourite report delete is success or not
        with empty name (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = ''

        #resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_29_favourite_report_delete_api_response_with_no_userId_parameter(self, rp_logger,resource):
        """
        This test validates favourite report delete is success or not
        no userId value (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted='userId'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_delete_api_response_with_deleting_keys(name,valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_30_favourite_report_delete_api_response_with_no_name_parameter(self, rp_logger,resource):
        """
        This test validates favourite report delete is success or not
        no name parameter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted = 'name'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_delete_api_response_with_deleting_keys(name,
                                                                                                               valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



#-------------------------------favourite report getdetails--------------------------------------

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp

    def test_31_favourite_report_getdetails_api_response(self, rp_logger,resource):
        """
        This test validates favourite report getdetails is success or not  (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_getdetails_api_response(name)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        #print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        with open(
                'response_schema/analytics_services/favourite_report_api/getdetails_api.json',
                'r') as s:
            expected_schema = json.loads(s.read())
        result = self.validate_json_schema_validations(actual_response=res, expected_response=expected_schema)

        if not result['status']:
            self.Failures.append("Expected Schema is not matching with Actual Schema and error"
                                 "message {arg}".format(arg=result['error_message']))




        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_32_favourite_report_getdetails_api_response_with_no_name_parameter(self, rp_logger,resource):
        """
        This test validates favourite report getdetails is success or not
        no_name_parameter (negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted = 'name'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_getdetails_api_response_with_deleting_keys(name,
                                                                                                               valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_33_favourite_report_getdetails_api_response_with_no_userid_parameter(self, rp_logger,resource):
        """
        This test validates favourite report getdetails is success or not
        no user id parameter(negative scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted = 'userId'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_getdetails_api_response_with_deleting_keys(name,
                                                                                                                   valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



#--------------------------------Update Last Run Api-------------------------------------------------

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_34_favourite_report_updateLastRun_api_response(self, rp_logger,resource):
        """
        This test validates favourite report updatelastrun is success or not
        (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_update_last_run_api_response(name)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.sendpro_analytics_api_snowflake_sp360commercial
    @pytest.mark.sendpro_analytics_api_snowflake_fedramp
    def test_35_favourite_report_updateLastRun_api_response_with_no_name_parameter(self, rp_logger,resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_name_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted = 'name'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_update_last_run_api_response_with_deleting_keys(name,
                                                                                                                   valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 200:
            self.Failures.append("There is a failure in api response : Expected:200 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    @pytest.mark.ignore
    def test_36_favourite_report_updateLastRun_api_response_with_no_userid_parameter(self, rp_logger,resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_userid_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        name = 'creating_from_script'
        valTobeDeleted = 'userId'
        resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        res, status_code = resource['favourite_report_api'].verify_favourite_report_getdetails_api_response_with_deleting_keys(name,
                                                                                                                   valTobeDeleted)
        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        # print(res)

        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)



#------------------------------------------Update favourite report api-----------------------------------------
    @pytest.mark.favourite
    def test_37_favourite_report_update_api_response(self, rp_logger,resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_userid_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        name = 'creating_from_script'

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        assert status_code==200

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        for i in res:
            if i['name'] == 'creating_from_script':
                report = i

        res, status_code_update = resource['favourite_report_api'].verify_favourite_report_update_api_response_with_key_and_value('groupByHierarchy','division',report)
        assert status_code_update==200




        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()


        for i in  res:

            if i['name']=='creating_from_script':
                field = i['templateInfo']['groupByHierarchy']['field1']
                if field!= 'division':
                    self.Failures.append(
                        "There is a failure in api response :  Favourite update report is is not working")



        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)


        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    def test_37_favourite_report_update_api_response(self, rp_logger, resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_userid_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        name = 'creating_from_script'

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        assert status_code == 200

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        for i in res:
            if i['name'] == 'creating_from_script':
                report = i

        res, status_code_update = resource[
            'favourite_report_api'].verify_favourite_report_update_api_response_with_key_and_value('groupByHierarchy',
                                                                                                   'division', report)
        assert status_code_update == 200

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()

        for i in res:

            if i['name'] == 'creating_from_script':
                field = i['templateInfo']['groupByHierarchy']['field1']
                if field != 'division':
                    self.Failures.append(
                        "There is a failure in api response :  Favourite update report is is not working")

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    def test_38_favourite_report_update_api_response_with_expired_token(self, rp_logger, resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_userid_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        name = 'creating_from_script'

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        assert status_code == 200

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        for i in res:
            if i['name'] == 'creating_from_script':
                report = i

        res, status_code = resource['favourite_report_api'].verify_favourite_report_update_api_authorization('groupByHierarchy',
                                                                                                   'division', report,'yes')
        if status_code != 401:
            self.Failures.append("There is a failure in api response : Expected:401 , Recieved  " + str(status_code))

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.favourite
    def test_39_favourite_report_update_api_response_with_invalid_header(self, rp_logger, resource):
        """
        This test validates favourite report updatelastrun is success or not
        no_userid_parameter (positive scenario)
        :return: return test status, response body

        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        name = 'creating_from_script'

        res, status_code = resource['favourite_report_api'].verify_favourite_report_creation_api_response(name)
        assert status_code == 200

        res, status_code = resource['favourite_report_api'].verify_favourite_report_get_api_response()
        for i in res:
            if i['name'] == 'creating_from_script':
                report = i

        res, status_code = resource['favourite_report_api'].verify_favourite_report_update_api_response_with_header(
            'groupByHierarchy',
            'division',report, 'Image/jpeg',)
        if status_code != 500:
            self.Failures.append("There is a failure in api response : Expected:500 , Recieved  " + str(status_code))

        resource['favourite_report_api'].verify_favourite_report_delete_api_response(name)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)