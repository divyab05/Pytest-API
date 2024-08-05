import pytest
from APIObjects.sendtech_apps.device_subscription import Subscription
from APIObjects.sendtech_apps.shipping_device_token import generate_shipping_app_token
from APIObjects.sendtech_apps.stamps import DeviceStampsActions

from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(app_config,context):

    stampsActions = {
        'app_config': app_config,
        'subscription': Subscription(app_config, context['cseries_okta_token']),
        'stampsActions': DeviceStampsActions(app_config, context['cseries_okta_token'])

    }
    yield stampsActions


class TestMailingCheckRates(common_utils):

    @pytest.fixture()
    def test_verify_get_customer_context(self, resource):
        res = resource['subscription'].get_customer_context()
        # self.log.info(f'customer context response json is: {res.json()}')
        self.carrierProfileId = res.json()['carrierProfilesSummaries']['usps']['carrierProfiles'][0]['id']


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "MailingCheckratesTestData.xlsx",
                                                                "mailingCheckRate"))
    def test_verify_mailing_checkrates(self, resource,test_data,test_verify_get_customer_context):

        resp = resource['stampsActions'].post_verify_mailing_checrates(self.carrierProfileId,test_data)
        # self.log.info(f'response json is: {res.json()}')
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True


        #  --------Schema Validation------------
        # with open(r'./response_schema/cseries_services/get_accounts.json', 'r') as s:
        #     expected_schema = json.loads(s.read())

        #
        # assert_that(self.validate_response_template(res,
        #                                             expected_schema, 200))

    @pytest.mark.skip(reason="failing")
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    def test_fusiondevice_iot_event(self, resource):
        resp = resource['stampsActions'].post_verify_fusion_iot_event()
        # self.log.info(f'response json is: {res.json()}')
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "MailingCheckratesTestData.xlsx",
                                                                "stampsheetMailingRate"))
    def test_verify_mailing_stampsheet_rate(self,resource,test_data,test_verify_get_customer_context):
        resp = resource['stampsActions'].post_verify_stampsheet_mailing_rates(self.carrierProfileId,test_data)
        # self.log.info(f'response json is: {res.json()}')
        assert self.validate_expected_and_actual_response_code(200, resp['response_code']) is True








