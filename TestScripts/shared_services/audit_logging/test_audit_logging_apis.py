import inspect
import json
import time
from datetime import timedelta, date

import pytest
import logging
from hamcrest import assert_that, equal_to

from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.audit_logging_api import Audit_logging
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.custom_fields_api import Custom_fields
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.common_utils import common_utils
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    """
    The resource fixture used for the test class - TestUserSubscriptionManagementAPI.

    :param app_config: The application configuration to get the environment and project name details.
    :param generate_access_token: The method used for generating access token with admin user credentials.
    :param client_token: The method used for generating access token with client user credentials.
    :returns: Subscription_API object.
    """
    audit_logging_api = {
        'app_config': app_config,
        'audit_logging_api': Audit_logging(app_config, generate_access_token, client_token),
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'product_metadata_api': ProductMetadata(app_config, generate_access_token, client_token),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
        'custom_fields_api': Custom_fields(app_config, generate_access_token, client_token),
        'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
    }
    yield audit_logging_api


# create update and delete loc

@pytest.mark.usefixtures('initialize')
class TestUserCustomFieldsManagementAPI(common_utils):
    """
    The test class to place all the tests of Custom Field APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - AuditLoggingAPI.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.login = LoginAPI(app_config)

        self.admin_user, admin_pwd, self.client_user, client_pwd, self.sub_id = resource[
            'audit_logging_api'].retrieve_user_credentials()
        self.admin_token = self.login.get_access_token_for_user_credentials(username=self.admin_user,
                                                                            password=admin_pwd)
        self.client_token = self.login.get_access_token_for_user_credentials(username=self.client_user,
                                                                             password=client_pwd)

        yield

    @pytest.fixture(scope='function')
    def trigger_events_func(self, resource):

        name, asignpageform, sub_id, ent_id, division_id, loc_id, \
        user_emailID, location_id, location_id_list, siteid_on_def_loc, site_list, cf_list_values = \
            resource['custom_fields_api'].get_custom_field_required_details(resource=resource, admin_level='E',
                                                                            sub_id=self.sub_id,
                                                                            user_emailID=self.client_user)
        # create your own ids as ids will be displaying in view details of event logs
        al_div_id = 'Audit_div_id'+generate_random_string(char_count=5)
        al_loc_id = 'Audit_loc_id'+generate_random_string(char_count=5)
        #add division
        div_name = 'Audit_div_'+generate_random_string(char_count=5)
        add_div_res = resource['client_mgmt'].add_division_api(div_id=al_div_id, name=div_name,
                                                               sub_id=self.sub_id, ent_id=ent_id[0])
        created_div_id = add_div_res.json()['divisionID']
        #update division
        updated_div_name = 'updated_' + div_name
        update_div_res = resource['client_mgmt'].update_division_api(div_id=created_div_id, name=updated_div_name,
                                                                     sub_id=self.sub_id, ent_id=ent_id[0])
        #add location
        fetched_loc_name = "Audit_loc_" + generate_random_string(char_count=5)
        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=al_loc_id,
                                                                  loc_name=fetched_loc_name,
                                                                  ent_id=ent_id[0], sub_id=self.sub_id, is_admin=True)

        fetched_loc_id = add_loc_res.json()['locationID']
        fetched_bpn = add_loc_res.json().get('locationProperties').get('shipToBPN')

        #update location
        updated_loc_name = "updated_" + fetched_loc_name
        update_loc_res = resource['client_mgmt'] \
            .update_location_api(div_id=created_div_id, loc_id=fetched_loc_id, loc_name=updated_loc_name, ent_id=ent_id[0],
                                 sub_id=self.sub_id, bpn=fetched_bpn)

        #update site
        updated_site_name = "Auto_site_name_updated"

        update_site_resp = resource['client_mgmt'].verify_update_site_api(is_admin=True, sub_id=self.sub_id,
                                                                          name=updated_site_name,
                                                                          inbound_type='site',
                                                                          status='ACTIVE',
                                                                          site_id=site_list[0])
        #delete apis

        del_loc_res = resource['client_mgmt'].delete_location_api(add_loc_res.json()['locationID'])
        del_div_res = resource['client_mgmt'].delete_division_api(add_div_res.json()['divisionID'])
        del_site = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='Y', sub_id=self.sub_id,
                                                                                site_id=site_list[0])
        del_site = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='Y', sub_id=self.sub_id,
                                                                                site_id=site_list[1])
        #create cost account
        prmsn_by_entity = 'E'
        test_name = inspect.currentframe().f_code.co_name
        prmsn_by_value = str(resource['data_reader'].pd_get_data("COST_ACCT_MGMT", test_name, 'Test_Input'))
        accountID = "Audit_ca_"+generate_random_string(char_count=5)
        code = accountID
        name = accountID
        add_cost_acct_resp = resource['account_mgmt'].add_cost_account_api(accountID, code, name,
                                                                           prmsn_by_entity=prmsn_by_entity,
                                                                           prmsn_by_value=prmsn_by_value,
                                                                           sub_id=self.sub_id, is_admin=True)
        #delete cost account
        archive_cost_acct_resp = resource['account_mgmt'].archive_cost_account_api(acct_id=accountID,
                                                                                   sub_id=self.sub_id, is_admin=True)
        #add contact
        contact_name = "Audit_contact_"+generate_random_string(char_count=5)
        add_cont_resp = resource['addressbook_api'].add_new_contact_api(contact_type='RECIPIENT', type='S',
                                                                        name=contact_name, sub_id=self.sub_id, is_admn=True)
        contact_id = str(add_cont_resp.json())
        #update contact
        updated_contact_name = "Audit_update_contact_" + generate_random_string(char_count=5)
        update_cont_resp = resource['addressbook_api'].update_contact_api(contact_type='RECIPIENT', type='S',
                                                                        name=updated_contact_name, sub_id=self.sub_id,
                                                                        is_admn=True, cont_id=contact_id)
       #delete contact
        del_cont_resp = resource['addressbook_api'].patch_v1_delete_contact_api(cont_id=str(add_cont_resp.json()),
                                                                                sub_id=self.sub_id, is_admin=True)
        #add custom field
        add_custom_field_resp = resource['custom_fields_api'].add_custom_field_api(sub_id=self.sub_id,
                                                                                   is_admin=True,
                                                                                   admin_level='E',
                                                                                   name='Audit_cf_' + generate_random_string(char_count=5),
                                                                                   ent_id=ent_id,
                                                                                   asignPageForm=asignpageform,
                                                                                   token=self.admin_token,
                                                                                   cf_list_values=cf_list_values,
                                                                                   cf_type='TEXT')
        cf_id = str(add_custom_field_resp.json()['customFieldID'])
        #update custom field
        updated_cf_name = 'Auto_update' + generate_random_string(char_count=5)

        update_status = resource['custom_fields_api'].put_update_custom_field_api(sub_id=self.sub_id,
                                                                                  admin_level='E',
                                                                                  name=updated_cf_name, ent_id=ent_id,
                                                                                  config_id=cf_id,
                                                                                  asignPageForm=asignpageform,
                                                                                  is_admin=True,
                                                                                  token=self.admin_token,
                                                                                  cf_list_values=cf_list_values,
                                                                                  cf_type='TEXT')
        #delet custom field
        del_status = resource['custom_fields_api'].delete_custom_field_api(sub_id=sub_id,
                                                                           is_admin=True,
                                                                           config_id=str(add_custom_field_resp.json()['customFieldID']),
                                                                           token=self.admin_token)
        yield

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.audit_logging_management_sp360commercial
    @pytest.mark.parametrize('is_admin, event_type', [(True, 'INSERT'), (True, 'INSERT'),
                                                      (False, 'UPDATE'), (False, 'UPDATE')])
    def test_01_get_insert_and_update_audit_events(self, resource, event_type, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        today = date.today()
        from_date = today - timedelta(days=8)

        user_token = self.client_token

        if is_admin:
            user_token = self.admin_token

        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(is_admin=is_admin,
                                                                                   sub_id=self.sub_id,
                                                                                   event_type=event_type,
                                                                                   token=user_token,
                                                                                   fromDate=from_date,
                                                                                   toDate=today)
        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        # I will add the check on basis of ID once the DEV changes are done and its available to test.

        # if len(get_audit_events_resp.json()['data']):
        #     for i in range(len(get_audit_events_resp.json()['data'])):
        #         eventType = get_audit_events_resp.json()['data'][i]['eventType']
        #         subscription_id = get_audit_events_resp.json()['data'][i]['subscriptionId']
        #         assert_that(eventType.lower(), equal_to(event_type.lower()))
        #         assert_that(subscription_id, equal_to(self.sub_id))
        # else:
        #     # pytest.fail("########Data is not available in this date range########")
        #     pytest.warns("########Data is not available in this date range########")

        for i in range(len(get_audit_events_resp.json()['data'])):
            eventType = get_audit_events_resp.json()['data'][i]['eventType']
            subscription_id = get_audit_events_resp.json()['data'][i]['subscriptionId']
            assert_that(eventType.lower(), equal_to(event_type.lower()))
            assert_that(subscription_id, equal_to(self.sub_id))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin, collection_name',
                             [(True, 'DIVISION'), (True, 'LOCATION'), (True, 'SITE'), (True, 'customFields'),
                              (True, 'account'), (True, 'subscription'), (True, 'subCarrier'),
                              (False, 'DIVISION'), (False, 'LOCATION'), (False, 'SITE'), (False, 'customFields'),
                              (False, 'account'), (False, 'subscription'), (False, 'subCarrier')])
    def test_02_get_diff_collections_audit_events(self, resource, is_admin, collection_name):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        today = date.today()
        from_date = today - timedelta(days=8)

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   collection_name=collection_name,
                                                                                   token=user_token,
                                                                                   fromDate=from_date,
                                                                                   toDate=today)
        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        for i in range(len(get_audit_events_resp.json()['data'])):
            coll_name = get_audit_events_resp.json()['data'][i]['collectionName']
            subscription_id = get_audit_events_resp.json()['data'][i]['subscriptionId']
            assert_that(coll_name.lower(), equal_to(collection_name.lower()))
            assert_that(subscription_id, equal_to(self.sub_id))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_03_get_view_details(self, resource, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   token=user_token)

        audit_number = get_audit_events_resp.json()['data'][0]['auditNumber']
        collection_name = get_audit_events_resp.json()['data'][0]['collectionName']

        get_view_details_resp = resource['audit_logging_api'].get_view_details_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   audit_number=audit_number,
                                                                                   token=user_token)
        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        assert_that(audit_number, equal_to(get_view_details_resp.json()['auditNumber']))
        assert_that(collection_name.lower(), equal_to(get_view_details_resp.json()['collectionName'].lower()))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_04_get_audit_events_date_filter(self, resource, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        today = date.today()
        from_date = today - timedelta(days=8)
        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   token=user_token,
                                                                                   fromDate=from_date,
                                                                                   toDate=today,
                                                                                   pageSize=100
                                                                                   )
        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        var = 0
        for i in range(len(get_audit_events_resp.json()['data'])):
            time_stamp = get_audit_events_resp.json()['data'][i]['timestamp']
            subscription_id = get_audit_events_resp.json()['data'][i]['subscriptionId']
            if (time_stamp.__contains__(str(today)) and subscription_id == self.sub_id) \
                    or (time_stamp.__contains__(str(from_date)) and subscription_id == self.sub_id):
                var = 0
                assert_that(subscription_id, equal_to(self.sub_id))
            else:
                if time_stamp < str(today) and time_stamp > str(from_date):
                    var = 0
                    assert_that(subscription_id, equal_to(self.sub_id))
                else:
                    var = 1  # pytes.fail
                    pytest.fail(i+"th log does not satisfy the date filter")

        assert_that(var, equal_to(0))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin, event_type, collection_name',
                             [(True, 'INSERT', 'DIVISION'), (True, 'UPDATE', 'DIVISION'),
                              (True, 'INSERT', 'location'), (True, 'UPDATE', 'location'),
                              (False, 'INSERT', 'DIVISION'), (False, 'UPDATE', 'DIVISION'),
                              (False, 'INSERT', 'location'), (False, 'UPDATE', 'location')])
    def test_05_diff_filter_audit_events(self, resource, is_admin, event_type, collection_name):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        today = date.today()
        from_date = today - timedelta(days=8)
        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   event_type=event_type,
                                                                                   collection_name=collection_name,
                                                                                   token=user_token,
                                                                                   fromDate=from_date,
                                                                                   toDate=today,
                                                                                   pageSize=20)

        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        for i in range(len(get_audit_events_resp.json()['data'])):
            coll_name = get_audit_events_resp.json()['data'][i]['collectionName']
            eventType = get_audit_events_resp.json()['data'][i]['eventType']
            subscription_id = get_audit_events_resp.json()['data'][i]['subscriptionId']

            assert_that(coll_name.lower(), equal_to(collection_name.lower()))
            assert_that(eventType.lower(), equal_to(eventType.lower()))
            assert_that(subscription_id, equal_to(self.sub_id))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_06_get_audit_events_with_search_filter(self, resource, is_admin, trigger_events_func):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        get_audit_events_resp = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                   is_admin=is_admin,
                                                                                   token=user_token)
        user_id_to_search = ""
        for i in range(len(get_audit_events_resp.json()['data'])):
            user_id_to_search = get_audit_events_resp.json()['data'][i]['userId']
            if user_id_to_search != "":
                break

        get_audit_events_resp_new = resource['audit_logging_api'].get_audit_events_api(sub_id=self.sub_id,
                                                                                       is_admin=is_admin,
                                                                                       token=user_token,
                                                                                       searchBy=user_id_to_search)
        assert_that(self.validate_response_code(get_audit_events_resp, 200))

        for i in range(len(get_audit_events_resp_new.json()['data'])):
            user_id = get_audit_events_resp_new.json()['data'][i]['userId']
            subscription_id = get_audit_events_resp_new.json()['data'][i]['subscriptionId']

            assert_that(user_id, equal_to(user_id_to_search))
            assert_that(subscription_id, equal_to(self.sub_id))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_07_get_signin_events(self, resource, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        get_signin_events_resp = resource['audit_logging_api'].get_signin_events_api(sub_id=self.sub_id,
                                                                                     is_admin=is_admin,
                                                                                     token=user_token)
        assert_that(self.validate_response_code(get_signin_events_resp, 200))

        for i in range(len(get_signin_events_resp.json()['data'])):
            subscription_id = get_signin_events_resp.json()['data'][i]['subscriptionId']
            assert_that(subscription_id, equal_to(self.sub_id))

    @pytest.mark.audit_logging_management_sp360commercial_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_08_get_signin_events_with_search_filter_admin_user(self, resource, is_admin):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        user_token = self.client_token
        if is_admin:
            user_token = self.admin_token

        #     fetch the 1st email id from the respose and search with it

        get_signin_events_resp = resource['audit_logging_api'].get_signin_events_api(sub_id=self.sub_id,
                                                                                     is_admin=is_admin,
                                                                                     token=user_token)
        user_name_to_search = ""
        for i in range(len(get_signin_events_resp.json()['data'])):
            user_name_to_search = get_signin_events_resp.json()['data'][i]['userName']
            if user_name_to_search != "":
                break

        get_signin_events_resp_new = resource['audit_logging_api'].get_signin_events_api(sub_id=self.sub_id,
                                                                                         is_admin=is_admin,
                                                                                         token=user_token,
                                                                                         searchBy=user_name_to_search)

        for i in range(len(get_signin_events_resp_new.json()['data'])):
            user_name = get_signin_events_resp_new.json()['data'][i]['userName']
            subscription_id = get_signin_events_resp_new.json()['data'][i]['subscriptionId']
            assert_that(user_name, equal_to(user_name_to_search))
            assert_that(subscription_id, equal_to(self.sub_id))
