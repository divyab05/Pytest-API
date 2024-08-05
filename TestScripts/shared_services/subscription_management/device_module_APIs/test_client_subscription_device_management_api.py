""" This module contains all test cases."""

import datetime
import random
import sys

import allure
import pytest

from APIObjects.shared_services.subscription_api import SubscriptionAPI
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from FrameworkUtilities.common_utils import common_utils

exe_status = ExecutionStatus()


# subscription_api = SubscriptionAPI()
# data_reader = DataReader()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    subscription_api = {}
    subscription_api['app_config'] = app_config
    subscription_api['subscription_api'] = SubscriptionAPI(app_config, generate_access_token, client_token)
    subscription_api['data_reader'] = DataReader(app_config)
    yield subscription_api


@pytest.mark.usefixtures('initialize')
class TestSubscription_Client_Device_Management_API(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, rp_logger, resource):
        exe_status.__init__()

        def cleanup():
            # data cleaning steps to be written here
            rp_logger.info('Cleaning Test Data.')

        yield
        cleanup()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, request, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "SUBSCRIPTION_MGMT"
        if resource['data_reader'].get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    # Test cases of Device module starts here


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_79_verify_get_devices_api(self, rp_logger, resource):
        """
        This test validates that enriched token can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the response of get all devices API and validate the response: "):
            get_devices_resp = resource['subscription_api'].get_devices_api()
            res = get_devices_resp.json()
            status_code = get_devices_resp.status_code
            total_size = len(res)
            if status_code != 200 and total_size == 0:
                self.Failures.append(
                    "There is a failure in fetching device details. Expected: 200 and >=1, Received : " + str(
                        status_code) + " and " + total_size)
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_80_verify_get_device_details_by_sub_id_api(self, rp_logger, resource):
        """
        This test validates that device details can be fetched by sub Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the response of get all devices API and validate the response: "):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_device_details_by_sub_id_api(sub_id)
            total_size = len(res)
            if status_code != 200 and total_size == 0:
                self.Failures.append(
                    "There is a failure in fetching device details. Expected: 200 and >=1, Received : " + str(
                        status_code) + " and " + total_size)
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # Test Cases for device module

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_81_verify_get_device_details_by_invalid_sub_id_api(self, rp_logger, resource):
        """
        This test validates that device details can be fetched by sub Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the response of get all devices API and validate the response: "):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_device_details_by_sub_id_api(sub_id)
            total_size = len(res)
            if status_code != 400:
                self.Failures.append(
                    "Error should be obtained. Expected: 400, Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_82_verify_register_device_info_api(self, rp_logger, resource):
        """
        This test validates that device details can be registered as per the provided info (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that device can be registered with valid details: "):

            location = str(resource['data_reader'].get_data(self.configparameter, test_name, 'locId'))
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)

            if status_code != 201:
                self.Failures.append("Device is not registered successfully. Expected : 201, Received : " + str(
                    status_code))

            else:
                created_dev_id = res['deviceID']
                created_client_id = res['clientID']

            with allure.step("Fetches the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                                device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                fetched_dev_id = res['deviceID']
                fetched_client_id = res['clientID']

            with allure.step("Validates that fetched details match to that of created device: "):
                if created_client_id != fetched_client_id and created_dev_id != fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the created one")

            with allure.step("Delete the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_delete_device_details_by_device_sno_api(sub_id,
                                                                                                   dev_serial_no,
                                                                                                   device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in deleting the device details. Expected : 200, Received : " + str(
                            status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_83_verify_register_duplicate_device_info_api(self, rp_logger, resource):
        """
        This test validates that duplicate device can not be registered (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that device can be registered with valid details: "):

            location = str(resource['data_reader'].get_data(self.configparameter, test_name, 'locId'))
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)

            if status_code != 201:
                self.Failures.append(
                    "Device is not registered successfully. Expected : 201, Received : " + str(
                        status_code))

        with allure.step("Register the same device again and verify that error is obtained: "):
            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            if res['errors'][0]['errorDescription'] != error_msg and status_code != 400:
                self.Failures.append(
                    "Error should be obtained when registering duplicate device: Expected status code: 400. Received" + str(
                        status_code))

        with allure.step("Delete the details of registered device: "):
            res, status_code = resource['subscription_api'].verify_delete_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                               device_type)
            if status_code != 200:
                self.Failures.append(
                    "There is an error in deleting the device details. Expected : 200, Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_84_verify_get_device_by_serial_num_api(self, rp_logger, resource):
        """
        This test validates that device details can be registered as per the provided info (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that device can be registered with valid details: "):

            location = str(resource['data_reader'].get_data(self.configparameter, test_name, 'locId'))
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)

            if status_code != 201:
                self.Failures.append("Device is not registered successfully. Expected : 201, Received : " + str(
                    status_code))

            else:
                created_dev_id = res['deviceID']
                created_client_id = res['clientID']

            with allure.step("Fetches the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                                device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                fetched_dev_id = res['deviceID']
                fetched_client_id = res['clientID']

            with allure.step("Validates that fetched details match to that of created device: "):
                if created_client_id != fetched_client_id and created_dev_id != fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the created one")

            with allure.step("Delete the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_delete_device_details_by_device_sno_api(sub_id,
                                                                                                   dev_serial_no,
                                                                                                   device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in deleting the device details. Expected : 200, Received : " + str(
                            status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_85_verify_get_device_by_invalid_sub_id_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when invalid subId is passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that error should be obtained when device is fetched with invalid subId: "):
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                            device_type)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            error_msg = error_msg.replace("?", sub_id)
            if res['errors'][0]['errorDescription'] != error_msg and status_code != 400:
                self.Failures.append(
                    "Error should be obtained when fetching device details by invalid subId: Expected status code: 400. Received" + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_86_verify_get_device_by_invalid_serial_num_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when invalid serial number is passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that error should be obtained when device is fetched with invalid subId: "):
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                            device_type)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            if res['errors'][0]['errorDescription'] != error_msg and status_code != 404:
                self.Failures.append(
                    "Error should be obtained when fetching device details by invalid serial number: Expected status code: 404. Received" + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_87_verify_get_device_by_invalid_device_type_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when invalid device type is passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that error should be obtained when device is fetched with invalid device type: "):
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                            device_type)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            if res['errors'][0]['errorDescription'] != error_msg and status_code != 404:
                self.Failures.append(
                    "Error should be obtained when fetching device details by invalid device type: Expected status code: 404. Received" + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_88_verify_swap_device_info_api(self, rp_logger, resource):
        """
        This test validates that device details can be registered as per the provided info (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that device can be registered with valid details: "):

            location = str(resource['data_reader'].get_data(self.configparameter, test_name, 'locId'))
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)
            if status_code != 201:
                self.Failures.append("Device is not registered successfully. Expected : 201, Received : " + str(
                    status_code))

            else:
                created_dev_id = res['deviceID']
                created_client_id = res['clientID']

            with allure.step("Fetches the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                                device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                fetched_dev_id = res['deviceID']
                fetched_client_id = res['clientID']

            with allure.step("Validates that fetched details match to that of created device: "):
                if created_client_id != fetched_client_id and created_dev_id != fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the created one")

            with allure.step("Swap the details of registered device: "):
                swap_dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'swapDeviceSNo'))
                swap_dev_typ = str(resource['data_reader'].get_data(self.configparameter, test_name, 'swapDeviceType'))

                res, status_code = resource['subscription_api'].verify_swap_device_info_api(loc_id=location,
                                                                                swap_device_type=swap_dev_typ,
                                                                                swap_device_sno=swap_dev_serial_no,
                                                                                sub_id=sub_id, device_id=created_dev_id)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                swapped_dev_id = res['deviceID']

            with allure.step("Fetches the details of swapped device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id,
                                                                                                swap_dev_serial_no,
                                                                                                swap_dev_typ)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                updt_fetched_dev_id = res['deviceID']

            with allure.step("Validates that fetched details match to that of swapped device: "):
                if swapped_dev_id != updt_fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the swapped one")

            with allure.step("Delete the details of swapped device: "):
                res, status_code = resource['subscription_api'].verify_delete_device_details_by_device_sno_api(sub_id,
                                                                                                   swap_dev_serial_no,
                                                                                                   swap_dev_typ)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in deleting the device details. Expected : 200, Received : " + str(
                            status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    @pytest.mark.regression
    def test_89_verify_swap_device_info_from_claim_api(self, rp_logger, resource):
        """
        This test validates that device details can be registered as per the provided info (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Verifies that device can be registered with valid details: "):

            location = str(resource['data_reader'].get_data(self.configparameter, test_name, 'locId'))
            device_type = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))

            res, status_code = resource['subscription_api'].verify_register_device_info_api(loc_id=location,
                                                                                device_type=device_type,
                                                                                device_sno=dev_serial_no, sub_id=sub_id)
            if status_code != 201:
                self.Failures.append("Device is not registered successfully. Expected : 201, Received : " + str(
                    status_code))

            else:
                created_dev_id = res['deviceID']
                created_client_id = res['clientID']

            with allure.step("Fetches the details of registered device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id, dev_serial_no,
                                                                                                device_type)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                fetched_dev_id = res['deviceID']
                fetched_client_id = res['clientID']

            with allure.step("Validates that fetched details match to that of created device: "):
                if created_client_id != fetched_client_id and created_dev_id != fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the created one")

            with allure.step("Swap the details of registered device: "):
                swap_dev_serial_no = str(resource['data_reader'].get_data(self.configparameter, test_name, 'swapDeviceSNo'))
                swap_dev_typ = str(resource['data_reader'].get_data(self.configparameter, test_name, 'swapDeviceType'))

                res, status_code = resource['subscription_api'].verify_swap_device_info_from_claim_api(loc_id=location,
                                                                                           swap_device_type=swap_dev_typ,
                                                                                           swap_device_sno=swap_dev_serial_no,
                                                                                           device_id=created_dev_id)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                swapped_dev_id = res['deviceID']

            with allure.step("Fetches the details of swapped device: "):
                res, status_code = resource['subscription_api'].verify_get_device_details_by_device_sno_api(sub_id,
                                                                                                swap_dev_serial_no,
                                                                                                swap_dev_typ)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in fetching device details. Expected : 200, Received : " + str(
                            status_code))
                updt_fetched_dev_id = res['deviceID']

            with allure.step("Validates that fetched details match to that of swapped device: "):
                if swapped_dev_id != updt_fetched_dev_id:
                    self.Failures.append("Fetched device details do not match with the swapped one")

            with allure.step("Delete the details of swapped device: "):
                res, status_code = resource['subscription_api'].verify_delete_device_details_by_device_sno_api(sub_id,
                                                                                                   swap_dev_serial_no,
                                                                                                   swap_dev_typ)
                if status_code != 200:
                    self.Failures.append(
                        "There is an error in deleting the device details. Expected : 200, Received : " + str(
                            status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
