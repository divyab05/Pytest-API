import inspect
import json
import os
import random
import pytest
import logging
import csv
from hamcrest import assert_that

from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.cost_account_api import CostAccountManagement
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities import Crypt
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string, get_current_timestamp


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    data_generator = {
        'app_config': app_config,
        'subscription_api': SubscriptionAPI(app_config, generate_access_token, client_token),
        'login_api': LoginAPI(app_config),
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'clientmgmt_api': ClientManagementAPI(app_config, generate_access_token, client_token),
        'account_mgmt': CostAccountManagement(app_config, generate_access_token, client_token),
        'data_generator': DataGenerator(app_config)
    }
    yield data_generator


@pytest.mark.usefixtures('initialize')
class TestUserSubscriptionManagementAPI(common_utils):
    """
    The test class to place all the tests of User subscription management APIs.
    """

    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        """
        The initialize method for the test class - TestUserSubscriptionManagementAPI.

        :param app_config: The application configuration to get the environment and project name details.
        :param resource: The resource required for the api requests.
        """
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.env = str(self.app_config.env_cfg['env']).lower()

    @pytest.mark.spss_data_generator
    @pytest.mark.parametrize('admin_level', ['E', 'D', 'L', 'User'])
    def test_create_n_subs_users_in_a_subscription(self, resource, admin_level):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        sub_id = '8735'
        n = 1

        ent_name = 'Sohail MFA Enabled Email 1'
        division_id = '6L0j97xdW7V'
        location_id = 'xz6dj0mPy08'
        ent_id = ['5926']
        subs_role_ids = ['USER']

        for i in range(0, n):
            fname = 'PyAuto' + str(i+1)
            lname = '.MFAE.qa.sub1.' + str(random.randint(1, 999))
            dispname = str(fname + lname)
            mailid = str(dispname + "@yopmail.net")
            #mailid = str(dispname + "@yopmail.com")
            password = "Horizon#123"

            resource['subscription_api']\
                .create_active_subs_user(sub_id=sub_id, admin_level=admin_level, fname=fname, lname=lname,
                                         dispname=dispname, mailid=mailid, password=password, ent_name=ent_name,
                                         division_id=division_id, location_id=location_id, ent_id=ent_id,
                                         subs_role_ids=subs_role_ids)

    @pytest.mark.spss_data_generator
    @pytest.mark.create_active_subs_users
    #@pytest.mark.parametrize('admin_level', ['E', 'D', 'L', 'User'])
    @pytest.mark.parametrize('admin_level', ['E',])
    def test_create_n_active_subs_users(self, resource, admin_level):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        ent_name = 'Sohail PSE ConsType 2 PPD Ent3'
        sub_id = '4Wr5JBk99kN'
        ent_id = ['zBlOQNXaBZ4']
        division_id = ['Wq2vRl61n8N']
        location_id = 'RyYVPEakQOxP7W6'
        sub_role_id = ['ADMIN']

        if admin_level == 'User':
            sub_role_id = ['USER']

        n = 1
        self.log.info(f'Creating {n} active users in the Ent - {ent_name}, sub_id - {sub_id}')

        for i in range(0, n):
            first_name = generate_random_string(uppercase=False, digits=False, char_count=5)
            last_name = generate_random_string(uppercase=False, digits=False, char_count=5)
            disp_name = str(first_name) + str(last_name)
            adm = str(admin_level).lower()
            email = f'{first_name}.{adm}{i}@yopmail.com'
            password = 'Horizon#123'

            resource['subscription_api'] \
                .create_active_subs_user(sub_id=sub_id, admin_level=admin_level, fname=first_name, lname=last_name,
                                         dispname=disp_name, mailid=email, password=password, ent_name=ent_name,
                                         division_id=division_id, location_id=location_id, ent_id=ent_id,
                                         subs_role_ids=sub_role_id)
            self.log.info(f'Created {i} active users in the Ent - {ent_name}, sub_id - {sub_id}!!!')

    @pytest.mark.spss_data_generator
    @pytest.mark.create_active_subs_users
    def test_activate_invited_subs_users(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        sub_id = 'sa59b7d'
        ent_id = ['ent_auto_sa59b7d']
        sub_role_id = ['ADMIN']

        # user_id, email, pwd, fname, lname, disp_name = (
        #     resource['subscription_api'].retrieve_user_credentials_from_ent(sub_id=sub_id, ent_id=ent_id, user_status='INVITED'))

        pwd = 'Horizon#123'

        users = resource['subscription_api'].users_advance_search_api(sub_id=sub_id, ent_id=ent_id, status='INVITED', is_admin=True)
        users_data = users.json().get('usersDetailWithSubLocation')
        if users_data:
            for user in users_data:
                if user['detail']['active'] and user['subLocation']['status'] == 'INVITED':
                    user_id = user['detail']['id']
                    email = user['detail']['profile']['email']
                    fname = user['detail']['profile']['firstName']
                    lname = user['detail']['profile']['lastName']
                    disp_name = user['detail']['profile']['displayName']

                    resource['login_api'].check_user_login_status(email, pwd)
                    (resource['subscription_api']
                     .patch_update_subs_user_details_by_user_id_api(user_id=user_id, sub_id=sub_id, fname=fname, lname=lname,
                                                                       disp_name=disp_name, subs_roles=sub_role_id))

                    self.log.info(f'Email: {email}, UserId: {user_id}, SubId: {sub_id}')

    @pytest.mark.spss_data_generator
    @pytest.mark.create_invited_subs_users
    @pytest.mark.parametrize('admin_level', ['E', 'D', 'L', 'User'])
    def test_create_invited_subs_users(self, resource, admin_level):

        ent_name = 'SPSS Perf Testing (sac0afa)'
        sub_id = 'sac0afa'
        ent_id = ['x86JnMpB6n5']
        division_id = ['VPjq60WM4Bd']
        location_id = 'BKjZm3nmY2V'
        sub_role_id = ['ADMIN']

        if admin_level == 'User':
            sub_role_id = ['USER']

        n = 1000
        self.log.info(f'Creating {n} invited users in the Ent - {ent_name}, sub_id - {sub_id}')

        for i in range(0, n):
            first_name = generate_random_string(uppercase=False, digits=False, char_count=5)
            last_name = generate_random_string(uppercase=False, digits=False, char_count=5)
            disp_name = str(first_name) + str(last_name)
            adm = str(admin_level).lower()
            email = f'{first_name}.{adm}{i}@yopmail.com'
            password = 'Horizon#123'

            resource['subscription_api'].create_invited_subs_user(sub_id=sub_id, admin_level=admin_level,
                                                                  fname=first_name, lname=last_name, dispname=disp_name,
                                                                  mailid=email, password=password,
                                                                  subs_role_ids=sub_role_id, ent_name=ent_name, ent_id=ent_id,
                                                                  division_id=division_id, location_id=location_id)

            self.log.info(f'Created {i} invited users in the Ent - {ent_name}, sub_id - {sub_id}!!!')

    @pytest.mark.spss_data_generator
    def test_generate_address_book_import_file(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        n = 1  # number of records

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            filename = '/reports/' + str(i) + '_generated_address_book_import_' + str(n) + 'records_' \
                       + str(random.randint(1, 99999)) + '.csv'
            file_path = os.getcwd() + filename

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    ['Name', 'Company', 'Email', 'Phone', 'Street Address 1', 'Street Address 2', 'Street Address 3',
                     'City', 'State/Province', 'Postal/ZIP Code', 'Country', 'InternalDelivery', 'PersonalID',
                     'OfficeLocation', 'MailStopID', 'Accessibility', 'NotificationAll', 'PrimaryLocation',
                     'AdditionalEmailIds'])

                for _ in range(n):
                    writer.writerow(resource['data_generator'].address_book_data_setter())
            self.log.info(f'{i}. Generated Address book import file: {filename}')



    @pytest.mark.spss_data_generator
    def test_generate_user_import_file(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        n = 6800  # number of records

        for i in range(20, 41):  # range(1, 2) > generates 1 import file
            filename = '/reports/' + str(i) + '_generated_user_import_' + str(n) + 'records_' \
                       + str(random.randint(1, 99999)) + '.csv'
            file_path = os.getcwd() + filename

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['First Name', 'Last Name', 'E-Mail', 'Role', 'Division', 'BPN', 'Location',
                                 'Company Name', 'Customer Address', 'City', 'State', 'Country', 'Zip', 'Phone',
                                 'Default Cost Account'])

                for _ in range(n):
                    writer.writerow(resource['data_generator'].user_data_setter())
            self.log.info(f'{i}. Generated user import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_user_import_with_file_size(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        size = 1  # target file size

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            filename = '/reports/' + str(i) + '_generated_user_import_' + str(size) + 'MB_' \
                       + str(random.randint(1, 99999)) + '.csv'
            file_path = os.getcwd() + filename

            target_size = size * 1024 * 1024  # target file size in bytes

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['First Name', 'Last Name', 'E-Mail', 'Role', 'Division', 'BPN', 'Location',
                                 'Company Name', 'Customer Address', 'City', 'State', 'Country', 'Zip', 'Phone',
                                 'Default Cost Account'])

                file_size = os.path.getsize(file_path)

                while file_size < target_size:

                    for _ in range(999999):
                        writer.writerow(resource['data_generator'].user_data_setter())

                        file_size = os.path.getsize(file_path)

                        if file_size >= target_size:
                            break
            self.log.info(f'{i}. Generated user import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_bulk_import_contacts_using_generated_files(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        sub_ids = []
        for i in range(1, 30):  # range(1, 2) >> creates 1 enterprise and subscription
            ent_name = 'SPSS UserImport ' + str(i)
            ent_id = str(random.randint(1, 9999))
            sub_id = str(random.randint(1, 9999))
            resource['clientmgmt_api'].add_enterprise_api(ent_id=ent_id, name=ent_name)
            resource['subscription_api'].create_subscription_api(sub_id=sub_id, ent_id=ent_id)
            sub_ids.append(sub_id)

        self.log.info(f'Created enterprises and subscriptions - {sub_ids}')

        data_directory = os.getcwd() + '/TestData/shared_services/generated_test_data'

        for j in range(0, len(os.listdir(data_directory))):
            # print(os.listdir(data_directory)[j])
            # print(sub_ids[j])
            file_path = data_directory + '/' + os.listdir(data_directory)[j]
            self.log.info(f'Using address book import file - {os.listdir(data_directory)[j]} for Subs {sub_ids[j]}')
            resource['addressbook_api'].import_contacts_process_and_check_status(file_path=file_path, sub_id=sub_ids[j])

    @pytest.mark.spss_data_generator
    def test_generate_alm_cost_account_import_file(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        n = 80000  # number of records

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            timestamp = get_current_timestamp(fmt='%m%d%H%M%S')
            filename = f'/reports/{timestamp}_generated_alm_cost_acct_{n}records_{i}.csv'
            file_path = os.getcwd() + filename

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Code', 'Description', 'PasswordEnabled', 'PasswordCode', 'Status',
                                 'ParentName', 'NextParentName', 'Billable'])
                # rows = [resource['data_generator'].cost_account_data_setter() for _ in range(n)]
                # writer.writerows(rows)
                for _ in range(n):
                    account_data = resource['data_generator'].cost_account_data_setter()
                    if account_data:  # Check if the account data is not None
                        writer.writerow(account_data)
            self.log.info(f'{i}. Generated ALM Cost Account Import file: {filename}')

    @pytest.mark.spss_data_generator
    # @pytest.mark.parametrize('admin_level, status',
    #                          [('E', 'ACTIVE'), ('E', 'INACTIVE'), ('E', 'INVITED'),
    #                           ('D', 'ACTIVE'), ('D', 'INACTIVE'), ('D', 'INVITED'),
    #                           ('L', 'ACTIVE'), ('L', 'INACTIVE'), ('L', 'INVITED'),
    #                           ('User', 'ACTIVE'), ('User', 'INACTIVE'), ('User', 'INVITED')])
    @pytest.mark.parametrize('admin_level, status',
                             [('E', 'ACTIVE'), ('D', 'ACTIVE'), ('L', 'ACTIVE'), ('User', 'ACTIVE')])
    # @pytest.mark.parametrize('admin_level, status', [('E', 'ACTIVE')])
    def test_create_different_types_of_subs_users(self, resource, admin_level, status):
        sub_id = '2794'
        ent_name = 'API Automation'
        ent_id = ['9685']
        div_id = ['GBd08nxz7Yj']
        loc_id = 'n847LM8qdAk'
        sub_role_id = ['ADMIN']
        if admin_level == 'User':
            sub_role_id = ['USER']

        # first_name = generate_random_string(uppercase=False, digits=False, char_count=5)
        first_name = f'{sub_id}_Auto_{generate_random_string(uppercase=False, digits=False, char_count=5)}'
        last_name = generate_random_string(uppercase=False, digits=False, char_count=5)
        disp_name = f'{str(first_name)} {str(last_name)}'
        adm = str(admin_level).lower()
        sts = str(status).lower()
        # email = str(first_name) + '.' + adm + '.' + sts + '@yopmail.com'
        email = f'{str(first_name)}.{self.env}.{adm}1@yopmail.com'
        password = 'Horizon#123'

        if status == 'ACTIVE':
            # resource['subscription_api']\
            #     .create_active_subs_user(sub_id=sub_id, admin_level=admin_level, fname=first_name, lname=last_name,
            #                              dispname=disp_name, mailid=email, password=password)

            resource['subscription_api']\
                .create_active_subs_user(sub_id=sub_id, admin_level=admin_level, fname=first_name, lname=last_name,
                                         dispname=disp_name, mailid=email, password=password, ent_name=ent_name,
                                         division_id=div_id, location_id=loc_id, ent_id=ent_id,
                                         subs_role_ids=sub_role_id)

        elif status == 'INACTIVE':
            fname, lname, mailid, dispname, password, user_id, ent_id, loc_id, carrier_accounts, subs_role_ids = \
                resource['subscription_api'].create_active_subs_user(sub_id=sub_id, admin_level=admin_level,
                                                                     fname=first_name, lname=last_name,
                                                                     dispname=disp_name, mailid=email, password=password)

            resource['subscription_api']\
                .change_active_status_for_subs_user_by_user_id_api(user_id=user_id, active_flag=False, sub_id=sub_id,
                                                                   fname=first_name, lname=last_name,
                                                                   disp_name=disp_name, email=email)
        elif status == 'INVITED':
            resource['subscription_api'].create_invited_subs_user(sub_id=sub_id, admin_level=admin_level,
                                                                  fname=first_name, lname=last_name, dispname=disp_name,
                                                                  mailid=email, password=password)

    @pytest.mark.spss_data_generator
    def test_hard_delete_users_in_subs(self, resource):
        sub_id = 'sa8abca'
        user_status = 'INVITED'
        ent_user = 'adminuiautomation01@yopmail.com'

        # users = resource['subscription_api'].get_users_api(is_admin=True, sub_id=sub_id, limit='100')
        users = resource['subscription_api'].users_advance_search_api(is_admin=True, sub_id=sub_id, limit='100', status=user_status)

        # is_admin=False, sub_id=None, ent_id=None, skip='0', limit='10', archive='false',
        #                                  status='ACTIVE', payload=None, admin_token='', client_token=''
        users_data = users.json().get('usersDetailWithSubLocation')
        if users_data:
            for user in users_data:
                retrieved_user_status = user['subLocation']['status']
                if retrieved_user_status == user_status:
                    user_id = user['detail']['id']
                    user_email = user['detail']['profile']['email']
                    if user_email != ent_user:
                        resource['subscription_api'].delete_user_api(sub_id=sub_id, user_id=user_id, is_admin='y')
                        self.log.info(f'Deleted user - {user_email} of status - {retrieved_user_status}!!!')

    @pytest.mark.spss_data_generator
    def test_hard_delete_all_users_in_subs(self, resource):
        sub_id = 'sa8abca'
        user_status = 'INACTIVE'
        ent_user = 'adminuiautomation01@yopmail.com'
        page = 0
        page_size = 100  # Adjust the page size as needed
        limit = 100

        while True:
            users = resource['subscription_api'].users_advance_search_api(
                is_admin=True,
                sub_id=sub_id,
                limit=limit,
                skip=page * page_size,
                status=user_status
            )

            users_data = users.json().get('usersDetailWithSubLocation', [])
            if not users_data:
                self.log.info(f'No users data found.')
                break

            for user in users_data:
                retrieved_user_status = user['subLocation']['status']
                if retrieved_user_status == user_status:
                    user_id = user['detail']['id']
                    user_email = user['detail']['profile']['email']
                    if user_email != ent_user:
                        resource['subscription_api'].delete_user_api(sub_id=sub_id, user_id=user_id, is_admin='y')
                        self.log.info(f'Deleted user - {user_email} of status - {retrieved_user_status}!!!')

            # Increment page for the next iteration
            page += 1

    @pytest.mark.spss_data_generator
    def test_split_csv_records(self):
        input_file = self.prop.get('ADDRESSBOOK_MGMT', 'bofa_cost_account_file')
        output_file = self.prop.get('ADDRESSBOOK_MGMT', 'bofa_splitted_cost_account_file')

        rows = []

        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        modified_rows = []  # New list to hold modified rows

        for row in rows:
            split_values = row[0].split("-")
            modified_rows.append(split_values)  # Add modified row to the list

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(modified_rows)  # Write the modified rows to the output file

    @pytest.mark.spss_data_generator
    def test_delete_all_sso_users_mappings(self, resource):

        sub_id = 'sa81ce4'

        get_sso_users_mappings_resp = resource['subscription_api']\
            .get_sso_users_mappings_api(is_admin=True, sub_id=sub_id)
        assert_that(self.validate_response_code(get_sso_users_mappings_resp, 200))

        user_mappings = get_sso_users_mappings_resp.json()['federatedUserMapping']

        total_count = get_sso_users_mappings_resp.json()['pageInfo']['totalCount']
        self.log.info(f'Total sso users mappings: {total_count}')

        while total_count != 0:
            for user_mapping in user_mappings:
                fed_user_mapping_id = user_mapping['fedUserMappingID']
                uid = user_mapping['uid']
                loc_id = user_mapping['locationID']
                loc_name = user_mapping['locationName']
                role_id = user_mapping['roleID']
                role_name = user_mapping['roleName']

                del_resp = resource['subscription_api']\
                    .delete_sso_users_mappings_api(is_admin=True, sub_id=sub_id, fed_user_mapping_id=fed_user_mapping_id,
                                                   uid=uid, loc_id=loc_id, loc_name=loc_name, role_id=role_id,
                                                   role_name=role_name, archived=True)

                assert_that(self.validate_response_code(del_resp, 201))
                self.log.info(f'Archived sso user mapping for uid - {uid}')

    @pytest.mark.spss_data_generator
    def test_generate_sso_users_mappings_data(self):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        size = 10  # target file size

        headers = ['UID', 'Role', 'Division', 'BPN', 'Location', 'Company Name', 'Customer Address', 'City',
                   'State', 'Country', 'Zip', 'Phone', 'DefaultCostCentre', 'Archive']

        # SSO Ent2 for Platform (sa81ce4)
        data = [
            ['1-ssouser50K@example.com', 'ADMIN', 'Default', '16726220', 'D2-L2-Test', 'Custom Location',
             '243 Hall Place', 'Longview', 'TX', 'US', '75601', '6666768712', 'Test CA 001', 'FALSE'],
            ['2-ssouser50K@example.com', 'Test_Dash', 'TestD1', '13175228', 'Sohail Fremont Address',
             'VA MEDICAL CENTER', '27 Waterview Dr', 'Orland Park', 'CT', 'US', '60462', '9517429463',
             'Test CA 002', 'FALSE']
        ]

        # SPSS SSO PB.Com (sa84676)
        # data = [
        #     ['1-ssouser@platform.com', 'ADMIN', 'Default', '0016726220', 'Default', 'SPSS SSO PB.Com',
        #      '243 Hall Place', 'Longview', 'TX', 'US', '75601', '6666768712', 'PB CA Parent 001', 'FALSE'],
        #     ['2-ssouser@platform.com', 'Regular User', 'Default', '0013461262', 'Calgary',
        #      'ABC', '170-2880 GLENMORE TRAIL SE', 'CALGARY', 'AL', 'CA', 'T2C 2E7', '9517429463',
        #      'PB CA Parent 002', 'FALSE']
        # ]

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            filename = f'/reports/sa84676_generated_sso_users_mappings_{size}MB_{random.randint(1, 99999)}.csv'
            file_path = os.getcwd() + filename

            uid_start = 1  # Start UID number
            target_size = size * 1024 * 1024  # target file size in bytes

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                file_size = os.path.getsize(file_path)

                while file_size < target_size:
                    for row in data:
                        row[0] = f'{uid_start}-ssouser@example.com'
                        #row[0] = f'{uid_start}-ssouser@platform.com'
                        writer.writerow(row)

                        uid_start += 1

                        file_size = os.path.getsize(file_path)

                        if file_size >= target_size:
                            break

            self.log.info(f'{i}. Generated SSO Users Mappings csv file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_auto_import_cost_accounts_file(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        n = 10000  # number of records

        for i in range(1, 11):  # range(1, 2) > generates 1 import file
            filename = f'/reports/{i}_generated_alm_cost_acct_{n}records_{random.randint(1, 99999)}.csv'
            file_path = os.getcwd() + filename

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Code', 'Description', 'PasswordEnabled', 'PasswordCode', 'Status',
                                 'ParentName', 'NextParentName', 'Billable', 'AccessLevel', 'AccessLevelValue',
                                 'DivisionName'])
                rows = [resource['data_generator'].auto_import_cost_account_data_setter() for _ in range(n)]
                writer.writerows(rows)
            self.log.info(f'{i}. Generated ALM Cost Account Import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_cost_account_import_file_with_size(self):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        size = 1  # target file size

        headers = ['Name', 'Code', 'Description', 'PasswordEnabled', 'PasswordCode', 'Status', 'ParentName',
                   'NextParentName', 'Billable', 'AccessLevel', 'AccessLevelValue', 'DivisionName']

        access_level = random.choice(['E', 'D', 'L', ''])
        access_lvl_value = ''
        div_name = ''

        if access_level == 'L':
            access_lvl_value = 'Default'
            div_name = 'Default'

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            filename = f'/reports/sa81ce4_generated_sso_users_mappings_{size}MB_{random.randint(1, 99999)}.csv'
            file_path = os.getcwd() + filename

            target_size = size * 1024 * 1024  # target file size in bytes

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                file_size = os.path.getsize(file_path)

                while file_size < target_size:
                    row_data = [resource['data_generator'].cost_account_data_setter(access_level=access_level,
                                                                               access_lvl_value=access_lvl_value,
                                                                               div_name=div_name) for _ in range(999999)]
                    writer.writerow(row_data)

                    file_size = os.path.getsize(file_path)

                    if file_size >= target_size:
                        break

            self.log.info(f'{i}. Generated Cost Accounts Import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_unique_alm_cost_account_import_file(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        n = 5000  # number of records

        account_names = set()
        account_codes = set()

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            timestamp = get_current_timestamp(fmt='%m%d%H%M%S')
            filename = f'/reports/{timestamp}_generated_alm_cost_acct_{n}records_{i}.csv'
            file_path = os.getcwd() + filename

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Code', 'Description', 'PasswordEnabled', 'PasswordCode', 'Status',
                                 'ParentName', 'NextParentName', 'Billable'])
                for _ in range(n):
                    account_data = resource['data_generator'].cost_account_data_setter()
                    name, code = account_data[0], account_data[1]
                    while name in account_names or code in account_codes:
                        # If the name or code is not unique, regenerate the data
                        account_data = resource['data_generator'].cost_account_data_setter()
                        name, code = account_data[0], account_data[1]
                    account_names.add(name)
                    account_codes.add(code)
                    writer.writerows([account_data])

            self.log.info(f'{i}. Generated ALM Cost Account Import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_unique_cost_account_import_file_with_size(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        size = 2  # target file size

        account_names = set()
        account_codes = set()

        for i in range(1, 2):  # range(1, 2) > generates 1 import file
            timestamp = get_current_timestamp(fmt='%m%d%H%M%S')
            filename = f'/reports/{timestamp}_generated_alm_cost_acct_{size}MB_{i}.csv'
            file_path = os.getcwd() + filename

            target_size = size * 1024 * 1024  # target file size in bytes

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Code', 'Description', 'PasswordEnabled', 'PasswordCode', 'Status',
                                 'ParentName', 'NextParentName', 'Billable'])

                file_size = os.path.getsize(file_path)

                while file_size < target_size:

                    for _ in range(999999):
                        account_data = resource['data_generator'].cost_account_data_setter()
                        name, code = account_data[0], account_data[1]
                        while name in account_names or code in account_codes:
                            # If the name or code is not unique, regenerate the data
                            account_data = resource['data_generator'].cost_account_data_setter()
                            name, code = account_data[0], account_data[1]
                        account_names.add(name)
                        account_codes.add(code)
                        writer.writerows([account_data])

                        file_size = os.path.getsize(file_path)

                        if file_size >= target_size:
                            break

            self.log.info(f'{i}. Generated ALM Cost Account Import file: {filename}')

    @pytest.mark.spss_data_generator
    def test_convert_json_response_into_csv(self):

        # Read the JSON file
        with open(self.prop.get('COMMON_SHARED_SERVICES', 'retrieved_non_sso_admin_users_pbcom_list'), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)

        # Collect all unique keys from the JSON data
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        # Convert JSON data to CSV
        filename = f'/reports/converted_csv_file_{random.randint(1, 99999)}.csv'
        file_path = os.getcwd() + filename
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(all_keys)  # Write header

            for row in data:
                csvwriter.writerow([row.get(key, '') for key in all_keys])

        # Count the data rows
        data_row_count = len(data)

        # Print the count and filename
        self.log.info(f"Number of data rows: {data_row_count} added in the file - {filename}")

    @pytest.mark.spss_data_generator
    def test_convert_json_response_into_csv_and_include_only_pb_com_users(self):
        # Read the JSON file
        with open(self.prop.get('COMMON_SHARED_SERVICES', 'retrieved_non_sso_admin_users_pbcom_list'), 'r',
                  encoding='utf-8') as f:
            data = json.load(f)

        domain = "@pb.com"
        all_keys = set()

        # Collect all unique keys from the JSON data
        for item in data:
            all_keys.update(item.keys())
            if "profile" in item:
                all_keys.update(item["profile"].keys())

        filename = f'/reports/converted_csv_file_{random.randint(1, 99999)}.csv'
        file_path = os.getcwd() + filename

        # Filter the data and write to CSV
        filtered_data = [user for user in data if
                         "profile" in user and "email" in user["profile"] and domain in user["profile"]["email"]]

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(all_keys)  # Write header

            for user in filtered_data:
                row = []
                for key in all_keys:
                    if key in user:
                        row.append(user[key])
                    elif "profile" in user and key in user["profile"]:
                        row.append(user["profile"][key])
                    else:
                        row.append('')
                csvwriter.writerow(row)

        # Count the filtered data rows
        data_row_count = len(filtered_data)

        # Print the count and filename
        self.log.info(f"Number of data rows: {data_row_count} added in the file - {filename}")

    @pytest.mark.spss_data_generator
    def test_encrypt_and_decrypt_string(self, input_string=None):
        input_string = "Basic c3VwZXJ1c2VyOkhPVFNJWEpFS0x2dFRMV25tTUk5SG05ZmpIbHJ0dkpHSkZsWVpwaFc="

        encrypted_value = Crypt.encode("DBENCRYPTIONKEY", input_string)
        decrypted_value = Crypt.decode("DBENCRYPTIONKEY", encrypted_value)

        self.log.info(encrypted_value)
        self.log.info(decrypted_value)

        return encrypted_value, decrypted_value

    @pytest.mark.spss_data_generator
    def test_prepare_client_users_list_from_json_file(self, resource):
        self.log.info(f'###### TEST EXECUTION STARTED :: {inspect.currentframe().f_code.co_name} ######')

        with open(self.prop.get('COMMON_SHARED_SERVICES', 'client_users_list')) as file:
            client_users_list = json.load(file)

        users_data = client_users_list['usersDetailWithSubLocation']

        self.log.info(f"Total users available in the json file: {len(users_data)}")

        user_row_data = []

        for user in users_data:
            detail = user.get('detail', {})
            profile = detail.get('profile', {})
            uid = detail.get('id', '')
            if profile:
                email = profile.get('email', '')
                user_type = "Non-SSO"
            else:
                email = uid
                user_type = "SSO"
            user_row_data.append({'uid': uid, 'email': email, 'user_type': user_type})

        # Sort user_rows by user_type
        user_row_data.sort(key=lambda x: x['user_type'])

        # Convert JSON data to CSV
        timestamp = get_current_timestamp(fmt='%m%d%H%M%S')
        filename = f'/reports/prepared_users_list_{timestamp}.csv'
        file_path = os.getcwd() + filename
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['userID', 'Email', 'User Type'])
            for row in user_row_data:
                csvwriter.writerow(row.values())
        self.log.info(f'Generated CSV file: {filename}')

    @pytest.mark.spss_data_generator
    def test_convert_json_file_into_csv_file(self):

        # Read the JSON file
        with open(self.prop.get('COMMON_SHARED_SERVICES', 'client_sso_users_mapping_list')) as f:
            data = json.load(f)

        # Convert JSON data to CSV
        timestamp = get_current_timestamp(fmt='%m%d%H%M%S')
        filename = f'/reports/converted_client_sso_users_mapping_list_{timestamp}.csv'
        file_path = os.getcwd() + filename
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            header = data['federatedUserMapping'][0].keys()
            csvwriter.writerow(header)
            for row in data['federatedUserMapping']:
                csvwriter.writerow(row.values())

        # Count the data rows
        data_row_count = len(data)

        self.log.info(f"Number of data rows: {data_row_count}")
        self.log.info(f'Generated CSV file: {filename}')

    @pytest.mark.spss_data_generator
    def test_generate_db_update_script_from_csv_file(self):

        # Read the JSON file
        with open(self.prop.get('COMMON_SHARED_SERVICES', 'cost_account_parent_name_data_file')) as csv_file:
            csv_reader = csv.DictReader(csv_file)

            filename = f'/reports/cost_accounts_parent_name_generated_db_script.txt'
            text_file_path = os.getcwd() + filename

            with open(text_file_path, 'w') as text_file:
                for row in csv_reader:
                    sub_id = row['subID']
                    parent = row['parent']
                    parent_name = row['parentName']

                    db_command = (f'db.account.updateOne({{subID:"{sub_id}", parent:"{parent}"}}, '
                                  f'{{$set:{{parentName:"{parent_name}"}}}})\n')
                    text_file.write(db_command)
