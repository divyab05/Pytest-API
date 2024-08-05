""" This module contains all test cases."""

import datetime
import inspect
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
class TestSubscription_Client_API(common_utils):

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
    def test_47_verify_get_subscription_user_from_claim_by_sub_id_api(self, rp_logger, resource):
        """
        This test fetches the claims of a user as per the subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch subscription user from claim: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_user_from_claim_by_sub_id_api()
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching subscription user from claim API: Expected: 200 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_49_verify_get_subscription_user_from_claim_by_user_id_api(self, rp_logger, resource):
        """
        This test fetches the claims of a user as per the subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch subscription user from claim: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_user_from_claim_by_user_id_api()
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching subscription user from claim API: Expected: 200 , Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_50_verify_add_roles_to_subscription_from_claim_api(self, rp_logger, resource):
        """
        This test adds the roles to a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step(
                "Fetch the total subscriptions available in the subscription role before adding any new role: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_roles_from_claim_api()

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching roles from subscription : Expected: 200 , Received : " + str(
                        status_code))
            else:
                sub_role_id = res[0]['roleID']

                with allure.step("Delete the added role from subscription: "):
                    status_code = resource['subscription_api'].verify_delete_subscription_role_from_claim_by_api(
                        sub_role_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                status_code))
                    else:
                        status_code = resource['subscription_api'].verify_add_roles_to_subscription_from_claim_api(
                            sub_role_id)
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in adding new role to subscription : Expected: 200 , Received : " + str(
                                    status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_51_verify_update_roles_to_subscription_from_claim_api(self, rp_logger, resource):
        """
        This test validates that added roles can be updated (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Add new role to the subscription claim: "):
            role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            status_code = resource['subscription_api'].verify_add_roles_to_subscription_from_claim_api(role_id)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in adding new role to subscription : Expected: 200 , Received : " + str(
                        status_code))

        with allure.step("Add new role to the subscription claim: "):
            updated_name = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            status_code = resource['subscription_api'].verify_update_roles_to_subscription_from_claim_api(role_id,
                                                                                                          updated_name)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in updating role to subscription : Expected: 200 , Received : " + str(
                        status_code))

        with allure.step("Delete the added role from subscription: "):
            status_code = resource['subscription_api'].verify_delete_subscription_role_from_claim_by_api(role_id)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_52_verify_delete_subscription_roles_from_claim_api(self, rp_logger, resource):
        """
        This test deletes the added roles to a subscription (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step(
                "Fetch the total subscriptions available in the subscription role before adding any new role: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_roles_from_claim_api()

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching roles from subscription : Expected: 200 , Received : " + str(
                        status_code))
            else:
                sub_role_id = res[0]['roleID']

                with allure.step("Delete the added role from subscription: "):
                    status_code = resource['subscription_api'].verify_delete_subscription_role_from_claim_by_api(
                        sub_role_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in deleting the added role. Expected: 200 , Received : " + str(
                                status_code))

                    else:
                        with allure.step("Add new role to the subscription claim: "):
                            role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
                            status_code = resource['subscription_api'].verify_add_roles_to_subscription_from_claim_api(
                                sub_role_id)
                            if status_code != 200:
                                self.Failures.append(
                                    "There is a failure in adding new role to subscription : Expected: 200 , Received : " + str(
                                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_53_verify_delete_subscription_roles_from_claim_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when invalid id is passed while deleting subscription roles (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Error should be obtained when invalid role id is deleted: "):
            role_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'entId'))
            status_code = resource['subscription_api'].verify_delete_subscription_role_from_claim_by_api(role_id)
            if status_code != 400:
                self.Failures.append(
                    "Correct error code is not obtained. Expected: 400 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_54_verify_duplicate_subscription_roles_from_claim_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when duplicate roles are added to a subscription (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step(
                "Fetch the total subscriptions available in the subscription role before adding any new role: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_roles_from_claim_api()

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching roles from subscription : Expected: 200 , Received : " + str(
                        status_code))
            else:
                sub_role_id = res[0]['roleID']

        with allure.step("Add duplicate role to the subscription claim: "):
            status_code = resource['subscription_api'].verify_add_roles_to_subscription_from_claim_api(sub_role_id)
            if status_code != 400:
                self.Failures.append(
                    "There is a failure in adding duplicate role to subscription : Expected: 400 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_55_verify_add_features_to_subscription_from_claim_api(self, rp_logger, resource):
        """
        This test validates that features can be added to subscription claim successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step(
                "Fetch the total subscriptions available in the subscription role before adding any new role: "):
            res, status_code = resource['subscription_api'].verify_get_subscription_roles_from_claim_api()

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching roles from subscription : Expected: 200 , Received : " + str(
                        status_code))
            else:
                sub_role_id = res[0]['roleID']

                status_code = resource['subscription_api'].verify_add_features_to_subscription_from_claim_api(
                    sub_role_id)
                if status_code != 200:
                    self.Failures.append(
                        "There is a failure in adding features to subscription : Expected: 200 , Received : " + str(
                            status_code))
                else:
                    with allure.step("Delete the added role from subscription: "):
                        status_code = resource['subscription_api'].verify_delete_subscription_features_from_claim_api(
                            sub_role_id)
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in deleting the added feature. Expected: 200 , Received : " + str(
                                    status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_57_verify_update_subscription_properties_from_claim_api(self, rp_logger, resource):
        """
        This test validates that subscription properties can be updated (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Update properties of subscription claim : "):
            status_code = resource['subscription_api'].verify_update_subscription_properties_from_claim_api()
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in updating properties of subscription claim: Expected: 200 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_58_verify_get_subscription_prop_from_claim_api(self, rp_logger, resource):
        """
        This test validates that subscription properties can be fetched from claim (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch properties of subscription claim : "):
            res, status_code = resource['subscription_api'].verify_get_subscription_prop_from_claim_api()
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching properties of subscription claim: Expected: 200 , Received : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    # Test cases of user module starts here


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_59_verify_get_users_api(self, rp_logger, resource):
        """
        This test validates that users can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch list of users : "):
            get_users_resp = resource['subscription_api'].get_users_api()
            if get_users_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching users. Expected: 200 , Received : " + str(
                        get_users_resp.status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_60_verify_get_all_db_users_api(self, rp_logger, resource):
        """
        This test validates that all users lists can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetch list of all db users: "):
            limit = "3"
            get_userslist_with_limit_resp = resource['subscription_api'].get_all_users_list_api(limit)
            if get_userslist_with_limit_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching users. Expected: 200 , Received : "
                    + str(get_userslist_with_limit_resp.status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_61_verify_add_user_api(self, rp_logger, resource):
        """
        This test validates that user can be added successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Validate that users can be created successfully"):
            fname = "AutoFirst" + str(random.randint(1, 10000))
            lname = "AutoLast" + str(random.randint(1, 10000))
            mailid = str(fname + "." + lname + "@yopmail.com")
            dispname = str(fname + "." + lname)
            group_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            subId = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subId'))
            add_user_resp = resource['subscription_api'].add_admin_user_api(fname, lname, mailid, dispname, group_id)
            with allure.step("Validate that satus code of create user is correct"):
                if add_user_resp.status_code != 201:
                    self.Failures.append(
                        "There is a failure in creating a new user : Expected: 200 , Received : " + str(
                            add_user_resp.status_code))

                else:
                    created_user_id = add_user_resp.json()['userID']

                    with allure.step("Validate that satus code of create user is correct"):
                        get_user_by_user_id_resp = resource['subscription_api']\
                            .get_user_by_user_id_api(created_user_id)
                        if get_user_by_user_id_resp.status_code != 200:
                            self.Failures.append(
                                "There is a failure in fetching the created user api response : Expected: 200 , "
                                "Received : " + str(get_user_by_user_id_resp.status_code))

                    with allure.step("Delete the created user"):
                        del_user_resp = resource['subscription_api']\
                            .delete_user_api(user_id=created_user_id, sub_id=subId, is_admin='y')
                        if del_user_resp.status_code != 200:
                            self.Failures.append(
                                "There is a failure in Delete user api response : Expected: 200 , Received : "
                                + str(del_user_resp.status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_62_verify_get_user_profile_api(self, rp_logger, resource):
        """
        This test validates that user profiles fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the user profile: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_admin_user_profile_resp = resource['subscription_api'].get_admin_user_profile_by_user_id_api(user_id)
            if get_admin_user_profile_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching users. Expected: 200 , Received : "
                                     + str(get_admin_user_profile_resp.status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_63_verify_get_user_profile_by_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that error should be obtained when invalid id is passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Validate that error is obtained when invalid user id is provided: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_admin_user_profile_resp = resource['subscription_api'].get_admin_user_profile_by_user_id_api(user_id)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            error_msg = error_msg.replace("?", user_id)
            if get_admin_user_profile_resp.json()['errors'][0]['errorDescription'] != error_msg \
                    and get_admin_user_profile_resp.status_code != 404:
                self.Failures.append("Error should be obtained when fetching properties of invalid user id: "
                                     "Expected status code: 404. Received"
                                     + str(get_admin_user_profile_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_64_verify_get_user_profile_from_claim_api(self, rp_logger, resource):
        """
        This test validates user profile can be fetched from user claim
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the user profile from claim: "):
            get_admin_users_profile_resp = resource['subscription_api'].get_admin_users_profile_api()
            if get_admin_users_profile_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching user profiles from claim. Expected: 200 , "
                                     "Received : " + str(get_admin_users_profile_resp.status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_65_verify_get_user_by_id_api(self, rp_logger, resource):
        """
        This test validates that all users lists can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the user profile as per provided Id: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_by_user_id_resp = resource['subscription_api'].get_user_by_user_id_api(user_id)
            if get_user_by_user_id_resp.status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching user by given Id. Expected: 200 , Received : " + str(
                        get_user_by_user_id_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_66_verify_get_user_by_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when invalid Id is passed (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Validates that error is obtained when invalid user Id is provided: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_by_user_id_resp = resource['subscription_api'].get_user_by_user_id_api(user_id)
            error_msg = resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg')
            error_msg = error_msg.replace("?", user_id)
            if get_user_by_user_id_resp.json()['errors'][0]['errorDescription'] != error_msg \
                    and get_user_by_user_id_resp.status_code != 404:
                self.Failures.append(
                    "Error should be obtained when fetching properties of invalid user id: "
                    "Expected status code: 404. Received" + str(get_user_by_user_id_resp.status_code))
            exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_67_verify_get_roll_up_entity_api(self, rp_logger, resource):
        """
        This test validates that roll up entity can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the entity available in user profile: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_roll_up_entity_resp = resource['subscription_api'].get_user_roll_up_entity_api(user_id)
            entities = len(get_user_roll_up_entity_resp.json())
            if get_user_roll_up_entity_resp.status_code != 200 and entities == 0:
                self.Failures.append("There is a failure in fetching entity details of user by given Id. Expected: 200 "
                                     "and > 1 , Received : " + str(get_user_roll_up_entity_resp.status_code) +
                                     " and " + str(entities))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_68_verify_get_user_by_email_api(self, rp_logger, resource):
        """
        This test validates that users can be fetched by passing valid email (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the details of user as per the provided email: "):
            email = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            get_user_by_email_resp = resource['subscription_api'].get_user_by_email_api(email)
            if get_user_by_email_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching user details by email Id. Expected: 200, "
                                     "Received : " + str(get_user_by_email_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_69_verify_get_user_by_invalid_email_api(self, rp_logger, resource):
        """
        This test validates that errors is obtained when users is fetched by passing an invalid email (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Validates that error is obtained when invalid email is passed: "):
            email = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            get_user_by_email_resp = resource['subscription_api'].get_user_by_email_api(email)
            if get_user_by_email_resp.status_code != 400:
                self.Failures.append("Error should be obtained when fetching user by invalid email: Expected status "
                                     "code: 400. Received" + str(get_user_by_email_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_70_verify_get_user_properties_api(self, rp_logger, resource):
        """
        This test validates that user properties can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the entity available in user profile: "):
            get_user_properties_resp = resource['subscription_api'].get_user_properties_api()
            if get_user_properties_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching user details by email Id. Expected: 200, "
                                     "Received : " + str(get_user_properties_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_71_verify_get_enterprises_by_user_api(self, rp_logger, resource):
        """
        This test validates that enterprise details can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the entity available in user profile: "):
            get_enterprises_by_user_resp = resource['subscription_api'].get_enterprises_by_user_api()
            if get_enterprises_by_user_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching enterprise by user response. Expected: 200, "
                                     "Received : " + str(get_enterprises_by_user_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_72_verify_get_admin_entity_from_claim_api(self, rp_logger, resource):
        """
        This test validates that admin entity can be fetched successfully from subscription claim (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the admin entity available in user claim: "):
            get_user_admin_entity_resp = resource['subscription_api'].get_user_admin_entity_api()
            if get_user_admin_entity_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching enterprise by user claim response. Expected: 200, "
                                     "Received : " + str(get_user_admin_entity_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_73_verify_get_admin_level_entity_by_user_api(self, rp_logger, resource):
        """
        This test validates that admin level entity can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the admin entity available in user claim: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            get_user_admin_entity_user_id_resp = resource['subscription_api']\
                .get_user_admin_entity_by_user_id_api(user_id)
            if get_user_admin_entity_user_id_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching enterprise by user response. Expected: 200, "
                                     "Received : " + str(get_user_admin_entity_user_id_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)


    @pytest.mark.subscription_management_sp360commercial
    @pytest.mark.subscription_management_sp360commercial_reg
    @pytest.mark.skip(reason="Need refactoring and fixes")
    def test_74_verify_get_user_sublocation_by_userid_and_prodid_api(self, rp_logger, resource):
        """
        This test validates that users sublocation can be fetched successfully by valid userid and product Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the admin entity available in user claim: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            prod_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'inputParam'))
            get_user_by_id_prod_id_resp = resource['subscription_api']\
                .get_user_sub_location_by_user_id_and_prod_id_api(user_id, prod_id)
            if get_user_by_id_prod_id_resp.status_code != 200:
                self.Failures.append("There is a failure in fetching user sub-location response. Expected: 200, "
                                     "Received : " + str(get_user_by_id_prod_id_resp.status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @pytest.mark.subscription_management_sp360commercial_reg
    def test_75_verify_get_enriched_token_api(self, rp_logger, resource):
        """
        This test validates that enriched token can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        with allure.step("Fetches the enriched token as per the provided user Id and scope: "):
            user_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'userId'))
            status_code = resource['subscription_api'].verify_get_enriched_token_api(user_id)
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in fetching enriched token response. Expected: 200, Received : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
