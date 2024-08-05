"""This module is used for main page objects."""
import datetime
import json
import logging
import platform
from datetime import datetime

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class ConfigurationAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.access_token = "Bearer " + access_token

    def verify_set_heartbeat_properties_for_locker_bank(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        UpdateHeartbeat	/api/v1/lockerBank/{id}/heartbeat
        This function validates the set of heartbeat properties of locker bank
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration', 'set_heartbeat_locker'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        now = datetime.utcnow()
        current_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.json_data['heartbeatTimestamp'] = current_time
        self.json_data['kioskErrors'][0]['timestamp'] = current_time

        set_locker_heartbeat_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/heartbeat"
        set_locker_heartbeat_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/heartbeat/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.put_api_response(
                endpoint=set_locker_heartbeat_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.put_api_response(
                endpoint=set_locker_heartbeat_endpoint_invalid, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_lockerbank_heartbeat(self, locker_bank, token_type, resource_type):
        """
        GetHeartbeat	/api/v1/lockerBank/{id}/heartbeat
        This function validates if a locker bank heartbeat is successfully fetch or not
        :return: this function returns response and status code
        """

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            get_locker_heartbeat_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/heartbeat"
            res = self.api.get_api_response(
                endpoint=get_locker_heartbeat_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            get_locker_heartbeat_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/heartbeat/" + self.invalid_path
            res = self.api.get_api_response(
                endpoint=get_locker_heartbeat_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_post_api_to_set_the_dropoff_property(self, locker_bank, token_type, resource_type):
        """
        SetPkgDropoffProperties	/api/v1/lockerBank/{id}/properties/dropoff
        This function validates the dropoff properties are successfully set or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration',
                                                                                      'Dropoff_properties'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_dropoff_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff"
        post_dropoff_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=post_dropoff_properties_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=post_dropoff_properties_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_dropoff_properties(self, locker_bank, token_type, resource_type):
        """
        GetPkgDropoffProperties	/api/v1/lockerBank/{id}/properties/dropoff
        This function validates dropoff Properties of selected locker bank is successfully fetch or not
        :return: this function returns response and status code
        """
        get_dropoff_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff"
        get_dropoff_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_dropoff_properties_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_dropoff_properties_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_post_api_to_set_the_pickup_property(self, locker_bank, token_type, resource_type):
        """
        SetPkgPickupProperties	/api/v1/lockerBank/{id}/properties/pickup
        This function validates the pickup properties are successfully set or not
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration',
                                                                                      'Pickup_properties'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_pickup_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup"
        post_pickup_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=post_pickup_properties_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=post_pickup_properties_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_pickup_properties(self, locker_bank, token_type, resource_type):
        """
        GetPkgPickupProperties	/api/v1/lockerBank/{id}/properties/pickup
        This function validates pickup Properties of selected locker bank is successfully fetch or not
        :return: this function returns response and status code
        """
        get_pickup_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup"
        get_pickup_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_pickup_properties_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_pickup_properties_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_patch_pro_configuration_status(self, locker_bank, samplejson, token_type, resource_type):
        """
        UpdateProConfiguration	/api/v1/lockerBank/{id}/proConfiguration/status
        This function validates the proconfiguration status of the lockerbank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_proconfig_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/proConfiguration/status"
        post_proconfig_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/proConfiguration/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_pro_configuration_status(self, locker_bank, token_type, resource_type, kioskToken=None):
        """
        GetProConfiguration	/api/v1/lockerBank/{id}/proConfiguration/status
        This function validates the proconfiguration status of lockerbank
        :return: this function returns response and status code
        """
        get_pro_configuration_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/proConfiguration/status"
        get_pro_configuration_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/proConfiguration/status/" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_pro_configuration_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_pro_configuration_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_email_configuration_status(self, locker_bank, emailEnabled, token_type, resource_type):
        """
        GetEmailConfigurationStatus	/api/v1/lockerBank/{id}/emailConfiguration/status
        This function validates the updation of email configuration status of the selected locker bank
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration',
                                                                                      'Email_config_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['enabled'] = bool(emailEnabled)

        get_updated_email_configuration_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration/status"
        get_updated_email_configuration_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(endpoint=get_updated_email_configuration_status_endpoint,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(endpoint=get_updated_email_configuration_status_endpoint_invalid,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_email_configuration_status(self, locker_bank, token_type, resource_type):
        """
        UpdateEmailConfigurationStatus	/api/v1/lockerBank/{id}/emailConfiguration/status
        This function validates the email configuration status of the selected locker bank
        :return: this function returns response and status code
        """
        get_email_configuration_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration/status"
        get_email_configuration_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_email_configuration_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(endpoint=get_email_configuration_status_endpoint_invalid,
                                            headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_eventQ_configuration_status(self, locker_bank, eventQstatus, token_type, resource_type):
        """
        UpdateEventQConfiguration	/api/v1/lockerBank/{id}/eventQConfiguration/status
        This function validates the eventQ configuration status at locker bank
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration',
                                                                                      'body_path_eventQ_config_status'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['status'] = bool(eventQstatus)

        get_update_eventQ_config_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/eventQConfiguration/status"
        get_update_eventQ_config_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/eventQConfiguration/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(endpoint=get_update_eventQ_config_status_endpoint,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(endpoint=get_update_eventQ_config_status_endpoint_invalid,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_eventQ_configuration_status(self, locker_bank, token_type, resource_type):
        """
        GetEventQConfiguration	/api/v1/lockerBank/{id}/eventQConfiguration/status
        This function validates the eventQ configuration status at locker bank
        :return: this function returns response and status code
        """
        get_eventQ_config_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/eventQConfiguration/status"
        get_eventQ_config_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/eventQConfiguration/status/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_eventQ_config_status_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(endpoint=get_eventQ_config_status_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_update_pickage_expire_duration(self, locker_bank, token_type, resource_type):
        """
        SetPkgExpireDuration	/api/v1/lockerBank/{id}/pkgExpireDuration
        This function validates the pickage expire duration at selected locker bank
        :return: this function returns response and status code
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_Configuration', 'body_path_pickage_exp_duration'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        get_update_pickage_expire_duration_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pkgExpireDuration"
        get_update_pickage_expire_duration_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pkgExpireDuration/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(endpoint=get_update_pickage_expire_duration_endpoint,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(endpoint=get_update_pickage_expire_duration_endpoint_invalid,
                                              headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_pickage_expireduration(self, locker_bank, token_type, resource_type):
        """
        GetPkgExpireDuration	/api/v1/lockerBank/{id}/pkgExpireDuration
        This function validates the pickage expire duration at selected locker bank
        :return: this function returns response and status code
        """
        get_pickage_expire_duration_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pkgExpireDuration"
        get_pickage_expire_duration_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/pkgExpireDuration/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_pickage_expire_duration_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_pickage_expire_duration_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_patch_pickup_property(self, locker_bank, samplejson, token_type, resource_type):
        """
        UpdatePkgPickupProperties	/api/v1/lockerBank/{id}/properties/pickup
        This function validates the pickup property status of the lockerbank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_proconfig_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup"
        post_proconfig_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/pickup" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_patch_dropoff_property(self, locker_bank, samplejson, token_type, resource_type):
        """
        UpdatePkgDropoffProperties	/api/v1/lockerBank/{id}/properties/dropoff
        This function validates the pickup property status of the lockerbank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_proconfig_status_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff"
        post_proconfig_status_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties/dropoff" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=post_proconfig_status_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_pcn_configuration(self, token_type, resource_type):
        """
        AddPCNConfiguration	/api/v1/pcn
        This function validates the pcn's available on the environment
        :return: this function returns response and status code
        """
        get_pcn_endpoint = self.endpoint + "/api/v1/pcn"
        get_pcn_endpoint_invalid = self.endpoint + "/api/v1/pcn/" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(endpoint=get_pcn_endpoint, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(endpoint=get_pcn_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_patch_email_configuration(self, locker_bank, samplejson, token_type, resource_type):
        """
        UpdateEmailConfiguration	/api/v1/lockerBank/{id}/emailConfiguration
        This function validates the email configuration update of a locker bank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        patch_email_configuration_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration"
        patch_email_configuration_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=patch_email_configuration_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=patch_email_configuration_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_post_email_configuration(self, locker_bank, samplejson, token_type, resource_type):
        """
        SetEmailConfiguration	/api/v1/lockerBank/{id}/emailConfiguration
        This function validates the email configuration update of a locker bank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        post_email_configuration_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration"
        post_email_configuration_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/emailConfiguration" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=post_email_configuration_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=post_email_configuration_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_patch_properties(self, locker_bank, samplejson, token_type, resource_type):
        """
        UpdateBankProperties	/api/v1/lockerBank/{id}/properties
        This function validates the proconfiguration status of the lockerbank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(samplejson)

        with open(config_path) as f:
            self.json_data = json.load(f)

        patch_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties"
        patch_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=patch_properties_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=patch_properties_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_put_properties(self, locker_bank, samplejson, token_type, resource_type):
        """
        SetBankProperties	/api/v1/lockerBank/{id}/properties
        This function validates the proconfiguration status of the lockerbank
        :return: this function returns boolean status of the element located
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data = json.loads(json.dumps(samplejson))

        put_properties_endpoint = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties"
        put_properties_endpoint_invalid = self.endpoint + "/api/v1/lockerBank/" + locker_bank + "/properties" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.put_api_response(
                endpoint=put_properties_endpoint, headers=headers_update, body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.put_api_response(
                endpoint=put_properties_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code
