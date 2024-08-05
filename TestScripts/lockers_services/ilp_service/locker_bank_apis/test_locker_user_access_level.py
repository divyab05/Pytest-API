import sys
import pytest
from hamcrest import assert_that

from APIObjects.lockers_services.ilp_service.lockers_user_access import LockerUserAccessLevel
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, get_product_name):
    lockerbankapi = {'app_config': app_config,
                     'lockerbank_api': LockerUserAccessLevel(app_config, generate_access_token),
                     'data_reader': DataReader(app_config),
                     'login_api': LoginAPI(app_config),
                     'get_product_name': get_product_name}
    yield lockerbankapi


@pytest.mark.usefixtures('initialize')
class TestLockerUserAccessLevel(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """
        self.configparameter = "LOCKERS_Lockers_UserAccessLevel"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_admin_user(self, rp_logger, resource):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_enterprise_user(self, rp_logger, resource):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        MID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'MID')
        invalidMID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'invalidMID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_bank_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 4:
            self.Failures.append("get_sites_api does not have 4 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 5:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 5 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_activity_v2 does not have 5 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_activity_v1 does not have 5 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 5:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 5 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 5:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with MID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=MID,
                                                                                   token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_MID_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with invalidMID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=invalidMID,
                                                                                   token=token)
        if get_locker_banks_resp.status_code != 404:
            self.Failures.append("get_locker_bank_with_MID_api with invalid MID gives statuscode = " + str(
                get_locker_banks_resp.status_code))

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_d1_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        MID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'MID')
        invalidMID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'invalidMID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 3:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 3 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 3:
            self.Failures.append("get_locker_bank_api does not have 3 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 2:
            self.Failures.append("get_sites_api does not have 2 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 3:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 3 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 3:
            self.Failures.append("get_locker_activity_v2 does not have 3 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 3:
            self.Failures.append("get_locker_activity_v1 does not have 3 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 3:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 3 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 3:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 3 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with MID
        print(MID)
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=MID,
                                                                                   token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_MID_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with invalidMID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=invalidMID,
                                                                                   token=token)
        if get_locker_banks_resp.status_code != 404:
            self.Failures.append("get_locker_bank_with_MID_api with invalid MID gives statuscode = " + str(
                get_locker_banks_resp.status_code))

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.ilp_sp360commercial
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_lB_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')
        MID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'MID')
        invalidMID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'invalidMID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_bank_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 1:
            self.Failures.append("get_sites_api does not have 1 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 2:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 2 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_activity_v2 does not have 2 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_activity_v1 does not have 2 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 2:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 2 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with MID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=MID,
                                                                                   token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_MID_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with invalidMID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_MID(tenantID=tenantID, MID=invalidMID,
                                                                                   token=token)
        if get_locker_banks_resp.status_code != 404:
            self.Failures.append("get_locker_bank_with_MID_api with invalid MID gives statuscode = " + str(
                get_locker_banks_resp.status_code))

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_user(self, rp_logger, resource):
        """
        This test validates that locker banks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_bank_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 4:
            self.Failures.append("get_sites_api does not have 4 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 2:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 5 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_activity_v2 does not have 5 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_activity_v1 does not have 5 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 5:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 5 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 5:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_ent_locker_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_bank_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 4:
            self.Failures.append("get_sites_api does not have 4 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 1:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 1 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v2 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v1 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 1:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 1 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_div_locker_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_bank_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 4:
            self.Failures.append("get_sites_api does not have 4 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 1:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 1 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v2 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v1 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 1:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 1 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_loc_locker_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)
        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_bank_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 3:
            self.Failures.append("get_sites_api does not have 3 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 2:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 2 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_activity_v2 does not have 2 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 2:
            self.Failures.append("get_locker_activity_v1 does not have 2 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 2:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 2 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 2:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 2 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_get_lockerbanks_by_user_locker_user(self, rp_logger, resource):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        tenantID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'tenantID')
        siteID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'siteID')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'recipientID')

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')
        self.log.info(token)

        # Get Locker Banks by tenant
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks by site
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_tenant_and_site_api(tenantID=tenantID,
                                                                                                siteID=siteID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_banks_tenant_and_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_bank_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_with_site_api(siteID=siteID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Sites
        get_locker_banks_resp = resource['lockerbank_api'].get_sites_api(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['sites'])
        if record_total != 4:
            self.Failures.append("get_sites_api does not have 4 sites, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_siteID = str(response['sites'][i]['siteID'])
                print(get_siteID)

        # Get Reserved Units
        get_locker_banks_resp = resource['lockerbank_api'].get_reserved_units_across_tenant_api(tenantID=tenantID,
                                                                                                recipientID=recipientID,
                                                                                                token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['reservedUnits'])
        if record_total != 1:
            self.Failures.append(
                "get_reserved_units_across_tenant_api does not have 1 reservations, actual count = " + str(
                    record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['reservedUnits'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v2
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v2(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v2 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity v1
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_v1(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 1:
            self.Failures.append("get_locker_activity_v1 does not have 1 activity, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Activity Count
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_activity_count(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        if response['count'] != 1:
            print(record_total)
            self.Failures.append(
                "get_locker_activity_count does not have 1 activity count, actual count = " + str(record_total))

        # Get Locker Banks v2 with tenantID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_tenantID(tenantID=tenantID, token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_tenant_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Banks v2 with siteID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_banks_v2_siteID(tenantID=tenantID, siteID=siteID,
                                                                                      token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        response = get_locker_banks_resp.json()
        record_total = len(response['lockerBanks'])
        if record_total != 1:
            self.Failures.append(
                "get_locker_bank_v2_with_site_api does not have 1 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(response['lockerBanks'][i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank by ID
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_A", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_B", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_X", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("TEST_Y", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 403))

        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_by_id("Loc_B2", token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_integrator_token(self, rp_logger, resource, context):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        token = context['basic_integrator_token']
        self.log.info(token)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_bank_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with MID with matching integrator on same site
        get_locker_ID_resp_1 = resource['lockerbank_api'].get_locker_bank_by_id(MID='TEST_A', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_1, 200))

        # Get Locker Bank with MID with matching integrator on different site (JPMC use case)
        get_locker_ID_resp_2 = resource['lockerbank_api'].get_locker_bank_by_id(MID='TEST_B', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_2, 200))

        # Get Locker Bank with MID with different integrator
        get_locker_ID_resp_3 = resource['lockerbank_api'].get_locker_bank_by_id(MID='Loc_B2', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_3, 403))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.accesslevel
    @pytest.mark.regressioncheck_lockers
    def test_device_token(self, rp_logger, resource, context):
        """
        This test validates that lockerbanks can be fetched successfully for access level users  (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        token = context['basic_device_token']
        self.log.info(token)

        # Get Locker Bank
        get_locker_banks_resp = resource['lockerbank_api'].get_locker_bank_api(token=token)
        assert_that(self.validate_response_code(get_locker_banks_resp, 200))
        record_total = len(get_locker_banks_resp.json())
        if record_total != 5:
            self.Failures.append("get_locker_bank_api does not have 5 banks, actual count = " + str(record_total))
        else:
            print(record_total)
            for i in range(record_total):
                get_MID = str(get_locker_banks_resp.json()[i]['manufacturerID'])
                print(get_MID)

        # Get Locker Bank with MID with same locker
        get_locker_ID_resp_1 = resource['lockerbank_api'].get_locker_bank_by_id(MID='PPD2022', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_1, 200))

        # Get Locker Bank with MID with different locker same ent
        get_locker_ID_resp_2 = resource['lockerbank_api'].get_locker_bank_by_id(MID='DayLocker', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_2, 403))

        # Get Locker Bank with MID with different locker different ent
        get_locker_ID_resp_2 = resource['lockerbank_api'].get_locker_bank_by_id(MID='FB_INT', token=token)
        assert_that(self.validate_response_code(get_locker_ID_resp_2, 403))

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))
