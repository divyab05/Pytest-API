import pytest

from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token


class TestLogin:

    @pytest.mark.order(1)
    @pytest.mark.sending_legacy_service_sp360commercial_debug
    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360global_debug
    @pytest.mark.sending_legacy_service_sp360global
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.sendpro_anywhere_ui_p_series
    def test_verifyLogin(self,app_config,get_env, get_username, get_password,custom_logger,context):
        obj=generate_shipping_app_token(app_config)
        okta_token=obj.generate_cseries_access_token(get_env, get_username, get_password,custom_logger)
        # print("okta_token",okta_token)
        context['cseries_okta_token']=okta_token