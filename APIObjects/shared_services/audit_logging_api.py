"""This module is used for main page objects."""

import logging
import json

import requests

from APIObjects.shared_services.client_management_api import ClientManagementAPI
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.product_metadata_api import ProductMetadata
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.api_utils import APIUtilily
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string


class Audit_logging:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.common = common_utils()
        self.login = LoginAPI(app_config)
        self.client_mgmt_api = ClientManagementAPI(app_config, access_token, client_token)
        self.prod_metadata_api = ProductMetadata(app_config, access_token, client_token)
        self.prop = self.config.load_properties_file()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.prod_name = str(self.app_config.env_cfg['product_name']).lower()
        self.endpoint = str(self.app_config.env_cfg['audit_logging_endpoint'])
        self.headers = {"Accept": "*/*"}
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def retrieve_user_credentials(self):
        with open(self.prop.get('AUDIT_LOGGING', 'sample_subscription_ids_and_email_file')) as f:
            data = json.load(f)

        admin_user = data[self.prod_name][self.env]['admin_email_id']
        admin_pwd = data[self.prod_name][self.env]['admin_password']
        client_user = data[self.prod_name][self.env]['client_email_id']
        client_pwd = data[self.prod_name][self.env]['client_password']
        sub_id = data[self.prod_name][self.env]['subid']

        return admin_user, admin_pwd, client_user, client_pwd, sub_id

    def get_audit_events_api(self, is_admin=False, event_type='', pageNumber=0, pageSize=10,
                             collection_name='', sub_id=None, token=None, fromDate='', toDate='',
                             searchBy='', sort_by='desc'):

        if is_admin:
            query_params = '?pageNumber={args5}&pageSize={args6}&fromDate={args3}&toDate={args4}&eventType={args1}' \
                           '&collectionName={args2}&searchBy={args7}&sortBy=timestamp:{args8}&subId={args9}' \
                .format(args1=event_type, args2=collection_name, args3=fromDate, args4=toDate,
                        args5=pageNumber, args6=pageSize, args7=searchBy, args8=sort_by, args9=sub_id)

            self.headers['Authorization'] = token if token else self.admin_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/auditEvents' + query_params
        else:
            query_params = '?pageNumber={args5}&pageSize={args6}&fromDate={args3}&toDate={args4}&eventType={args1}' \
                           '&collectionName={args2}&searchBy={args7}&sortBy=timestamp:{args8}' \
                .format(args1=event_type, args2=collection_name, args3=fromDate, args4=toDate,
                        args5=pageNumber, args6=pageSize, args7=searchBy, args8=sort_by)

            self.headers['Authorization'] = token if token else self.client_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/auditEvents' + query_params

        response = self.api.get_api_response(get_audit_logging_endpoint, self.headers)
        # response = requests.get(url=get_audit_logging_endpoint, headers=self.headers, verify=False)

        return response

    def get_signin_events_api(self, is_admin=False, al_type='', pageNumber=0, pageSize=10,
                             collection_name='', sub_id=None, token=None, fromDate='', toDate='',
                             searchBy='', sort_by='desc'):

        if is_admin:
            query_params = '?pageNumber={args5}&pageSize={args6}&fromDate={args3}&toDate={args4}' \
                           '&searchBy={args7}&sortBy=timestamp:{args8}&subId={args9}' \
                .format(args3=fromDate, args4=toDate,
                        args5=pageNumber, args6=pageSize, args7=searchBy, args8=sort_by, args9=sub_id)

            self.headers['Authorization'] = token if token else self.admin_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/loginActivity' + query_params
        else:
            query_params = '?pageNumber={args5}&pageSize={args6}&fromDate={args3}&toDate={args4}' \
                           '&searchBy={args7}&sortBy=timestamp:{args8}' \
                .format(args3=fromDate, args4=toDate,
                        args5=pageNumber, args6=pageSize, args7=searchBy, args8=sort_by)

            self.headers['Authorization'] = token if token else self.client_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/loginActivity' + query_params

        response = self.api.get_api_response(get_audit_logging_endpoint, self.headers)
        # response = requests.get(url=get_audit_logging_endpoint, headers=self.headers, verify=False)
        return response

    def get_view_details_api(self, is_admin=False, al_type=None, audit_number='', limit='300',
                             collection_name=None, sub_id=None, token=None):

        if is_admin:
            query_params = '?auditNumber={args1}&collection={args2}&subId={args3}' \
                .format(args2=collection_name, args1=audit_number, args3=sub_id)
            self.headers['Authorization'] = token if token else self.admin_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/auditDetail' + query_params
        else:
            query_params = '?auditNumber={args1}&collection={args2}' \
                .format(args2=collection_name, args1=audit_number)
            self.headers['Authorization'] = token if token else self.client_token
            get_audit_logging_endpoint = self.endpoint + '/api/v1/auditDetail' + query_params

        response = self.api.get_api_response(get_audit_logging_endpoint, self.headers)
        # response = requests.get(url=get_audit_logging_endpoint, headers=self.headers, verify=False)
        return response