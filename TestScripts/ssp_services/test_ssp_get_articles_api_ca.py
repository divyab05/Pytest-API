import sys
import json
import pytest

from APIObjects.ssp_services.articles_api import ArticlesAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus

exe_status = ExecutionStatus()

@pytest.fixture()
def resource(app_config):
    articles = {}
    articles['app_config'] = app_config
    articles['articles_api'] = ArticlesAPI(app_config)
    articles['data_reader'] = DataReader(app_config)
    yield articles

@pytest.mark.usefixtures('initialize')
class TestSSP_GetArticlesAPICA(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, rp_logger, resource):
        exe_status.__init__()

        def cleanup():
            # data cleaning steps to be written here
            rp_logger.info('Cleaning Test Data.')

        yield
        cleanup()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "SELFSERVICEPORTAL"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.mark.self_service_portal_api_sp360canada
    @pytest.mark.self_service_portal_api_sp360canada_smoke
    @pytest.mark.regression
    def test_01_verify_article_by_id_api(self, rp_logger, resource):
        """
        This test validates if content of an article is returned for an article number
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
        article_number = str(get_row_data['Article_Number'])
        locale = str(get_row_data['Locale'])
        res, status_code_id = resource['articles_api'].getArticleById(article_number.zfill(9),locale)

        # Validate the response of Article By Id API:
        assert self.validate_expected_and_actual_response_code(200, status_code_id) is True

        # Verify the schema of Article By Id:
        with open(self.prop.get('SELFSERVICEPORTAL', 'article_by_id_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['articles_api'].verify_res_schema(res=res, expected_schema=expected_schema)

        if len(isValid) > 0:
            rp_logger.info("Schema validation not successful")
            self.Failures.append(
                "Response schema of upload file doesn't match with expected schema" + str(isValid))
        else:
            rp_logger.info("Schema validation successful")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.self_service_portal_api_sp360canada
    @pytest.mark.self_service_portal_api_sp360canada_smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ssp_services","./sp360canada/ArticlesAPITestData.xlsx","TC_02_article_list"))
    def test_02_verify_article_list_api(self, rp_logger, resource, test_data):
        """
        This test validates if article list is returned for a given product
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code_list = resource['articles_api'].getArticleList(test_data)

        # Validate the response of Article List API:
        assert self.validate_expected_and_actual_response_code(200, status_code_list) is True

        # Verify the schema of Article By Id:
        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['articles_api'].verify_res_schema(res=res, expected_schema=expected_schema)

        if len(isValid) > 0:
            rp_logger.info("Schema validation not successful")
            self.Failures.append("Response schema of upload file doesn't match with expected schema" + str(isValid))
        else:
            rp_logger.info("Schema validation successful")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.self_service_portal_api_sp360canada
    @pytest.mark.self_service_portal_api_sp360canada_smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("test_data",common_utils.read_excel_data_store("ssp_services", "./sp360canada/ArticlesAPITestData.xlsx","TC_03_article_list_mtr_product"))
    def test_03_verify_article_list_meterproducts_api(self, rp_logger, resource, test_data):
        """
         This test validates if article list is returned for a given product and plans of meter products
         """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code_list = resource['articles_api'].getArticleListWithMeter(test_data)

        # Validate the response of Article List API:
        assert self.validate_expected_and_actual_response_code(200, status_code_list) is True

        # Verify the schema of Article By Id:
        with open(self.prop.get('SELFSERVICEPORTAL', 'article_list_meter_schema')) as schema:
             expected_schema = json.load(schema)

        isValid = resource['articles_api'].verify_res_schema(res=res, expected_schema=expected_schema)

        if len(isValid) > 0:
            rp_logger.info("Schema validation not successful")
            self.Failures.append("Response schema of upload file doesn't match with expected schema" + str(isValid))
        else:
            rp_logger.info("Schema validation successful")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.self_service_portal_api_sp360canada
    @pytest.mark.self_service_portal_api_sp360canada_smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("test_data", common_utils.read_excel_data_store("ssp_services","./sp360canada/ArticlesAPITestData.xlsx","TC_04_coveo_search"))
    def test_04_verify_coveo_search_response(self, rp_logger, resource, test_data):
        """
         This test validates if coveo search results are returned
         """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code_list = resource['articles_api'].getCoveoSearchResult(test_data)

        # Validate the response of Article List API:
        assert self.validate_expected_and_actual_response_code(200, status_code_list) is True

        # Verify the schema of Article By Id:
        with open(self.prop.get('SELFSERVICEPORTAL', 'coveo_search_schema')) as schema:
            expected_schema = json.load(schema)

        isValid = resource['articles_api'].verify_res_schema(res=res, expected_schema=expected_schema)

        if len(isValid) > 0:
            rp_logger.info("Schema validation not successful")
            self.Failures.append("Response schema of upload file doesn't match with expected schema" + str(isValid))
        else:
            rp_logger.info("Schema validation successful")

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

