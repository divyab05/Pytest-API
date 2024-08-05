""" This module contains all test cases."""

import random
import inspect
import uuid

import pytest
import json
import logging
import FrameworkUtilities.logger_utility as log_utils
from hamcrest import assert_that, equal_to, greater_than
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    client_mgmt = {'app_config': app_config,
                   'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
                   'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
                   'data_reader': DataReader(app_config)}
    client_mgmt['login_api']: LoginAPI(app_config)
    yield client_mgmt


@pytest.mark.usefixtures('initialize')
class TestClientMgmtEnterpriseAPI(common_utils):

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.configparameter = "CLIENT_MGMT"

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_enterprise_expected_response_body')) as f1:
            self.sample_add_enterprise_expected_res = json.load(f1)
        with open(self.prop.get('CLIENT_MGMT', 'sample_get_enterprise_by_Id_expected_response_body')) as f2:
            self.sample_get_enterprise_by_Id_expected_res = json.load(f2)

        with open(self.prop.get('CLIENT_MGMT', 'sample_error_expected_response_body')) as f3:
            self.sample_error_expected_response_body = json.load(f3)

        with open(self.prop.get('CLIENT_MGMT', 'sample_add_division_expected_response_body')) as f4:
            self.sample_add_division_expected_response_body = json.load(f4)

        yield

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_smoke
    @pytest.mark.client_management_fedramp_reg
    @pytest.mark.active_active_ppd
    def test_create_new_enterprise_api(self, resource):
        """
        This test validates that new enterprise can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
        # "Call add enterprise API and verify the response"
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        fetched_enterprise_name = get_enterprise_res.json()['name']
        assert_that(fetched_enterprise_name, equal_to(ent_name))

        # delete the created enterprise

        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

        # fetch the deleted enterprise again

        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)

        self.validate_response_code(get_enterprise_res, 404)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_update_enterprise_api(self, resource):
        """
        This test validates that enterprise can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        # Call add enterprise API and verify the response
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        fetched_enterprise_name = get_enterprise_res.json()['name']
        assert_that(fetched_enterprise_name, equal_to(ent_name))

        # Verify that created enterprise can be updated successfully
        updated_name = "Auto_update_ent_Name_" + str(random.randint(1, 500))
        status_code = resource['client_mgmt'].update_enterprise_api(ent_id=created_ent_id, name=updated_name)

        assert_that(status_code, equal_to(200))

        # Verify that updated enterprise can be fetched successfully
        get_enterprise_resp = resource['client_mgmt'].get_enterprise_by_ent_id_api(ent_id=created_ent_id)
        self.validate_response_code(get_enterprise_resp, 200)

        updated_fetched_name = get_enterprise_resp.json()['name']

        assert_that(updated_fetched_name, equal_to(updated_name))

        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

        # fetch the deleted enterprise again

        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)

        self.validate_response_code(get_enterprise_res, 404)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_all_enterprise_api(self, resource):
        """
        This test validates that all enterprises can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Call get enterprise API and validate that response is not empty
        get_all_enterprises_resp = resource['client_mgmt'].get_all_enterprises_api()

        self.validate_response_code(get_all_enterprises_resp, 200)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_enterprise_count_api(self, resource):
        """
        This test validates that total count of enterprise can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # Verify that enterprise count is returned successfully:
        res, status_code = resource['client_mgmt'].get_enterprise_count_api()

        self.validate_expected_and_actual_response_code(status_code, 200)

        count = res['count']
        assert_that(count, greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_create_duplicate_enterprise_api(self, resource):
        """
        This test validates that error is obtained when duplicate enterprise is added (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        # Call add enterprise API and verify the response
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        fetched_enterprise_name = get_enterprise_res.json()['name']
        assert_that(fetched_enterprise_name, equal_to(ent_name))

        # Add duplicate enterprise API and verify that error is obtained:
        add_duplicate_ent_res = resource['client_mgmt'].add_enterprise_api(ent_id=created_ent_id, name=ent_name)
        assert_that(add_duplicate_ent_res.status_code, equal_to(400))

        duplicate_error_msg = add_duplicate_ent_res.json()['errors'][0]['errorCode']

        assert_that(duplicate_error_msg, equal_to('already_exists'))

        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

        # fetch the deleted enterprise again

        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)

        self.validate_response_code(get_enterprise_res, 404)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_enterprise_by_invalid_id_api(self, resource):
        """
        This test validates that error is obtained when invalid enterprise Id is fetched (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_id_ip = "  "

        # Verify error is obtained when blank enterprise Id is fetched
        res = resource['client_mgmt'].get_enterprise_by_ent_id_api(ent_id_ip)

        self.validate_response_code(res, 404)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_update_enterprise_with_longer_desc_api(self, resource):
        """
        This test validates that error should be obtained when description contains more than 50 characters (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        # Call add enterprise API and verify the response
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        fetched_enterprise_name = get_enterprise_res.json()['name']
        assert_that(fetched_enterprise_name, equal_to(ent_name))

        desc = "Test DIVISION1 Updateuuytutyuuykjhkjkjhgkhjhkuukuerhg"

        # Call Update enterprise API to updated the enterprise with longer description
        status_code = resource['client_mgmt'].update_enterprise_api(ent_id=ent_id, name=desc)
        assert_that(status_code, equal_to(400))

        # Delete the created enterprise
        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_del_divisions_in_enterprise_api(self, resource):
        """
        This test validates that division can be added and deleted from enterprise (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        div_id, div_name = resource['client_mgmt'].create_div_in_ent()
        div_list = [div_id]
        division_list = json.dumps(div_list)

        # Call add enterprise API and verify the response
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        # fetch the divisions before adding
        div_before_adding = len(get_enterprise_res.json()['divisions'])

        # Add the division to the created enterprise
        add_div_status_code = resource['client_mgmt'].add_division_in_ent_api(ent_id=created_ent_id, div=division_list)
        assert_that(add_div_status_code.status_code, equal_to(200))

        # Fetch the available divisions after adding:
        get_enterprise_resp = resource['client_mgmt'].get_enterprise_by_ent_id_api(ent_id=created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        # fetch the divisions added to enterprise
        div_after_adding = len(get_enterprise_resp.json()['divisions'])
        assert_that(div_after_adding, greater_than(div_before_adding))

        # delete the added divisions from enterprise
        status_code = resource['client_mgmt'].delete_division_from_ent_api(ent_id=created_ent_id, div=division_list)
        assert_that(status_code, equal_to(200))

        get_enterprise_resp = resource['client_mgmt'].get_enterprise_by_ent_id_api(ent_id=created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        # fetch the divisions added to enterprise
        div_after_deleting = len(get_enterprise_resp.json()['divisions'])
        assert_that(div_after_deleting, equal_to(div_before_adding))

        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_invalid_division_in_enterprise_api(self, resource):
        """
        This test validates that error should be obtained when invalid division is added to enterprise (negative scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()
        # ent_id = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'Test_Input'))

        division_list = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, 'divisionId'))

        # "Verify that error is obtained when invalid divisions are added"
        add_invalid_div_res = resource['client_mgmt'].add_division_in_ent_api(ent_id=ent_id, div=division_list)

        assert_that(self.validate_response_template(add_invalid_div_res, self.sample_error_expected_response_body, 400))

        assert_that(add_invalid_div_res.json()['errors'][0]['errorCode'], equal_to('not_found'))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_archive_enterprise_api(self, resource):
        """
        This test validates that enterprise can be archived successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        # "Call add enterprise API and verify the response"
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))

        created_ent_id = add_enterprise_res.json()['enterpriseID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        assert_that(self.validate_response_template(get_enterprise_res,
                                                    self.sample_get_enterprise_by_Id_expected_res, 200))

        fetched_enterprise_name = get_enterprise_res.json()['name']
        assert_that(fetched_enterprise_name, equal_to(ent_name))

        # Archive the created enterprise:
        archive_status_code = resource['client_mgmt'].archive_ent_api(ent_id=created_ent_id)
        assert_that(archive_status_code, equal_to(200))

        get_enterprise_res = resource['client_mgmt'].get_enterprise_by_ent_id_api(created_ent_id)
        self.validate_response_code(get_enterprise_res, 404)

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    def test_get_divisions_by_ent_id_api(self, resource):
        """
        This test validates that division can be fetched from enterprise (positive scenario)
        :return: return test status
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        # generate enterprise name and Id
        ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()

        # Call add enterprise API and verify the response
        add_enterprise_res = resource['client_mgmt'].add_enterprise_api(ent_id=ent_id, name=ent_name)
        assert_that(self.validate_response_template(add_enterprise_res,
                                                    self.sample_add_enterprise_expected_res, 201))
        created_ent_id = add_enterprise_res.json()['enterpriseID']

        create_subs_resp = resource['subscription_api'].create_subscription_api(ent_id=created_ent_id)
        assert_that(self.validate_response_code(create_subs_resp, 201))
        sub_id = create_subs_resp.json()['subID']

        # fetch the details of created enterprise and validate the enterprise name
        get_enterprise_res = resource['client_mgmt'].get_divisions_by_ent_id_api(created_ent_id)
        assert_that(get_enterprise_res.status_code, equal_to(200))
        div_before_adding = len(get_enterprise_res.json())

        unique_id = str(uuid.uuid4().hex)[:8]
        div_name = f'auto_div_{unique_id}'
        div_id = f'div_id_{unique_id}'

        # "Call add division API and verify the response"
        add_div_res = resource['client_mgmt'].create_division_api(div_id=div_id, name=div_name, sub_id=sub_id,
                                                                  ent_id=ent_id, is_admin=True)
        assert_that(self.validate_response_code(add_div_res, 201))
        created_div_id = add_div_res.json()['divisionID']

        # Fetch the available divisions after adding:
        get_div_frm_ent_resp = resource['client_mgmt'].get_divisions_by_ent_id_api(ent_id=created_ent_id)
        assert_that(get_div_frm_ent_resp.status_code, equal_to(200))

        # fetch the divisions added to enterprise
        div_after_adding = len(get_div_frm_ent_resp.json())
        assert_that(div_after_adding, greater_than(div_before_adding))

        del_div_resp = resource['client_mgmt'].delete_division_api(div_id=div_id)
        assert_that(self.validate_response_code(del_div_resp, 200))
        div_after_deleting_resp = resource['client_mgmt'].get_divisions_by_ent_id_api(ent_id=created_ent_id)
        assert_that(self.validate_response_code(div_after_deleting_resp, 200))

        # fetch the divisions added to enterprise
        div_after_deleting = len(div_after_deleting_resp.json())
        assert_that(div_after_adding, greater_than(div_after_deleting))

        subs_status_code = resource['subscription_api'].archive_subscription_api(sub_id=sub_id)
        assert_that(subs_status_code, equal_to(200))

        del_enterprise_res = resource['client_mgmt'].delete_ent_api(created_ent_id)
        assert_that(del_enterprise_res, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    def test_add_enterprise_with_division_api(self, resource):
        """
        This test validates that enterprise can be added with division (positive scenario)
        :return: return test status
        """

        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        created_ent_id = None

        try:
            ent_name, ent_id = resource['client_mgmt'].generate_enterprise_data()
            div_id, div_name = resource['client_mgmt'].create_div_in_ent()
            div_list = [div_id]
            division_list = json.dumps(div_list)

            # Call add enterprise with division API and verify the response
            get_enterprise_res = (resource['client_mgmt']
                                  .add_enterprise_with_division_api(ent_id=ent_id, name=ent_name, div=division_list))
            assert_that(self.validate_response_template(get_enterprise_res,
                                                        self.sample_get_enterprise_by_Id_expected_res, 201))
            created_ent_id = get_enterprise_res.json()['enterpriseID']

            # Fetch the available divisions in enterprise
            get_divisions_resp = resource['client_mgmt'].get_divisions_by_ent_id_api(ent_id=created_ent_id)
            assert_that(get_divisions_resp.status_code, equal_to(200))
            assert_that(len(get_divisions_resp.json()), greater_than(0))

        finally:
            status_code = resource['client_mgmt'].delete_ent_api(ent_id=created_ent_id)
            assert_that(status_code, equal_to(200))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_smoke
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.active_active_ppd
    def test_get_location_from_enterprise_api(self, resource):
        """
        This test validates that locations can be fetched from enterprise (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        ent_id = resource['client_mgmt'].get_enterprise_id_from_file()
        get_loc_from_enterprise = resource['client_mgmt'].get_locations_by_ent_id_api(ent_id=ent_id)

        assert_that(self.validate_response_code(get_loc_from_enterprise, 200))
        total_locations = len(get_loc_from_enterprise.json())
        assert_that(total_locations, greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_sap_enterpriseIds_api(self, resource):
        """
        This test validates that sap enterprises can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_sap_enterprise = resource['client_mgmt'].get_sap_enterpriseIds_api()

        assert_that(self.validate_response_code(get_sap_enterprise, 200))
        total_sap_enterprise = len(get_sap_enterprise.json())
        assert_that(total_sap_enterprise, greater_than(0))

    @pytest.mark.client_management_sp360commercial
    @pytest.mark.client_management_sp360commercial_reg
    @pytest.mark.client_management_fedramp
    @pytest.mark.client_management_fedramp_reg
    def test_get_user_enterpriseIds_api(self, resource):
        """
        This test validates that user enterprises can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'###### TEST EXECUTION STARTED :: {test_name} ######')

        get_user_enterprise = resource['client_mgmt'].get_user_enterprise_api()

        assert_that(self.validate_response_code(get_user_enterprise, 200))
        total_user_enterprise = len(get_user_enterprise.json())
        assert_that(total_user_enterprise, greater_than(0))
