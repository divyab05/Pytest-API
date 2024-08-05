import json
import logging

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility


class Notifications:
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token, client_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['notification_api'])
        self.headers = {
            "Authorization": "Bearer {}".format(self.access_token)
        }
        self.admin_token = "Bearer " + access_token
        self.client_token = "Bearer " + client_token

    def get_system_inapp_notification_details_by_notification_config_id_api(self, is_admin=False, sub_id='',
                                                                      config_id=''):
        if is_admin:
            get_notification_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations/' + \
                                   config_id
            self.headers['Authorization'] = self.admin_token
        else:
            get_notification_url = self.endpoint + '/api/v1/notificationConfigurations/' + config_id
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(get_notification_url, self.headers)
        return response

    def get_system_inapp_notification_config_list_search_by_custom_query_api(self, is_admin=False, sub_id='', searchquery=''):
        if is_admin:
            get_notification_url = self.endpoint + '/api/v1/subscription' + sub_id + '/notificationConfigurations?' + \
                                   searchquery
            self.headers['Authorization'] = self.admin_token
        else:
            get_notification_url = self.endpoint + '/api/v1/notificationConfigurations?' + searchquery
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(endpoint=get_notification_url, headers=self.headers)
        return response

    def post_create_system_inapp_notification_api(self, is_admin=False, name='', sub_id='', type='', parentplan='', tempname='', tempbody='', channel='', tempsub='', token=''):

        with open(self.prop.get('NOTIFICATION_API', 'add_notification_req_body')) as f:
            self.json_data = json.load(f)

            self.json_data['name'] = name
            self.json_data['type'] = type
            self.json_data['parentPlan'] = parentplan
            self.json_data['notificationConfigDetail'][0]['templateName'] = tempname
            self.json_data['notificationConfigDetail'][0]['templateBody'] = tempbody
            self.json_data['notificationConfigDetail'][0]['channel'] = channel
            self.json_data['notificationConfigDetail'][0]['templateSubject'] = tempsub

        if is_admin:
            create_notification_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations'
            self.headers['Authorization'] = self.admin_token
        elif token:
            create_notification_url = self.endpoint + '/api/v1/notificationConfigurations'
            self.headers['Authorization'] = token
        else:
            create_notification_url = self.endpoint + '/api/v1/notificationConfigurations'
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=create_notification_url, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def put_update_system_inapp_notification_by_config_id_api(self, is_admin=False, config_id='', sub_id='', name='', type='', parentplan='', tempname='', tempbody='', channel='', tempsub='', token=''):

        with open(self.prop.get('NOTIFICATION_API', 'add_notification_req_body')) as f:
            self.json_data = json.load(f)

            self.json_data['configID'] = config_id
            self.json_data['name'] = name
            self.json_data['type'] = type
            self.json_data['parentPlan'] = parentplan
            self.json_data['notificationConfigDetail'][0]['templateName'] = tempname
            self.json_data['notificationConfigDetail'][0]['templateBody'] = tempbody
            self.json_data['notificationConfigDetail'][0]['channel'] = channel
            self.json_data['notificationConfigDetail'][0]['templateSubject'] = tempsub

        if is_admin:
            update_notification_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations/' + config_id
            self.headers['Authorization'] = self.admin_token
        elif token:
            update_notification_url = self.endpoint + '/api/v1/notificationConfigurations/' + config_id
            self.headers['Authorization'] = token
        else:
            update_notification_url = self.endpoint + '/api/v1/notificationConfigurations/' + config_id
            self.headers['Authorization'] = self.client_token

        response = self.api.post_api_response(endpoint=update_notification_url, headers=self.headers,
                                              body=json.dumps(self.json_data))
        return response

    def delete_system_inapp_notification_api(self, is_admin=False, sub_id='', config_id=''):
        if is_admin:
            del_system_notification = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations/' + \
                                        config_id
            self.headers['Authorization'] = self.admin_token

        else:
            del_system_notification = self.endpoint + '/api/v1/notificationConfigurations/' + config_id
            self.headers['Authorization'] = self.client_token

        response = self.api.get_api_response(del_system_notification, self.headers)
        return response

    def get_user_email_sms_notification_detail_by_config_id_api(self, is_admin=False, sub_id='', config_id=''):

        if is_admin:
            get_user_notification_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations/' + \
                                        config_id
            self.headers['Authorization'] = self.admin_token
        else:
            get_user_notification_url = self.endpoint + '/api/v1/notificationConfigurations/' + config_id
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(get_user_notification_url, self.headers)
        return response

    def get_user_email_sms_notification_detail_by_message_api(self, is_admin=False, sub_id='', message=''):

        if is_admin:
            get_user_notification_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfig/getMessage?' + \
                                        message
            self.headers['Authorization'] = self.admin_token
        else:
            get_user_notification_url = self.endpoint + '/api/v1/notificationConfig/getMessage?' + message
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(get_user_notification_url, self.headers)
        return response

    def get_user_email_sms_notification_config_list_api(self, is_admin=False, sub_id='', search=''):

        if is_admin:
            get_user_notification_config_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/notificationConfigurations?' + \
                                        search
            self.headers['Authorization'] = self.admin_token
        else:
            get_user_notification_config_url = self.endpoint + '/api/v1/notificationConfigurations?' + search
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(get_user_notification_config_url, self.headers)
        return response

    def get_custom_notification_detail_by_notification_config_id_api(self, is_admin=False, sub_id='', config_id='', token=''):
        if is_admin:
            get_custom_notification_config_url = self.endpoint + '/api/v1/subscription/' + sub_id + '/customNotificationConfigurations/' + config_id
            self.headers['Authorization'] = self.admin_token
        elif token:
            get_custom_notification_config_url = self.endpoint + '/api/v1/customNotificationConfigurations/' + config_id
            self.headers['Authorization'] = token
        else:
            get_custom_notification_config_url = self.endpoint + '/api/v1/customNotificationConfigurations/' + config_id
            self.headers['Authorization'] = self.client_token
        response = self.api.get_api_response(get_custom_notification_config_url, self.headers)
        return response




