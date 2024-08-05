"""This module is used for main page objects."""

import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility


class IntegrationAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.pt_endpoint = self.app_config.env_cfg['receiving_api']
        self.dh_endpoint = self.app_config.env_cfg['devicehub_api']
        self.notification_endpoint = self.app_config.env_cfg['notification_api']
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.headers['Authorization'] = "Bearer {}".format(access_token)

    def receiving_assets(self, trackingID, recipientID, receivingSiteID):
        """
        Add asset	/api/v1/assets
        This function adds an asset into receiving
        :return: this function returns response and status code
        """

        receiving_asset_endpoint = self.pt_endpoint + "/api/v1/assets"

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('Receiving', 'add_asset_body'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['asset']['trackingNumber'] = trackingID
        self.json_data['asset']['receiver']['contactID'] = recipientID
        self.json_data['asset']['currentLocation']['id'] = receivingSiteID
        self.json_data['activity']['location']['id'] = receivingSiteID

        response = self.api.post_api_response(endpoint=receiving_asset_endpoint, headers=self.headers,
                                              body=json.dumps(self.json_data))
        self.log.info(response)
        return response

    def receiving_decode(self, trackingID):
        """
            Decode	/api/v1/assets/tracking/decode
            This function adds an asset into receiving
            :return: this function returns response and status code
        """

        receiving_decode_endpoint = self.pt_endpoint + "/api/v1/assets/tracking/decode?trackingNum=" + trackingID

        response = self.api.get_api_response(endpoint=receiving_decode_endpoint, headers=self.headers)
        self.log.info(response)
        return response

    def post_ssm_activation_code(self, token_type, sample_json, kioskToken=None):
        """
        Post SSM Activation Code /api/v1/ssm/activationCode
        This function adds an asset into receiving
        :return: this function returns response and status code
        """

        devicehub_ssm_endpoint = self.dh_endpoint + "/api/v1/ssm/activationCode"

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))
        f = open(config_path, 'w')
        f.write(sample_json)
        with open(config_path) as f:
            self.json_data = json.load(f)

        if kioskToken is not None:
            self.access_token = kioskToken
        else:
            self.access_token = 'Bearer ' + self.access_token

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)
        res = self.api.post_api_response(endpoint=devicehub_ssm_endpoint, headers=headers_update, body=json.dumps(self.json_data))
        status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def notification_uniqueID(self, uniqueID, token=None):
        """
            notification_uniqueID	/api/v1/notification
            This function gets notification object using uniqueID
            :return: this function returns response and status code
        """

        notification_endpoint = self.notification_endpoint + "/api/v1/notification?searchBy=uniqueIdFromSender:" + uniqueID

        if token is not None:
            self.access_token = token
        else:
            self.access_token = 'Bearer ' + self.access_token

        res = self.api.get_api_response(endpoint=notification_endpoint, headers=self.headers)
        status_code = res.status_code

        if res is not None:
            try:
                res = res.json()
            except:
                res = res.text
        self.log.info(res)
        return res, status_code

    def get_locker_notifications(self, queryParam, token=None):
        """
            manageCustomNotificationConfigurations	/api/v2/manageCustomNotificationConfigurations
            This function gets notification object using uniqueID
            :return: this function returns response and status code
        """

        notification_endpoint = self.notification_endpoint + '/api/v2/manageCustomNotificationConfigurations?skip=0&limit=10&status=ACTIVE&searchBy=parentPlan:PitneyShip%20Pro,notificationApplicationCategoryID:Locker&userPlans=PITNEYSHIP_PRO,LOCKER_PLAN&showAll=true&&query=' + queryParam

        if token is not None:
            self.access_token = token
        else:
            self.access_token = 'Bearer ' + self.access_token

        res = self.api.get_api_response(endpoint=notification_endpoint, headers=self.headers)
        status_code = res.status_code

        # if res is not None:
        #     try:
        #         res = res.json()
        #     except:
        #         res = res.text
        self.log.info(json.loads(res.json()))
        return res, status_code
