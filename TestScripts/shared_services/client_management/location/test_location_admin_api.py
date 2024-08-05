""" This module contains all test cases."""

import json
import inspect
import pytest
from hamcrest import assert_that, greater_than, equal_to, is_not
import logging
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.generic_utils import generate_random_string


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    client_mgmt = {'app_config': app_config,
                   'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
                   'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
                   'data_reader': DataReader(app_config)}
    client_mgmt['login_api']: LoginAPI(app_config)
    yield client_mgmt


@pytest.mark.usefixtures('initialize')
class TestLocationAdminAPI(common_utils):
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

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_location_expected_response_body')) as f3:
            self.sample_add_location_expected_response_body = json.load(f3)

        with open(self.prop.get('CLIENT_MGMT', 'sample_get_field_list_expected_response_body')) as f4:
            self.sample_get_field_list_expected_response_body = json.load(f4)

        with open(self.prop.get('CLIENT_MGMT', 'sample_export_loc_expected_response_body')) as f5:
            self.sample_export_loc_expected_response_body = json.load(f5)

        with open(self.prop.get('CLIENT_MGMT', 'sample_fetch_job_status_expected_response_body')) as f6:
            self.sample_fetch_job_status_expected_response_body = json.load(f6)

        with open(self.prop.get('CLIENT_MGMT', 'add_inbound_site_list_resp')) as f7:
            self.sample_add_inboundsitelist_response_body = json.load(f7)

        with open(self.prop.get('CLIENT_MGMT', 'add_locations_ids_resp')) as f8:
            self.sample_add_locationsids_response_body = json.load(f8)

        yield

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    def test_01_get_all_locations_api(self, resource):
        """
        This test validates that all locations can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))

        get_all_loc_count = len(get_all_loc_res.json())
        assert_that(get_all_loc_count, greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    def test_02_create_del_location_api(self, resource):
        """
        This test validates that new locations can be added and deleted successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        div_name = ent_name + '_div_name'
        div_id = ent_id + '_div_id'
        loc_name = ent_name + '_loc_name'
        loc_id = ent_id + '_loc_id'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        self.log.info("sub_id: " + str(sub_id))
        self.log.info("ent_id: " + str(ent_id))

        # "Call add division API and verify the response"
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id, is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        # fetch the created location
        get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
        assert_that(self.validate_response_code(get_loc_by_id_res, 200))

        fetched_loc_id = get_loc_by_id_res.json()['locationID']
        fetched_loc_name = get_loc_by_id_res.json()['name']

        assert_that(fetched_loc_id, equal_to(loc_id))
        assert_that(fetched_loc_name, equal_to(loc_name))

        # delete the created location
        del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)
        assert_that(del_loc_res, equal_to(200))

        # fetch the deleted location
        get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id)
        assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

        # delete the created division
        del_div_res = resource['client_mgmt'].delete_division_api(div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_03_create_update_del_location_api(self, resource):
        """
        This test validates that new locations can be added and deleted successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id = f'{loc_name}_loc_id'

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        try:
            get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
            assert_that(self.validate_response_code(get_loc_by_id_res, 200))

            fetched_loc_id = get_loc_by_id_res.json()['locationID']
            fetched_loc_name = get_loc_by_id_res.json()['name']
            fetched_loc_properties = get_loc_by_id_res.json()['locationProperties']
            fetched_addr_line1 = get_loc_by_id_res.json()['addressLine1']
            fetched_bpn = get_loc_by_id_res.json().get('locationProperties').get('shipToBPN')

            assert_that(fetched_loc_id, equal_to(loc_id))
            assert_that(fetched_loc_name, equal_to(loc_name))

            # update name, address and phone of location
            updated_name = 'updated' + fetched_loc_name
            updated_addr_line1 = '10 Downing Street'
            updated_addr_line2 = 'Downing Street line 2'
            updated_city = 'Tracy'

            # Update the created location
            update_loc_res = resource['client_mgmt']\
                .update_location_api(div_id=created_div_id, loc_id=created_loc_id, loc_name=updated_name, ent_id=ent_id,
                                     sub_id=sub_id, bpn=fetched_bpn)
            assert_that(self.validate_response_code(update_loc_res, 200))

            # fetch the updated location details and verify that only name is updated
            get_updated_loc__res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
            assert_that(self.validate_response_code(get_updated_loc__res, 200))

            fetched_loc_id_after_name_update = get_updated_loc__res.json()['locationID']
            fetched_loc_name_after_name_update = get_updated_loc__res.json()['name']
            fetched_loc_properties_after_name_update = get_updated_loc__res.json()['locationProperties']
            fetched_addr_line1_after_name_update = get_updated_loc__res.json()['addressLine1']

            assert_that(fetched_loc_name_after_name_update, equal_to(updated_name))
            assert_that(fetched_loc_id_after_name_update, equal_to(fetched_loc_id))
            assert_that(fetched_addr_line1_after_name_update, equal_to(fetched_addr_line1))
            assert_that(fetched_loc_properties_after_name_update, equal_to(fetched_loc_properties))

            # update the address for created location
            update_loc_address_res = resource['client_mgmt']\
                .update_location_api(div_id=created_div_id, loc_id=created_loc_id, loc_name=updated_name, ent_id=ent_id,
                                     sub_id=sub_id, addr_ln1=updated_addr_line1, addr_ln2=updated_addr_line2,
                                     city=updated_city, bpn=fetched_bpn)
            assert_that(self.validate_response_code(update_loc_address_res, 200))

            # fetch the updated location details and verify that address is updated
            get_updated_loc_address_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
            assert_that(self.validate_response_code(get_updated_loc__res, 200))

            fetched_loc_id_after_addr_update = get_updated_loc_address_res.json()['locationID']
            fetched_loc_name_after_addr_update = get_updated_loc_address_res.json()['name']
            fetched_loc_properties_after_addr_update = get_updated_loc_address_res.json()['locationProperties']
            fetched_addr_line1_after_addr_update = get_updated_loc_address_res.json()['addressLine1']
            fetched_addr_line2_after_addr_update = get_updated_loc_address_res.json()['addressLine2']
            fetched_city_after_addr_update = get_updated_loc_address_res.json()['city']

            assert_that(fetched_loc_name_after_name_update, equal_to(fetched_loc_name_after_addr_update))
            assert_that(fetched_loc_id_after_name_update, equal_to(fetched_loc_id_after_addr_update))
            assert_that(fetched_addr_line1_after_addr_update, equal_to(updated_addr_line1))
            assert_that(fetched_addr_line2_after_addr_update, equal_to(updated_addr_line2))
            assert_that(fetched_city_after_addr_update, equal_to(updated_city))
            assert_that(fetched_loc_properties_after_addr_update, equal_to(fetched_loc_properties))

        finally:
            # delete the created location and division
            del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)
            assert_that(del_loc_res, equal_to(200))

            del_div_res = resource['client_mgmt'].delete_division_api(div_id)
            assert_that(self.validate_response_code(del_div_res, 200))

            get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id)
            assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_04_fetch_location_by_blank_id_api(self, resource):
        """
        This test validates that error should be obtained if invalid Id is provided to fetch location details (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        location_id = "  "

        # Verify that error is obtained when blank location Id is provided:
        blank_loc_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=location_id)
        assert_that(self.validate_response_template(blank_loc_id_res, self.sample_error_expected_response_body, 400))
        assert_that(blank_loc_id_res.json()['errors'][0]['errorDescription'],
                    equal_to('Invalid Request: No LocationID provided'))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_05_add_duplicate_location_api(self, resource):
        """
        This test validates that duplicate location shouldn't be added (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id = f'{loc_name}_loc_id'

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
        assert_that(self.validate_response_code(get_loc_by_id_res, 200))

        fetched_loc_id = get_loc_by_id_res.json()['locationID']
        fetched_loc_name = get_loc_by_id_res.json()['name']

        assert_that(fetched_loc_id, equal_to(loc_id))
        assert_that(fetched_loc_name, equal_to(loc_name))

        # add new location with same details
        add_duplicate_loc_res = resource['client_mgmt']\
            .create_location_api(div_id=created_div_id, loc_id=loc_id, loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                 is_admin=True)
        assert_that(self.validate_response_code(add_duplicate_loc_res, 400))
        assert_that(add_duplicate_loc_res.json()['errors'][0]['errorCode'], equal_to('DC-CR-CMLC2-E-locationName-exists'))

        # delete the created location and division
        del_loc_res = resource['client_mgmt'].delete_location_api(loc_id)
        assert_that(del_loc_res, equal_to(200))

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # fetch the deleted location
        get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id)
        assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_06_get_location_count_api(self, resource):
        """
        This test validates that total count of locations can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        res, status_code = resource['client_mgmt'].verify_get_loc_count_api()
        assert_that(status_code, equal_to(200))
        count = res['count']
        assert_that(count, is_not(equal_to(0)))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_07_archive_location_api(self, resource):
        """
        This test validates that new locations can be added and deleted successfully (positive scenario)
        :return: return test status
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id = f'{loc_name}_loc_id'

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id,
                                                                  loc_name=loc_name, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
        assert_that(self.validate_response_code(get_loc_by_id_res, 200))

        fetched_loc_id = get_loc_by_id_res.json()['locationID']
        fetched_loc_name = get_loc_by_id_res.json()['name']

        assert_that(fetched_loc_id, equal_to(loc_id))
        assert_that(fetched_loc_name, equal_to(loc_name))

        # delete the created location and division
        del_loc_res = resource['client_mgmt'].archive_location_api(loc_id)
        assert_that(del_loc_res, equal_to(200))

        del_div_res = resource['client_mgmt'].delete_division_api(div_id)
        assert_that(self.validate_response_code(del_div_res, 200))

        # fetch the deleted location
        get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id)
        assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    def test_08_export_location_api(self, resource):
        """
        This test validates that locations can be exported successfully (positive scenario)
        :return: return test status
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # get enterprise and locations
        sub_Id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # "Call get field list API"
        get_location_fields = resource['client_mgmt'].get_field_list()
        assert_that(self.validate_response_template(get_location_fields,
                                                    self.sample_get_field_list_expected_response_body, 200))

        get_location_fields = get_location_fields.json()

        # Call export location API
        export_loc_res = resource['client_mgmt'].export_locations_api(fieldList=get_location_fields, sub_Id=sub_Id,
                                                                      is_admin='y')
        assert_that(self.validate_response_template(export_loc_res, self.sample_export_loc_expected_response_body, 200))
        assert_that(export_loc_res.json()['message'],
                    equal_to('File is being processed. Please check the status with provided jobid'))

        job_id = export_loc_res.json()['jobId']

        # fetch job status
        fetch_process_status_res = resource['client_mgmt'].fetch_process_status_api(jobId=job_id, sub_Id=sub_Id,
                                                                                    is_admin='y')
        assert_that(self.validate_response_template(fetch_process_status_res,
                                                    self.sample_fetch_job_status_expected_response_body, 200))

        assert_that(fetch_process_status_res.json()['status'], equal_to('Processed'))

        export_file_loc = fetch_process_status_res.json()['exportFileLocation']
        file_url = self.decode_base_64(export_file_loc)

        res = resource['client_mgmt'].get_file_content(decoded_string=file_url)
        self.validate_response_code(res, 200)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_09_get_div_using_location_id(self, resource, is_admin):
        """
        This test validates that all divisions can be fetched successfully
         using locationID(positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        loc_id = get_all_loc_res.json()[0]["locationID"]
        div_id = get_all_loc_res.json()[0]["divisionID"]

        get_div_res = resource['client_mgmt'].get_div_from_location_id_api(loc_id=loc_id, is_admin=is_admin)
        assert_that(self.validate_response_code(get_div_res, 200))

        division_id = None
        location_id = None
        for i in range(len(get_div_res.json())):
            for k, v in get_div_res.json()[i].items():
                if k == 'archived' and v == False:
                    division_id = get_div_res.json()[i]['divisionID']
                    location_id = get_div_res.json()[i]['locations'][0]
                    break

        assert_that(div_id, equal_to(division_id))
        assert_that(loc_id, equal_to(location_id))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_10_get_loc_using_div_id_and_account_number(self, resource, is_admin):
        """
        This test validates that a locations can be fetched successfully
        using divsion id and account number (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        div_id = get_all_loc_res.json()[0]["divisionID"]
        acc_no = get_all_loc_res.json()[0]["locationProperties"]["shipToBPN"]
        loc_id = get_all_loc_res.json()[0]["locationID"]
        ent_id = get_all_loc_res.json()[0]["enterpriseID"]

        get_loc_res = resource['client_mgmt'].get_loc_from_div_id_and_account_number_api(div_id=div_id, acc_no=acc_no,
                                                                                         is_admin=is_admin)
        assert_that(self.validate_response_code(get_loc_res, 200))

        assert_that(div_id, equal_to(get_loc_res.json()["divisionID"]))
        assert_that(loc_id, equal_to(get_loc_res.json()["locationID"]))
        assert_that(acc_no, equal_to(get_loc_res.json()["locationProperties"]["shipToBPN"]))
        assert_that(ent_id, equal_to(get_loc_res.json()["enterpriseID"]))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    # @pytest.mark.client_management_fedramp
    # @pytest.mark.client_management_fedramp_test
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_11_get_all_div_using_user_and_sub_id(self, resource, is_admin):
        """
        This test validates that all divisions can be fetched successfully
         using user id and subscription id (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_sub_res = resource['subscription_api'].get_user_properties_api()
        user_id = get_sub_res.json()[0]["userID"]
        sub_id = get_sub_res.json()[0]["subID"]

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        div_id = get_all_loc_res.json()[0]["divisionID"]
        ent_id = get_all_loc_res.json()[0]["enterpriseID"]
        flag = 0
        for x in range(100):
            get_div_res = resource['client_mgmt'].get_div_from_user_and_sub_id_api(user_id=user_id, sub_id=sub_id,
                                                                                   is_admin=is_admin, skip=x, limit=10)
            assert_that(self.validate_response_code(get_div_res, 200))

            division_id = None
            subscription_id = None
            enterprise_id = None
            for i in range(len(get_div_res.json()['divisions'])):
                for k, v in get_div_res.json()['divisions'][i].items():
                    if k == 'divisionID' and v == div_id:
                        division_id = get_div_res.json()['divisions'][i]['divisionID']
                        subscription_id = get_div_res.json()['divisions'][i]['subID']
                        enterprise_id = get_div_res.json()['divisions'][i]['enterpriseID']
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 1:
                break

        assert_that(div_id, equal_to(division_id))
        assert_that(sub_id, equal_to(subscription_id))
        assert_that(ent_id, equal_to(enterprise_id))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    # @pytest.mark.client_management_fedramp
    # @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_12_get_all_loc_using_user_and_sub_id(self, resource, is_admin):
        """
        This test validates that all locations can be fetched successfully
         using user id and subscription id (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_sub_res = resource['subscription_api'].get_user_properties_api()
        user_id = get_sub_res.json()[0]["userID"]
        sub_id = get_sub_res.json()[0]["subID"]

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        loc_id = get_all_loc_res.json()[0]["locationID"]
        div_id = get_all_loc_res.json()[0]["divisionID"]
        ent_id = get_all_loc_res.json()[0]["enterpriseID"]
        flag = 0
        for x in range(100):
            get_loc_res = resource['client_mgmt'].get_loc_from_user_and_sub_id_api(user_id=user_id, sub_id=sub_id,
                                                                                   is_admin=is_admin, skip=x, limit=10)
            assert_that(self.validate_response_code(get_loc_res, 200))

            division_id = None
            subscription_id = None
            enterprise_id = None
            location_id = None
            for i in range(len(get_loc_res.json()['locations'])):
                for k, v in get_loc_res.json()['locations'][i].items():
                    if k == 'locationID' and v == loc_id:
                        location_id = get_loc_res.json()['locations'][i]['locationID']
                        division_id = get_loc_res.json()['locations'][i]['divisionID']
                        subscription_id = get_loc_res.json()['locations'][i]['subID']
                        enterprise_id = get_loc_res.json()['locations'][i]['enterpriseID']
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 1:
                break

        assert_that(loc_id, equal_to(location_id))
        assert_that(div_id, equal_to(division_id))
        assert_that(sub_id, equal_to(subscription_id))
        assert_that(ent_id, equal_to(enterprise_id))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_13_get_all_ent_using_paginate(self, resource, is_admin):
        """
        This test validates that all enterprise can be fetched successfully with pagination (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_id = resource['client_mgmt'].get_ent_id_having_divisions_and_locations()

        if ent_id:
            get_loc_res = (resource['client_mgmt']
                           .get_loc_from_ent_id_and_paginate_api(ent_id=ent_id, is_admin=is_admin,skip=0, limit=10))
            assert_that(self.validate_response_code(get_loc_res, 200))
            assert_that(ent_id, equal_to(get_loc_res.json()['locations'][0]['enterpriseID']))
        else:
            pytest.fail(f'Failed to retrieve ent_id having valid divisions and locations!')

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    def test_14_get_user_ent(self, resource):
        """
        This test validates that enterprise details can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_sub_res = resource['subscription_api'].get_user_properties_api()
        user_id = get_sub_res.json()[0]["userID"]
        sub_id = get_sub_res.json()[0]["subID"]

        get_div_res = resource['client_mgmt'].get_div_from_user_and_sub_id_api(user_id=user_id, sub_id=sub_id)
        ent_id = get_div_res.json()['divisions'][0]['enterpriseID']

        get_ent_res = resource['client_mgmt'].get_user_ent_api()
        assert_that(self.validate_response_code(get_ent_res, 200))
        assert_that(ent_id, equal_to(get_ent_res.json()['enterpriseID']))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_test
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_15_get_all_loc_using_ent_id_and_paginate(self, resource, is_admin):
        """
        This test validates that all location using enterprise id and paginate can be fetched successfully
         using enterprise id and paginate (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        loc_id = get_all_loc_res.json()[0]["locationID"]
        div_id = get_all_loc_res.json()[0]["divisionID"]
        ent_id = get_all_loc_res.json()[0]["enterpriseID"]
        sub_id = get_all_loc_res.json()[0]["subID"]
        flag = 0
        for x in range(100):
            get_loc_res = resource['client_mgmt'].get_loc_from_ent_id_and_paginate_api(ent_id=ent_id, is_admin=is_admin,
                                                                                       skip=x, limit=5)
            assert_that(self.validate_response_code(get_loc_res, 200))

            division_id = None
            subscription_id = None
            enterprise_id = None
            location_id = None
            for i in range(len(get_loc_res.json()['locations'])):
                for k, v in get_loc_res.json()['locations'][i].items():
                    if k == 'locationID' and v == loc_id:
                        location_id = get_loc_res.json()['locations'][i]['locationID']
                        division_id = get_loc_res.json()['locations'][i]['divisionID']
                        subscription_id = get_loc_res.json()['locations'][i]['subID']
                        enterprise_id = get_loc_res.json()['locations'][i]['enterpriseID']
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 1:
                break

        assert_that(loc_id, equal_to(location_id))
        assert_that(div_id, equal_to(division_id))
        assert_that(sub_id, equal_to(subscription_id))
        assert_that(ent_id, equal_to(enterprise_id))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.parametrize('is_admin', [True, False])
    def test_16_add_inboundsitelist_api(self, resource, is_admin):
        """
        This test validates that new sites can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        site_name = "Auto_site" + generate_random_string(char_count=5)
        type = 'site'
        sub_id = resource['client_mgmt'].get_subscription_id_from_file()

        get_all_loc_res = resource['client_mgmt'].get_all_locations_api()
        assert_that(self.validate_response_code(get_all_loc_res, 200))
        loc_id = get_all_loc_res.json()[0]["locationID"]

        # "Call add site API and verify the response":
        add_site_res, status_code = resource['client_mgmt'].verify_add_site_with_location_api(is_admin='Y',
                                                                                              sub_id=sub_id,
                                                                                              name=site_name,
                                                                                              location_id=loc_id,
                                                                                              type=type)
        assert_that(status_code, equal_to(201))

        created_site_id = add_site_res['inboundSiteID']

        # check the inboundsitelist post api if return's correct info of the given site_id

        sitelist_res = resource['client_mgmt'].inbound_sitelist_post_api(site_id=created_site_id, is_admin=is_admin)
        assigned_loc_id = sitelist_res.json()[0]["locationId"]

        assert_that(self.validate_response_template(sitelist_res,
                                                    [self.sample_add_inboundsitelist_response_body], 200))
        assert_that(self.compare_response_objects(sitelist_res.json()[0],
                                                  self.sample_add_inboundsitelist_response_body))
        assert_that(assigned_loc_id, equal_to(loc_id))

        # check the location/ids api which gets call after inboundsitelist api

        locationids_api_res = resource['client_mgmt'].locationids_post_api(loc_id=assigned_loc_id, is_admin=is_admin)

        assert_that(self.validate_response_template(locationids_api_res,
                                                    [self.sample_add_locationsids_response_body], 200))
        assert_that(self.compare_response_objects(locationids_api_res.json()[0],
                                                  self.sample_add_locationsids_response_body))
        assert_that(assigned_loc_id, equal_to(locationids_api_res.json()[0]["locationID"]))

        # Delete the created site":
        status_code = resource['client_mgmt'].verify_delete_inbound_site_by_id_api(is_admin='Y',
                                                                                   sub_id=sub_id,
                                                                                   site_id=created_site_id)
        assert_that(status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_17_verify_bpn_error_when_same_bpn_is_added_in_multiple_locations(self, resource):
        """
        This test validates the valid bpn already exists error when same bpn is added in multiple locations within same
        subscription.

        Please note: For Fedramp, same BPN validation is not added in the release v1.83 It will added later.
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        div_name = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        div_id = f'{div_name}_div_id'
        loc_name1 = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_name2 = f'auto_{generate_random_string(uppercase=False, digits=False, char_count=8)}'
        loc_id1 = f'{loc_name1}_loc_id'
        loc_id2 = f'{loc_name2}_loc_id'

        sub_id = resource['client_mgmt'].get_subscription_id_from_file()
        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()

        # Creating new division and location
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, ent_id=ent_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_div_res, self.sample_add_division_expected_response_body, 201))
        created_div_id = add_div_res.json()['divisionID']

        add_loc_res = resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id1,
                                                                  loc_name=loc_name1, ent_id=ent_id, sub_id=sub_id,
                                                                  is_admin=True)
        assert_that(self.validate_response_template(add_loc_res, self.sample_add_location_expected_response_body, 201))
        created_loc_id = add_loc_res.json()['locationID']

        try:
            get_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=created_loc_id)
            assert_that(self.validate_response_code(get_loc_by_id_res, 200))

            fetched_loc_id1 = get_loc_by_id_res.json()['locationID']
            fetched_loc_name1 = get_loc_by_id_res.json()['name']
            fetched_bpn = get_loc_by_id_res.json().get('locationProperties').get('shipToBPN')

            assert_that(fetched_loc_id1, equal_to(loc_id1))
            assert_that(fetched_loc_name1, equal_to(loc_name1))

            # add new location with same details
            add_same_bpn_in_new_loc_res = (
                resource['client_mgmt'].create_location_api(div_id=created_div_id, loc_id=loc_id2, loc_name=loc_name2,
                                                            ent_id=ent_id, sub_id=sub_id, bpn=fetched_bpn, is_admin=True))
            assert_that(self.validate_response_code(add_same_bpn_in_new_loc_res, 400))

            exp_bpn_loc_error_resp = resource['client_mgmt'].build_exp_error_message_bpn_loc_response(bpn=fetched_bpn)
            assert_that(self.validate_response_template(add_same_bpn_in_new_loc_res, exp_bpn_loc_error_resp, 400))
            self.log.info(f'BPN Error expected with 400 status, '
                          f'as same BPN cannot be added in another location within same Subscription!')

        finally:
            # delete the created location and division
            del_loc_res = resource['client_mgmt'].delete_location_api(loc_id1)
            assert_that(del_loc_res, equal_to(200))

            del_div_res = resource['client_mgmt'].delete_division_api(div_id)
            assert_that(self.validate_response_code(del_div_res, 200))

            # fetch the deleted location
            get_del_loc_by_id_res = resource['client_mgmt'].get_loc_by_id_api(loc_id=loc_id1)
            assert_that(self.validate_response_code(get_del_loc_by_id_res, 404))
            self.log.info(f'Successfully deleted the created division - {div_name} and location - {loc_name1}')
