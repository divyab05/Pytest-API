"""This module is used for main page objects."""
import json
import logging
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.config_utility import ConfigUtility


class CarrierAccountManagement:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config, access_token):
        self.app_config = app_config
        self.access_token = access_token
        self.config = ConfigUtility(app_config)
        self.api = APIUtilily()
        self.prop = self.config.load_properties_file()
        self.endpoint = str(self.app_config.env_cfg['subcarrieractmgmt_api'])
        self.headers = {"Accept": "*/*", 'Authorization': "Bearer {}".format(self.access_token)}

    def verify_get_subCarriers_api(self, subscription_id, carrier_id):
        """
        This function fetches details of sub carriers as per the provided subscription Id and carrier Id
        :return: this function returns the response and status code
        """
        query_param = "filter=carrierID:" + str(carrier_id) + "&skip=0&limit=10"
        get_subCarrier_endpoint = self.endpoint + "/api/v1/subscriptions/" + str(
            subscription_id) + "/subCarriers?" + query_param
        res = self.api.get_api_response(endpoint=get_subCarrier_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_get_subCarrier_By_Id_api(self, carrier_ID):
        """
        This function fetches details of sub carriers By Id
        :return: this function returns response and status code
        """
        get_subCarrier_byID_endpoint = self.endpoint + "/api/v1/subCarriers/" + carrier_ID
        res = self.api.get_api_response(endpoint=get_subCarrier_byID_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_get_subCarrier_By_Token_api(self, subcarrier_token):
        """
        This function returns error when fetched with sub carrier token
        :return: this function returns response and status code
        """
        get_subCarrier_byToken_endpoint = self.endpoint + "/api/v1/subCarriers/" + subcarrier_token
        res = self.api.get_api_response(endpoint=get_subCarrier_byToken_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_get_Carrier_Parameters_api(self, partner_id, country_code):
        """
        This function fetches details of carrier parameters
        :return: this function returns status code of response
        """
        query_param_partner_id = "gcsPartnerID=" + partner_id
        query_param_country_code = "countryCode=" + country_code

        get_Carrier_Parameters_endpoint = self.endpoint + "/api/v1/carriers/UPS/parameters?" + query_param_partner_id + "&" + query_param_country_code
        res = self.api.get_api_response(endpoint=get_Carrier_Parameters_endpoint, headers=self.headers)
        status = res.status_code
        return status

    def verify_get_License_Agreements_api(self, partner_id, country_code):
        """
        This function fetches details of license agreement
        :return: this function returns response and status code
        """
        query_param_partner_id = "gcsPartnerID=" + partner_id
        query_param_country_code = "countryCode=" + country_code

        get_Carrier_Parameters_endpoint = self.endpoint + "/api/v1/carriers/UPS/license-agreements?" + query_param_partner_id + "&" + query_param_country_code

        res = self.api.get_api_response(endpoint=get_Carrier_Parameters_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_create_subCarrier_api(self, subID='', carrierID='', accountNumber='', gcsPartnerID='', desc=''):
        """
        This function is validates if a subcarriers of different type can be created successfully or not
        :return: this function returns boolean status of element located
        """
        with open(self.prop.get('CARRIER_Account_MGMT', 'body_path_subcarrier')) as f:
            self.json_data = json.load(f)
        result = False

        if subID != "":
            self.json_data['subID'] = subID

        if desc != "":
            self.json_data['description'] = desc

        if carrierID != "":
            self.json_data['carrierID'] = carrierID

        if accountNumber != "":
            self.json_data['accountNumber'] = accountNumber

        if gcsPartnerID != "":
            self.json_data['gcsPartnerID'] = gcsPartnerID

        create_subCarrier_endPoint = self.endpoint + "/api/v1/subCarriers"
        res = self.api.post_api_response(
            endpoint=create_subCarrier_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_archive_subCarrier_api(self, carrier_ID):
        """
        This function is validates if a subscription gets deleted successfully or not
        :return: this function returns status code of response
        """
        created_subID = carrier_ID
        archive_subCarrier_endPoint = self.endpoint + "/api/v1/subCarriers/" + created_subID + "/archive"

        res = self.api.put_api_response(
            endpoint=archive_subCarrier_endPoint, headers=self.headers)
        status_code = res.status_code
        return status_code

    def verify_get_subscription_subcarriers_byType_api(self, subid, query_param):
        """
        This function fetches details of sub carriers as per the provided type
        :return: this function returns status code of response
        """
        #query_subType = query_param
        #subscription_id = subid

        get_subscription_subcarrier_endpoint = self.endpoint + "/api/v1/subscriptions/" + subid + "/subCarriers?" + query_param

        res = self.api.get_api_response(endpoint=get_subscription_subcarrier_endpoint, headers=self.headers)
        status = res.status_code
        return status

    def verify_get_subcarriers_by_Location_api(self, locationId):
        """
        This function fetches details of sub carriers as per the provided location
        :return: this function returns status code of response
        """
        #query_param = locationId

        get_subcarrier_by_location_endpoint = self.endpoint + "/api/v1/locations/RETURN/subCarriers?locations=" + locationId
        res = self.api.get_api_response(endpoint=get_subcarrier_by_location_endpoint, headers=self.headers)
        status = res.status_code
        return status

    def verify_get_carriers_by_partnerId_api(self, partnerId):
        """
        This function fetches details of sub carriers as per the provided partnerId
        :return: this function returns response and status code of response
        """
        get_carrier_by_id_endpoint = self.endpoint + "/api/v1/subCarriers/carrier/" + partnerId
        res = self.api.get_api_response(endpoint=get_carrier_by_id_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_get_carriers_by_locationId_api(self, subId, locationId):
        """
        This function fetches details of sub carriers as per the provided Location Id
        :return: this function returns response and status code of response
        """
        #loc_id = locationId
        #sub_id = subId

        get_carrier_by_loc_id_endpoint = self.endpoint + "/api/v1/subscriptions/" + subId + "/locations/" + locationId + "/subCarriers"
        res = self.api.get_api_response(endpoint=get_carrier_by_loc_id_endpoint, headers=self.headers)
        status = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status

    def verify_update_subCarrier_fedex_api(self, sub_id='', subCarrierID='', description='', carrier_id='', account_num='', gcs_partner_id=''):
        """
        This function is validates if a subscription gets updated successfully or not
        :return: this function returns status code of the response
        """
        with open(self.prop.get('CARRIER_Account_MGMT', 'update_fedex_req_body')) as f:
            self.json_data = json.load(f)
        result = False

        if sub_id != '':

            self.json_data['subID'] = sub_id

        if description != '':
            self.json_data['description'] = description

        if carrier_id != '':
            self.json_data['carrierID'] = carrier_id

        if account_num != '':
            self.json_data['accountNumber'] = account_num

        if gcs_partner_id != '':
            self.json_data['gcsPartnerID'] = gcs_partner_id

        if subCarrierID != '':
            self.json_data['subCarrierID'] = subCarrierID

        update_subCarrier_endPoint = self.endpoint + "/api/v1/subCarriers/" + subCarrierID

        res = self.api.put_api_response(
            endpoint=update_subCarrier_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        return status_code

    def verify_update_subCarrier_api(self, sub_id='', subCarrierID='', description='', carrier_id='', account_num='', gcs_partner_id=''):
        """
        This function is validates if a subscription gets updated successfully or not
        :return: this function returns status code of the response
        """
        with open(self.prop.get('CARRIER_Account_MGMT', 'update_sub_carrier_body')) as f:
            self.json_data = json.load(f)
        result = False

        if sub_id != '':

            self.json_data['subID'] = sub_id

        if description != '':
            self.json_data['description'] = description

        if carrier_id != '':
            self.json_data['carrierID'] = carrier_id

        if account_num != '':
            self.json_data['accountNumber'] = account_num

        if gcs_partner_id != '':
            self.json_data['gcsPartnerID'] = gcs_partner_id

        if subCarrierID != '':
            self.json_data['subCarrierID'] = subCarrierID

        update_subCarrier_endPoint = self.endpoint + "/api/v1/subCarriers/" + subCarrierID

        res = self.api.put_api_response(
            endpoint=update_subCarrier_endPoint, headers=self.headers, body=json.dumps(self.json_data))
        status_code = res.status_code

        return status_code

    def verify_import_subCarrier_ups_api(self, subscription_id, carrier_id):
        """
        This function validates that UPS subcarrier can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        if carrier_id == 'UPS':

            f = open(self.prop.get('CARRIER_Account_MGMT', 'ups_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'ups_import_template'), f)}

        elif carrier_id == 'FedEx' or carrier_id == 'FEDEX':
            f = open(self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'), f)}

        else:
            f = open(self.prop.get('CARRIER_Account_MGMT', 'usps_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'usps_import_template'), f)}

        import_subCarrier_endPoint = self.endpoint + "/api/v1/subscriptions/" + subscription_id + "/subCarriers/import?disableAPIIntegration_gcs=false&disableAPIIntegration_payment=false"
        res = self.api.post_api_response(endpoint=import_subCarrier_endPoint, files=files, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_import_subCarrier_fedEx_api(self, subscription_id):
        """
        This function validates that FedEx subcarrier can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        f = open(self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'))
        files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'), f)}

        sub_id = subscription_id

        import_subCarrier_endPoint = self.endpoint + "/api/v1/subscriptions/" + sub_id + "/subCarriers/import?disableAPIIntegration_gcs=false&disableAPIIntegration_payment=false"
        res = self.api.post_api_response(endpoint=import_subCarrier_endPoint, files=files, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

    def verify_import_subCarrier_api(self, subscription_id, carrier_id):
        """
        This function validates that UPS subcarrier can be created through Import (Positive scenario)
        :return: this function returns boolean status of element located
        """
        if carrier_id == 'UPS':

            f = open(self.prop.get('CARRIER_Account_MGMT', 'ups_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'ups_import_template'), f)}

        elif carrier_id == 'FedEx' or carrier_id == 'FEDEX':
            f = open(self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'fedex_import_template'), f)}

        else:
            f = open(self.prop.get('CARRIER_Account_MGMT', 'usps_import_template'))
            files = {"file": (self.prop.get('CARRIER_Account_MGMT', 'usps_import_template'), f)}

        import_subCarrier_endPoint = self.endpoint + "/api/v1/subscriptions/" + subscription_id + "/subCarriers/import?disableAPIIntegration_gcs=false&disableAPIIntegration_payment=false"
        res = self.api.post_api_response(endpoint=import_subCarrier_endPoint, files=files, headers=self.headers)
        status_code = res.status_code
        if res is not None:
            res = res.json()
            self.log.info(res)
            result = True
        return res, status_code

