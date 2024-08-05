"""This module is used for main page objects."""
import json
import logging
import platform

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.db_utils import DbUtility
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class lockerOnboarding:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.json_data = None
        self.app_config = app_config
        self.access_token = "Bearer " + access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.invalid_path = generate_random_alphanumeric_string()
        self.prop = self.config.load_properties_file()
        self.endpoint = (self.app_config.env_cfg['base_api'])
        self.headers = json.loads(self.prop.get('LOCKERS', 'headers'))
        self.env = self.app_config.env_cfg['env'].lower()
        self.db = DbUtility(app_config, self.env + "-receiving-transaction")

    def verify_get_pcn_configuration(self, token_type, resource_type):
        """
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

    def db_pcn_get(self, pcnID):
        db_client = self.db.db_connect()
        table_name = "pcn"
        condition = {'pcnID': pcnID}
        results = self.db.get_one(table_name, condition)
        print(results)
        self.db.db_disconnect(db_client)

    def verify_upload_the_PCN_data(self, token_type, PCN):
        """
        This function validates create the pcn data for visibility of data
        :return: this function returns response and status code
        """

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_locker_Onboarding',
                                                                                      'upload_pcn'))
        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['pcnID'] = PCN
        get_pcn_endpoint = self.endpoint + "/api/v1/pcn"

        headers_update = common_utils.set_lockers_request_headers(token_type, self.prop, self.access_token)

        res = self.api.post_api_response(endpoint=get_pcn_endpoint, headers=headers_update,
                                         body=json.dumps(self.json_data))
        return res

    def db_pcn_delete(self, pcnID):
        db_client = self.db.db_connect()
        table_name = "pcn"
        conditions = {'pcnID': pcnID}
        del_data = self.db.del_one(table_name, conditions)
        print(del_data)
        self.db.db_disconnect(db_client)

    def verify_add_locker_bank(self, bankName, manufacturerID, manHardwareID, wagoSerial,
                               deviceSerial, description, units):

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_locker_Onboarding',
                                                                                      'add_locker_config_in_progress'))
        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data['bankName'] = bankName
        self.json_data['manufacturerID'] = manufacturerID
        self.json_data['description'] = description
        self.json_data['units'] = units
        self.json_data['wagoDeviceSerialNumber'] = wagoSerial
        if manHardwareID != "":
            self.json_data['manufacturerHardwareID'] = manHardwareID
            self.json_data['userDevices'][0]['serialNumber'] = manHardwareID
            self.json_data['userDevices'][0]['modelName'] = manHardwareID
        if deviceSerial != "":
            self.json_data['userDevices'][1]['serialNumber'] = deviceSerial
            self.json_data['userDevices'][1]['modelName'] = deviceSerial

        add_lockerbank_endpoint = self.endpoint + "/api/v1/lockerBank"

        headers_update = common_utils.set_lockers_request_headers("valid", self.prop, self.access_token)

        res = self.api.post_api_response(endpoint=add_lockerbank_endpoint, headers=headers_update,
                                         body=json.dumps(self.json_data))
        return res

    # total 28 properties editable
    def verify_edit_locker_bank(self, body_json, bankName, manHardwareID, wagoSerial,
                                deviceSerial, description):

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS', 'sample_json'))

        with open(config_path) as f:
            self.json_data = json.load(f)

        self.json_data = json.loads(json.dumps(body_json))
        self.json_data['bankName'] = bankName
        self.json_data['description'] = description
        if manHardwareID != "":
            self.json_data['manufacturerHardwareID'] = manHardwareID
            self.json_data['userDevices'][0]['serialNumber'] = manHardwareID
            self.json_data['userDevices'][0]['modelName'] = manHardwareID
        if deviceSerial != "":
            self.json_data['userDevices'][1]['serialNumber'] = deviceSerial
            self.json_data['userDevices'][1]['modelName'] = deviceSerial

        add_lockerbank_endpoint = self.endpoint + "/api/v1/lockerBank"

        headers_update = common_utils.set_lockers_request_headers("valid", self.prop, self.access_token)

        res = self.api.post_api_response(endpoint=add_lockerbank_endpoint, headers=headers_update,
                                         body=json.dumps(self.json_data))
        return res

    def db_get_lockerbank(self, MID):
        db_client = self.db.db_connect()
        table_name = "lockerbank"
        conditions = {'manufacturerID': MID}
        results = self.db.get_one(table_name, conditions)
        print(results)
        self.db.db_disconnect(db_client)

    def db_delete_lockerbank(self, MID):
        db_client = self.db.db_connect()
        table_name = "lockerbank"
        conditions = {'manufacturerID': MID}
        del_data = self.db.del_one(table_name, conditions)
        print(del_data)
        self.db.db_disconnect(db_client)

    def verify_add_config_locker_bank(self, lockerBank, manHardwareID, wagoSerial, deviceSerial):

        os_name = platform.system()
        config_path = common_utils.get_config_path_based_on_os(os_name, self.prop.get('LOCKERS_locker_Onboarding',
                                                                                      'add_config_locker'))
        with open(config_path) as f:
            self.json_data = json.load(f)

        if manHardwareID != "":
            self.json_data['manufacturerHardwareID'] = manHardwareID
            self.json_data['userDevices'][0]['serialNumber'] = manHardwareID
            self.json_data['userDevices'][0]['modelName'] = manHardwareID
        if deviceSerial != "":
            self.json_data['userDevices'][1]['serialNumber'] = deviceSerial
            self.json_data['userDevices'][1]['modelName'] = deviceSerial
        if wagoSerial != "":
            for x in range(5):
                if x == 2: continue
                self.json_data['columns'][0]['units'][x]['wagoDeviceSerialNumber'] = wagoSerial

        add_config_lockerbank_endpoint = self.endpoint + "/api/v1/lockerBank/" + lockerBank + "/config"

        headers_update = common_utils.set_lockers_request_headers("valid", self.prop, self.access_token)

        res = self.api.post_api_response(endpoint=add_config_lockerbank_endpoint, headers=headers_update,
                                         body=json.dumps(self.json_data))
        return res

    def verify_get_config_lockerbank(self, lockerBank):
        """
        This function validates the pcn's available on the environment
        :return: this function returns response and status code
        """
        get_config_endpoint = self.endpoint + "/api/v1/lockerBank/" + lockerBank + "/config"

        headers_update = common_utils.set_lockers_request_headers("valid", self.prop, self.access_token)

        res = self.api.get_api_response(endpoint=get_config_endpoint, headers=headers_update)
        return res

    def db_delete_config_lockerbank(self, MID):
        db_client = self.db.db_connect()
        table_name = "lockerbank-config"
        conditions = {'manufacturerID': MID}
        del_data = self.db.del_one(table_name, conditions)
        print(del_data)
        self.db.db_disconnect(db_client)

    def db_delete_asset(self):
        db_client = self.db.db_connect()
        table_name = "asset"
        conditions = {'subID': '9087'}
        del_data = self.db.del_one(table_name, conditions)
        print(del_data)
        self.db.db_disconnect(db_client)
