import json
import random

import pytest
import logging
import inspect

import FrameworkUtilities.logger_utility as log_utils
from APIObjects.shared_services.data_generator import DataGenerator
from APIObjects.shared_services.login_api import LoginAPI
from APIObjects.shared_services.notification_api import Notifications
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from hamcrest import assert_that, equal_to

exe_status = ExecutionStatus()
api_util = APIUtilily()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    notification = {
        'app_config': app_config,
        'notification': Notifications(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config),
        'login_api': LoginAPI(app_config),
        'data_generator': DataGenerator(app_config)
        }
    yield notification


@pytest.mark.usefixtures('initialize')
class TestNotificationClientAPI(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, app_config, resource):
        exe_status.__init__()
        self.app_config = app_config
        self.configparameter = "NOTIFICATION_API"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        with open(self.prop.get('NOTIFICATION_API', 'sample_notification_mandatory_fields_resp')) as f1:
            self.sample_notification_mandatory_fields_resp = json.load(f1)

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_01_verify_get_system_client_notification_details_by_notification_config_id(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_notification_details_resp = resource[
            'notification'].get_system_inapp_notification_details_by_notification_config_id_api(sub_id='',
                                                                                          config_id='received')
        assert_that(self.validate_response_code(get_notification_details_resp,
                                                200))

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_02_verify_get_system_admin_notification_details_by_search_query(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_notification_search_detail_resp = resource[
            'notification'].get_system_inapp_notification_config_list_search_by_custom_query_api(searchquery='customTypeInputs.customAttributes')
        assert_that(self.validate_response_code(get_notification_search_detail_resp, 200))

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_03_verify_create_system_client_notification(self, resource):
        test = inspect.currentframe().f_code.co_name
        self.log.info(f'{test}')

        name = 'April USPS Rate Change' + str(random.randint(1, 500))
        parentPlan = 'SPONG'
        type = 'SYSTEM'
        Channel = "INAPP"
        templateName, templateBody, templateSubject = resource['data_generator'].notification_data_setter()
        get_notification_add_resp = resource['notification'].post_create_system_inapp_notification_api(name=name,
                                                                                                       type=type,
                                                                                                       parentplan=parentPlan,
                                                                                                       tempname=templateName,
                                                                                                       tempbody=templateBody,
                                                                                                       channel=Channel,
                                                                                                       tempsub=templateSubject,
                                                                                                       token='')
        fetch_configID = str(get_notification_add_resp.json()['notificationConfigId'])
        print(fetch_configID)
        assert_that(self.validate_response_code(get_notification_add_resp, 201))

        # 'Delete notification':
        del_status = resource['notification'].delete_system_inapp_notification_api(is_admin=True, sub_id='3082',
                                                                               config_id=fetch_configID)
        assert_that(self.validate_response_code(del_status, 200))

        # 'Verify that deleted notification is not available'
        get_notification_state = resource[
            'notification'].get_system_inapp_notification_details_by_notification_config_id_api(sub_id='3082',
                                                                                                config_id=fetch_configID)
        assert_that(self.validate_response_code(get_notification_state, 200))

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_04_get_user_email_sms_notification_detail_by_config_id_api(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        get_user_notification_details_resp = resource[
            'notification'].get_system_notification_details_by_notification_config_id_api(sub_id='',
                                                                                          config_id='received')
        assert_that(self.validate_response_code(get_user_notification_details_resp,
                                                200))

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_05_get_user_email_sms_notification_detail_by_message(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')

        message = 'searchBy=notificationApplicationCategoryID:Receiving,notificationRuleID:ATTEMPTED_DELIVERY,' \
                  'parentPlan:PitneyShip Pro&channel=Email '

        get_user_notification_detail_by_message_resp = resource[
            'notification'].get_user_email_sms_notification_detail_by_message_api(sub_id='', message=message)
        assert_that(self.validate_response_code(get_user_notification_detail_by_message_resp, 200))

    @pytest.mark.notification_sp360commercial
    @pytest.mark.notification_sp360commercial_reg
    def test_06_get_user_email_sms_notification_config_list(self, resource):
        self.log.info(f'{inspect.currentframe().f_code.co_name}')
        search = 'searchBy=parentPlan:PitneyShip Pro&query=Custom'
        get_user_notification_config_list = resource['notification'].get_user_email_sms_notification_config_list_api(
            sub_id='', search=search)
        assert_that(self.validate_response_code(get_user_notification_config_list, 200))
