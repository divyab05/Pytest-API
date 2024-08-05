import inspect
import pytest

from APIObjects.lockers_services.device_token import generate_kiosk_token
from APIObjects.lockers_services.ilp_lms.ilp_monitoring_apis import ilpLMS
from APIObjects.lockers_services.ilp_service.integration_api import IntegrationAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, client_token, generate_access_token, context):
    ilplms = {'app_config': app_config,
              'ilplms': ilpLMS(app_config, client_token, generate_access_token),
              'data_reader': DataReader(app_config),
              'integration_api': IntegrationAPI(app_config, client_token)}
    context['basic_device_token'] = generate_kiosk_token(app_config).kiosk_token
    yield ilplms


@pytest.mark.usefixtures('initialize')
class TestLMSMonitoringAPI(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.configparameter = "ILP_LMS"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.ilp_lms_sp360commercial
    @pytest.mark.ilp_lms_sp360commercial_smoke
    @pytest.mark.ilp_lms_fedramp
    @pytest.mark.ilp_lms_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_live_status(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        res, status_code = resource['ilplms'].get_live_status("valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_lms_sp360commercial
    @pytest.mark.ilp_lms_sp360commercial_smoke
    @pytest.mark.ilp_lms_fedramp
    @pytest.mark.ilp_lms_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_live_status_device_token(self, resource, context):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        res, status_code = resource['ilplms'].get_live_status("valid", "validResource", 'device', context['basic_device_token'])
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.ilp_lms_sp360commercial
    @pytest.mark.ilp_lms_sp360commercial_smoke
    @pytest.mark.ilp_lms_fedramp
    @pytest.mark.ilp_lms_fedramp_smoke
    @pytest.mark.regressioncheck_lockers
    def test_get_live_status_admin(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        res, status_code = resource['ilplms'].get_live_status("valid", "validResource", 'admin')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_lms_sp360commercial
    @pytest.mark.ilp_lms_sp360commercial_smoke
    @pytest.mark.ilp_lms_fedramp
    @pytest.mark.ilp_lms_fedramp_smoke
    def test_dh_ssm_activation_client_token(self, resource):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sample_json = '{"serialNumber": "Automation"}'

        res, status_code = resource['integration_api'].post_ssm_activation_code('valid', sample_json, None)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.regressioncheck_lockers
    @pytest.mark.ilp_lms_sp360commercial
    @pytest.mark.ilp_lms_sp360commercial_smoke
    @pytest.mark.ilp_lms_fedramp
    @pytest.mark.ilp_lms_fedramp_smoke
    def test_dh_ssm_activation_device_token(self, resource, context):
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        sample_json = '{"serialNumber": "Automation"}'

        res, status_code = resource['integration_api'].post_ssm_activation_code('valid', sample_json, context['basic_device_token'])
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
