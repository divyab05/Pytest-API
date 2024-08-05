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


class TestSubCostAccount(common_utils):

    @pytest.fixture
    def getEnterpriseIDFromSubscriptionAPI(self, resource):
        res = resource['costAccount'].get_enterprise_subscription_details()
        # self.log.info(f'customer context response json is: {res.json()}')
        self.enterpriseID = res.json()[0]['enterpriseID']
        self.subID = res.json()[0]['subID']
        print("enterpriseID ", self.enterpriseID)
        print("subscriptioID ", self.subID)

    @pytest.fixture()
    def getParentCostAccountID(self, resource, custom_logger):
        resp = resource['costAccount'].searchCostAccount(True)
        # print("cost account get detils response body",resp['response_body'])
        if  resp['response_code'] == 200:
            self.parentCostAccountID=resp['response_body']['content'][0]['id']
            print("parentCostAccID",self.parentCostAccountID)


    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.order(1)
    def test_create_sub_costAccount(self,resource, custom_logger,getEnterpriseIDFromSubscriptionAPI,getParentCostAccountID):
        resp = resource['costAccount'].createSubCostAccount( self.enterpriseID, self.subID,self.parentCostAccountID,costAccountStatus="Active")
        assert resp['response_code'] == 200

    @pytest.mark.sending_legacy_service_sp360commercial_reg
    @pytest.mark.order(2)
    def test_get_sub_costaccount(self,resource,getParentCostAccountID):
        resp = resource['costAccount'].getSubCostAccount(self.parentCostAccountID)
        assert resp['response_code'] == 200







