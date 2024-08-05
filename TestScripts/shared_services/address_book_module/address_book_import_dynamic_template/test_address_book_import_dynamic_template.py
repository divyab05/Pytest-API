""" This module contains all test cases."""
import inspect
import json
import logging
import pytest
from hamcrest import assert_that
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
import FrameworkUtilities.logger_utility as log_utils


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    resource_instances = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'product_metadata_api': ProductMetadata(app_config, generate_access_token, client_token),
        'client_management_api': ClientManagementAPI(app_config, generate_access_token, client_token)
    }
    yield resource_instances


@pytest.mark.usefixtures('initialize')
class TestAddressbookImportDynamicTemplate(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    @pytest.mark.parametrize('plan_case', ['case1', 'case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case8',
                                           'case9', 'case10'])
    def test_01_verify_dynamic_template_addressbook_import_with_admin_user(self, resource, plan_case):
        """
        This test validates that dynamic template address book import based on the subscription plans. It verifies
        based on the plans for - import csv template headers,import fields list, import of contacts with columns,
        export the contacts and compares the imported contacts within the exported contacts file.

        The following are the plans based on the test case:
         case1: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0", "LOCKER_PLAN", "PitneyTrack_Pro"]
         case2: ["SENDING_PLAN", "PITNEYSHIP_PRO", "LOCKER_PLAN", "FIREBALL_2.0"]
         case3: ["SENDING_PLAN", "PITNEYSHIP_PRO", "LOCKER_PLAN", "TRACKING_PLAN"]
         case4: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0","SMS_NOTIFICATION_PLAN"]
         case5: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0"]
         case6: ["SENDING_PLAN", "PITNEYSHIP_PRO", "TRACKING_PLAN"]
         case7: ["PITNEYSHIP_PRO", "TRACKING_PLAN"]
         case8: ["PITNEYSHIP_PRO", "LOCKER_PLAN"]
         case9: ["PITNEYSHIP_PRO", "FIREBALL_2.0"]
         case10: ["PITNEYSHIP_PRO", "SENDING_PLAN"]

        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_type = 'PITNEYSHIP_PRO'
        is_admin = True

        with open(self.prop.get('ADDRESSBOOK_MGMT', f'{plan_case}_exp_dynamic_addressbook_import_fields_list')) as f1:
            exp_dynamic_addressbook_import_fields_list = json.load(f1)

        # Retrieving the subs plans and updating subscription with dynamic template subs plans
        sub_id, email, pwd, ent_id, plans, csv_headers = resource['addressbook_api']\
            .get_required_details_for_dynamic_template(sub_type=sub_type, plan_case=plan_case, is_admin=is_admin)

        # Update subscription with the defined case plans
        resource['subscription_api']\
            .update_plans_in_subscription(is_admin=is_admin, ent_id=ent_id[0], sub_id=sub_id, plans=plans)

        # import of the contacts based on the plan
        sample_import_fields_resp = resource['addressbook_api']\
            .get_sample_import_fields_api(is_admin=is_admin, sub_id=sub_id)

        assert_that(self.validate_response_template(sample_import_fields_resp,
                                                    exp_dynamic_addressbook_import_fields_list, 200))

        # Delete existing contacts
        resource['addressbook_api'].delete_all_contacts(is_admin=is_admin, sub_id=sub_id)

        # Generating contacts import csv file based on the plans
        resource['addressbook_api']\
            .import_contacts_for_dynamic_template(import_file_case=plan_case, plan_headers=csv_headers,
                                                  is_admin=is_admin, sub_id=sub_id)

        export_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'dynamic_template_contacts_exported_data')

        resource['addressbook_api']\
            .export_contacts_check_status_and_download_export_file(sub_id=sub_id, is_admin=is_admin,
                                                                   export_csv_filepath=export_csv_filepath)

        import_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', f'{plan_case}_dynamic_addressbook_import_file')
        export_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'dynamic_template_contacts_exported_data')

        assert_that(self.compare_csv_rows(source_file=import_csv_filepath,
                                          target_file=export_csv_filepath, skip_header=True))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.address_book_fedramp
    @pytest.mark.address_book_fedramp_reg
    # @pytest.mark.parametrize('plan_case, admin_level', [('case1', 'E'), ('case2', 'D'), ('case3', 'L'), ('case4', 'U'),
    #                                                     ('case5', 'E'), ('case6', 'D'), ('case7', 'L'), ('case8', 'E'),
    #                                                     ('case9', 'D'), ('case10', 'L')])
    @pytest.mark.parametrize('plan_case, admin_level', [('case10', 'E')])
    # @pytest.mark.skip(reason="Need to check why it is failing only in CICD")
    def test_02_verify_dynamic_template_addressbook_import_with_client_user(self, resource, plan_case, admin_level):
        """
        This test validates that dynamic template address book import based on the subscription plans. It verifies
        based on the plans for - import csv template headers,import fields list, import of contacts with columns,
        export the contacts and compares the imported contacts within the exported contacts file.

        The following are the plans based on the test case:
         case1: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0", "LOCKER_PLAN", "PitneyTrack_Pro"]
         case2: ["SENDING_PLAN", "PITNEYSHIP_PRO", "LOCKER_PLAN", "FIREBALL_2.0"]
         case3: ["SENDING_PLAN", "PITNEYSHIP_PRO", "LOCKER_PLAN", "TRACKING_PLAN"]
         case4: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0","SMS_NOTIFICATION_PLAN"]
         case5: ["SENDING_PLAN", "PITNEYSHIP_PRO", "FIREBALL_2.0"]
         case6: ["SENDING_PLAN", "PITNEYSHIP_PRO", "TRACKING_PLAN"]
         case7: ["PITNEYSHIP_PRO", "TRACKING_PLAN"]
         case8: ["PITNEYSHIP_PRO", "LOCKER_PLAN"]
         case9: ["PITNEYSHIP_PRO", "FIREBALL_2.0"]
         case10: ["PITNEYSHIP_PRO", "SENDING_PLAN"]

        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        sub_type = 'PITNEYSHIP_PRO'
        is_admin = False

        with open(self.prop.get('ADDRESSBOOK_MGMT', f'{plan_case}_exp_dynamic_addressbook_import_fields_list')) as f1:
            exp_dynamic_addressbook_import_fields_list = json.load(f1)

        # Retrieving the subs plans and updating subscription with dynamic template subs plans
        sub_id, email, pwd, ent_id, plans, csv_headers = resource['addressbook_api'] \
            .get_required_details_for_dynamic_template(sub_type=sub_type, plan_case=plan_case, user_type=admin_level)

        self.log.info(f'Sub ID: {sub_id}, Ent ID: {ent_id}, User: {email} | {pwd}, Plans: {plans}')

        # Update subscription with the defined case plans
        resource['subscription_api'] \
            .update_plans_in_subscription(is_admin=True, ent_id=ent_id[0], sub_id=sub_id, plans=plans)

        # Generate user access token
        user_token = resource['login_api'].get_access_token_for_user_credentials(username=email, password=pwd)

        # import of the contacts based on the plan
        sample_import_fields_resp = resource['addressbook_api'] \
            .get_sample_import_fields_api(is_admin=is_admin, sub_id=sub_id, client_token=user_token)

        assert_that(self.validate_response_template(sample_import_fields_resp, exp_dynamic_addressbook_import_fields_list, 200))

        # Delete existing contacts
        resource['addressbook_api'].delete_all_contacts(is_admin=is_admin, sub_id=sub_id, client_token=user_token)

        # Generating contacts import csv file based on the plans
        resource['addressbook_api'] \
            .import_contacts_for_dynamic_template(import_file_case=plan_case, plan_headers=csv_headers,
                                                  is_admin=is_admin, sub_id=sub_id, client_token=user_token)

        import_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', f'{plan_case}_dynamic_addressbook_import_file')
        export_csv_filepath = self.prop.get('ADDRESSBOOK_MGMT', 'dynamic_template_contacts_exported_data')

        resource['addressbook_api'] \
            .export_contacts_check_status_and_download_export_file(sub_id=sub_id, is_admin=is_admin,
                                                                   client_token=user_token,
                                                                   export_csv_filepath=export_csv_filepath)

        assert_that(self.compare_csv_rows(source_file=import_csv_filepath,
                                          target_file=export_csv_filepath, skip_header=True))
