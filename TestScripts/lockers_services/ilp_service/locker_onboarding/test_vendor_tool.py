import sys
import pytest

from APIObjects.lockers_services.ilp_service.vendor_tool import vendorapitool
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, get_product_name):
    vendor_tool = {'app_config': app_config,
                   'vendor_tool': vendorapitool(app_config, generate_access_token),
                   'basicflow': LockerAPI(app_config, generate_access_token),
                   'data_reader': DataReader(app_config),
                   'get_product_name': get_product_name}
    yield vendor_tool


@pytest.mark.usefixtures('initialize')
class TestVendorAPI(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_locker_Onboarding"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

    # ------------------------------Get Onboarding status---------------------------------------------
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.ilp_fedramp
    @pytest.mark.ilp_sp360commercial_smoke
    @pytest.mark.ilp_fedramp_smoke
    @pytest.mark.ilp_sp360canada
    @pytest.mark.regressioncheck_lockers
    def test_locker_onbordingStatus(self, rp_logger, context,resource):
        """
        This test validates locker bank onbordingstatus details fetched (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['vendor_tool'].verify_getlocker_onboring_status(context['manufacturerHardwareID'], "valid",
                                                                                      "validResource",context)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        result = self.validate_json_schema_validations(res, self.read_json_file('get_onbording_status.json',
                                                                                'lockers_services/lockers_services'))
        if not result['status']: pytest.fail("Expected Schema is not matching with Actual Schema and error "
                                             "message {arg}".format(arg=result['error_message']))