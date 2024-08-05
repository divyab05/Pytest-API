"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class BadgeIDP:

    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['badge_idp'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.access_token = "Bearer " + access_token

    def verify_get_user_details(self, token_type, resource_type, context):
        """
        This  function is written for the  getting the user badge details present in mange user: it confirms that how
        may user has crated the badge login against their  access
        """

        get_user_badge_endpoint = self.endpoint + "/api/v1/subscription/" + "users"
        get_endpoint_for_specific_user = self.endpoint + "/api/v1/subscription/" + "users/" + context["badgeID"]
        get_user_badge_endpoint_invalid = self.endpoint + "/api/v1/subscription/" + "users" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_user_badge_endpoint, headers=headers_update)
            status_code = res.status_code

        elif resource_type == "SpecificBadge":
            res = self.api.get_api_response(
                endpoint=get_endpoint_for_specific_user, headers=headers_update)
            status_code = res.status_code

        else:
            res = self.api.get_api_response(
                endpoint=get_user_badge_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_Post_add_user_badge_for_user(self, token_type, resource_type):
        """
        This  function is written for the creating the user badge for onborded user in platform
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_badge_service',
                                                                                      'add_badge_user'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        add_user_badge_endpoint = self.endpoint + "/api/v1/subscription/" + "users"
        add_user_badge_endpoint_invalid = self.endpoint + "/api/v1/subscription/" + "users" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.post_api_response(
                endpoint=add_user_badge_endpoint, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.post_api_response(
                endpoint=add_user_badge_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_edit_user_badge_with_new_badge_ID(self, Newjson, context, token_type, resource_type):
        """
        This  function is written for the creating the user badge for onborded user in platform
        """
        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        f = open(config_path, 'w')
        f.write(Newjson)
        with open(config_path) as f:
            self.json_data = json.load(f)
        add_user_badge_endpoint = self.endpoint + "/api/v1/subscription/" + "users/"+ context["badgeID"]
        add_user_badge_endpoint_invalid = self.endpoint + "/api/v1/subscription/" + "users" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.patch_api_response(
                endpoint=add_user_badge_endpoint, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        else:
            res = self.api.patch_api_response(
                endpoint=add_user_badge_endpoint_invalid, headers=headers_update,
                body=json.dumps(self.json_data))
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_delete_user_badge_details(self, context, token_type, resource_type):
        """
        This  function is written for the deleting the user badge which is created
        """
        delete_user_badge_endpoint = self.endpoint + "/api/v1/subscription/" + "users/" + context["NewbadgeID"]
        delete_user_badge_endpoint_invalid = self.endpoint + "/api/v1/subscription/" + "users" + self.invalid_path

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.delete_api_response(
                endpoint=delete_user_badge_endpoint, headers=headers_update)
            status_code = res.status_code
        else:
            res = self.api.get_api_response(
                endpoint=delete_user_badge_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def verify_get_samal_user_badge(self, context, token_type, resource_type, kioskToken=None):
        """
        This  function is written for getting the samal token for userbadge
        """
        get_samal_user_badge_endpoint = self.endpoint + "/api/v1/samlidp/" + context["tenantID"] + "/users/" + "badge/" + context["badgeID"]
        get_samal_user_badge_endpoint_invalid = self.endpoint + "/api/v1/subscription/" + "users" + self.invalid_path

        if kioskToken is not None:
            self.access_token = kioskToken['basic_device_token']
        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        if resource_type == "validResource":
            res = self.api.get_api_response(
                endpoint=get_samal_user_badge_endpoint, headers=headers_update)
            status_code = res.status_code
        else:
            res = self.api.get_api_response(
                endpoint=get_samal_user_badge_endpoint_invalid, headers=headers_update)
            status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code