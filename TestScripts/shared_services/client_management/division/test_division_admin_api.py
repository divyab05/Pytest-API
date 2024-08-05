""" This module contains all test cases."""
import inspect
import json
import random
import uuid
import pytest
import logging
import FrameworkUtilities.logger_utility as log_utils
from hamcrest import assert_that, greater_than, equal_to
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.generic_utils import generate_random_string, get_current_timestamp


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    client_mgmt = {'app_config': app_config,
                   'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
                   'data_reader': DataReader(app_config)}
    client_mgmt['login_api']: LoginAPI(app_config)
    yield client_mgmt


@pytest.mark.usefixtures('initialize')
class TestDivisionAdminAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.configparameter = "CLIENT_MGMT"

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_division_expected_response_body')) as f1:
            self.sample_add_division_expected_response_body = json.load(f1)

        with open(self.prop.get('CLIENT_MGMT', 'sample_error_expected_response_body')) as f2:
            self.sample_error_expected_response_body = json.load(f2)
        yield

    # Test Cases: Division Module

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_all_divisions_api(self, resource):
        """
        This test validates that all divisions can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # "Call get division API and validate that status code is 200 and divisions are returned in response"
        get_div_res = resource['client_mgmt'].get_all_divisions_api()

        assert_that(self.validate_response_code(get_div_res, 200))
        # Getting lib\json\decoder.py:353: MemoryError due to large divs data in response.
        # assert_that(len(get_div_res.json()), greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_division_count_api(self, resource):
        """
        This test validates that total count of divisions can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Verify that division count is returned successfully:
        get_div_count = resource['client_mgmt'].get_div_count_api()
        assert_that(self.validate_response_code(get_div_count, 200))

        count = get_div_count.json()['count']
        assert_that(count, greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    def test_add_division_api(self, resource):
        """
        This test validates that new divisions can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + 'div_name'
        div_id = ent_id + 'div_id'
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()

        # Call add division API and verify the response
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_template(add_div_res,
                                                    self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']
        # Verify that created division can be fetched successfully
        get_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_div_res, 200))

        # Delete the created division:
        del_div_res = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # Verify that deleted division can not be fetched and error should be obtained
        get_deleted_div = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(get_deleted_div, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_duplicate_division_api(self, resource):
        """
        This test validates that error is obtained when duplicate division is added (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + 'div_name'
        div_id = ent_id + 'div_id'
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Call add division API and verify the response
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_template(add_div_res,
                                                    self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']
        # Verify that created division can be fetched successfully
        get_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_div_res, 200))

        # Add division again using same details
        add_dup_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id, ent_id=ent_id)
        assert_that(self.validate_response_template(add_dup_div_res,
                                                    self.sample_error_expected_response_body, 400))

        assert_that(add_dup_div_res.json()['errors'][0]['errorCode'], equal_to('already_exists'))

        # Delete the created division:
        del_div_res = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # Verify that deleted division can not be fetched and error should be obtained
        get_deleted_div = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(get_deleted_div, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_division_by_invalid_id_api(self, resource):
        """
        This test validates that error is obtained when invalid division Id is fetched (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # division_id_ip = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'divisionId')
        division_id_ip = " "

        # "Verify error is obtained when blank division Id is passed":
        get_blank_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=division_id_ip)
        assert_that(self.validate_response_template(get_blank_div_res, self.sample_error_expected_response_body, 404))
        assert_that(get_blank_div_res.json()['errors'][0]['errorCode'], equal_to('not_found'))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    def test_update_division_api(self, resource):
        """
        This test validates that divisions can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + 'div_name'
        div_id = ent_id + 'div_id'
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # "Call add division API and verify the response"
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_template(add_div_res,
                                                    self.sample_add_division_expected_response_body, 201))

        created_div_id = add_div_res.json()['divisionID']
        # "Verify that created division can be fetched successfully"
        get_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_div_res, 200))

        div_name = get_div_res.json()['name']
        locations = get_div_res.json()['locations']
        archived = get_div_res.json()['archived']

        updated_name = 'updated_' + div_name

        # "Verify that created division can be updated successfully":
        update_div_res = resource['client_mgmt'].update_division_api(div_id=created_div_id, name=updated_name, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_code(update_div_res, 200))

        # Verify that updated division can be fetched successfully:
        get_update_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_update_div_res, 200))

        fetched_updated_name = get_update_div_res.json()['name']
        locations_after_update = get_update_div_res.json()['locations']
        archived_status_after_update = get_update_div_res.json()['archived']

        assert_that(fetched_updated_name, equal_to(updated_name))
        assert_that(locations_after_update, equal_to(locations))
        assert_that(archived_status_after_update, equal_to(archived))

        # "Archive the created division":
        del_api_res = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(del_api_res.status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_update_division_with_longer_desc_api(self, resource):
        """
        This test validates that error should be obtained when description contains more than 50 characters (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = generate_random_string()
        div_id = ent_id + '_div_id'
        desc = generate_random_string(char_count=60)
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Call add division API and verify the response
        add_div_res = resource['client_mgmt'].add_division_api(div_id=div_id, name=div_name, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_template(add_div_res,
                                                    self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']
        # Verify that created division can be fetched successfully
        get_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_div_res, 200))

        # "Call add division API and verify the response":
        update_div_res = resource['client_mgmt'].update_division_api(div_id=div_id, name=desc, sub_id=sub_Id, ent_id=ent_id)

        assert_that(self.validate_response_template(update_div_res,
                                                    self.sample_error_expected_response_body, 400))

        assert_that(update_div_res.json()['errors'][0]['errorDescription'],
                    equal_to('name - length must be less than 50'))

        # Delete the created division:
        del_div_res = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_locations_in_division_api(self, resource):
        """
        This test validates that locations can be added to the divisions (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        unique_id = str(uuid.uuid4().hex)[:8]
        div_name = f'auto_div_{unique_id}'
        div_id = f'div_id_{unique_id}'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Call add division API and verify the response
        add_div_res = resource['client_mgmt']\
            .add_division_api(div_id=div_id, name=div_name, sub_id=sub_id, ent_id=ent_id)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        # Verify that created division can be fetched successfully:
        get_loc_from_div_res = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(get_loc_from_div_res, 200))

        locations_before_updt = len(get_loc_from_div_res.json()['locations'])

        # Add locations to the created division:
        loc_name = f'auto_div_{unique_id}'
        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, ent_id=ent_id,
                                                                  sub_id=sub_id, loc_name=loc_name, is_admin=True)
        assert_that(self.validate_response_code(add_loc_res, 201))
        created_loc_id = add_loc_res.json()['locationID']

        # fetch the added locations
        fetch_added_loc_response = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(fetch_added_loc_response, 200))

        locations_after_updt = len(fetch_added_loc_response.json()['locations'])
        assert_that(locations_after_updt, greater_than(locations_before_updt))

        del_loc_from_div_res = resource['client_mgmt']\
            .delete_location_v2_api(loc_id=created_loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(del_loc_from_div_res, 200))

        update_dev_resp = resource['client_mgmt']\
            .put_update_division_with_loc_id_api(loc_id=created_loc_id, div_id=created_div_id)
        assert_that(self.validate_response_code(update_dev_resp, 200))

        # fetch locations after deleting from division
        fetch_deleted_loc_response = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(fetch_deleted_loc_response, 200))

        locations_after_deleting = len(fetch_deleted_loc_response.json()['locations'])
        assert_that(locations_after_deleting, equal_to(locations_before_updt))

        # Delete the created division:
        del_div_res = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # Verify that deleted division can not be fetched and error should be obtained
        get_deleted_div = resource['client_mgmt'].get_div_by_id_api(div_id=created_div_id)
        assert_that(self.validate_response_code(get_deleted_div, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_division_with_loc_api(self, resource):
        """
        This test validates that locations can be added to the divisions (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        division_id = "Auto_div_Id_" + str(random.randint(1, 50000))
        name_ip = "Auto_div_Nam_" + str(random.randint(1, 50000))
        location = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locationId')

        # "Call add division with location API and verify the response":
        add_div_with_loc = resource['client_mgmt'].add_division_with_location_api(div_id=division_id, div_name=name_ip,
                                                                                  loc=location)
        assert_that(self.validate_response_template(add_div_with_loc,
                                                    self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_with_loc.json()['divisionID']

        # "Verify that created division can be fetched successfully":
        get_loc_frm_div = resource['client_mgmt'].get_loc_from_div_api(div_id=created_div_id)

        assert_that(self.validate_response_code(get_loc_frm_div, 200))

        loc_count = len(get_loc_frm_div.json())

        assert_that(loc_count, greater_than(0))

        # "Delete the created division":
        del_api_status_code = resource['client_mgmt'].delete_division_api(div_id=created_div_id)
        assert_that(self.validate_response_code(del_api_status_code, 200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_division_locations_paginate_api(self, resource):
        """
        This test fetches the division details as per the pagination (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_id = None
        loc_id = None
        sub_id = None

        try:
            sub_id = resource['client_mgmt'].get_subscription_id_from_file()
            div_id, div_name, loc_id, loc_name = resource['client_mgmt'].create_loc_div_in_ent()

            get_loc_paginated_resp = resource['client_mgmt'].get_loc_in_div_paginated_api(div_id=div_id)
            assert_that(self.validate_response_code(get_loc_paginated_resp, 200))
            page_info = get_loc_paginated_resp.json()['pageInfo']
            location = get_loc_paginated_resp.json()['locations'][0]

            assert_that(page_info['totalCount'], greater_than(0))
            assert_that(page_info['startCount'], greater_than(0))
            assert_that(location['locationID'], equal_to(loc_id))
            assert_that(location['name'], equal_to(loc_name))
            assert_that(location['divisionID'], equal_to(div_id))

        finally:
            self.log.info(f'Deleting created div and location')
            resource['client_mgmt'].del_div_loc(div_id=div_id, loc_id=loc_id, sub_id=sub_id)
