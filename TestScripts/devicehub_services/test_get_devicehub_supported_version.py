import pytest
from hamcrest import assert_that, equal_to, ends_with

from APIObjects.devicehub_services.Get_Supported_Versions import Get_Supported_Version
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    req = Get_Supported_Version(general_config, app_config, custom_logger)
    yield req


class Test_get_devicehub_supported_versions(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    def test_get_supported_versions(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_supported_versions("valid", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Supported_version.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

        assert_that(len(resp['response_body']['supportedVersions']), equal_to(2), "Expected length 2 is not "
                                                                                  "match with the actual")
        assert_that(str(resp['response_body']['windowBuildLocation']), ends_with(".msi"),
                    "Expected file extension should be .msi not matched with actual {arg1}".format(
                        arg1=resp['response_body']['windowBuildLocation']))

        assert_that(str(resp['response_body']['macBuildLocation']), ends_with(".pkg"),
                    "Expected file extension should be .pkg not matched with actual {arg1}".format(
                        arg1=resp['response_body']['macBuildLocation']))

        assert_that(str(resp['response_body']['exeBuildLocation']), ends_with(".exe"),
                    "Expected file extension should be .exe not matched with actual {arg1}".format(
                        arg1=resp['response_body']['exeBuildLocation']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_supported_version_invalid_path(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_supported_versions("valid", generate_access_token, "invalid_path")
        assert_that(self.validate_expected_and_actual_response_code(404, resp['response_code']),
                    "Expected Status code 404 is not matched with actual {arg1}".format(arg1=resp['response_code']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_supported_version_passing_expired_token(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_supported_versions("invalid_token", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(401, resp['response_code']),
                    "Expected Status code 401 is not matched with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_fedramp_smoke
    @pytest.mark.device_hub_fedramp
    @pytest.mark.device_hub_fedramp_reg
    def test_get_supported_versions_fedramp(self, resource, generate_access_token, custom_logger):
        resp = resource.send_get_devicehub_supported_versions("valid", generate_access_token, None)

        assert_that(self.validate_expected_and_actual_response_code(200, resp['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp['response_code']))

        expected_schema = self.read_json_file('Supported_version.json', 'devicehub_services')
        res = self.validate_json_schema_validations(resp['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

        assert_that(len(resp['response_body']['supportedVersions']), equal_to(2), "Expected length 2 is not "
                                                                                  "match with the actual")
        assert_that(str(resp['response_body']['windowBuildLocation']), ends_with(".msi"),
                    "Expected file extension should be .msi not matched with actual {arg1}".format(
                        arg1=resp['response_body']['windowBuildLocation']))

        assert_that(str(resp['response_body']['exeBuildLocation']), ends_with(".exe"),
                    "Expected file extension should be .exe not matched with actual {arg1}".format(
                        arg1=resp['response_body']['exeBuildLocation']))