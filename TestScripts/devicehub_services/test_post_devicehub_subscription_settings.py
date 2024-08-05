import pytest
from hamcrest import assert_that, equal_to
from APIObjects.devicehub_services.Get_Subscription_settings import Get_Subscription_settings
from APIObjects.devicehub_services.Post_Subscription_settings import Post_Subscription_settings
from FrameworkUtilities.common_utils import common_utils
from body_jsons.devicehub_services.post_subscription_settings_body import post_subscription_settings_payload


@pytest.fixture()
def resource(general_config, app_config, custom_logger):
    subs_obj = {"post_obj": Post_Subscription_settings(general_config, app_config, custom_logger),
                "get_obj": Get_Subscription_settings(general_config, app_config, custom_logger)
                }

    yield subs_obj


class Test_post_devicehub_subscription_settings(common_utils):

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    def test_post_devicehub_subs_settings_to_true(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("valid", generate_access_token, None,
                                                                                 auto_update_flg=True,
                                                                                 error_condition=False)

        assert_that(self.validate_expected_and_actual_response_code(200, resp_post['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp_post['response_code']))

        assert_that(resp_post['response_body']['response'],
                    equal_to("DeviceHub auto-update settings saved successfully"))

        resp_get = resource["get_obj"].send_get_devicehub_subscription_settings("valid", generate_access_token, None)

        assert_that(str(resp_get['response_body']['automaticUpdatesDisabled']), equal_to("True"))

        assert_that(resp_get['response_body']['subscriptionId'],
                    equal_to(post_subscription_settings_payload["subscriptionId"]))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial
    @pytest.mark.device_hub_sp360commercial_reg
    def test_post_devicehub_subs_settings_to_false(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("valid", generate_access_token, None,
                                                                                 auto_update_flg=False,
                                                                                 error_condition=False)

        assert_that(self.validate_expected_and_actual_response_code(200, resp_post['response_code']),
                    "Expected Status code 200 is not match with actual {arg1}".format(arg1=resp_post['response_code']))

        assert_that(resp_post['response_body']['response'],
                    equal_to("DeviceHub auto-update settings saved successfully"))

        resp_get = resource["get_obj"].send_get_devicehub_subscription_settings("valid", generate_access_token, None)

        assert_that(str(resp_get['response_body']['automaticUpdatesDisabled']), equal_to("False"))

        assert_that(resp_get['response_body']['subscriptionId'],
                    equal_to(post_subscription_settings_payload["subscriptionId"]))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    def test_error_post_devicehub_subs_settings(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("valid", generate_access_token, None,
                                                                                 auto_update_flg=False,
                                                                                 error_condition=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp_post['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp_post['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp_post['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    def test_error_post_devicehub_subs_settings_with_blank_flag(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("valid", generate_access_token, None,
                                                                                 auto_update_flg=None,
                                                                                 error_condition=True)

        assert_that(self.validate_expected_and_actual_response_code(400, resp_post['response_code']),
                    "Expected Status code 400 is not match with actual {arg1}".format(arg1=resp_post['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp_post['response_body'], expected_schema)

        assert_that(res['status'], "Expected Schema is not matching with Actual Schema and error message {arg}".format(
            arg=res['error_message']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    def test_error_post_devicehub_subs_settings_with_invalid_path(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("valid", generate_access_token,
                                                                                 "invalid_path",
                                                                                 auto_update_flg=False,
                                                                                 error_condition=False)

        assert_that(self.validate_expected_and_actual_response_code(404, resp_post['response_code']),
                    "Expected Status code 404 is not match with actual {arg1}".format(
                        arg1=resp_post['response_code']))

    @pytest.mark.device_hub_sp360commercial_smoke
    @pytest.mark.device_hub_sp360commercial_reg
    @pytest.mark.device_hub_sp360commercial
    def test_error_post_devicehub_subs_settings_with_expired_token(self, resource, generate_access_token):
        resp_post = resource["post_obj"].send_post_subscription_settings_request("invalid_token", generate_access_token,
                                                                                 None, auto_update_flg=False,
                                                                                 error_condition=False)

        assert_that(self.validate_expected_and_actual_response_code(401, resp_post['response_code']),
                    "Expected Status code 401 is not match with actual {arg1}".format(
                        arg1=resp_post['response_code']))

        expected_schema = self.read_json_file('Error_Schema.json', 'ecommerce_services')
        res = self.validate_json_schema_validations(resp_post['response_body'], expected_schema)

        assert_that(res['status'],
                    "Expected Schema is not matching with Actual Schema and error message {arg}".format(
                        arg=res['error_message']))
