import base64
import configparser
import csv
import filecmp
import json
import os
# import pymongo as pymongo
import re
import logging
import random
import string

import allure
import jsonschema
import jwt
import pandas as pd
import pytest
from hamcrest import assert_that, equal_to, not_none, is_, none, matches_regexp
from jsonschema import validate
from FrameworkUtilities import excel_utils, request_utils
from FrameworkUtilities.CustomException import ValidationError
from FrameworkUtilities.generic_utils import generate_random_number
import FrameworkUtilities.logger_utility as log_utils


class common_utils:
    """
    This method is to return Excel data Records and required below parameters
    file_name: Name of the excel file provided
    sheet_name: Name of the sheet provided in file
    """

    log = log_utils.custom_logger(logging.INFO)

    @staticmethod
    def read_excel_data_store(folder_name, file_name, sheet_name):
        file_path = os.getcwd() + "/TestData/{arg1}/{arg2}".format(arg1=folder_name, arg2=file_name)
        results = excel_utils.read_from_excel(file_path, sheet_name)
        return results['Records']

    """
        This method is to return Excel data Records based on column value and required below parameters
        file_name: Name of the excel file provided
        sheet_name: Name of the sheet provided in file
        col_name: Cell value provided
    """

    @staticmethod
    def read_excel_data_store_by_col_name(folder_name, file_name, sheet_name, col_name):
        file_path = os.getcwd() + "/TestData/{arg1}/{arg2}".format(arg1=folder_name, arg2=file_name)
        results = excel_utils.read_excel_based_on_col_value(file_path, sheet_name, col_name)
        return results

    """
        This method is to convert Python class object to Json and require below params
        obj: Python class object provided
    """

    @staticmethod
    def convert_object_to_json(obj):
        json_str = json.dumps(obj, default=lambda o: o.__dict__)
        return json_str

    """
        This method is to set request headers  and require below params
        store_name: Name of the store provide i.e shopify
        integrator_id: Name of the application provided from command line i.e. spo/spog/spe
        cnfig: Config object provide
        valid_token: token type provided
        access_token: Access token to set the authorization header
    """

    @staticmethod
    def set_request_headers_connector(integrator_id, cnfig, valid_token, access_token, cartId, conflict):
        headers = {}
        if cartId.__contains__("mckesson")or cartId.__contains__("epic"):
            if not valid_token:
                headers['Authorization'] = "Bearer " + cnfig.env_cfg['expired_access_token']
            else:
                headers['Authorization'] = "Bearer " + access_token
            headers['integratorid'] = integrator_id
            headers['subscriptionId'] = cnfig.env_cfg['subscriptionid']
            headers['countryCode'] = cnfig.env_cfg['country_code']
            headers['X-PB-TransactionId'] = cnfig.env_cfg['X-PB-TransactionId']
            headers['CartId'] = cartId
        elif cartId.__contains__("shopify") or cartId.__contains__("magento"):
            if not valid_token:
                headers['Authorization'] = "Bearer " + cnfig.env_cfg['expired_access_token']
                headers['integratorid'] = integrator_id
                headers['subscriptionId'] = cnfig.env_cfg['subscriptionid']
                headers['countryCode'] = cnfig.env_cfg['country_code']
                headers['CartId'] = cartId

            else:
                if not conflict:
                    headers['Authorization'] = "Bearer " + access_token
                    headers['integratorid'] = integrator_id
                    headers['subscriptionId'] = cnfig.env_cfg['subscriptionid']
                    headers['countryCode'] = cnfig.env_cfg['country_code']
                    headers['CartId'] = cartId
                else:
                    headers['Authorization'] = "Bearer " + access_token
                    headers['integratorid'] = integrator_id
                    headers['subscriptionId'] = str(cnfig.env_cfg['subid']).replace("{unique_no}",
                                                                                         generate_random_number(6))
                    headers['countryCode'] = cnfig.env_cfg['country_code']
                    headers['CartId'] = cartId
        return headers


    @staticmethod
    def set_devicehub_request_headers(cnfig, valid_token, access_token):
        headers = {}
        if not valid_token:
            headers['Authorization'] = "Bearer " + cnfig.env_cfg['expired_access_token']

        else:
            headers['Authorization'] = "Bearer " + access_token
        headers['X-PB-TransactionId'] = str(cnfig.env_cfg['X-PB-TransactionId']).replace("{unique}",
                                                                                         generate_random_number(6))
        headers['X-PB-PartnerId'] = cnfig.env_cfg['X-PB-PartnerId']
        headers['X-PB-IntegratorId'] = cnfig.env_cfg['X-PB-IntegratorId']
        return headers

    @staticmethod
    def set_request_headers_DA(cnfig, valid_token, access_token, env):
        headers = {}
        if not valid_token:
            headers['Authorization'] = "Bearer " + cnfig.env_cfg['expired_access_token']
        else:
            headers['Authorization'] = "Bearer " + access_token
        headers['X-Cresco-Environment'] = env
        return headers


    """
    This function is to validate Json Schema Validation based and require two params
    actual_response: actual json response payload
    expected_response: Expected Json Schema's stored under resources//JsonSchema Folder
    """

    @allure.step("Validate JsonSchema Validation")
    def validate_json_schema_validations(self, actual_response, expected_response):
        results = {}
        try:
            validate(instance=actual_response, schema=expected_response)
        except jsonschema.exceptions.ValidationError as err:
            results['error_message'] = err
            results['status'] = False
            return results
        except jsonschema.exceptions.SchemaError as err:
            results['error_message'] = err
            results['status'] = False
            return results
        except jsonschema.exceptions.FormatError as err:
            results['error_message'] = err
            results['status'] = False
            return results
        except Exception as e:
            results['error_message'] = e
            results['status'] = False
            return results
        results['error_message'] = ""
        results['status'] = True
        return results

    """
    This function is used to read Json File and requires two params
    file_name: Name of the file user wants to read
    folder_name: Name of the folder where file is present
    """

    def read_json_file(self, file_name, folder_name):
        file_path = os.getcwd() + "/response_schema/{arg1}/".format(arg1=folder_name)
        json_file = open(os.path.join(file_path, file_name), mode='r')
        data = json.load(json_file)
        json_file.close()
        return data

    """
    This function is used to read config.txt File and return config object
    config_section_header: Name of the section present in config file
    config_key: Key user wants to read
    """

    @staticmethod
    def read_config_return_value(folder_name, config_section_header, config_key):
        path = os.getcwd() + "/ConfigFiles/{arg1}/".format(arg1=folder_name)
        config = configparser.RawConfigParser()
        config.read(os.path.join(path, "config.txt"))
        return config.get(config_section_header, config_key)

    """
    This function is used to write config.txt File and requires below params
    config_section_header: Name of the section present in config file
    config_key: Key user wants to read
    value: user wants to write to the config file
    """

    @staticmethod
    def write_config_based_on_key(folder_name, config_section_header, config_key, value):
        path = os.getcwd() + "/ConfigFiles/{arg1}/".format(arg1=folder_name)
        config = configparser.RawConfigParser()
        config.read(os.path.join(path, "config.txt"))
        config.set(config_section_header, config_key, value)
        with open(os.path.join(path, "config.txt"), 'w') as configfile:
            config.write(configfile)

    """
    This function is used to parse json based on a particular key
    json_data: Json data user needs to parse
    key: Key to pass
    """

    @staticmethod
    def parse_json_and_return_data_based_on_key(json_data, key):
        return json_data[key]

    """
    This function is used to parse json based on a parent key
    json_data: Json data user needs to parse
    parent_key: Parent node key
    child_key: child present under the parent node
    """

    @staticmethod
    def parse_json_and_return_data_based_on_parent_key(json_data,
                                                       parent_key, child_key):
        parent_data = json_data[parent_key]
        child_data = parent_data[0][child_key]
        return child_data

    """
    This function is used to remove null value from the Dictionary
    results: Dictionary to pass
    """

    @staticmethod
    def remove_null_values_dict(results):

        res = []
        for index in range(0, len(results)):
            if str(results[index]['expected_res']).__contains__('{}'):
                continue
            else:
                res.append(results[index])
        return res

    """
    This function is used compare expected json response and actual json response 
    and return the diff if presents
    expected_resp: Expected Json Response
    actual_resp: Actual json Response
    custom_logger: Custom logger used for logging 
    """

    @staticmethod
    @allure.step("Validate Expected Json Response payload matches with the actual Response")
    def compare_expected_actual_response(expected_resp, actual_resp, custom_logger):
        expected_results = {}
        actual_results = {}

        for key in expected_resp:
            try:
                custom_logger.info('Validating actual response and expected response '
                                   'for key {arg1}'.format(arg1=key))

                assert str(actual_resp[key]) == str(expected_resp[key])
                custom_logger.info('Actual response matches with expected response '
                                   'for key {arg1}'.format(arg1=key))
            except AssertionError as err:
                custom_logger.error('Actual response {arg1} does not matched with expected response {arg2} '
                                    'for key {arg3}'.format(arg1=actual_resp[key], arg2=expected_resp[key], arg3=key))
                expected_results[key] = expected_resp[key]
                actual_results[key] = actual_resp[key]

        return {'expected_res': expected_results,
                'actual_res': actual_results}

    """
     This function is used to convert csv file to json and requires below parameter
     file_name: Name of the csv file 
    """

    @staticmethod
    def convert_csv_to_json(file_name, folder_name):

        file_path = os.getcwd() + "/TestData/{arg1}/{arg2}/".format(arg1=folder_name, arg2=file_name)
        data = {}

        # Open a csv reader called DictReader
        with open(file_path, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)

            # Convert each row into a dictionary
            # and add it to data
            for rows in csvReader:
                # Assuming a column named 'No' to
                # be the primary key
                key = rows['storeId']
                data[key] = rows

        dt = json.dumps(data, indent=4)

        return dt

    """
    This function is used to compare expected and actual json response based on their data type,
    their exact value , compare keys present in json  and compare their values and requires below
    parameters 
    expected_json_response: Expected Json Response
    actual_json_response: Actual Json Response
    custom_logger: Custom Logger used for logging and reporting
    """

    def compare_object(self, expected_json_response, actual_json_response, custom_logger):
        if type(expected_json_response) != type(actual_json_response):
            return {"results": False, "message": 'Expected type {arg1} does not match with Actual type {arg2} for key '
                .format(arg1=type(expected_json_response), arg2=type(actual_json_response))}
        elif type(expected_json_response) is dict:
            return self.compare_dict(expected_json_response, actual_json_response, custom_logger)
        elif type(expected_json_response) is list:
            return self.compare_list(expected_json_response, actual_json_response, custom_logger)
        else:
            if expected_json_response == actual_json_response:
                return {"results": True, "message": 'Actual response matched with expected response'}
            elif type(expected_json_response) == str and str(expected_json_response).strip() == str(
                    actual_json_response).strip():
                return {"results": True, "message": 'Actual response matched with expected response'}
            else:
                with allure.step("Actual response value {arg1} does not matched "
                                 "with expected response value {arg2}"
                                         .format(arg1=actual_json_response, arg2=expected_json_response)):
                    if expected_json_response != actual_json_response:
                        custom_logger.error("Actual response {arg1} does not matched "
                                            "with expected response {arg2}"
                                            .format(arg1=actual_json_response, arg2=expected_json_response))
                        raise ValidationError("Actual response value {arg1} does not matched "
                                              "with expected response value {arg2}"
                                              .format(arg1=actual_json_response, arg2=expected_json_response))
                return {"results": False, "message": 'Actual response {arg1}'
                                                     'does not matched with expected response {arg2}'
                    .format(arg1=actual_json_response, arg2=expected_json_response)}

    """
    This function is used to compare dictionaries and return results and requires below parameters 
    expected_json_response: Expected Json Response
    actual_json_response: Actual Json Response
    custom_logger: Custom Logger used for logging and reporting
    """

    def compare_dict(self, expected_json_response, actual_json_response, custom_logger):
        if len(expected_json_response) != len(actual_json_response):
            return {"results": False, "message": 'Expected length{arg1} does not match with Actual '
                                                 'length '
                                                 '{arg2}'.format(arg1=len(expected_json_response),
                                                                 arg2=len(actual_json_response))}
        else:
            for k, v in expected_json_response.items():
                if not k in actual_json_response:
                    raise ValidationError("key {arg1} does not present in "
                                          "actual response {arg2}"
                                          .format(arg1=k, arg2=actual_json_response))
                else:
                    if not (self.compare_object(v, actual_json_response[k], custom_logger))['results']:
                        return {"results": False, "message": 'Actual response payload \n {arg1} and \n expected '
                                                             '\n {arg2}'
                                                             'does not match for key {arg3}'
                            .format(arg1=actual_json_response[k], arg2=v, arg3=k), "key": k}
        return {"results": True, "message": 'Actual response matched with expected response'}

    """
       This function is used to compare lists and return results and requires below parameters 
       expected_json_response: Expected Json Response
       actual_json_response: Actual Json Response
       custom_logger: Custom Logger used for logging and reporting
    """

    def compare_list(self, expected_json_response, actual_json_response, custom_logger):
        if len(expected_json_response) != len(actual_json_response):
            return {"results": False, "message": 'Expected length{arg1} does not match with Actual '
                                                 'length '
                                                 '{arg2}'.format(arg1=len(expected_json_response),
                                                                 arg2=len(actual_json_response))}
        else:
            for i in range(len(expected_json_response)):
                if not (self.compare_object(expected_json_response[i], actual_json_response[i],
                                            custom_logger))['results']:
                    return {"results": False, "message": 'Actual {arg1} and expected {arg2}'
                                                         'does not match '
                        .format(arg1=actual_json_response[i], arg2=expected_json_response[i])}
        return {"results": True, "message": 'Actual response matched with expected response'}

    @allure.step("Validate Expected Response payload matches with  the actual Response")
    def validate_expected_and_response_payload(self, expectd_response, actual_response, output_results):

        if not output_results['results']:
            pytest.fail("Expected response payload is not matching with "
                        "Actual Response payload and error message {arg1}"
                        .format(arg1=output_results['message']))
        else:
            pass

    @allure.step("Validate Expected and Actual Response status code")
    def validate_expected_and_actual_response_code(self, expectd_resp_code, actual_response_code):
        if expectd_resp_code != actual_response_code:
            pytest.fail("Expected Response status code {arg1} not matched with Actual {arg2}"
                        .format(arg1=expectd_resp_code, arg2=actual_response_code))
        else:
            return True

    @allure.step("Validate returned response isn't empty")
    def validate_retruned_response_length_code(self, returned_resp):
        if returned_resp == 0:
            pytest.fail("No records are fetched in response. Returned response is empty")

        else:
            return True

    @allure.step("Validate Expected and Actual values")
    def validate_expected_and_actual_values_code(self, expectd_obj_val, actual_obj_val):
        if expectd_obj_val != actual_obj_val:
            pytest.fail("Expected Response status code {arg1} is not matched with Actual value {arg2}"
                        .format(arg1=expectd_obj_val, arg2=actual_obj_val))
        else:
            return True

    @allure.step("Validate Expected and Actual values comparison")
    def validate_values_comparison_code(self, expected_obj_val, actual_obj_val):
        if expected_obj_val != actual_obj_val:
            return False
        else:
            return True

    @staticmethod
    def get_config_path_based_on_os(os_name, json_path):
        if os_name == "Darwin":
            config_path = os.getcwd() + json_path
            print(config_path)
        else:
            config_path = os.getcwd() + json_path
            print(config_path)

        return config_path

    @staticmethod
    def set_lockers_request_headers(token_type, prop_obj, access_token):
        unique_no = generate_random_number(5)
        headers = json.loads(prop_obj.get('LOCKERS', 'headers'))
        if token_type != "valid":
            headers['Authorization'] = prop_obj.get('LOCKERS', 'Invalid_token_qa')

        else:
            headers['Authorization'] = access_token

        headers['X-PB-TransactionId'] = str(headers['X-PB-TransactionId']).replace('{unique_no}', unique_no)
        common_utils.log.info("X-PB-TransactionID: " + headers['X-PB-TransactionId'])
        return headers

    @allure.step("Validate Expected and Actual Response status code")
    def validate_expected_and_actual_response_code_with_msg(self, expected_resp_code, actual_response_code, error_msg):
        if expected_resp_code != actual_response_code:
            pytest.fail("Expected Response status code {arg1} not matched with Actual {arg2} and error as below {arg3}"
                        .format(arg1=expected_resp_code, arg2=actual_response_code, arg3=error_msg))
        else:
            return True

    @staticmethod
    def decode_base_64(coded_string):
        decoded_string = base64.b64decode(coded_string).decode('utf-8')
        return decoded_string

    @staticmethod
    def encode_base_64(client_id, client_secret):
        secret = str(client_id) + ':' + str(client_secret)
        secret_byte = secret.encode('utf-8')
        encoded_value = base64.b64encode(secret_byte)
        return encoded_value.decode('utf-8')

    def get_basic_auth(self, client_id, client_secret):
        auth_encoded = self.encode_base_64(client_id, client_secret)
        basic_auth = "Basic " + str(auth_encoded)
        return basic_auth

    def text_to_csv(self, res_text):
        return pd.read_csv(res_text)

    @staticmethod
    def validate_response_code(actual_response, exp_resp_status_code):
        """
        This function is used to compare expected and actual json response status code.

        :param actual_response: Actual response
        :param exp_resp_status_code: Expected response status code

        :return: True if actual response status code matches with expected response status code otherwise False.
        """

        if actual_response.status_code != exp_resp_status_code:
            pytest.fail("Actual status code - {arg1} does not match with Expected status code - {arg2}.\n"
                        "Actual response: {arg3}"
                        .format(arg1=actual_response.status_code, arg2=exp_resp_status_code,
                                arg3=json.dumps(actual_response.json())))
        else:
            return True

    def validate_response_template(self, actual_response, expected_response, exp_resp_status_code):
        """
        This function is used to compare expected and actual json response status code. In addition, it also compares
        the actual json response to that of the expected json response.

        :param actual_response: Actual response
        :param expected_response: Expected response
        :param exp_resp_status_code: Expected response status code

        :return: True if actual response matches with expected response otherwise False.
        """
        self.validate_response_code(actual_response, exp_resp_status_code)

        assert_that(type(actual_response.json()), equal_to(type(expected_response)),
                    "Actual response type {arg1} does not match with Expected response type {arg2}.\n"
                    "Actual response: {arg3}"
                    .format(arg1=type(actual_response.json()), arg2=type(expected_response),
                            arg3=json.dumps(actual_response.json())))

        return self.compare_response_objects(actual_response.json(), expected_response)

    def compare_response_objects(self, actual, expected):
        """
        This function is used to equate the expected response keys and their values with that of the actual
        response keys and their values.

        :param actual: Actual json response
        :param expected: Expected json response

        :return: True if expected response matches with actual response otherwise False.
        """
        try:
            if type(actual) is dict:
                # for k, v in expected.items():
                #     if k not in actual:
                #         self.log.warning(f"Expected '{k}' is not available in the actual response!")
                for k, v in actual.items():
                    if k not in expected:
                        self.log.warning(f"Actual '{k}' is not available in the expected response!")
                    else:
                        error_message = "Actual response - '{k1}: {v1}' does not match with Expected response - " \
                                        "'{k1}: {v2}'".format(k1=k, v1=v, v2=expected[k])

                        if type(v) is dict:
                            self.compare_response_objects(v, expected[k])
                        elif isinstance(v, list) and isinstance(expected[k], list):
                            for i in range(len(v)):
                                self.compare_values(actual[k][i], expected[k][i], error_message)
                        else:
                            self.compare_values(v, expected[k], error_message)

            elif type(actual) is list:
                for i in range(len(actual)):
                    error_message = "Actual {arg1} does not match with Expected {arg2}" \
                        .format(arg1=actual[i], arg2=expected[i])
                    self.compare_values(actual[i], expected[i], error_message)
            else:
                self.compare_response_objects(actual, expected)

            return {"results": True, "message": "The actual response matches with the expected response."}
        except (IndexError, KeyError, ValueError, Exception) as e:
            raise Exception(f"{e}\nError: JSON Comparison Failed!\nActual: {actual}\nExpected: {expected}") from None

    def compare_values(self, actual, expected, error_message):
        """
        This function is used to equate the actual response keys and their values with that of the expected
        response keys and their set values. The expected response values can be set as:
        \n'only_chars': The value to be expected as Characters only.
        \n'only_digits': The value to be expected as Digits only.
        \n'skip': The expected value comparison will be skipped.
        \n'should_not_be_null': The value to be expected as not null or not none.

        :param actual: Actual json response
        :param expected: Expected json response
        :param error_message: Built-up error message to be displayed upon assertion error.

        :return: True if expected response matches with actual response otherwise False.
        """
        try:
            if type(actual) is dict:
                self.compare_response_objects(actual, expected)
            elif type(expected) is bool or type(expected) is int:
                assert_that(actual, equal_to(expected), error_message)
            else:
                if expected is None:
                    assert_that(actual, is_(none()), error_message)
                elif "only_chars" in expected:
                    assert_that(str(actual), matches_regexp("^[ a-zA-Z]+$"), error_message)
                elif "only_digits" in expected:
                    assert_that(str(actual), matches_regexp("^[ 0-9]+$"), error_message)
                elif "skip" in expected:
                    pass  # do nothing
                elif "should_not_be_null" in expected:
                    assert_that(actual, is_(not_none()), error_message)
                else:
                    assert_that(actual, equal_to(expected), error_message)
            return {"results": True, "message": "The expected values are matching with the actual values"}
        except (IndexError, KeyError, ValueError, Exception) as e:
            raise Exception(f"{e}\nError: Comparison of JSON values Failed!") from None

    @staticmethod
    def get_x_user_id_from_okta(access_token):
        """This function is used to get x_userId from access_token,
        We are decoding JWT Token(okta Token) and from that getting key response as json.
        In response json uid key is our x_userId"""
        token =access_token
        decoded = jwt.decode(token, verify=False)
        return decoded['uid']

    def read_csv_file(self, filepath, skip_header=False):
        """
        Reads a CSV file and returns its content as a list of rows.

        :param filepath: The path to the CSV file.
        :param skip_header: Whether to skip the header row. Defaults to False.

        :return: A list of rows from the CSV file. Each row is represented as a list of values.
        """
        rows = []
        try:
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                if skip_header:
                    next(reader)  # Skip the header row
                for row in reader:
                    rows.append(row)
        except FileNotFoundError as e:
            self.log.error(f"File not found: {filepath}\n{e}")
        return rows

    def compare_csv_rows(self, source_file=None, target_file=None, skip_header=False):
        """
        Compares the first three columns of two CSV files and checks if all rows from the source file are present in the
        target file.

        :param source_file: The path to the source CSV file.
        :param target_file: The path to the target CSV file.
        :param skip_header: Whether to skip the header row. Defaults to False.

        :return: True if all rows from the source file are found in the target file, otherwise fails the comparison.
        """
        source_rows = self.read_csv_file(source_file, skip_header)
        target_rows = self.read_csv_file(target_file, skip_header)

        source_row_count = len(source_rows)
        target_row_count = len(target_rows)

        for i in range(source_row_count):
            source_row = source_rows[i][:3]
            found = False

            for target_row in target_rows:
                if source_row == target_row[:3]:
                    found = True
                    break

            if not found:
                pytest.fail(f"The row from the source file at index {i} is not found in the target file.\n"
                            f"Source row: {source_row}\n Target rows: {target_rows}")

        self.log.info('CSV Rows Comparison Result: All rows from the source file are found in the target file.')
        return True

    def compare_html(self, source_file=None, target_file=None):
        """
        Compares the 2 files

        :param source_file: The path to the source file.
        :param target_file: The path to the target file.

        :return: True if both files are matching, otherwise fails the comparison.
        """
        source_text = open(source_file)
        target_text = open(target_file)

        result = filecmp.cmp(source_text, target_text, shallow=False)
        return result
