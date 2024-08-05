""" This module contains all test cases."""

import random
import inspect
import pytest
from hamcrest import assert_that, greater_than, equal_to
import logging
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    client_mgmt = {'app_config': app_config,
                   'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
                   'data_reader': DataReader(app_config)}
    client_mgmt['login_api']: LoginAPI(app_config)
    yield client_mgmt


@pytest.mark.usefixtures('initialize')
class TestInboundSiteUserAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.configparameter = "CLIENT_MGMT"

        # with open(self.prop.get('CLIENT_MGMT', 'sample_add_division_expected_response_body')) as f1:
        #     self.sample_add_division_expected_response_body = json.load(f1)
        #
        # with open(self.prop.get('CLIENT_MGMT', 'sample_error_expected_response_body')) as f2:
        #     self.sample_error_expected_response_body = json.load(f2)
        #
        # with open(self.prop.get('CLIENT_MGMT', 'sample_add_location_expected_response_body')) as f3:
        #     self.sample_add_location_expected_response_body = json.load(f3)
        #
        # with open(self.prop.get('CLIENT_MGMT', 'sample_get_field_list_expected_response_body')) as f4:
        #     self.sample_get_field_list_expected_response_body = json.load(f4)
        #
        # with open(self.prop.get('CLIENT_MGMT', 'sample_export_loc_expected_response_body')) as f5:
        #     self.sample_export_loc_expected_response_body = json.load(f5)
        #
        # with open(self.prop.get('CLIENT_MGMT', 'sample_fetch_job_status_expected_response_body')) as f6:
        #     self.sample_fetch_job_status_expected_response_body = json.load(f6)
        yield

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    def test_add_site_user_api(self, resource):
        """
        This test validates that new sites can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        # sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # "Call add site API and verify the response":
        add_site_res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id,
                                                                                name=site_name,
                                                                                type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        # "Verify that created site can be fetched successfully":
        get_inbound_site_res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                                                                      sub_id=sub_id,
                                                                                                      site_id=created_site_id)
        assert_that(status_code, equal_to(200))

        # total_ancestors = len(get_inbound_site_res['ancestorlist'])

        # assert_that(total_ancestors, greater_than(0))

        # Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n',
                                                                                   sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))

        # "Verify that deleted site can not be fetched and error should be obtained":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                                                     sub_id=sub_id,
                                                                                     site_id=created_site_id)

        assert_that(status_code, equal_to(404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_add_duplicate_site_user_api(self, resource):
        """
        This test validates that duplicate sites can not be added (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        # sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # "Call add site API and verify the response":
        add_site_res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id,
                                                                                name=site_name,
                                                                                type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        # "Verify that created site can be fetched successfully":
        get_inbound_site_res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                                                                      sub_id=sub_id,
                                                                                                      site_id=created_site_id)
        assert_that(status_code, equal_to(200))

        # "Call add site API with same Id and verify the response":
        add_dup_site_res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id,
                                                                                    name=site_name,
                                                                                    type=type)
        assert_that(status_code, equal_to(400))

        assert_that(add_dup_site_res['errors'][0]['errorCode'], equal_to('already_exists'))

        # Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n',
                                                                                   sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))

        # "Verify that deleted site can not be fetched and error should be obtained":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                                                     sub_id=sub_id,
                                                                                     site_id=created_site_id)

        assert_that(status_code, equal_to(404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_add_inbound_sites_user_api(self, resource):
        """
        This test validates that new inbound sites of different types (ofice, floor, mailstop) can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # Call Add site API to create site (toplevel)":
        add_site_res, add_site_status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id,
                                                                                         name=site_name,
                                                                                         type=type)
        assert_that(add_site_status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        # "Create a site of type building with site as parent: "

        build_site_name = "Auto_build_site" + str(random.randint(1, 50000))
        parent = str(created_site_id)
        type = 'building'

        # "Call add inbound site API to create building site:":

        add_inbound_site_res, add_inbound_site_status_code = resource['client_mgmt'].verify_add_inbound_site_api(
            is_admin='n', sub_id=sub_id, name=build_site_name, parent_id=parent, type=type)

        assert_that(add_inbound_site_status_code, equal_to(201))

        building_site_id = add_inbound_site_res['inboundSiteID']

        # "Verify that created building site can be fetched successfully":
        get_inbound_site_res, get_inbound_site_res_status_code = resource[
            'client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                             sub_id=sub_id,
                                                             site_id=building_site_id)
        assert_that(get_inbound_site_res_status_code, equal_to(200))

        total_ancestors = len(get_inbound_site_res['ancestorlist'])
        parent_id = str(get_inbound_site_res['parent'])

        assert_that(total_ancestors, greater_than(0))

        assert_that(parent_id, equal_to(parent))

        # "Create a site of type office with parent as building":
        office_site_name = "Auto_office_site" + str(random.randint(1, 50000))
        parent = str(building_site_id)
        type = 'office'

        # "Call add inbound site API to create Office:"

        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=office_site_name,
                                                                               parent_id=parent,
                                                                               type=type)
        assert_that(status_code, equal_to(201))

        office_site_id = res['inboundSiteID']

        # "Verify that created office site can be fetched successfully":

        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=office_site_id)

        assert_that(status_code, equal_to(200))

        total_ancestors = len(res['ancestorlist'])

        assert_that(total_ancestors, greater_than(1))

        # "Create a site of type floor with parent as office":

        floor_site_name = "Auto_floor_site" + str(random.randint(1, 50000))
        parent = str(office_site_id)
        type = 'floor'

        # "Call add inbound site API to create floor: "

        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=floor_site_name, parent_id=parent,
                                                                               type=type)

        assert_that(status_code, equal_to(201))

        floor_site_id = res['inboundSiteID']

        # "Verify that created floor site can be fetched successfully":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=floor_site_id)

        assert_that(status_code, equal_to(200))

        total_ancestors = len(res['ancestorlist'])
        parent_id = res['parent']

        assert_that(total_ancestors, greater_than(2))

        assert_that(parent_id, equal_to(parent))

        # "Create a site of type mailstop with parent as floor":

        mailstop_site_name = "Auto_mailstop_site" + str(random.randint(1, 50000))

        parent = str(floor_site_id)
        type = 'mailstop'

        # "Call add inbound site API to create mailstop: ":

        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=mailstop_site_name,
                                                                               parent_id=parent, type=type)

        assert_that(status_code, equal_to(201))

        mailstop_site_id = res['inboundSiteID']

        # "Verify that created mailstop site can be fetched successfully":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=mailstop_site_id)

        assert_that(status_code, equal_to(200))

        total_ancestors = len(res['ancestorlist'])
        parent_id = res['parent']

        assert_that(total_ancestors, greater_than(3))

        assert_that(parent_id, equal_to(parent))

        # "Delete the created mailstop site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=mailstop_site_id)

        assert_that(status_code, equal_to(200))

        # "Delete the created floor site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=floor_site_id)

        assert_that(status_code, equal_to(200))

        # "Delete the created office":

        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=office_site_id)
        assert_that(status_code, equal_to(200))

        # "Delete the created building":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=building_site_id)

        assert_that(status_code, equal_to(200))

        # "Verify that deleted inbound site can not be fetched and error should be obtained":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=building_site_id)

        assert_that(status_code, equal_to(404))

        # "Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_site_id)

        assert_that(status_code, equal_to(200))

        # "Verify that deleted site can not be fetched and error should be obtained":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n',
                                                                                     sub_id=sub_id,
                                                                                     site_id=created_site_id)
        assert_that(status_code, equal_to(404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_update_inbound_sites_building_user_api(self, resource):
        """
        This test validates that new inbound sites can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # "Call add site API and verify the response":
        res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id, name=site_name,
                                                                       type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = res['inboundSiteID']

        inbound_site_name = "Auto_inbound_site" + str(random.randint(1, 50000))
        parent = str(created_site_id)
        type = 'building'

        # Call add inbound site API and verify the response":
        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=inbound_site_name,
                                                                               parent_id=parent, type=type)
        assert_that(status_code, equal_to(201))

        created_inbound_site_id = res['inboundSiteID']

        # "Verify that created inbound site can be fetched successfully":
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=created_inbound_site_id)
        assert_that(status_code, equal_to(200))

        total_ancestors = len(res['ancestorlist'])
        parent_id = res['parent']

        assert_that(total_ancestors, greater_than(0))

        assert_that(parent_id, equal_to(parent))

        # "Verify that created inbound site can be updated successfully":
        updated_name_ip = "Auto_site_updated_desc"
        status_ip = "INACTIVE"

        update_site_resp = resource['client_mgmt'].verify_update_site_api(is_admin=False, sub_id=sub_id,
                                                                     name=updated_name_ip,
                                                                     inbound_type=type,
                                                                     status=status_ip,
                                                                     site_id=created_inbound_site_id)
        assert_that(update_site_resp.status_code, equal_to(200))

        # "Verify that updated details are fetched correctly: "
        res, status_code = resource['client_mgmt'].verify_get_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                     site_id=created_inbound_site_id)

        assert_that(status_code, equal_to(200))

        status_val = str(res['status'])
        updated_name = str(res['name'])

        assert_that(status_val, equal_to(status_ip))

        assert_that(updated_name, equal_to(updated_name_ip))

        # "Delete the created building. ":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_inbound_site_id)
        assert_that(status_code, equal_to(200))

        # "Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n',
                                                                                   sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_update_inbound_sites_longer_name_user_api(self, resource):
        """
        This test validates that error should be obtained when name length is > 50 charcters (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        allowed_char = 200
        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # Call add site API and verify the response:
        res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id, name=site_name,
                                                                       type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = res['inboundSiteID']

        inbound_site_name = "Auto_inbound_site" + str(random.randint(1, 50000))
        parent = str(created_site_id)
        type = 'building'

        # "Call add inbound site API and verify the response":
        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=inbound_site_name,
                                                                               parent_id=parent, type=type)
        assert_that(status_code, equal_to(201))

        created_inbound_site_id = res['inboundSiteID']

        # "Verify that created inbound site can be updated successfully":
        updated_name_ip = generate_random_string(char_count=201)
        status_ip = "INACTIVE"

        update_site_resp = resource['client_mgmt'].verify_update_site_api(is_admin=False, sub_id=sub_id,
                                                                          name=updated_name_ip,
                                                                          inbound_type=type,
                                                                          status=status_ip,
                                                                          site_id=created_inbound_site_id)

        assert_that(update_site_resp.status_code, equal_to(400))

        err_msg = update_site_resp.json()['errors'][0]['errorDescription']

        assert_that(err_msg, equal_to(f'name - length must be less than {allowed_char}'))

        # "Delete the created building site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_inbound_site_id)
        assert_that(status_code, equal_to(200))

        # "Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_delete_parent_with_active_child_user_api(self, resource):
        """
        This test validates that error should be obtained when a parent with active child is deleted
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # "Call add site API and verify the response":
        res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id, name=site_name,
                                                                       type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = res['inboundSiteID']

        inbound_site_name = "Auto_inbound_site" + str(random.randint(1, 50000))
        parent = str(created_site_id)
        type = 'building'

        # Call add inbound site API and verify the response:
        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                               name=inbound_site_name,
                                                                               parent_id=parent, type=type)
        assert_that(status_code, equal_to(201))

        created_inbound_site_id = res['inboundSiteID']

        # Try to delete the ancestor having active child site:
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))  # SP360-3778 - parent inbound gets deleted even if it has active child

        # "Delete the created building site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_inbound_site_id)
        assert_that(status_code, equal_to(400)) # child was deleted already

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_add_site_with_invalid_type_user_api(self, resource):
        """
        This test validates that error is obtained when invalid site is provided in request body (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'SITE'
        sub_id = 'ABCG67'

        #"Call add site API and verify that error is obtained: "
        res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id, name=site_name,
                                                                           type=type)
        assert_that(status_code, equal_to(400))

        err_desc = str(res['errors'][0]['errorCode'])
        assert_that(err_desc, equal_to('not_found'))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_update_inbound_sites_invalid_type_user_api(self, resource):
        """
        This test validates that error should be obtained when invalid status is provided to update the site (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        #"Call add site API and verify the response":
        res, status_code = resource['client_mgmt'].verify_add_site_api(is_admin='n', sub_id=sub_id, name=site_name,
                                                                           type=type)

        assert_that(status_code, equal_to(201))

        created_site_id = res['inboundSiteID']

        inbound_site_name = "Auto_inbound_site" + str(random.randint(1, 50000))
        parent = str(created_site_id)
        type = 'building'

        #Call add inbound site API and verify the response:
        res, status_code = resource['client_mgmt'].verify_add_inbound_site_api(is_admin='n', sub_id=sub_id,
                                                                                           name=inbound_site_name,
                                                                                           parent_id=parent, type=type)

        assert_that(status_code, equal_to(201))

        created_inbound_site_id = res['inboundSiteID']

        #"Verify that created inbound site can be updated successfully":
        updated_name_ip = "Auto_site_updated_description"
        status_ip = "INACTIVEEE"

        update_site_resp = resource['client_mgmt'].verify_update_site_api(is_admin=False, sub_id=sub_id,
                                                                          name=updated_name_ip, inbound_type=type,
                                                                          status=status_ip,
                                                                          site_id=created_inbound_site_id)
        assert_that(update_site_resp.status_code, equal_to(400))

        #Delete the created building site:
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                                       site_id=created_inbound_site_id)
        assert_that(status_code, equal_to(200))

        #Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n',
                                                                                               sub_id=sub_id,
                                                                                               site_id=created_site_id)
        assert_that(status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_get_inbound_site_by_location_user_api(self, resource):
        """
        This test validates that new sites can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        # sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + '_div_name'
        div_id = ent_id + '_div_id'
        loc_name = ent_name + '_loc_name'
        loc_id = ent_id + '_loc_id'
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # "Call add division API and verify the response"
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id,
                                                               ent_id=ent_id)

        created_div_id = add_div_res.json()['divisionID']

        # add location with the created division
        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id, ent_id=ent_id,
                                                                  sub_id=sub_id, loc_name=loc_name, is_admin=True)
        assert_that(self.validate_response_code(add_loc_res, 201))
        created_loc_id = add_loc_res.json()['locationID']

        # "Call add site API and verify the response":
        add_site_res, status_code = resource['client_mgmt'].verify_add_site_with_location_api(is_admin='n',
                                                                                              sub_id=sub_id,
                                                                                              name=site_name,
                                                                                              type=type,
                                                                                              location_id=created_loc_id)
        assert_that(status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        get_site_by_loc_id, status_code = resource['client_mgmt'].verify_get_inbound_site_by_loc_id_api(is_admin='n',
                                                                                                        sub_id=sub_id,
                                                                                                        loc_id=created_loc_id)

        assert_that(status_code, equal_to(200))

        # Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_site_id)

        assert_that(status_code, equal_to(200))

        # Delete created location

        del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)

        assert_that(del_loc_res, equal_to(200))

        # Delete the created division

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)

        assert_that(self.validate_response_code(del_div_res, 200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_fetch_active_inbound_sites_user_api(self, resource):
        """
        This test validates that ACTIVE inbound sites can be fetched
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        search_param = 'searchBy=status:' + 'ACTIVE'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        # Fetch the created site with searchBy Type API

        search_by_site_type_res, search_by_site_type_status_code = resource[
            'client_mgmt'].verify_get_inbound_site_by_search_criteria_api(is_admin='Y',
                                                                          sub_id=sub_id,
                                                                          search_param=search_param)
        assert_that(search_by_site_type_status_code, equal_to(200))

        total_sites = len(search_by_site_type_res['inboundsites'])

        for i in range(total_sites):
            assert_that(search_by_site_type_res['inboundsites'][i]['status'], equal_to("ACTIVE"))
            assert_that(search_by_site_type_res['inboundsites'][i]['archived'], equal_to(False))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need fixes!")
    def test_delete_associated_location_reference_check_user_api(self, resource):
        """
        This test validates that locations on which sites are added shouldn't be deleted (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_Admin_site" + str(random.randint(1, 50000))
        type = 'site'
        # sub_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'subID'))
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + '_div_name'
        div_id = ent_id + '_div_id'
        loc_name = ent_name + '_loc_name'
        loc_id = ent_id + '_loc_id'
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # "Call add division API and verify the response"
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id,
                                                               ent_id=ent_id)

        created_div_id = add_div_res.json()['divisionID']
        # add location with the created division

        add_loc_res = resource['client_mgmt'].add_location_api(div_id=created_div_id, loc_id=loc_id, ent_id=ent_id,
                                                               subId=sub_Id, loc_name=loc_name)

        created_loc_id = add_loc_res.json()['locationID']

        # "Call add site API and verify the response":
        add_site_res, status_code = resource['client_mgmt'].verify_add_site_with_location_api(is_admin='n',
                                                                                              sub_id=sub_id,
                                                                                              name=site_name,
                                                                                              type=type,
                                                                                              location_id=created_loc_id)
        assert_that(status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        get_site_by_loc_id, status_code = resource['client_mgmt'].verify_get_inbound_site_by_loc_id_api(is_admin='n',
                                                                                                        sub_id=sub_id,
                                                                                                        loc_id=created_loc_id)

        assert_that(status_code, equal_to(200))

        #Delete the location before deleting the inbound site

        del_v2_locn_res, del_loc_status_code = resource['client_mgmt'].delete_location_v2_api(is_admin=False,sub_id=sub_id, loc_id=created_loc_id)

        assert_that(del_loc_status_code, equal_to(400))

        assert_that(del_v2_locn_res['errors'][0]['errorCode'], equal_to('DD-DL-CMLC1-E-locationId.referencefound'))


        # Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='n', sub_id=sub_id,
                                                                                   site_id=created_site_id)

        assert_that(status_code, equal_to(200))

        # Delete created location

        del_loc_res = resource['client_mgmt'].delete_location_v2_api(is_admin=False, sub_id=sub_id, loc_id=created_loc_id)

        assert_that(del_loc_res, equal_to(200))

        # Delete the created division

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)

        assert_that(self.validate_response_code(del_div_res, 200))




