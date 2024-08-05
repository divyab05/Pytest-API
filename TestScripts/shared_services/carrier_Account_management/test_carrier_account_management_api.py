""" This module contains all test cases."""
import sys

import allure
import pytest

from APIObjects.shared_services.carrier_account_management_api import CarrierAccountManagement
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus

exe_status = ExecutionStatus()


# subCarrier = CarrierAccountManagement()
# data_reader = DataReader()


@pytest.fixture()
def resource(app_config, generate_access_token):
    subCarrier = {}
    subCarrier['app_config'] = app_config
    subCarrier['subCarrier'] = CarrierAccountManagement(app_config, generate_access_token)
    subCarrier['data_reader'] = DataReader(app_config)
    yield subCarrier


@pytest.mark.usefixtures('initialize')
class TestSubcarrierAPI:

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

        self.configparameter = "CARRIER_Account_MGMT"
        if resource['data_reader'].get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")
        self.Failures = []

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_01_verify_subcarrier_fedex_creation(self, rp_logger, resource):
        """
        This test validates FedEx subcarrier creation is success or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'FedEx'
            desc = 'Auto_FedEx_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in Create subCarrier API response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Call Get SubCarriers by Id API and Validate the response"):
                        res_get_API, status_code_get_API = resource['subCarrier'].verify_get_subCarrier_By_Id_api(
                            created_subCarrier_Id)

                        if status_code_get_API != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                        else:
                            subCarrierId_get_res = res_get_API['subCarrierID']
                            if subCarrierId_get_res != created_subCarrier_Id:
                                self.Failures.append(
                                    "Fetched subCarrier is different from created one : Expected: " + created_subCarrier_Id + ", Recieved : " + subCarrierId_get_res)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

                            else:
                                with allure.step("Fetch the deleted carrier and validate error message: "):
                                    get_res, get_carrier_status = resource[
                                        'subCarrier'].verify_get_subCarrier_By_Id_api(
                                        created_subCarrier_Id)
                                    if get_carrier_status != 404:
                                        self.Failures.append(
                                            "There is a failure in get subCarrier response : Expected:404 , Recieved" + get_carrier_status)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_02_verify_subcarrier_ups_creation(self, rp_logger, resource):
        """
         This test validates UPS subcarrier creation is success or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'UPS'
            desc = 'Auto_UPS_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in Create subCarrier API response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Call Get SubCarriers by Id API and Validate the response"):
                        res_get_API, status_code_get_API = resource['subCarrier'].verify_get_subCarrier_By_Id_api(
                            created_subCarrier_Id)

                        if status_code_get_API != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                        else:
                            subCarrierId_get_res = res_get_API['subCarrierID']
                            if subCarrierId_get_res != created_subCarrier_Id:
                                self.Failures.append(
                                    "Fetched subCarrier is different from created one : Expected: " + created_subCarrier_Id + ", Recieved : " + subCarrierId_get_res)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

                            else:
                                with allure.step("Fetch the deleted carrier and validate error message: "):
                                    get_res, get_carrier_status = resource[
                                        'subCarrier'].verify_get_subCarrier_By_Id_api(
                                        created_subCarrier_Id)
                                    if get_carrier_status != 404:
                                        self.Failures.append(
                                            "There is a failure in get subCarrier response : Expected:404 , Recieved" + get_carrier_status)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_03_verify_get_subcarriers_api(self, rp_logger, resource):
        """
        This test fetches the details of subCarriers as per the provided subscription Id API (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
        carrier_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'carrier_id'))
        with allure.step("Call Get SubCarriers API and Validate fetched subscription Id"):
            res, status_code = resource['subCarrier'].verify_get_subCarriers_api(sub_id_input, carrier_id_input)

        with allure.step("Validate that satus code of get subcarrier API is correct"):
            if status_code != 200:
                self.Failures.append(
                    "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(status_code))

            else:
                subId = res["subCarriers"][0]["subID"]
                with allure.step("Validate that correct subscription Id is fetched"):
                    if subId != str(sub_id_input):
                        self.Failures.append(
                            "Incorrect subscription id is obained in get subCarrier response : Expected: " + str(
                                sub_id_input) + ", Recieved " + subId)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_04_verify_get_subcarrier_by_id_api(self, rp_logger, resource):
        """
         This test validates that created subcarrier can be fetched by its ID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'UPS'
            desc = 'Auto_UPS_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in Create subCarrier API response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Call Get SubCarriers by Id API and Validate the response"):
                        res_get_API, status_code_get_API = resource['subCarrier'].verify_get_subCarrier_By_Id_api(
                            created_subCarrier_Id)

                        if status_code_get_API != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                        else:
                            subCarrierId_get_res = res_get_API['subCarrierID']
                            if subCarrierId_get_res != created_subCarrier_Id:
                                self.Failures.append(
                                    "Fetched subCarrier is different from created one : Expected: " + created_subCarrier_Id + ", Recieved : " + subCarrierId_get_res)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

                            else:
                                with allure.step("Fetch the deleted carrier and validate error message: "):
                                    get_res, get_carrier_status = resource[
                                        'subCarrier'].verify_get_subCarrier_By_Id_api(
                                        created_subCarrier_Id)
                                    if get_carrier_status != 404:
                                        self.Failures.append(
                                            "There is a failure in get subCarrier response : Expected:404 , Recieved" + get_carrier_status)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_05_verify_get_subcarriers_by_invalid_id_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when Invalid ID is provided to fetch subcarrier details (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Get SubCarriers by Invalid Id API and Validate error code and error message:"):
            invalid_sub_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            expected_err_msg = str(resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg'))

            res, status_code = resource['subCarrier'].verify_get_subCarrier_By_Id_api(carrier_ID=invalid_sub_id)
            err_Description = res["errors"][0]['errorDescription']

            if status_code != 404 and err_Description != expected_err_msg:
                self.Failures.append(
                    "There is a failure in get subCarrier response : Expected status code for invalid Id:404 , Recieved" + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_06_verify_get_subcarriers_by_token_api(self, rp_logger, resource):
        """
        This test fetches the details of subcarriers based on the provided token (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        token = str(resource['data_reader'].get_data(self.configparameter, test_name, 'token_id'))
        with allure.step("Call Get SubCarriers by token API and Validate the response"):
            res, status_code = resource['subCarrier'].verify_get_subCarrier_By_Token_api(subcarrier_token=token)

            if status_code != 200:
                self.Failures.append(
                    "There is a failure in error message : Expected status code is 200:, Recieved : " + str(
                        status_code))
            else:
                subId = res["subCarrierID"]
                if subId != token:
                    self.Failures.append(
                        "Fetched subcarrier Id is different from the expected Id: Expected: " + token + " received token : " + subId)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_07_verify_get_subcarriers_by_invalid_token_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when Invalid token is provided to fetch subcarrier details (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        invalid_token = str(resource['data_reader'].get_data(self.configparameter, test_name, 'token_id'))
        expected_err_msg = str(resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg'))

        with allure.step("Call Get SubCarriers by token API, pass an invalid token and Validate the response"):
            res, status_code = resource['subCarrier'].verify_get_subCarrier_By_Token_api(subcarrier_token=invalid_token)
            err_Description = res["errors"][0]['errorDescription']
            if status_code != 404 and err_Description != expected_err_msg:
                self.Failures.append(
                    "There is a failure in error code and : Expected status code is 404:, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_08_verify_get_carrier_parameters_api(self, rp_logger, resource):
        """
        This test fetches the details of carrier parameters based on provided partnerId and country code (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'partnerId'))
        country_code = str(resource['data_reader'].get_data(self.configparameter, test_name, 'CountryCode'))
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Get Carrier Parameters API and Validate response"):
            status_code = resource['subCarrier'].verify_get_Carrier_Parameters_api(partner_id=gcs_partner_id,
                                                                                   country_code=country_code)
            if status_code != 200:
                self.Failures.append(
                    "Get carrier parameters API didn't respond correctly. Expected status code: 200, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_09_verify_get_carrier_parameters_invalid_country_code_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when get Carrier parameters is fetched with invalid country code (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'partnerId'))
        country_code = str(resource['data_reader'].get_data(self.configparameter, test_name, 'CountryCode'))
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Get Carrier Parameters API by passing invalid country code and Validate response"):
            status_code = resource['subCarrier'].verify_get_Carrier_Parameters_api(partner_id=gcs_partner_id,
                                                                                   country_code=country_code)
            if status_code != 400:
                self.Failures.append(
                    "Get carrier parameters by invalid country code API didn't respond correctly. Expected status code: 400, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_10_verify_get_carrier_parameters_longer_cc_api(self, rp_logger, resource):
        """
        This test validates that error is obtained when get Carrier parameters is fetched with invalid(longer) country code (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'partnerId'))
        country_code = str(resource['data_reader'].get_data(self.configparameter, test_name, 'CountryCode'))
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Get Carrier Parameters API by passing invalid country code and Validate response"):
            status_code = resource['subCarrier'].verify_get_Carrier_Parameters_api(partner_id=gcs_partner_id,
                                                                                   country_code=country_code)
            if status_code != 400:
                self.Failures.append(
                    "Get carrier parameters by invalid/longer country code API didn't respond correctly. Expected status code: 400, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_11_verify_get_license_agreements_api(self, rp_logger, resource):
        """
        This test fetches the details of license agreement of subcarriers (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'partnerId'))
        country_code = str(resource['data_reader'].get_data(self.configparameter, test_name, 'CountryCode'))
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Get License agreement and Validate response"):
            res, status_code = resource['subCarrier'].verify_get_License_Agreements_api(partner_id=gcs_partner_id,
                                                                                        country_code=country_code)
            if status_code != 200:
                self.Failures.append(
                    "Get license agreements didn't respond correctly. Expected status code: 200, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_12_verify_subscription_subcarriers_by_type_api(self, rp_logger, resource):
        """
        This test fetches the subcarriers details based on the provided type (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        query_param_sending = 'filter=subCarrierType:sending'
        query_param_recieving = 'filter=subCarrierType:recieving'
        subscription_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
        with allure.step("Call Get SubCarriers by token API and Validate"):
            status_code = resource['subCarrier'].verify_get_subscription_subcarriers_byType_api(subscription_id,
                                                                                                query_param_sending)
            if status_code != 200:
                self.Failures.append(
                    "Get subcarrier API(sending) didn't respond correctly . Expected status code: 200, Recieved : " + str(
                        status_code))

        with allure.step("Call Get SubCarriers by token API and Validate"):
            status_code = resource['subCarrier'].verify_get_subscription_subcarriers_byType_api(subscription_id,
                                                                                                query_param_recieving)
            if status_code != 200:
                self.Failures.append(
                    "Get subcarrier API(recieving) didn't respond correctly . Expected status code: 200, Recieved : " + str(
                        status_code))
        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_13_verify_get_subcarriers_by_location_api(self, rp_logger, resource):
        """
        This test fetches the subarriers as per the provided location (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        loc_Id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'location_id'))
        with allure.step("Call Get SubCarriers by token API and Validate"):
            status_code = resource['subCarrier'].verify_get_subcarriers_by_Location_api(loc_Id)
            if status_code != 200:
                self.Failures.append(
                    "Get carrier by location didn't respond correctly . Expected status code: 200, Recieved : " + str(
                        status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_14_verify_get_carriers_by_partner_id_api(self, rp_logger, resource):
        """
        This test fetches the subarriers as per the provided partner Id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'partnerId'))
        total_count = 0

        with allure.step("Call Get SubCarriers by UPS partner Id and Validate"):
            res, status_code = resource['subCarrier'].verify_get_carriers_by_partnerId_api(partner_id)
            if status_code != 200:
                self.Failures.append(
                    "Get carrier by partner id didn't respond correctly . Expected status code: 200, Recieved : " + str(
                        status_code))

            else:
                total_count = res['pageInfo']['totalCount']
                if total_count == 0:
                    self.Failures.append(
                        "No carriers are available for this partner ID. Total carriers available are : " + str(
                            total_count))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_15_verify_get_carriers_by_location_id_api(self, rp_logger, resource):
        """
        This test fetches the details of carriers based on the provided location ID (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")

        subscription_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
        location_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'location_id'))

        with allure.step("Call Get SubCarriers by Location ID API and Validate"):
            res, status_code = resource['subCarrier'].verify_get_carriers_by_locationId_api(subscription_id,
                                                                                            location_id)
            total_count = res['pageInfo']['totalCount']

            if status_code != 200:
                self.Failures.append(
                    "Get carrier by location ID didn't respond correctly . Expected status code: 200, Recieved : " + str(
                        status_code))

            else:
                if total_count == 0:
                    self.Failures.append(
                        "No carriers are available for this location ID. Total carriers available are : " + str(
                            total_count))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_16_verify_duplicate_subcarrier_fedex_creation(self, rp_logger, resource):
        """
        This test validates that duplicate subcarrier should not be created (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'FedEx'
            desc = 'Auto_FedEx_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api Create Fedex subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))
                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Add FedEx subcarrier again and Validate that error is obtained"):
                        res, dup_status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                                   carrierID=carrier_id_input,
                                                                                                   accountNumber=account_number,
                                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                                   desc=desc)

                        if dup_status_code != 400:
                            self.Failures.append(
                                "Duplicate subcarrier should not be created. Expected status code: 400 , Recieved" + str(
                                    dup_status_code))

                        else:
                            duplicate_creation_error_message = res['errors'][0]['errorDescription']
                            expected_error_message = str(
                                resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg'))

                            if duplicate_creation_error_message != expected_error_message:
                                self.Failures.append(
                                    "Correct error message should be obtained when duplicate subcarrier is created. Expected error message: " + expected_error_message + ", Recieved" + str(
                                        duplicate_creation_error_message))

                    with allure.step("Delete the created subcarrier and validate the status code: "):
                        status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                        if status != 200:
                            self.Failures.append(
                                "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                    status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_17_verify_duplicate_subcarrier_ups_creation(self, rp_logger, resource):
        """
        This test validates that duplicate subcarrier should not be created (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'UPS'
            desc = 'Auto_FedEx_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api Create UPS subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Re create UPS subcarrier and Validate that error is obtained"):
                        res, dup_status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                                   carrierID=carrier_id_input,
                                                                                                   accountNumber=account_number,
                                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                                   desc=desc)
                        if dup_status_code != 400:
                            self.Failures.append(
                                "Duplicate subcarrier should not be created. Expected status code: 400 , Recieved" + str(
                                    dup_status_code))

                        else:
                            duplicate_creation_error_message = res['errors'][0]['errorDescription']
                            expected_error_message = str(
                                resource['data_reader'].get_data(self.configparameter, test_name, 'ErrorMsg'))

                            if duplicate_creation_error_message != expected_error_message:
                                self.Failures.append(
                                    "Correct error message should be obtained when duplicate subcarrier is created. Expected error message: " + expected_error_message + ", Recieved" + str(
                                        duplicate_creation_error_message))

                            with allure.step("Delete the created subcarrier and validate the status code: "):
                                status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                                if status != 200:
                                    self.Failures.append(
                                        "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                            status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_18_verify_update_subcarrier_fedex(self, rp_logger, resource):
        """
        This test validates that subcarrier can be updated (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'FedEx'
            desc = 'Auto_FedEx_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api Create Fedex subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Update created FedEx subcarrier and Validate the response"):
                        desc_to_be_updated = 'Fedex Test-Updated-Desc'

                        status_code = resource['subCarrier'].verify_update_subCarrier_api(sub_id=sub_id_input,
                                                                                          subCarrierID=created_subCarrier_Id,
                                                                                          description=desc_to_be_updated,
                                                                                          carrier_id=carrier_id_input,
                                                                                          account_num=account_number,
                                                                                          gcs_partner_id=gcs_partner_id)
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in updating FedEx subcarrier: Expected status code: 200 , Recieved: " + str(
                                    status_code))
                        else:
                            with allure.step("Call Get SubCarriers by Id API and Validate the updated description"):
                                res_get_API, status_code_get_API = resource[
                                    'subCarrier'].verify_get_subCarrier_By_Id_api(
                                    created_subCarrier_Id)
                                updated_desc = res_get_API['description']

                                if status_code_get_API != 200:
                                    self.Failures.append(
                                        "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                            status_code))
                                else:
                                    if updated_desc != desc_to_be_updated:
                                        self.Failures.append(
                                            "Subcarrer is not updated correctly : Expected: " + desc_to_be_updated + ", Recieved : " + updated_desc)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_19_verify_update_subcarrier_ups(self, rp_logger, resource):
        """
        This test validates that subcarrier can be updated (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'UPS'
            desc = 'Auto_UPS_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

        with allure.step("Validate if Subcarrier is created successfully"):
            if status_code != 201:
                self.Failures.append(
                    "There is a failure in api Create UPS subCarrier response : Expected:201 , Recieved  " + str(
                        status_code))
            else:
                created_subCarrier_Id = res['subCarrierID']

                with allure.step("Update created UPS subcarrier and Validate the response"):
                    desc_to_be_updated = 'UPS Test-Updated-Desc'
                    status_code = resource['subCarrier'].verify_update_subCarrier_api(sub_id=sub_id_input,
                                                                                      subCarrierID=created_subCarrier_Id,
                                                                                      description=desc_to_be_updated,
                                                                                      carrier_id=carrier_id_input,
                                                                                      account_num=account_number,
                                                                                      gcs_partner_id=gcs_partner_id)
                    if status_code != 200:
                        self.Failures.append(
                            "There is a failure in updating UPS subcarrier: Expected status code: 200 , Recieved" + str(
                                status_code))

                with allure.step("Call Get SubCarriers by Id API and Validate the updated description"):
                    res_get_API, status_code_get_API = resource['subCarrier'].verify_get_subCarrier_By_Id_api(
                        created_subCarrier_Id)
                    updated_desc = res_get_API['description']

                    if status_code_get_API != 200:
                        self.Failures.append(
                            "There is a failure in get subCarrier response : Expected:200 , Recieved: " + str(
                                status_code))
                    else:
                        if updated_desc != desc_to_be_updated:
                            self.Failures.append(
                                "Subcarrer is not updated correctly : Expected: " + desc_to_be_updated + ", Recieved : " + updated_desc)

                with allure.step("Delete the created subcarrier and validate the status code: "):
                    status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                    if status != 200:
                        self.Failures.append(
                            "There is a failure in archive subCarrier response : Expected:200 , Recieved: " + str(
                                status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_20_verify_subcarrier_creation_with_invalid_id(self, rp_logger, resource):
        """
        This test validates that subcarrier should not be created with invalid Id (negative scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'FedEx'
            desc = 'Auto_FedEx_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)
            with allure.step("Validate that error is obtained"):
                if status_code != 400:
                    self.Failures.append(
                        "There is a failure in api Create Fedex subCarrier response : Expected:400 , Recieved  " + str(
                            status_code))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_21_verify_import_subCarrier_ups_api(self, rp_logger, resource):
        """
        This test validates that UPS subcarrier can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call import subcarrier API and Validate"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            carrier_id = 'UPS'

            res, status_code = resource['subCarrier'].verify_import_subCarrier_api(sub_id_input, carrier_id)

            with allure.step("Validate that creation is successful through import"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api import UPS subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    with allure.step("Validate that creation message is correct"):
                        if res['uploadedRecords'] == 0:
                            self.Failures.append('Carrier is not imported successfully. Uploaded Records should be >=1')

                    carrier_id_input = str(
                        resource['data_reader'].get_data(self.configparameter, test_name, 'carrier_id'))

                    with allure.step("Call Get SubCarriers API and Validate fetched subscription Id"):
                        res, status_code = resource['subCarrier'].verify_get_subCarriers_api(sub_id_input,
                                                                                             carrier_id_input)

                    with allure.step("Validate that satus code of get subcarrier API is correct"):
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                        else:
                            subcarrierId = res["subCarriers"][0]["subCarrierID"]
                            with allure.step("Delete the created subcarrier and validate the status code: "):
                                status = resource['subCarrier'].verify_archive_subCarrier_api(subcarrierId)
                                if status != 200:
                                    self.Failures.append(
                                        "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                            status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_22_verify_import_subCarrier_fedEx_api(self, rp_logger, resource):
        """
        This test validates that FedEx subcarrier can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call import subcarrier API and Validate"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            carrier_id = 'FedEx'

            res, status_code = resource['subCarrier'].verify_import_subCarrier_api(sub_id_input, carrier_id)
            with allure.step("Validate that creation is successful through import"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api import UPS subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    with allure.step("Validate that creation message is correct"):
                        if res['uploadedRecords'] == 0:
                            self.Failures.append('Carrier is not imported successfully. Uploaded Records should be >=1')

                    carrier_id_input = str(
                        resource['data_reader'].get_data(self.configparameter, test_name, 'carrier_id'))

                    with allure.step("Call Get SubCarriers API and Validate fetched subscription Id"):
                        res, status_code = resource['subCarrier'].verify_get_subCarriers_api(sub_id_input,
                                                                                             carrier_id_input)
                        subcarrierId = res["subCarriers"][0]["subCarrierID"]
                    with allure.step("Validate that satus code of get subcarrier API is correct"):
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                    with allure.step("Delete the created subcarrier and validate the status code: "):
                        status = resource['subCarrier'].verify_archive_subCarrier_api(subcarrierId)
                        if status != 200:
                            self.Failures.append(
                                "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                    status))

            exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_23_verify_subcarrier_usps_creation(self, rp_logger, resource):
        """
         This test validates USPS subcarrier creation  is success or not (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'USPS'
            desc = 'Auto_USPS_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in Create subCarrier API response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Call Get SubCarriers by Id API and Validate the response"):
                        res_get_API, status_code_get_API = resource['subCarrier'].verify_get_subCarrier_By_Id_api(
                            created_subCarrier_Id)

                        if status_code_get_API != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                        else:
                            subCarrierId_get_res = res_get_API['subCarrierID']
                            if subCarrierId_get_res != created_subCarrier_Id:
                                self.Failures.append(
                                    "Fetched subCarrier is different from created one : Expected: " + created_subCarrier_Id + ", Recieved : " + subCarrierId_get_res)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

                            else:
                                with allure.step("Fetch the deleted carrier and validate error message: "):
                                    get_res, get_carrier_status = resource[
                                        'subCarrier'].verify_get_subCarrier_By_Id_api(
                                        created_subCarrier_Id)
                                    if get_carrier_status != 404:
                                        self.Failures.append(
                                            "There is a failure in get subCarrier response : Expected:404 , Recieved" + get_carrier_status)

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_24_verify_update_subcarrier_usps(self, rp_logger, resource):
        """
        This test validates that subcarrier can be updated (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call Subscription Creation API and Validate"):
            carrier_id_input = 'USPS'
            desc = 'Auto_usps_SubCarrier'
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            account_number = str(resource['data_reader'].get_data(self.configparameter, test_name, 'account_num'))
            gcs_partner_id = str(resource['data_reader'].get_data(self.configparameter, test_name, 'gcs_partner_id'))

            res, status_code = resource['subCarrier'].verify_create_subCarrier_api(subID=sub_id_input,
                                                                                   carrierID=carrier_id_input,
                                                                                   accountNumber=account_number,
                                                                                   gcsPartnerID=gcs_partner_id,
                                                                                   desc=desc)

            with allure.step("Validate if Subcarrier is created successfully"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api Create USPS subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    created_subCarrier_Id = res['subCarrierID']

                    with allure.step("Update created USPS subcarrier and Validate the response"):
                        desc_to_be_updated = 'USPS Test-Updated-Desc'

                        status_code = resource['subCarrier'].verify_update_subCarrier_api(sub_id=sub_id_input,
                                                                                          subCarrierID=created_subCarrier_Id,
                                                                                          description=desc_to_be_updated,
                                                                                          carrier_id=carrier_id_input,
                                                                                          account_num=account_number,
                                                                                          gcs_partner_id=gcs_partner_id)
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in updating USPS subcarrier: Expected status code: 200 , Recieved: " + str(
                                    status_code))
                        else:
                            with allure.step("Call Get SubCarriers by Id API and Validate the updated description"):
                                res_get_API, status_code_get_API = resource[
                                    'subCarrier'].verify_get_subCarrier_By_Id_api(
                                    created_subCarrier_Id)
                                updated_desc = res_get_API['description']

                                if status_code_get_API != 200:
                                    self.Failures.append(
                                        "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                            status_code))
                                else:
                                    if updated_desc != desc_to_be_updated:
                                        self.Failures.append(
                                            "Subcarrer is not updated correctly : Expected: " + desc_to_be_updated + ", Recieved : " + updated_desc)

                        with allure.step("Delete the created subcarrier and validate the status code: "):
                            status = resource['subCarrier'].verify_archive_subCarrier_api(created_subCarrier_Id)
                            if status != 200:
                                self.Failures.append(
                                    "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                        status))

        exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)

    @allure.testcase("Carrier Account Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.subscription_carrier_acct_mgmt
    def test_25_verify_import_subCarrier_usps_api(self, rp_logger, resource):
        """
        This test validates that FedEx subcarrier can be created through Import (Positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " +
                       test_name + " ######")
        with allure.step("Call import subcarrier API and Validate"):
            sub_id_input = str(resource['data_reader'].get_data(self.configparameter, test_name, 'subscription_id'))
            carrier_id = 'USPS'

            res, status_code = resource['subCarrier'].verify_import_subCarrier_api(sub_id_input, carrier_id)
            with allure.step("Validate that creation is successful through import"):
                if status_code != 201:
                    self.Failures.append(
                        "There is a failure in api import UPS subCarrier response : Expected:201 , Recieved  " + str(
                            status_code))

                else:
                    with allure.step("Validate that creation message is correct"):
                        if res['uploadedRecords'] == 0:
                            self.Failures.append('Carrier is not imported successfully. Uploaded Records should be >=1')

                    carrier_id_input = str(
                        resource['data_reader'].get_data(self.configparameter, test_name, 'carrier_id'))

                    with allure.step("Call Get SubCarriers API and Validate fetched subscription Id"):
                        res, status_code = resource['subCarrier'].verify_get_subCarriers_api(sub_id_input,
                                                                                             carrier_id_input)
                        subcarrierId = res["subCarriers"][0]["subCarrierID"]
                    with allure.step("Validate that satus code of get subcarrier API is correct"):
                        if status_code != 200:
                            self.Failures.append(
                                "There is a failure in get subCarrier response : Expected:200 , Recieved" + str(
                                    status_code))

                    with allure.step("Delete the created subcarrier and validate the status code: "):
                        status = resource['subCarrier'].verify_archive_subCarrier_api(subcarrierId)
                        if status != 200:
                            self.Failures.append(
                                "There is a failure in archive subCarrier response : Expected:200 , Recieved" + str(
                                    status))

            exe_status.mark_final(test_step=",".join(self.Failures), result=len(self.Failures) == 0)
