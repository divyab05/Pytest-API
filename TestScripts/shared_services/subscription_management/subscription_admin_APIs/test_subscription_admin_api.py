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
class TestSubscriptionAPI(common_utils):

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


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_01_verify_subscription_creation(self, rp_logger, resource):
        """
        This test validates subscription creation is success or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        # "Call Subscription Creation API and Validate"):
        SubID = "AutoSub" + str(datetime.datetime.now())
        entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
        res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        # "Validate that satus code of create subscription API is correct"):
        assert self.validate_expected_and_actual_response_code(201, status_code) is True
        created_sub_id = res['subID']

        # Fetch the created subscription
        res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(created_sub_id)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        # "Delete the created subscription: ":
        status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)

        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(created_sub_id)

        assert self.validate_expected_and_actual_response_code(404, status_code) is True


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_02_verify_duplicate_subscription_creation(self, rp_logger, resource):
        """
        This test validates duplicate subscription creation is success or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        # "Call Subscription Creation API and Validate":
        SubID = "AutoSub" + str(datetime.datetime.now())
        entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
        result, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
        expected_error_msg = str(resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg'))

        assert self.validate_expected_and_actual_response_code(201, status_code) is True

        created_sub_id = result['subID']

        res, status_code = resource['subscription_api'].verify_create_duplicate_subscription_api(SubID, EntID=entId)

        assert self.validate_expected_and_actual_response_code(400, status_code) is True

        assert self.validate_expected_and_actual_values_code(str(res['errors'][0]['errorCode']),
                                                             expected_error_msg) is True

        status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
        assert self.validate_expected_and_actual_response_code(200, status_code) is True

        res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(created_sub_id)

        assert self.validate_expected_and_actual_response_code(404, status_code) is True


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_03_verify_subscription_creation_with_Invalid_enterprise(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with Invalid enterprise (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        # "Call Subscription Creation API with invalid EnterpriseId and Validate" :
        SubID = "SUBTEST" + str(datetime.datetime.now())
        EntID = "InvalidEnterprise"
        res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=EntID)
        error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
        error_msg = error_msg.replace("?", EntID)

        assert self.validate_expected_and_actual_response_code(400, status_code) is True

        assert self.validate_expected_and_actual_values_code(str(res['errors'][0]['errorDescription']),
                                                             str(error_msg)) is True
        # if res['errors'][0]['errorDescription'] != error_msg and status_code != 400:
        #     self.Failures.append(
        #         "There is a failure in creation of subscription with invalid enterprise response : Expected status code: 400 , Received : " + str(
        #             status_code))


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_04_verify_subscription_creation_with_invalid_plan(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with Invalid plan (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        # "Call Subscription Creation API with invalid Plans and Validate" :
        SubID = "AutoSub" + str(datetime.datetime.now())
        planID = ["Invalid_Plan"]
        entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
        res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId, PlanIDs=planID)
        # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, )
        error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
        error_msg = error_msg.replace("?", planID[0])
        if res['errors'][0]['errorDescription'] != error_msg and status_code != 400:
            self.Failures.append(
                "There is a failure in creation of subscription with invalid plans response : Expected status code: 400 , Received : " + str(
                    status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_05_verify_subscription_creation_with_invalid_carrier(self, rp_logger, resource):
        """
        This test validates subscription creation is failure or not with Invalid carrier (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API with invalid Carrier and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            CarrierID = ["Invalid_Carrier"]
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')

            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId, Carriers=CarrierID)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            error_msg = error_msg.replace("?", CarrierID[0])
            if res['errors'][0]['errorDescription'] != error_msg and status_code != 400:
                self.Failures.append(
                    "There is a failure in creation of subscription with invalid carrier response : Expected status code: 400 , Received : " + str(
                        status_code))
            exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_06_verify_get_subscription_plans_api(self, rp_logger, resource):
        """
        This test validates that plans can be fetched from subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            planID = ["SENDING_PLAN"]
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId, PlanIDs=planID)

            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, PlanIDs=planID)

            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected status code: 201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Call Get Subscription plan API and Validate"):
                    res, status_code = resource['subscription_api'].verify_get_subscription_plans(SubID)
                    if res != planID and status_code != 200:
                        self.Failures.append(
                            "There is a failure in get subscription API response : Expected status code: 200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_07_verify_add_location_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that location can be added to the subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_location_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_08_verify_get_locations_from_subscription_api(self, rp_logger, resource):
        """
        This test validates hat locations can be fetched from subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_location_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added locations from subscription "):
                    res, status_code = resource['subscription_api'].verify_get_locations_from_subscription_plans(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching the locations : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_09_verify_add_plans_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that plans can be added to the created subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_plans_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_10_verify_get_plans_from_subscription_api(self, rp_logger, resource):
        """
        This test validates that plans can be fetched from subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch the plans available in a subscription "):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_plans_from_subscription_plans_api(sub_id_input)
            plans_size = len(res)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching the locations : Expected:200 , Received : " + str(status_code))
            if plans_size == 0:
                self.Failures.append(
                    "There are no available plans the subscription. : ")
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_11_verify_delete_plans_from_subscription_api(self, rp_logger, resource):
        """
        This test validates that plans can be deleted from the created subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that plans can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_plans_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding plans to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added plans from subscription "):
                    res, status_code = resource['subscription_api'].verify_get_plans_from_subscription_plans_api(created_sub_id)
                    total_plans = len(res)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching the plans : Expected:200 , Received : " + str(status_code))

                with allure.step("Delete the plans from subscription: "):
                    status_code = resource['subscription_api'].verify_delete_plans_from_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the plans from subscription after deleting some: "):
                    res, status_code = resource['subscription_api'].verify_get_plans_from_subscription_plans_api(created_sub_id)
                    updated_plans = len(res)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching the plans : Expected:200 , Received : " + str(status_code))
                    if updated_plans == total_plans:
                        self.Failures.append(
                            "Plans are not deleted successfully")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_12_verify_delete_locations_from_subscription_api(self, rp_logger, resource):
        """
        This test validates that locations can be deleted successfully from subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_location_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added locations from subscription "):
                    res, status_code = resource['subscription_api'].verify_get_locations_from_subscription_plans(created_sub_id)
                    total_locations = len(res)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching the locations : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Validate that locations can be deleted from subscription"):
                    status_code = resource['subscription_api'].verify_delete_locations_from_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added locations from subscription "):
                    res, status_code = resource['subscription_api'].verify_get_locations_from_subscription_plans(created_sub_id)
                    updated_total_locations = len(res)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching the locations : Expected:200 , Received : " + str(
                                status_code))

                    if updated_total_locations == total_locations:
                        self.Failures.append(
                            "Locations are not deleted successfully")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_13_verify_add_duplicate_plans_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that duplicate plans can not be added to the created subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_plans_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Validate that duplicate locations can not be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_plans_subscription_api(created_sub_id)
                    if status_code != 400:
                        self.Failures.append(
                            "Error is not obtained while adding duplicate locations. Expected status code: 400, Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_14_verify_add_duplicate_location_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that duplicate loctaion can not be added to subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that locations can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_location_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding location to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Validate that duplicate locations can not be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_location_subscription_api(created_sub_id)
                    if status_code != 400:
                        self.Failures.append(
                            "Duplicate locations shouldn't be added. Expected: 400 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_15_verify_add_carriers_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that carriers can be added successfully to subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that carriers can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_carriers_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added carriers from the subscripton and validate that size is > 0"):
                    res, status_code = resource['subscription_api'].verify_get_carriers_from_subscription_plans_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))
                    else:
                        carriers_size = len(res)
                        if carriers_size == 0:
                            self.Failures.append("Carriers are not added to the subscription : ")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_16_verify_delete_carriers_from_subscription_api(self, rp_logger, resource):
        """
        This test validates that carriers can be deleted successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that carriers can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_carriers_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added carriers from the subscripton and validate that size is > 0"):
                    res, status_code = resource['subscription_api'].verify_get_carriers_from_subscription_plans_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))
                    else:
                        carriers_size = len(res)

                        if carriers_size == 0:
                            self.Failures.append("Carriers are not added to the subscription : ")

                with allure.step(
                        "Delete some of the added carriers from the subscripton and validate status code and total carriers"):
                    status_code = resource['subscription_api'].verify_delete_carriers_from_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting carriers from created subscription : Expected:200 , Received : " + str(
                                status_code))

                    res, status_code = resource['subscription_api'].verify_get_carriers_from_subscription_plans_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))
                    updated_carriers_size = len(res)

                    if updated_carriers_size >= carriers_size:
                        self.Failures.append(
                            "Carriers are not deleted successfully. Size after deleting should be <= carriers size")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_17_verify_get_carriers_from_subscription_api(self, rp_logger, resource):
        """
        This test validates that carriers can be fetched from subscription successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that carriers can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_carriers_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the added carriers from the subscripton and validate that size is >0"):
                    res, status_code = resource['subscription_api'].verify_get_carriers_from_subscription_plans_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in fetching carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))
                    carriers_size = len(res)
                    if carriers_size == 0:
                        self.Failures.append("Carriers are not added to the subscription : ")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_18_verify_add_duplicate_carriers_to_subscription_api(self, rp_logger, resource):
        """
        This test validates that duplicate carriers can not be added to subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Validate that carriers can be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_carriers_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding carriers to created subscription : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Validate that duplicate carriers can not be added to created subscription"):
                    status_code = resource['subscription_api'].verify_add_carriers_subscription_api(created_sub_id)
                    if status_code != 400:
                        self.Failures.append(
                            "Duplicate carriers shouldn't be added to the subscription. Expected status code: 400. Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_19_verify_get_subscriptions_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            res, status_code = resource['subscription_api'].verify_get_subscriptions_api()

        with allure.step("Validate that satus code of get subscriptions API is correct"):
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in get subscriptions API response : Expected:200 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_20_verify_get_subscription_by_id_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(sub_id_input)

        with allure.step("Validate that satus code of get subscriptions API is correct"):
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in get subscriptions API response : Expected:200 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_21_verify_get_subscription_by_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription by invalid id and Validate status code"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(sub_id_input)

        with allure.step("Validate that correct error code is obtained"):
            if status_code != 404 and res['errors'][0]['errorDescription'] != str(
                    resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')):
                self.Failures.append(
                    "There is a failure in fetching subscription by invalid Id: Expected: 404 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_22_verify_get_subscriptions_count_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            res, status_code = resource['subscription_api'].verify_get_subscription_count_api()
            sub_count = res['count']

        with allure.step("Validate that satus code of get subscriptions count is correct and count is > 0"):
            if status_code != 200 and sub_count == 0:
                self.Failures.append(
                    "There is a failure in fetching subscription count: Expected: > 1 , Received : " + str(
                        sub_count))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_23_verify_get_subscription_user_by_user_id_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            user_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_subs_user_by_user_id_resp = resource['subscription_api'].get_subscription_user_by_user_id_api(sub_id_input, user_input)

        with allure.step("Validate that status code of fetch user API is correct."):
            if get_subs_user_by_user_id_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching users by Id: Expected: 200 , Received : " + str(
                        get_subs_user_by_user_id_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_24_verify_get_user_subscriptions_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            user_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_subs_resp = resource['subscription_api'].get_user_subscription_details_by_user_id_api(user_input)

        with allure.step("Validate that status code of fetch user API is correct."):
            if get_user_subs_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching users by Id: Expected: 200 , Received : " + str(
                        get_user_subs_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_25_verify_get_user_subscriptions_by_invalid_user_id_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            user_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_subs_resp = resource['subscription_api'].get_user_subscription_details_by_user_id_api(user_input)

        with allure.step("Validate that status code of fetch user API is correct."):
            if get_user_subs_resp.status_code != 404 and get_user_subs_resp['errors'][0]['errorDescription'] != str(
                    resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')):
                self.Failures.append(
                    "There is a failure in fetching subscription by invalid Id: Expected: 404 , Received : " + str(
                        get_user_subs_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_26_verify_get_subscriptions_by_enterprise_id_api(self, rp_logger, resource):
        """
        This test validates that subscriptions can be fetched successfully by enterprise Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            ent_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            res, status_code = resource['subscription_api'].verify_get_subscriptions_by_enterprise_id_api(ent_id)

        with allure.step("Validate that status code of fetch user API is correct."):
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching subscriptions by ent Id: Expected: 200 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_27_verify_get_subscription_properties_api(self, rp_logger, resource):
        """
        This test validates that subscription properties can be fetched successfully by enterprise Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_subscription_properties_api(sub_id)

        with allure.step("Validate that status code of fetch user API is correct."):
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching subscription properties. Expected: 200 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_28_verify_get_subscription_properties_by_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when subscription properties are fetched by invalid subId (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_subscription_properties_api(sub_id)

        with allure.step("Validate that status code of fetch user API is correct."):
            if status_code != 400:
                self.Failures.append(
                    "Wrong status code obtained. Expected: 400 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_29_verify_get_subscription_roles_api(self, rp_logger, resource):
        """
        This test validates that subscription roles can be fetched successfully by enterprise Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            get_subs_roles_resp = resource['subscription_api'].get_subscription_roles_api(sub_id)

        with allure.step("Validate that status code of fetch user API is correct."):
            if get_subs_roles_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching subscription properties. Expected: 200 , Received : " + str(
                        get_subs_roles_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_30_verify_get_subscription_roles_by_invalid_sub_id_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when roles are fetched by negative subId (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call get subscription API and Validate status code"):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            get_subs_roles_resp = resource['subscription_api'].get_subscription_roles_api(sub_id)

        with allure.step("Validate that status code of fetch user API is correct."):
            if get_subs_roles_resp.status_code != 400:
                self.Failures.append(
                    "There is a failure in fetching subscription properties. Expected: 400 , Received : " + str(
                        get_subs_roles_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_31_verify_update_subscription_api(self, rp_logger, resource):
        """
        This test validates subscription can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step(
                        "Call Get Subscription plan API and fetch the total plans and carriers size before update: "):
                    res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(SubID)
                    total_plans = len(res['plans'])
                    carriers_size = len(res['carriers'])

                with allure.step("Call update Subscription plan API and Validate"):
                    status_code = resource['subscription_api'].verify_update_subscription_api(SubID, EntID=entId)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in update subscription API response : Expected:200 , Received : " + str(
                                status_code))

                with allure.step(
                        "Call Get Subscription plan API and fetch the updated plans and updated carriers size: "):
                    res, status_code = resource['subscription_api'].verify_get_subscription_by_id_api(SubID)
                    total_plans_updated = len(res['plans'])
                    carriers_size_updated = len(res['carriers'])

                with allure.step("Validate that updated size is greater than the original one: "):
                    if total_plans_updated < total_plans and carriers_size_updated < carriers_size:
                        self.Failures.append("Subscription plans are not updated successfully")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_32_verify_update_subscription_properties_api(self, rp_logger, resource):
        """
        This test validates subscription properties cn be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']
                with allure.step(
                        "Call Get Subscription properties API and fetch the value of maxTxLimit before update: "):
                    res, status_code = resource['subscription_api'].verify_get_subscription_properties_api(created_sub_id)
                    ledgerProductID_before_update = str(res['ledgerProductID'])

                with allure.step("Call update Subscription properties API and Validate"):
                    ledgerProductID = 'ABC123'
                    res, status_code = resource['subscription_api'].verify_update_subscription_properties_api(created_sub_id,
                                                                                                  ledgerProductID)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in update subscription properties API response : Expected:200 , Received : " + str(
                                status_code))
                    else:
                        res, status_code = resource['subscription_api'].verify_get_subscription_properties_api(created_sub_id)
                        systemUserNotification_after_update = str(res['systemUserNotification'])
                        # maxTxLimit_after_update = str(res['maxTxLimit'])
                        if systemUserNotification_after_update == ledgerProductID:
                            self.Failures.append(
                                "Value of systemUserNotification_before_update is not matching the provided value.")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_33_verify_update_locker_size_api(self, rp_logger, resource):
        """
        This test validates that locker size can be updated as per the provided value (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Call update locker size API and fetch the value of updated length: "):
                    length = resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam')
                    res, status_code = resource['subscription_api'].verify_update_locker_size_api(created_sub_id, length)
                    length_received = str(res[0]['dimension']['length'])

                    if status_code != 200 and length_received != length:
                        self.Failures.append(
                            "There is a failure in updating the locker size : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_34_verify_get_locker_size_api(self, rp_logger, resource):
        """
        This test fetches the locker size of subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)
            # res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Call update locker size API and fetch the value of updated length: "):
                    length = resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam')
                    res, status_code = resource['subscription_api'].verify_update_locker_size_api(created_sub_id, length)

                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in updating the locker size : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Fetch the updated locker size: "):
                    res, status_code = resource['subscription_api'].verify_get_locker_size_api(created_sub_id)
                    length_received = str(res[0]['dimension']['length'])
                    if status_code != 200 and length_received != length:
                        self.Failures.append(
                            "There is a failure in fetching the locker size : Expected:200 , Received : " + str(
                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_35_verify_get_locker_size_by_invalid_sub_id_api(self, rp_logger, resource):
        """
        This test fetches the locker size of subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch the updated locker size by invalid id: "):
            sub_id = resource['data_reader'].get_data(self.configparameter, test_name, 'subId')
            res, status_code = resource['subscription_api'].verify_get_locker_size_api(sub_id)
            if status_code != 400:
                self.Failures.append(
                    "There is a failure in fetching the locker size by invalid id : Expected:400 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_36_verify_get_locker_sub_properties_api(self, rp_logger, resource):
        """
        This test fetches the sub properties of locker size (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch the updated locker size by invalid id: "):
            sub_id = resource['data_reader'].get_data(self.configparameter, test_name, 'subId')
            res, status_code = resource['subscription_api'].verify_get_locker_sub_properties_api(sub_id)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching locker subproperty API response : Expected:200 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_37_verify_get_locker_sub_properties_by_invalid_api(self, rp_logger, resource):
        """
        This test fetches the sub properties of locker size by invalid id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch the updated locker size by invalid id: "):
            sub_id = resource['data_reader'].get_data(self.configparameter, test_name, 'subId')
            res, status_code = resource['subscription_api'].verify_get_locker_sub_properties_api(sub_id)
            if status_code != 400:
                self.Failures.append(
                    "There is a failure in fetching locker subproperty API response : Expected:400 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_38_verify_get_roles_from_subscription_api(self, rp_logger, resource):
        """
        This test fetches the roles assigned in a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch the roles available in subscription: "):
            sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(sub_id)
            total_roles = len(res)

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching roles from get roles from subscription API: Expected: 200 , Received : " + str(
                        status_code))

            if total_roles == 0:
                self.Failures.append(
                    "No roles are added to the subscription plan. Expected > 0, Received " + str(
                        total_roles))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_39_verify_add_roles_subscription_api(self, rp_logger, resource):
        """
        This test adds the roles to a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)

                if status_code != 200:
                    self.Failures.append(
                        "There is a failure in fetching roles from get roles from subscription API: Expected: 200 , Received : " + str(
                            status_code))
                total_roles = len(res)

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:
                        with allure.step("Fetch the roles available in the subscription after adding new roles: "):
                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            total_updated_roles = len(res)
                            added_role_id = res[0]['roleID']
                            if status_code != 200 and total_updated_roles < total_roles:
                                self.Failures.append(
                                    "New roles are not added successfully to the subscription.")

                            else:
                                with allure.step("Delete the added role: "):
                                    status_code = resource['subscription_api'].verify_delete_roles_from_subscription_api(
                                        created_sub_id,
                                        added_role_id)
                                    if status_code != 200:
                                        self.Failures.append(
                                            "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                                status_code))
                    with allure.step("Delete the created subscription: "):
                        status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                    status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_40_verify_update_roles_subscription_api(self, rp_logger, resource):
        """
        This test fetches updates the roles assigned in a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Add new roles to the subscription: "):

                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                with allure.step("Fetch the roles available in the subscription after adding new roles: "):
                    res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                    total_updated_roles = len(res)

                    added_role_id = res[total_updated_roles - 1]['roleID']
                    if status_code != 200 and total_updated_roles < created_sub_id:
                        self.Failures.append(
                            "New roles are not added successfully to the subscription.")

                with allure.step("Update the name of added role: "):
                    updated_name_val = 'Auto_plan_update_'
                    update_subs_role_resp = resource['subscription_api'].update_subscription_role_api(created_sub_id, added_role_id,
                                                                                            updated_name_val)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in updating the name of the added role. Expected: 200 , Received : " + str(
                                update_subs_role_resp.status_code))
                    else:
                        with allure.step(
                                "Fetch the roles available in the subscription after updating the name of the new role: "):
                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            updated_role_name = str(res[total_updated_roles - 1]['name'])
                            if updated_role_name != updated_name_val:
                                self.Failures.append(
                                    "Name is not updated successfully. Expected name: " + updated_name_val + " Updated name : " + updated_role_name)

                        with allure.step("Delete the created subscription: "):
                            status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_41_verify_delete_roles_subscription_api(self, rp_logger, resource):
        """
        This test fetches deleted the roles assigned in a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:
                        with allure.step("Fetch the roles available in the subscription after adding new roles: "):
                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            total_updated_roles = len(res)
                            added_role_id = res[0]['roleID']
                            if status_code != 200:
                                self.Failures.append(
                                    "New roles are not added successfully to the subscription.")

                            else:
                                with allure.step("Delete the added role: "):
                                    status_code = resource['subscription_api'].verify_delete_roles_from_subscription_api(
                                        created_sub_id,
                                        added_role_id)
                                    if status_code != 200:
                                        self.Failures.append(
                                            "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                                status_code))
                                    else:
                                        with allure.step(
                                                "Fetch the roles available in the subscription after deleting the new roles: "):
                                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(
                                                created_sub_id)
                                            total_roles_after_delete = len(res)
                                            if status_code != 200:
                                                self.Failures.append(
                                                    "There is a failure in fetching roles from get roles from subscription API: Expected: 200 , Received : " + str(
                                                        status_code))

                                            if total_roles_after_delete > total_updated_roles:
                                                self.Failures.append("Total roles after deleting do not match.")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_42_verify_delete_non_existent_roles_subscription_api(self, rp_logger, resource):
        """
        This test fetches updates the roles assigned in a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)

                if status_code != 200:
                    self.Failures.append(
                        "There is a failure in fetching roles from get roles from subscription API: Expected: 200 , Received : " + str(
                            status_code))
                total_roles = len(res)

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:
                        with allure.step("Fetch the roles available in the subscription after adding new roles: "):
                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            total_updated_roles = len(res)
                            added_role_id = res[0]['roleID']
                            if status_code != 200 and total_updated_roles < total_roles:
                                self.Failures.append(
                                    "New roles are not added successfully to the subscription.")

                            else:
                                with allure.step("Delete the added role: "):
                                    status_code = resource['subscription_api'].verify_delete_roles_from_subscription_api(
                                        created_sub_id,
                                        added_role_id)
                                    if status_code != 200:
                                        self.Failures.append(
                                            "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                                status_code))

                                    else:
                                        with allure.step("Try to delete the added role again: "):
                                            status_code = resource['subscription_api'].verify_delete_roles_from_subscription_api(
                                                created_sub_id, added_role_id)
                                            if status_code != 400:
                                                self.Failures.append(
                                                    "Error should be obtained while deleting the non existent role. Expected: 400 , Received : " + str(
                                                        status_code))

                        with allure.step("Delete the created subscription: "):
                            status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_43_verify_add_features_to_subscription_role_api(self, rp_logger, resource):
        """
        This test adds the features to the subscription roles (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:

                        with allure.step(
                                "Fetch the features available in the subscription role before adding any new feature: "):

                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            role = res[0]['roleID']
                            role_id = str(role)
                            features_before_add = len(res[0]['features'])

                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in fetching features from subscription roles : Expected: 200 , Received : " + str(
                                    status_code))

                        with allure.step("Add features to subscription roles : "):

                            # role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
                            status_code = resource['subscription_api'].verify_add_features_in_subscription_role_api(created_sub_id,
                                                                                                        role_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in adding features to subscription roles : Expected: 200 , Received : " + str(
                                        status_code))

                            else:
                                res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(
                                    created_sub_id)

                                if status_code != 200:
                                    self.Failures.append(
                                        "There is a failure in fetching features from subscription roles : Expected: 200 , Received : " + str(
                                            status_code))

                                else:
                                    features_after_add = len(res[0]['features'])

                                    if features_before_add > features_after_add:
                                        self.Failures.append(
                                            "Features are not added to the plan : ")

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_45_verify_delete_non_existent_features_from_subscription_role_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when non existent features are deleted from subscription roles (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:

                        with allure.step(
                                "Fetch the features available in the subscription role before adding any new feature: "):

                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            role = res[0]['roleID']
                            role_id = str(role)

                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in fetching features from subscription roles : Expected: 200 , Received : " + str(
                                    status_code))

                        with allure.step("Add features to subscription roles : "):

                            # role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
                            status_code = resource['subscription_api'].verify_add_features_in_subscription_role_api(created_sub_id,
                                                                                                        role_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in adding features to subscription roles : Expected: 200 , Received : " + str(
                                        status_code))

                            else:
                                res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(
                                    created_sub_id)

                                if status_code != 200:
                                    self.Failures.append(
                                        "There is a failure in fetching features from subscription roles : Expected: 200 , Received : " + str(
                                            status_code))

                                else:
                                    features_after_add = len(res[0]['features'])
                                    with allure.step("Delete the added feature from subscription role: "):
                                        status_code = resource['subscription_api'].verify_delete_features_in_subscription_role_api(
                                            created_sub_id, role_id)
                                        if status_code != 200:
                                            self.Failures.append(
                                                "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                                    status_code))

                                    with allure.step("Delete the added feature from subscription role again: "):
                                        status_code = resource['subscription_api'].verify_delete_features_in_subscription_role_api(
                                            created_sub_id, role_id)
                                        if status_code != 400:
                                            self.Failures.append(
                                                "Error should be obtained while deleting non existent features. Expected: 400 , Received : " + str(
                                                    status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_46_verify_duplicate_features_to_subscription_role_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when duplicate features are added to subscription roles (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Call Subscription Creation API and Validate"):
            SubID = "AutoSub" + str(datetime.datetime.now())
            entId = resource['data_reader'].get_data(self.configparameter, test_name, 'entId')
            res, status_code = resource['subscription_api'].verify_create_subscription_api(SubID, EntID=entId)

        with allure.step("Validate that satus code of create subscription API is correct"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in create subscription API response : Expected:201 , Received : " + str(
                        status_code))

            else:
                created_sub_id = res['subID']

                with allure.step("Add new roles to the subscription: "):
                    add_roles_resp = resource['subscription_api'].add_subscription_roles_to_subscription_api(created_sub_id)
                    if add_roles_resp.status_code != 200:
                        self.Failures.append(
                            "There is a failure in adding new roles Expected: 200 , Received : " + str(
                                add_roles_resp.status_code))

                    else:

                        with allure.step(
                                "Fetch the features available in the subscription role before adding any new feature: "):

                            res, status_code = resource['subscription_api'].verify_get_roles_from_subscription_api(created_sub_id)
                            role = res[0]['roleID']
                            role_id = str(role)
                            features_before_add = len(res[0]['features'])

                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in fetching features from subscription roles : Expected: 200 , Received : " + str(
                                    status_code))

                        with allure.step("Add features to subscription roles : "):

                            # role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
                            status_code = resource['subscription_api'].verify_add_features_in_subscription_role_api(created_sub_id,
                                                                                                        role_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in adding features to subscription roles : Expected: 200 , Received : " + str(
                                        status_code))

                            else:
                                with allure.step(
                                        "Add duplicate features to subscription roles and verify that error is obtained : "):

                                    status_code = resource['subscription_api'].verify_add_features_in_subscription_role_api(
                                        created_sub_id,
                                        role_id)
                                    if status_code != 400:
                                        self.Failures.append(
                                            "Error sould be obtained while adding duplicate features to subscription roles : Expected: 400 , Received : " + str(
                                                status_code))

                with allure.step("Delete the created subscription: "):
                    status_code = resource['subscription_api'].archive_subscription_api(created_sub_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the subscription : Expected:200 , Received : " + str(
                                status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
