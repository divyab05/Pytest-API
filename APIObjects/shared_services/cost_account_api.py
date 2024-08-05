"""This module is used for main page objects."""
import json
import logging
import random
import time
import pandas as pd
from hamcrest import equal_to
from hamcrest.core import assert_that
import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility


class CostAccountManagement:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.access_token = access_token
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.login = LoginAPI(app_config)
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['costactmgmt_api'])
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.headers = {"Accept": "*/*"}

        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

        with open(self.prop.get('COST_ACCT_MGMT', 'alm_sample_test_data')) as f1:
            self.alm_sample_test_data = json.load(f1)

        with open(self.prop.get('COST_ACCT_MGMT', 'body_path_create_account')) as f2:
            self.body_path_create_account = json.load(f2)

        with open(self.prop.get('COST_ACCT_MGMT', 'add_cost_acct_dialog_request')) as f3:
            self.add_cost_acct_dialog_request = json.load(f3)

        with open(self.prop.get('COST_ACCT_MGMT', 'advance_search_cost_acct_request')) as f4:
            self.advance_search_cost_acct_request = json.load(f4)

        with open(self.prop.get('COST_ACCT_MGMT', 'update_cost_account_request')) as f5:
            self.update_cost_acct_request = json.load(f5)

    @staticmethod
    def generate_cost_account_data():
        cost_acc_name = "ALM_CA_" + str(random.randint(1, 9999))
        cost_acc_code = "ALM_CD_" + str(random.randint(1, 9999))
        cost_acc_id = "ALM_ID_" + str(random.randint(1, 9999))

        return cost_acc_name, cost_acc_code, cost_acc_id

    def get_alm_subscription_id_from_file(self):
        alm_sub_id = self.alm_sample_test_data[self.env]['almSubId']
        return alm_sub_id

    def get_alm_enterprise_id_from_file(self):
        alm_ent_id = self.alm_sample_test_data[self.env]['almEnterprise']
        return alm_ent_id

    def get_alm_divisions_from_file(self):
        div_list = self.alm_sample_test_data[self.env]['almDivisionId']
        return div_list

    def get_alm_locations_from_file(self):
        loc_list = self.alm_sample_test_data[self.env]['almLocations']
        return loc_list

    def get_test_data_from_file(self):
        alm_sub_id = self.alm_sample_test_data[self.env]['almSubId']
        alm_ent_id = self.alm_sample_test_data[self.env]['almEnterprise']
        div_list = self.alm_sample_test_data[self.env]['almDivisionId']
        loc_list = self.alm_sample_test_data[self.env]['almLocations']
        return alm_sub_id, alm_ent_id, div_list, loc_list

    def get_sub_id_user_cred_from_cost_acct_file(self, sub_type='PITNEYSHIP_PRO', user_type='E'):
        """
        Retrieves the subscription ID and user credentials from an cost account management JSON file.
        :param sub_type: The type of subscribed product. ex: PITNEYSHIP_PRO
        :param user_type: The type of client users. ex: Enterprise, Division, Location and User.
        :return: The subscription ID corresponding to the provided subscription type.
        """

        with open(self.prop.get('COST_ACCT_MGMT', 'sample_cost_acct_subs_all_details')) as file:
            json_data = json.load(file)

        data = json_data[self.prod_name][self.env][sub_type]
        sub_id = data['sub_id']
        email = None
        pwd = None

        if user_type == 'E' or not user_type:
            email = data['ent_user']
            pwd = data['ent_pwd']
        elif user_type == 'D':
            email = data['div_user']
            pwd = data['div_pwd']
        elif user_type == 'L':
            email = data['loc_user']
            pwd = data['loc_pwd']
        elif user_type == 'User' or user_type == 'U':
            email = data['user']
            pwd = data['user_pwd']

        return sub_id, email, pwd

    def get_cost_accounts_search_api(self, parent='', page='0', limit='20', sub_id='', is_admin='y', status='true'):
        """
        This function fetches details of cost accounts
        :return: this function returns response and status code
        """
        query_params = "?parent=" + parent + "&skip=" + page + "&limit=" + limit + "&status=" + status

        if is_admin == 'y':
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts" + query_params
            self.headers['Authorization'] = self.admin_token

        else:
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/costAccounts" + query_params
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_cost_accounts_endpoint, headers=self.headers)
        return response

    def get_cost_accounts_by_sub_id_user_id_api(self, sub_id, page='0', limit='10', status='true', is_admin='', user_id='', query=''):
        """
        This function fetches details of cost accounts as per the subId
        :return: this function returns response and status code
        """
        query_params = "?skip=" + page + "&limit=" + limit + "&status=" + status + "&" + query
        if is_admin == 'Y':
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts" + query_params
            self.headers['Authorization'] = self.admin_token
        else:
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/costAccounts/" + query_params
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_cost_accounts_endpoint, headers=self.headers)
        return response

    def get_cost_account_by_acct_id_api(self, acct_id='', sub_id='', is_admin=False, token=None):
        """
        This method uses cost account v2 API to fetch the cost account details using account id.

        :param acct_id: The cost account's account id.
        :param sub_id: The subscription id.
        :param is_admin: Admin flag to determine the API is called using admin or client token.
        :param token: The access token generated from an admin or client user credentials.

        :return: It returns response and status code.
        """

        if is_admin:
            get_cost_acct_url = f'{self.endpoint}/api/v2/costAccounts/{acct_id}?subID={sub_id}'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            get_cost_acct_url = f'{self.endpoint}/api/v2/costAccounts/{acct_id}'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.get_api_response(endpoint=get_cost_acct_url, headers=self.headers)
        return response

    def get_cost_account_by_account_id_v1_api(self, acc_id='', is_admin='y'):
        """
        This function fetches details of cost accounts as per the account Id
        :return: this function returns response and status code
        """

        if is_admin == 'y':
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/costAccounts/" + str(acc_id)
            self.headers['Authorization'] = self.admin_token
        else:
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/costAccounts/" + str(acc_id)
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_cost_accounts_endpoint, headers=self.headers)
        return response

    def verify_cost_account_hierarchy_access_level_and_return_extracted_data(self, parent_acct_id='', sub_id='',
                                                                             is_admin=False, token=None):
        """
        This method verifies the access level of sub and sub-sub cost account with its parent cost account.

        :param parent_acct_id: The parent cost account's account id.
        :param sub_id: The subscription id.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses
                         client user. Default is False.
        :param token: The admin or client user access token.

        :return: An extracted_account_data list, parent, sub, and sub-sub cost account access level.
        """

        def extract_cost_account_info(account_data=None):
            """
            This is a recursive method to iterate with the given cost account response data and stores the required
            cost account's parent and its children data and returns it.
            """

            account_info = {
                "accountID": account_data.get('accountID'),
                "name": account_data.get('name'),
                "parentName": account_data.get('parentName'),
                "nextParentName": account_data.get('nextParentName'),
                "accessLevel": account_data.get('permission').get('permissionByEntity')
            }

            result = [account_info]

            if "children" in account_data and account_data['children']:
                for child in account_data['children']:
                    result.extend(extract_cost_account_info(account_data=child))

            return result

        parent_acct_resp = self.get_cost_account_by_acct_id_api(acct_id=parent_acct_id, sub_id=sub_id,
                                                                is_admin=is_admin, token=token)
        assert_that(common_utils.validate_response_code(parent_acct_resp, 200))

        extracted_account_data = extract_cost_account_info(parent_acct_resp.json())

        parent_acct_access_lvl = None
        sub_acct_access_lvl = None
        sub_sub_acct_access_lvl = None

        for data in extracted_account_data:
            if not data.get('parentName'):
                parent_acct_access_lvl = data.get('accessLevel')
            elif data.get('parentName') and not data.get('nextParentName'):
                sub_acct_access_lvl = data.get('accessLevel')
            elif data.get('parentName') and data.get('nextParentName'):
                sub_sub_acct_access_lvl = data.get('accessLevel')

        assert_that(sub_sub_acct_access_lvl, equal_to(sub_acct_access_lvl))
        assert_that(sub_acct_access_lvl, equal_to(parent_acct_access_lvl))

        return parent_acct_resp, extracted_account_data, parent_acct_access_lvl, sub_acct_access_lvl, sub_sub_acct_access_lvl

    def create_parent_child_cost_accounts(self, sub_account=True, sub_sub_account=True, sub_id='', ent_id='',
                                          divisions='', loc_id='', cost_acct_access_level='E', is_admin=False,
                                          token=None):
        """
        Creates a hierarchy of cost accounts (parent, sub, and sub-sub) with specified parameters.

        :param sub_account: Whether to create a sub cost account under the parent account. Default is True.
        :param sub_sub_account: Whether to create a sub-sub cost account under the sub cost account. Default is True.
        :param sub_id: The subscription id.
        :param ent_id: The enterprise id required for cost account when selected access level is 'E'.
        :param divisions: The divisions id required for cost account when selected access level is 'D'.
        :param loc_id: The locations id required for cost account when selected access level is 'L'.
        :param cost_acct_access_level: The access level of the cost account. Default is 'E'.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses
                         client user. Default is False.
        :param token: The admin or client user access token.

        :return: A tuple containing the IDs of the created parent, sub, and sub-sub cost accounts
                       (if created), respectively.

        :raises AssertionError: If the response code for any cost account creation is not 201 (Created).
        """

        wait_time = 10

        def create_cost_account(parent_id=None):
            account_data = DataGenerator.cost_account_data_setter()
            response = self.add_cost_account_api(
                code=account_data[1], name=account_data[0], desc=account_data[2],
                prmsn_by_entity=cost_acct_access_level, billable=account_data[8],
                prmsn_by_value=entity_value, parent=parent_id, sub_id=sub_id,
                is_admin=is_admin, token=token
            )
            assert_that(common_utils.validate_response_code(response, 201))
            account_id = response.json().get('accountID')
            self.log.info(
                f'Created cost account - "{account_data[0]}" with access level "{cost_acct_access_level}" successfully!')
            return account_id

        def get_entity_value():
            if cost_acct_access_level == 'E':
                return ent_id
            elif cost_acct_access_level == 'D':
                return divisions
            elif cost_acct_access_level == 'L':
                return [loc_id]
            return None

        entity_value = get_entity_value()

        created_parent_acct_id = create_cost_account()
        time.sleep(wait_time)  # Sleep after creating the parent account

        created_sub_acct_id = None
        created_sub_sub_acct_id = None

        if sub_account:
            created_sub_acct_id = create_cost_account(parent_id=created_parent_acct_id)
            time.sleep(wait_time)  # Sleep after creating the sub cost account

            if sub_sub_account:
                created_sub_sub_acct_id = create_cost_account(parent_id=created_sub_acct_id)
                time.sleep(wait_time)  # Sleep after creating the sub-sub account

        return created_parent_acct_id, created_sub_acct_id, created_sub_sub_acct_id

    def add_cost_account_api(self, acct_id='', code='', name='', desc='', status=True, prmsn_by_entity='',
                             billable=False, prmsn_by_value=None, parent='', sub_id='', pwd_enabled=False,
                             pwd_code='', budget_amt='', frequency='', budget_notification_enable='',
                             budget_system_alert_enable='', year_begin_month='', year_begin_day='',
                             notification_emails='', notification_numbers='', notification_threshold='',
                             is_admin=False, token=None):
        """
        This method sets up and sends a request to add a cost account using the provided parameters.
        It configures various attributes of the cost account and manages the permissions, budget settings,
        and notification settings.

        :param acct_id: The account ID.
        :param code: The account code.
        :param name: The name of the account.
        :param desc: The description of the account.
        :param status: The status of the account (default is True).
        :param prmsn_by_entity: Permissions by entity.
        :param billable: Whether the account is billable (default is False).
        :param prmsn_by_value: Permissions by value.
        :param parent: The parent account ID.
        :param sub_id: The sub ID.
        :param pwd_enabled: Whether a password is enabled (default is False).
        :param pwd_code: The password code.
        :param budget_amt: The budget amount.
        :param frequency: The frequency of budget notifications.
        :param budget_notification_enable: Whether budget notifications are enabled.
        :param budget_system_alert_enable: Whether budget system alerts are enabled.
        :param year_begin_month: The month the budget year begins.
        :param year_begin_day: The day the budget year begins.
        :param notification_emails: Notification emails.
        :param notification_numbers: Notification phone numbers.
        :param notification_threshold: Notification threshold.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses
                         client user. Default is False.
        :param token: The admin or client user access token.

        :return: The response of the API request (success or failure).
        """
        self.add_cost_acct_dialog_request['name'] = name
        self.add_cost_acct_dialog_request['code'] = code
        self.add_cost_acct_dialog_request['subID'] = sub_id
        self.add_cost_acct_dialog_request['accountID'] = acct_id
        self.add_cost_acct_dialog_request['status'] = status
        self.add_cost_acct_dialog_request['permission']['permissionByEntity'] = prmsn_by_entity
        if type(prmsn_by_value) is str:
            self.add_cost_acct_dialog_request['permission']['permissionByValue'].append(prmsn_by_value)
        else:
            self.add_cost_acct_dialog_request['permission']['permissionByValue'] = prmsn_by_value

        self.add_cost_acct_dialog_request['passwordEnabled'] = pwd_enabled
        self.add_cost_acct_dialog_request['billable'] = billable

        if pwd_enabled and pwd_code:
            self.add_cost_acct_dialog_request['passwordEnabled'] = pwd_enabled
            self.add_cost_acct_dialog_request['passwordCode'] = pwd_code
        if parent:
            self.add_cost_acct_dialog_request['parent'] = parent
        if desc:
            self.add_cost_acct_dialog_request['description'] = desc

        if budget_amt:
            self.add_cost_acct_dialog_request['budgetAmount'] = budget_amt
            self.add_cost_acct_dialog_request['budgetNotification']['frequency'] = frequency
            self.add_cost_acct_dialog_request['budgetNotification']['budgetNotificationEnable'] = budget_notification_enable
            self.add_cost_acct_dialog_request['budgetNotification']['budgetSystemAlertsEnable'] = budget_system_alert_enable
            self.add_cost_acct_dialog_request['budgetNotification']['yearBeginsMonth'] = year_begin_month
            self.add_cost_acct_dialog_request['budgetNotification']['yearBeginsDay'] = year_begin_day
            self.add_cost_acct_dialog_request['budgetNotification']['notificationEmails'] = notification_emails
            self.add_cost_acct_dialog_request['budgetNotification']['notificationNumbers'] = notification_numbers
            self.add_cost_acct_dialog_request['budgetNotification']['notificationThreshold'] = notification_threshold

        if is_admin:
            add_cost_acct_endpoint = self.endpoint + '/api/v2/costAccounts'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            add_cost_acct_endpoint = self.endpoint + '/api/v2/costAccounts'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.post_api_response(endpoint=add_cost_acct_endpoint, headers=self.headers,
                                              body=json.dumps(self.add_cost_acct_dialog_request))
        return response

    def put_update_cost_account_api(self, acct_id='', code='', name='', desc='', status=True, prmsn_by_entity='',
                                    billable=False, prmsn_by_value=None, parent='', sub_id='', pwd_enabled=False,
                                    pwd_code='', budget_amt='', frequency='', budget_notification_enable='',
                                    budget_system_alert_enable='', year_begin_month='', year_begin_day='',
                                    notification_emails='', notification_numbers='', notification_threshold='',
                                    acct_list_ids='', is_admin=False, token=None):
        """
        This method sets up and sends a request to update an existing cost account using the provided parameters.

        :param acct_id: The account ID.
        :param code: The account code.
        :param name: The name of the account.
        :param desc: The description of the account.
        :param status: The status of the account (default is True).
        :param prmsn_by_entity: Permissions by entity.
        :param billable: Whether the account is billable (default is False).
        :param prmsn_by_value: Permissions by value.
        :param parent: The parent account ID.
        :param sub_id: The sub ID.
        :param pwd_enabled: Whether a password is enabled (default is False).
        :param pwd_code: The password code.
        :param budget_amt: The budget amount.
        :param frequency: The frequency of budget notifications.
        :param budget_notification_enable: Whether budget notifications are enabled.
        :param budget_system_alert_enable: Whether budget system alerts are enabled.
        :param year_begin_month: The month the budget year begins.
        :param year_begin_day: The day the budget year begins.
        :param notification_emails: Notification emails.
        :param notification_numbers: Notification phone numbers.
        :param notification_threshold: Notification threshold.
        :param acct_list_ids: The account list ids (reference locations) in 'List' type.
        :param is_admin: The flag to determine admin or client user. If true then admin user otherwise uses
                         client user. Default is False.
        :param token: The admin or client user access token.

        :return: The response of the API request (success or failure).
        """

        def set_payload_value(key, value):
            if value not in ['', None]:
                keys = key.split('.')
                target = self.update_cost_acct_request
                for k in keys[:-1]:
                    target = target.setdefault(k, {})
                target[keys[-1]] = value

        set_payload_value('name', name)
        set_payload_value('code', code)
        set_payload_value('subID', sub_id)
        set_payload_value('accountID', acct_id)
        set_payload_value('status', status)

        # Set permissions
        if 'permission' not in self.update_cost_acct_request:
            self.update_cost_acct_request['permission'] = {}

        set_payload_value('permission.permissionByEntity', prmsn_by_entity)

        if type(acct_list_ids) is str:
            if 'acctListIDs' not in self.update_cost_acct_request:
                self.update_cost_acct_request['acctListIDs'] = []
            self.update_cost_acct_request['acctListIDs'].append(acct_list_ids)
        else:
            set_payload_value('acctListIDs', acct_list_ids)

        if type(prmsn_by_value) is str:
            if 'permission.permissionByValue' not in self.update_cost_acct_request:
                self.update_cost_acct_request['permission.permissionByValue'] = []
            self.update_cost_acct_request['permission.permissionByValue'].append(prmsn_by_value)
        else:
            set_payload_value('permission.permissionByValue', prmsn_by_value)

        set_payload_value('passwordEnabled', pwd_enabled)
        set_payload_value('billable', billable)

        if pwd_enabled and pwd_code:
            set_payload_value('passwordCode', pwd_code)

        set_payload_value('parent', parent)
        set_payload_value('description', desc)

        if budget_amt:
            set_payload_value('budgetAmount', budget_amt)
            if 'budgetNotification' not in self.update_cost_acct_request:
                self.update_cost_acct_request['budgetNotification'] = {}
            set_payload_value('budgetNotification.frequency', frequency)
            set_payload_value('budgetNotification.budgetNotificationEnable', budget_notification_enable)
            set_payload_value('budgetNotification.budgetSystemAlertsEnable', budget_system_alert_enable)
            set_payload_value('budgetNotification.yearBeginsMonth', year_begin_month)
            set_payload_value('budgetNotification.yearBeginsDay', year_begin_day)
            set_payload_value('budgetNotification.notificationEmails', notification_emails)
            set_payload_value('budgetNotification.notificationNumbers', notification_numbers)
            set_payload_value('budgetNotification.notificationThreshold', notification_threshold)

        if is_admin:
            add_cost_acct_endpoint = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/costAccounts/{acct_id}'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            add_cost_acct_endpoint = f'{self.endpoint}/api/v2/costAccounts/{acct_id}'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.put_api_response(endpoint=add_cost_acct_endpoint, headers=self.headers,
                                             body=json.dumps(self.update_cost_acct_request))
        return response

    def archive_cost_account_api(self, acct_id='', sub_id='', is_admin=False, token=None):
        """
        This method uses cost account api with v2 version to archive the given cost account id.

        :param acct_id: The cost account id.
        :param sub_id: The subscription id.
        :param is_admin: Admin flag to determine the API is called using admin or client token.
        :param token: The access token generated from an admin or client user credentials.

        :return: It returns response and status code.
        """

        if is_admin:
            archive_cost_acct_url = f'{self.endpoint}/api/v2/subscriptions/{sub_id}/costAccounts/{acct_id}/archive'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            archive_cost_acct_url = f'{self.endpoint}/api/v2/costAccounts/{acct_id}/archive'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.put_api_response(endpoint=archive_cost_acct_url, headers=self.headers)
        return response

    def archive_cost_account_v1_api(self, acct_id='', sub_id='', is_admin=''):
        """
        This function is validates if a subscription gets deleted successfully or not
        :return: this function returns status code of response
        """

        if is_admin == 'y':
            archive_cost_acct_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/" + acct_id + "/archive"
            self.headers['Authorization'] = self.admin_token
        else:
            archive_cost_acct_endpoint = self.endpoint + "/api/v1/costAccounts/" + acct_id + "/archive"
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(endpoint=archive_cost_acct_endpoint, headers=self.headers)
        return response

    def update_cost_account_api(self, accountID, code, name, desc='', SubID='', is_admin='', parent='', status=''):
        """
        This function is validates if a subscription is updated successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('COST_ACCT_MGMT', 'body_path_update_account')) as f:
            self.json_data = json.load(f)

        self.json_data['accountID'] = accountID
        self.json_data['code'] = code
        self.json_data['name'] = name
        self.json_data['description'] = desc
        if status != '':
            self.json_data['status'] = status
        self.json_data['parent'] = parent

        if SubID != "":
            self.json_data['SubID'] = SubID

        if is_admin == 'y':
            update_cost_acc_endpoint = self.endpoint + '/api/v2/subscriptions/' + SubID + '/costAccounts/' + accountID
            self.headers['Authorization'] = self.admin_token
        else:
            update_cost_acc_endpoint = self.endpoint + '/api/v2/costAccounts/' + accountID
            self.headers['Authorization'] = self.client_token

        response = self.api.put_api_response(endpoint=update_cost_acc_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        return response

    def validate_passcode_api(self, sub_id, acc_id, pwd=''):
        """
        This function validates the passcode and accountId combination
        :return: this function returns response and status code
        """
        with open(self.prop.get('COST_ACCT_MGMT', 'body_path_validate_pass_code')) as f:
            self.json_data = json.load(f)
        if pwd != '':
            self.json_data['passwordCode'] = pwd

        validate_pass_code_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/" + acc_id + "/validatePasscode"
        self.headers['Authorization'] = self.admin_token
        response = self.api.post_api_response(endpoint=validate_pass_code_endpoint, headers=self.headers, body=json.dumps(self.json_data))
        return response

    def import_cost_account_api(self, acc_id='', sub_id='', name='', code='', permission_by_ent='',
                                permission_val='', status='', is_admin=''):
        """
        This function validates that cost account management can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        cost_account_import_file = self.prop.get('COST_ACCT_MGMT', 'create_cost_account_import_template')

        df = pd.read_csv(cost_account_import_file)

        if acc_id != '':
            df.loc[0, 'AccountID'] = acc_id

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id

        df.loc[0, 'Name'] = name

        if code != '':
            df.loc[0, 'Code'] = code

        if permission_by_ent != '':
            df.loc[0, 'PermissionByEntity'] = permission_by_ent

        if permission_val != '':
            df.loc[0, 'PermissionByValue'] = permission_val

        df.loc[0, 'Status'] = status

        df.to_csv(cost_account_import_file, index=False)

        cost_acc_file = open(self.prop.get('COST_ACCT_MGMT', 'create_cost_account_import_template'))

        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'create_cost_account_import_template'), cost_acc_file)}

        if is_admin == 'y':
            import_cost_acct_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/import"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acct_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/import"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acct_endpoint, files=files, headers=self.headers)
        return response

    def import_cost_account_single_hierarchy_api(self, sub_id='', status='', is_admin=''):
        """
        This function validates that cost account management can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        cost_account_import_file = self.prop.get('COST_ACCT_MGMT',
                                                 'create_hierarchy_cost_account_single_step_import_template')

        df = pd.read_csv(cost_account_import_file)

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id

        df.loc[0, 'Status'] = status

        df.to_csv(cost_account_import_file, index=False)

        cost_acc_file = open(
            self.prop.get('COST_ACCT_MGMT', 'create_hierarchy_cost_account_single_step_import_template'))

        files = {"file": (
            self.prop.get('COST_ACCT_MGMT', 'create_hierarchy_cost_account_single_step_import_template'),
            cost_acc_file)}

        if is_admin == 'y':
            import_cost_acct_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/import"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acct_endpoint = self.endpoint + "/api/v1/costAccounts/import"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acct_endpoint, files=files, headers=self.headers)
        return response

    def import_update_account_api(self, sub_id, is_admin=''):
        """
        This function validates that cost account management can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        f = open(self.prop.get('COST_ACCT_MGMT', 'update_cost_account_import_template'))
        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'update_cost_account_import_template'), f)}

        if is_admin == 'y':
            import_cost_acct_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/import"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acct_endpoint = self.endpoint + "/api/v1/costAccounts/import"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acct_endpoint, files=files, headers=self.headers)
        return response

    def get_cost_account_by_location_and_sub_id_api(self, loc_id, sub_id, is_admin=''):
        """
        This function fetches details of cost accounts
        :return: this function returns response and status code
        """
        if is_admin == 'y':
            get_accounts_by_loc_and_subid_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/locations/" + loc_id + "/costAccounts"
            self.headers['Authorization'] = self.admin_token
        else:
            get_accounts_by_loc_and_subid_endpoint = self.endpoint + "/api/v1/locations/" + loc_id + "/costAccounts"
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_accounts_by_loc_and_subid_endpoint, headers=self.headers)
        return response

    def get_cost_account_by_user_and_sub_id_api(self, user_id, sub_id, is_admin=''):
        """
        This function fetches details of cost accounts
        :return: this function returns response and status code
        """
        if is_admin == 'y':
            get_accounts_by_users_and_subid_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/costAccounts"
            self.headers['Authorization'] = self.admin_token
        else:
            get_accounts_by_users_and_subid_endpoint = self.endpoint + "/api/v1/users/" + user_id + "/costAccounts"
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=get_accounts_by_users_and_subid_endpoint, headers=self.headers)
        return response

    def cost_accounts_pagination_api(self, sub_id, is_admin='', user_id='', status=''):
        """
        This test validates if pagination is working correctly or not (positive scenario)
        :return: this function returns response and status code
        """

        if is_admin == 'Y':
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts?status=" + status
            self.headers['Authorization'] = self.admin_token
        else:
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/costAccounts?status=" + status
            self.headers['Authorization'] = self.client_token

        is_paginated = self.api.pagination_util(endpoint=get_cost_accounts_endpoint, headers=self.headers)
        return is_paginated

    def cost_accounts_sorting_api(self, sort_col, sub_id, is_admin='', account_status='', user_id=''):
        """
        This test validates if sorting is working correctly or not (positive scenario)
        :return: this function returns response and status code
        """
        if is_admin == 'Y':
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts"
            self.headers['Authorization'] = self.admin_token
        else:
            get_cost_accounts_endpoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/users/" + user_id + "/costAccounts" + account_status
            self.headers['Authorization'] = self.client_token

        is_sorted = self.api.sort_list_util(endpoint=get_cost_accounts_endpoint, sort_col=sort_col,
                                            headers=self.headers)
        return is_sorted

    def upload_cost_acc_file_api(self, acc_id='', sub_id='', name='', code='', is_admin='', permission_by_ent='',
                                 permission_val='', status=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        cost_account_import_file = self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template')

        df = pd.read_csv(cost_account_import_file)

        if acc_id != '':
            df.loc[0, 'AccountID'] = acc_id

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id

        df.loc[0, 'Name'] = name

        if code != '':
            df.loc[0, 'Code'] = code

        if permission_by_ent != '':
            df.loc[0, 'PermissionByEntity'] = permission_by_ent

        if permission_val != '':
            df.loc[0, 'PermissionByValue'] = permission_val

        if status !='':
            df.loc[0, 'Status'] = status

        df.to_csv(cost_account_import_file, index=False)

        cost_acc_file = open(self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template'))

        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template'), cost_acc_file)}

        if is_admin == 'y':
            import_cost_acc = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/upload"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acc = self.endpoint + "/api/v3/costAccounts/upload"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acc, files=files, headers=self.headers)
        return response

    def alm_upload_cost_acc_file_api(self, sub_id='', name='', code='', is_admin='', status=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        alm_import_file = self.prop.get('COST_ACCT_MGMT', 'create_alm_import_file')

        df = pd.read_csv(alm_import_file)

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id

        df.loc[0, 'Name'] = name

        if code != '':
            df.loc[0, 'Code'] = code

        if status !='':
            df.loc[0, 'Status'] = status

        df.to_csv(alm_import_file, index=False)

        alm_import_file = open(self.prop.get('COST_ACCT_MGMT', 'create_alm_import_file'))

        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'create_alm_import_file'), alm_import_file)}

        if is_admin == 'y':
            import_cost_acc = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/upload"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acc = self.endpoint + "/api/v3/costAccounts/upload"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acc, files=files, headers=self.headers)
        return response

    def upload_cost_acc_file_v1_api(self, acc_id='', sub_id='', name='', code='', is_admin='', permission_by_ent='',
                                    permission_val='', status=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        cost_account_import_file = self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template')

        df = pd.read_csv(cost_account_import_file)

        if acc_id != '':
            df.loc[0, 'AccountID'] = acc_id

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id

        df.loc[0, 'Name'] = name

        if code != '':
            df.loc[0, 'Code'] = code

        if permission_by_ent != '':
            df.loc[0, 'PermissionByEntity'] = permission_by_ent

        if permission_val != '':
            df.loc[0, 'PermissionByValue'] = permission_val

        if status != '':
            df.loc[0, 'Status'] = status

        df.to_csv(cost_account_import_file, index=False)

        cost_acc_file = open(self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template'))

        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'cost_account_import_template'), cost_acc_file)}

        if is_admin == 'y':
            import_cost_acc = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/upload"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acc = self.endpoint + "/api/v1/costAccounts/upload"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acc, files=files, headers=self.headers)
        return response

    def upload_cost_acct_hierarchy_file_api(self, sub_id='', prmsn_by_val_parent='', prmsn_by_val_loc='',
                                            prmsn_by_val_div='', is_admin=''):
        """
        This function validates that cost accounts hierarchy can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        cost_account_hierarchy_file = self.prop.get('COST_ACCT_MGMT',
                                                    'create_hierarchy_cost_account_import_template')

        df = pd.read_csv(cost_account_hierarchy_file)

        if prmsn_by_val_parent != '':
            df.loc[0, 'PermissionByValue'] = prmsn_by_val_parent

        if prmsn_by_val_loc != '':
            df.loc[1, 'PermissionByValue'] = prmsn_by_val_loc

        if prmsn_by_val_div != '':
            df.loc[2, 'PermissionByValue'] = prmsn_by_val_div

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id
            df.loc[1, 'SubID'] = sub_id
            df.loc[2, 'SubID'] = sub_id

        df.to_csv(cost_account_hierarchy_file, index=False)

        cost_acc_file = open(self.prop.get('COST_ACCT_MGMT', 'create_hierarchy_cost_account_import_template'))

        files = {"file": (
            self.prop.get('COST_ACCT_MGMT', 'create_hierarchy_cost_account_import_template'), cost_acc_file)}

        if is_admin == 'y':
            import_cost_acc = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/upload"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acc = self.endpoint + "/api/v3/costAccounts/upload"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acc, files=files, headers=self.headers)
        return response

    def assigned_cost_acct_import_file_api(self, sub_id='', is_admin='', permission_val=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        assigned_cost_account_import_file = self.prop.get('COST_ACCT_MGMT', 'assigned_cost_account_template')

        df = pd.read_csv(assigned_cost_account_import_file)

        if permission_val != '':
            df.loc[0, 'PermissionByValue'] = permission_val
            df.loc[1, 'PermissionByValue'] = permission_val
            df.loc[2, 'PermissionByValue'] = permission_val

        if sub_id != '':
            df.loc[0, 'SubID'] = sub_id
            df.loc[1, 'SubID'] = sub_id
            df.loc[2, 'SubID'] = sub_id

        df.to_csv(assigned_cost_account_import_file, index=False)

        assigned_cost_account_import_file = open(self.prop.get('COST_ACCT_MGMT', 'assigned_cost_account_template'))

        files = {"file": (self.prop.get('COST_ACCT_MGMT', 'assigned_cost_account_template'), assigned_cost_account_import_file)}

        if is_admin == 'y':
            import_cost_acc = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/upload"
            self.headers['Authorization'] = self.admin_token
        else:
            import_cost_acc = self.endpoint + "/api/v3/costAccounts/upload"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_cost_acc, files=files, headers=self.headers)
        return response

    def job_process_by_sub_id_job_id_api(self, sub_id='', job_id='', is_admin=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            import_process = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/process"
            self.headers['Authorization'] = self.admin_token
        else:
            import_process = self.endpoint + "/api/v3/costAccounts/jobs/" + job_id + "/process"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_process, headers=self.headers)
        return response

    def alm_job_process_by_sub_id_job_id_api(self, sub_id='', job_id='', is_admin='', param_val=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            import_process = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/process?"+param_val
            self.headers['Authorization'] = self.admin_token

        else:
            import_process = self.endpoint + "/api/v3/costAccounts/jobs/" + job_id + "/process?"+param_val
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_process, headers=self.headers)
        return response

    def process_file_response_v1_api(self, sub_id='', job_id='', is_admin=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            import_process = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/process"
            self.headers['Authorization'] = self.admin_token
        else:
            import_process = self.endpoint + "/api/v1/costAccounts/jobs/" + job_id + "/process"
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=import_process, headers=self.headers)
        return response

    def job_status_by_sub_id_job_id_api(self, sub_id='', job_id='', is_admin=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        file_status = 'FileInProgress'
        response = None

        if is_admin == 'y':
            import_status = self.endpoint + "/api/v3/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.admin_token
        else:
            import_status = self.endpoint + "/api/v3/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.client_token

        while file_status == 'FileInProgress':
            response = self.api.get_api_response(endpoint=import_status, headers=self.headers)
            file_status = response.json()['status']

        return response

    def job_status_v1_by_job_id_api(self, sub_id='', job_id='', is_admin=''):
        """
        This function validates that cost accounts can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        file_status = 'FileInProgress'
        response = None

        if is_admin == 'y':
            import_status = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.admin_token
        else:
            import_status = self.endpoint + "/api/v1/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.client_token

        while file_status == 'FileInProgress':
            response = self.api.get_api_response(endpoint=import_status, headers=self.headers)
            file_status = response.json()['status']

        return response

    def verify_res_schema(self, res, expected_schema):

        isValid = self.api.schema_validation(response_schema=res, expected_schema=expected_schema)

        return isValid

    def export_cost_acct_by_sub_id_api(self, sub_id='', is_admin=''):
        """
        This function validates that cost accounts can be exported (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            export_cost_acc = self.endpoint + "/api/v2/subscriptions/" + sub_id + "/costAccounts/export"
            self.headers['Authorization'] = self.admin_token
        else:
            export_cost_acc = self.endpoint + "/api/v2/costAccounts/export"
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=export_cost_acc, headers=self.headers)
        return response

    def export_job_status_by_sub_id_job_id_api(self, sub_id='', job_id='', is_admin=''):
        """
        This function validates that cost accounts can be created exported (Positive scenario)
        :return: this function returns boolean status of element located
        """

        if is_admin == 'y':
            export_status = self.endpoint + "/api/v2/subscriptions/" + sub_id + "/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.admin_token
        else:
            export_status = self.endpoint + "/api/v2/costAccounts/jobs/" + job_id + "/status"
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(endpoint=export_status, headers=self.headers)
        return response

    def cost_account_sync_by_sub_id_api(self, sync_type='SP360_TO_ALM', sub_id=''):
        """
        This API is to sync the cost accounts from SP360 to ALM and vice-versa.

        :param sync_type: Sync required from one place to another.
                          SP360_TO_ALM - Sync cost accounts from SP360 to ALM
                          ALM_TO_SP360 - Sync cost accounts from ALM to SP360
        :param sub_id: The subscription id.
        :return: The response of the cost_accounts_sync API.
        """
        query_params = '?syncType=' + sync_type + '&subID=' + sub_id
        cost_acct_sync_endpoint = self.endpoint + '/api/v1/CostAccounts/sync' + query_params
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(endpoint=cost_acct_sync_endpoint, headers=self.headers)
        return response

    def hard_delete_cost_accounts_api(self, sub_id='', kind='ALL'):
        """
        This API is to hard delete the cost accounts from both SP360 and ALM.
        
        :param sub_id: The subscription id.
        :param kind: The type of the cost account to be deleted. Ex: 'ALL' will delete all type of cost accounts. 
        :return: The response of the hard_delete_cost_accounts API.
        """
        query_params = '?subID=' + sub_id + '&type=' + kind
        hard_del_cost_acct_endpoint = self.endpoint + '/api/v1/CostAccounts/cleanup' + query_params
        self.headers['Authorization'] = self.admin_token

        response = self.api.post_api_response(endpoint=hard_del_cost_acct_endpoint, headers=self.headers)
        return response

    def advance_search_cost_accounts_api(self, page='0', limit='100', status='true', search_in_all_levels='true',
                                         query='', sub_id=None, filter_div_ids=None, filter_loc_ids=None,
                                         is_admin=False, token=None):

        payload = self.advance_search_cost_acct_request

        if filter_div_ids:
            payload['divisionIds'] = filter_div_ids
        if filter_loc_ids:
            payload['locationIds'] = filter_loc_ids

        if is_admin:
            query_params = (f'?skip={page}&limit={limit}&status={status}&searchInAllLevels={search_in_all_levels}'
                            f'&query={query}&subId={sub_id}')
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            query_params = (f'?skip={page}&limit={limit}&status={status}&searchInAllLevels={search_in_all_levels}'
                            f'&query={query}')
            self.headers['Authorization'] = token if token else self.client_token

        self.headers['Content-Type'] = 'application/json'
        adv_search_cost_acct_url = f'{self.endpoint}/api/v1/costAccounts/advanceSearch{query_params}'

        response = self.api.post_api_response(endpoint=adv_search_cost_acct_url, headers=self.headers,
                                              body=json.dumps(payload))
        return response

    def advance_search_cost_accounts_in_all_levels_api(self, page='0', limit='100', status='true', div_id=None,
                                                       loc_id=None, sub_id=None, search_in_all_levels='true', search='',
                                                       is_admin=False, admin_token=None, client_token=None):

        payload = self.advance_search_cost_acct_request

        if div_id:
            payload['divisionIds'] = div_id
        if loc_id:
            payload['locationIds'] = loc_id

        if is_admin:
            query_params = (f'?skip={page}&limit={limit}&status={status}&searchInAllLevels={search_in_all_levels}'
                            f'&query={search}&subId={sub_id}')
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            query_params = (f'?skip={page}&limit={limit}&status={status}&searchInAllLevels={search_in_all_levels}'
                            f'&query={search}')
            self.headers['Authorization'] = client_token if client_token else self.client_token

        self.headers['Content-Type'] = 'application/json'
        adv_search_cost_acct_url = f'{self.endpoint}/api/v1/costAccounts/advanceSearch{query_params}'

        response = self.api.post_api_response(endpoint=adv_search_cost_acct_url, headers=self.headers,
                                              body=json.dumps(payload))
        return response

    def advance_search_meter_api(self, sub_id='', page='0', limit='10', div_id=None, loc_id=None, is_admin='y'):

        query_params = '?subID=' + sub_id + '&skip=' + page + '&limit=' + limit

        if is_admin == 'y':
            self.headers['Authorization'] = self.admin_token
        else:
            self.headers['Authorization'] = self.client_token

        self.headers['Content-Type'] = 'application/json'

        adv_search_cost_acct_url = self.endpoint + '/api/v1/meters/advanceSearch' + query_params
        self.advance_search_cost_acct_request['divisionIds'] = div_id
        self.advance_search_cost_acct_request['locationIds'] = loc_id

        response = self.api.post_api_response(endpoint=adv_search_cost_acct_url, headers=self.headers,
                                              body=json.dumps(self.advance_search_cost_acct_request))
        return response

    def get_account_lists(self, account_list_id=None, is_admin=False, admin_token=None, client_token=None):

        if is_admin:
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            self.headers['Authorization'] = client_token if client_token else self.client_token

        if account_list_id:
            acct_lists_url = f'{self.endpoint}/api/v1/accountLists/{account_list_id}'
        else:
            acct_lists_url = f'{self.endpoint}/api/v1/accountLists'

        response = self.api.get_api_response(endpoint=acct_lists_url, headers=self.headers)
        return response

    def get_multiple_accounts_details_api(self, sub_id=None, account_id=None, is_admin=False, admin_token=None,
                                          client_token=None):

        if is_admin:
            get_multiple_accounts_url = f'{self.endpoint}/api/v1/subscription/{sub_id}/getMultipleAccountDetails'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_multiple_accounts_url = f'{self.endpoint}/api/v1/getMultipleAccountDetails'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        payload = [account_id]

        response = self.api.post_api_response(endpoint=get_multiple_accounts_url, headers=self.headers,
                                              body=json.dumps(payload))
        return response

    def get_cost_account_name_using_account_id(self, sub_id=None, account_id=None, is_admin=False, admin_token=None,
                                               client_token=None):

        cost_account_resp = self.get_multiple_accounts_details_api(sub_id=sub_id, account_id=account_id,
                                                                   is_admin=is_admin, admin_token=admin_token,
                                                                   client_token=client_token)

        assert_that(common_utils.validate_response_code(cost_account_resp, 200))

        self.log.info(f'cost_account_resp: {cost_account_resp.json()}')

        sub_id = cost_account_resp.json()[0]['subID']
        acct_id = cost_account_resp.json()[0]['accountID']
        acct_name = cost_account_resp.json()[0]['name']

        return sub_id, acct_id, acct_name

    def get_all_cost_accounts_using_sub_id(self, sub_id=None, is_admin=False, token=None):

        cost_acct_data = []

        cost_acct_resp = self.advance_search_cost_accounts_api(sub_id=sub_id, is_admin=is_admin, token=token)
        assert_that(common_utils.validate_response_code(cost_acct_resp, 200))

        cost_accts = cost_acct_resp.json()['accounts']
        for cost_acct in cost_accts:
            cost_acct_data.append({'acct_id': cost_acct['accountID'], 'acct_name': cost_acct['name']})

        return cost_acct_data

    def pick_random_cost_acct_id_name(self, cost_acct_data=None, excluded_acct_ids=None):
        if cost_acct_data is None:
            return None, None

        if excluded_acct_ids is None:
            excluded_acct_ids = []

        # Filter cost_acct_data to exclude specific acct_id and acct_name
        filtered_cost_acct_data = [cost_acct for cost_acct in cost_acct_data
                                   if cost_acct['acct_id'] not in excluded_acct_ids]

        if filtered_cost_acct_data:
            # Pick a random cost account from the filtered list
            random_cost_acct = random.choice(filtered_cost_acct_data)
            cost_acct_id = random_cost_acct['acct_id']
            cost_acct_name = random_cost_acct['acct_name']

            # Trim any extra whitespace from cost_acct_name
            cost_acct_name = ' '.join(cost_acct_name.strip().split())

            return cost_acct_id, cost_acct_name

        else:
            return None, None

    def get_search_parent_cost_accounts_api(self, sub_id='', loc_id='', skip='0', limit='100', search_by='parent:',
                                            parent_cost_acct_id='', is_admin=False, admin_token=None, client_token=None):

        query_params = f'?skip={skip}&limit={limit}&searchBy={search_by}{parent_cost_acct_id}'

        if is_admin:
            search_parent_cost_acct_url = (f'{self.endpoint}/api/v1/subscriptions/{sub_id}/locations/'
                                           f'{loc_id}/costAccounts{query_params}')
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            search_parent_cost_acct_url = f'{self.endpoint}/api/v1/locations/{loc_id}/costAccounts{query_params}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=search_parent_cost_acct_url, headers=self.headers)
        return response

    def get_sub_cost_accounts_api(self, sub_id='', parent_acct_id='', skip='0', limit='100', is_admin=False, token=None):

        if is_admin:
            query_params = f'?subID={sub_id}&skip={skip}&limit={limit}'
            get_sub_cost_acct_url = f'{self.endpoint}/api/v1/costAccounts/{parent_acct_id}/subAccounts{query_params}'
            self.headers['Authorization'] = token if token else self.admin_token
        else:
            query_params = f'?skip={skip}&limit={limit}'
            get_sub_cost_acct_url = f'{self.endpoint}/api/v1/costAccounts/{parent_acct_id}/subAccounts{query_params}'
            self.headers['Authorization'] = token if token else self.client_token

        response = self.api.get_api_response(endpoint=get_sub_cost_acct_url, headers=self.headers)
        return response

    def get_cost_account_hierarchy_based_on_level(self, sub_id='', filter_loc_ids=None, filter_div_ids=None, skip='0',
                                                  limit='100', status='true', hierarchy_lvl=0, is_admin=False, token=None):

        """
        Retrieves cost account hierarchy based on the specified level of sub cost accounts.

        Args:
            sub_id (str): Subscription ID.
            filter_loc_ids (list): List of location IDs to filter the cost accounts.
            filter_div_ids (list): List of division IDs to filter the cost accounts.
            skip (str): Page number of cost accounts in the search page.
            limit (str): Limit number of cost accounts per page.
            status (str): Status of cost accounts.
            hierarchy_lvl (int): Level of cost account to retrieve.
                                 0 represents parent cost account.
                                 1 represents sub cost account.
                                 2 represents sub-sub cost account.
            is_admin (bool): Flag indicating if the API call to be made using admin user.
            token (str): Use custom passed Admin token for API authentication.

        Returns:
            tuple: A tuple containing the cost account id, cost account name, and cost account hierarchy.

        """
        sub_acct_id, acct_id, acct_name, acct_hierarchy = None, None, None, None

        search_cost_accts_resp = (
            self.advance_search_cost_accounts_api(page=skip, limit=limit, status=status, filter_div_ids=filter_div_ids,
                                                  filter_loc_ids=filter_loc_ids, sub_id=sub_id, is_admin=is_admin,
                                                  token=token))
        assert_that(common_utils.validate_response_code(search_cost_accts_resp, 200))

        cost_accts_data = search_cost_accts_resp.json().get('accounts', [])
        for cost_acct in cost_accts_data:
            if hierarchy_lvl == 0:
                if cost_acct['SubAcctCounts'] == hierarchy_lvl:
                    acct_id = cost_acct.get('accountID')
                    acct_name = cost_acct.get('name')
                    acct_hierarchy = cost_acct.get('hierarchy')
                    return acct_id, acct_name, acct_hierarchy

            elif cost_acct['SubAcctCounts'] == hierarchy_lvl:
                sub_acct_id = cost_acct.get('accountID')
                break

        if sub_acct_id:
            sub_cost_accts_resp = self.get_sub_cost_accounts_api(sub_id=sub_id, parent_acct_id=sub_acct_id, skip=skip,
                                                                 limit=limit, is_admin=is_admin, token=token)
            assert_that(common_utils.validate_response_code(sub_cost_accts_resp, 200))
            sub_acct_json = sub_cost_accts_resp.json().get('accounts', [])
            if hierarchy_lvl == 0:
                for sub_acct in sub_acct_json:
                    acct_id = sub_acct.get('accountID', '')
                    acct_name = sub_acct.get('name', '')
                    acct_hierarchy = sub_acct.get('hierarchy', '')
                    ancestors = sub_acct.get('ancestors', [])

                    if len(ancestors) == hierarchy_lvl:
                        return acct_id, acct_name, acct_hierarchy
            else:
                for _ in range(hierarchy_lvl):
                    for sub_acct in sub_acct_json:
                        acct_id = sub_acct.get('accountID', '')
                        acct_name = sub_acct.get('name', '')
                        acct_hierarchy = sub_acct.get('hierarchy', '')
                        ancestors = sub_acct.get('ancestors', [])

                        while len(ancestors) != hierarchy_lvl:
                            sub_cost_accts_resp = self.get_sub_cost_accounts_api(sub_id=sub_id, parent_acct_id=acct_id,
                                                                                 skip=skip, limit=limit,
                                                                                 is_admin=is_admin, token=token)
                            assert_that(common_utils.validate_response_code(sub_cost_accts_resp, 200))
                            sub_acct_json = sub_cost_accts_resp.json().get('accounts', [])
                            for sub_acct_data in sub_acct_json:
                                acct_id = sub_acct_data.get('accountID', '')
                                acct_name = sub_acct_data.get('name', '')
                                acct_hierarchy = sub_acct_data.get('hierarchy', '')
                                ancestors = sub_acct_data.get('ancestors', [])
                        break
                    break

        return acct_id, acct_name, acct_hierarchy

    def get_import_field_list_api(self, acct_type='default', is_admin=False, admin_token=None, client_token=None):

        query_param = f'?type={acct_type}'
        if is_admin:
            get_import_field_list_url = f'{self.endpoint}/api/v1/costAccounts/import/fieldsList{query_param}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_import_field_list_url = f'{self.endpoint}/api/v1/costAccounts/import/fieldsList{query_param}'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.get_api_response(endpoint=get_import_field_list_url, headers=self.headers)
        return response

    def get_cost_account_details_by_code_api(self, sub_id='', acct_code=None, is_admin=False, admin_token=None, client_token=None):

        payload = acct_code

        if not isinstance(acct_code, list):
            payload = [acct_code]

        if is_admin:
            get_cost_acct_details_url = f'{self.endpoint}/api/v1/costAccounts/detailsByCode?subID={sub_id}'
            self.headers['Authorization'] = admin_token if admin_token else self.admin_token
        else:
            get_cost_acct_details_url = f'{self.endpoint}/api/v1/costAccounts/detailsByCode'
            self.headers['Authorization'] = client_token if client_token else self.client_token

        response = self.api.post_api_response(endpoint=get_cost_acct_details_url, headers=self.headers,
                                              body=json.dumps(payload))
        return response
    