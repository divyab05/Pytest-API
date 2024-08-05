import pytest

from APIObjects.sendtech_apps.device_cost_account import CostAccount
from FrameworkUtilities.common_utils import common_utils


@pytest.fixture()
def resource(app_config,context):

    costAccount = {
        'app_config': app_config,
        'costAccount': CostAccount(app_config, context['cseries_okta_token'])

    }
    yield costAccount


class TestCostAccount(common_utils):

    @pytest.fixture()
    def getEnterpriseIDFromSubscriptionAPI(self, resource):
        res = resource['costAccount'].get_enterprise_subscription_details()
        # self.log.info(f'customer context response json is: {res.json()}')
        self.enterpriseID = res.json()[0]['enterpriseID']
        self.subID = res.json()[0]['subID']
        print("enterpriseID ",self.enterpriseID)
        print("subscriptionID ", self.subID)


    @pytest.mark.sending_legacy_service_sp360commercial
    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.parametrize("test_data",
                             common_utils.read_excel_data_store("sendtechapps_services",
                                                                "CostAccountTestData.xlsx",
                                                                "costAccount"))
    def test_create_costaccount(self, resource, custom_logger,test_data,getEnterpriseIDFromSubscriptionAPI):
        resp = resource['costAccount'].createCostAccount(test_data,self.enterpriseID,self.subID)
        print(resp['response_body'])
        assert resp['response_code'] == 200







