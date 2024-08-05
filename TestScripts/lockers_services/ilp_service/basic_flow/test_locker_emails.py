""" This module contains all test cases for email Notification.
emailSSTO - Runs tests for old notification
emailtest - Runs tests fot new notification
"""
import base64
import random
import string
import sys
import time
import pytest

from APIObjects.lockers_services.ilp_service.locker_bank_apis import LockerBankAPI
from APIObjects.lockers_services.ilp_service.configuration_apis import ConfigurationAPI
from APIObjects.lockers_services.ilp_service.reserve_with_pin import ReserveWithPin
from APIObjects.lockers_services.ilp_service.day_locker_apis import DayLocker
from APIObjects.lockers_services.ilp_service.cancel_reservation import CancelReservation
from APIObjects.lockers_services.ilp_service.lockers_api import LockerAPI
from APIObjects.lockers_services.ilp_service.department_services import DepartmentLockerAPI
from APIObjects.lockers_services.ilp_service.integration_api import IntegrationAPI
from FrameworkUtilities.gmail_client import GmailClient
from APIObjects.shared_services.login_api import LoginAPI
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities import Crypt


@pytest.fixture()
def resource(app_config, client_token):
    emailNotification = {'app_config': app_config,
                         'gmailClient': GmailClient(app_config),
                         'reserveWithPin': ReserveWithPin(app_config, client_token),
                         'storage': DayLocker(app_config, client_token),
                         'lockerapi': LockerAPI(app_config, client_token),
                         'configuration': ConfigurationAPI(app_config, client_token),
                         'cancelreservation': CancelReservation(app_config, client_token),
                         'dept_api': DepartmentLockerAPI(app_config, client_token),
                         'event_api': LockerBankAPI(app_config, client_token),
                         'data_reader': DataReader(app_config),
                         'login_api': LoginAPI(app_config),
                         'integration': IntegrationAPI(app_config, client_token)}
    yield emailNotification


@pytest.mark.usefixtures('initialize')
class TestReserveStorage(common_utils):

    @pytest.fixture(scope='function')
    def initialize(self, request, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the Excel file.
        :return: it returns nothing
        """

        self.configparameter = "LOCKERS_Email_Notification"
        if resource['data_reader'].pd_get_data(self.configparameter, request.function.__name__, "Runmode") != "Y":
            pytest.skip("Excluded from current execution run.")

        self.Failures = []

    @pytest.mark.emailSSTO
    def test_email_configuration_ssto(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        sample_json = '{"emailProvider":"PB_SSTO"}'

        res, status_code = resource['configuration'].verify_patch_email_configuration(locker_bank, sample_json, "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_email_configuration_platform(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')

        sample_json = '{"emailProvider":"PB_PLATFORM"}'

        res, status_code = resource['configuration'].verify_patch_email_configuration(locker_bank, sample_json, "valid",
                                                                                      "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        encrypted_value = Crypt.encode(key="GMAILENCRYPTIONKEY", clear=resource['app_config'].env_cfg['imap_password'])
        rp_logger.info(encrypted_value)

    # Delivery total 5 templates - 1. Deposit Recipient 2. Deposit Department 3. Pickup 4. Removed 5. Time Out
    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_email_recipient_deposit_pickup(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EmailTestRecipient" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_email_department_deposit_pickup(self, rp_logger, context, resource):
        """
        This test validates 2 email for department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'manvi123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_email_recipient_stale_mail(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EmailTestRecipient" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_email_department_stale_mail(self, rp_logger, context, resource):
        """
        This test validates 2 email for department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'pravin123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # Return and Exchange total 3 templates - 1. Dropoff return 2. Cancel Return 3. Exchange Request
    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_return_email_recipient_to_recipient_full_flow(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                         size=locker_size,
                                                                                         reservation_type="return",
                                                                                         accessible=""
                                                                                         , refrigeration="",
                                                                                         climate_type="",
                                                                                         TrackingID=trackingID,
                                                                                         receiver=receiver,
                                                                                         depositor=depositor,
                                                                                         departmentMail=False
                                                                                         , flagRecipient=flagRecipient,
                                                                                         flagDepositor=flagDepositor,
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_return_email_recipient_to_recipient_cancel_flow(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                         size=locker_size,
                                                                                         reservation_type="return",
                                                                                         accessible=""
                                                                                         , refrigeration="",
                                                                                         climate_type="",
                                                                                         TrackingID=trackingID,
                                                                                         receiver=receiver,
                                                                                         depositor=depositor,
                                                                                         departmentMail=False
                                                                                         , flagRecipient=flagRecipient,
                                                                                         flagDepositor=flagDepositor,
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_exchange_email_recipient_to_recipient_full_flow(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                         size=locker_size,
                                                                                         reservation_type="exchange",
                                                                                         accessible=""
                                                                                         , refrigeration="",
                                                                                         climate_type="",
                                                                                         TrackingID=trackingID,
                                                                                         receiver=receiver,
                                                                                         depositor=depositor,
                                                                                         departmentMail=False
                                                                                         , flagRecipient=flagRecipient,
                                                                                         flagDepositor=flagDepositor,
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # Return using unit api for total 2 templates - 1. Dropoff return 2. Cancel Return
    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_return_unit_email_department_to_department_full_flow(self, rp_logger, resource, context):
        """
        This test validates the reservation of return flow for Department to Department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                            locker_unit=locker_unit,
                                                                                            size=locker_size,
                                                                                            reservation_type="return",
                                                                                            accessible=""
                                                                                            , refrigeration="",
                                                                                            climate_type="",
                                                                                            TrackingID=trackingID,
                                                                                            receiver=receiver,
                                                                                            depositor=depositor,
                                                                                            departmentMail=True
                                                                                            ,
                                                                                            flagRecipient=flagRecipient,
                                                                                            flagDepositor=flagDepositor,
                                                                                            token_type="valid",
                                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        departmentpickcode = "pravin123"
        departmentMail = True
        context['manufacturerLockerID_dept'] = locker_unit

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, receiver,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    @pytest.mark.emailSSTO
    def test_return_unit_email_department_to_department_cancel_flow(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        locker_unit = str(resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_unit"))
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "department"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_based_on_unit(locker_bank=locker_bank,
                                                                                            locker_unit=locker_unit,
                                                                                            size=locker_size,
                                                                                            reservation_type="return",
                                                                                            accessible=""
                                                                                            , refrigeration="",
                                                                                            climate_type="",
                                                                                            TrackingID=trackingID,
                                                                                            receiver=receiver,
                                                                                            depositor=depositor,
                                                                                            departmentMail=True
                                                                                            ,
                                                                                            flagRecipient=flagRecipient,
                                                                                            flagDepositor=flagDepositor,
                                                                                            token_type="valid",
                                                                                            resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']
        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank, "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    # Day Locker total 6 templates - 1.Reservation Request 2.Reservation Successful 3.Pickup 4.Removed 5.Opened 6.TimeOut
    @pytest.mark.emailtest
    def test_employee_daylocker(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_visitor_daylocker(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=res['visitorID'],
                                                                         personalID=res["personalID"],
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_employee_daylocker_stale_mail(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_visitor_daylocker_stale_mail(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        visitor = "visitor" + str(random.randint(1, 35000)) + "@yopmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=res['visitorID'],
                                                                         personalID=res["personalID"],
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    def test_status(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        status = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'status')
        print(status)
        print(type(status))

    # ------------- GMAIL Tests for System Level Notifications ------------------------
    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_recipient_flow(self, rp_logger, resource):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EmailTestRecipient" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        time.sleep(50)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package placed in locker":
            self.Failures.append("Did not get deposit email, subject =" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(50)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Picked-up":
            self.Failures.append("Did not get pickup email, subject =" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_department_flow(self, rp_logger, resource, context):
        """
        This test validates 2 emails for department (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EmailTestDepartment" + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'locker123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource")

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Placed in Department Locker":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Removed from Locker":
            self.Failures.append("Did not get stalemailpickup email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_dropoff_cancel(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                         size=locker_size,
                                                                                         reservation_type="return",
                                                                                         accessible=""
                                                                                         , refrigeration="",
                                                                                         climate_type="",
                                                                                         TrackingID=trackingID,
                                                                                         receiver=receiver,
                                                                                         depositor=depositor,
                                                                                         departmentMail=False
                                                                                         , flagRecipient=flagRecipient,
                                                                                         flagDepositor=flagDepositor,
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Request for package drop-off at locker":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['cancelreservation'].cancel_reservation_basedon_lockerunitID(locker_unit,
                                                                                                 locker_bank,
                                                                                                 "valid",
                                                                                                 "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Your reservation has been cancelled":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_exchange(self, rp_logger, resource):
        """
        This test validates the reservation of return flow for recipient to recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        flagRecipient = flagDepositor = "personal"
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        depositor = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'depositor')

        res, status_code = resource['reserveWithPin'].verify_reserve_with_pin_locker_api(locker_bank=locker_bank,
                                                                                         size=locker_size,
                                                                                         reservation_type="exchange",
                                                                                         accessible=""
                                                                                         , refrigeration="",
                                                                                         climate_type="",
                                                                                         TrackingID=trackingID,
                                                                                         receiver=receiver,
                                                                                         depositor=depositor,
                                                                                         departmentMail=False
                                                                                         , flagRecipient=flagRecipient,
                                                                                         flagDepositor=flagDepositor,
                                                                                         token_type="valid",
                                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Request for package exchange at locker":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_daylocker(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        receiver = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=receiver, personalID="",
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Reservation Created Successfully":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Locker opened":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Belongings Picked-up":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_email_visitor_daylocker(self, rp_logger, resource):
        """
        This test validates authenticate day locker after deposit using personal id (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")
        trackingID = test_name + str(random.randint(1, 35000))
        visitor = "lockerspitney@gmail.com"
        username = "Visitor" + (''.join(random.choices(string.ascii_letters, k=5)))

        res, status_code = resource['storage'].day_locker_pre_reservation(locker_bank=locker_bank, Name=username,
                                                                          EmailID=visitor, token_type="valid",
                                                                          resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Reservation Request Created":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['storage'].verify_reserve_day_locker(locker_bank=locker_bank, size=locker_size,
                                                                         reservation_type="storage", accessible="",
                                                                         refrigeration="", climate_type="",
                                                                         TrackingID=trackingID,
                                                                         receiver=res['visitorID'],
                                                                         personalID=res["personalID"],
                                                                         expireReservedDate=None,
                                                                         token_type="valid",
                                                                         resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(trackingID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        res, status_code = resource['event_api'].verify_post_locker_activity_event(locker_bank=locker_bank,
                                                                                   locker_unit=locker_unit,
                                                                                   token_type="valid",
                                                                                   resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(201, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", True)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Belongings removed":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------- GMAIL Tests for Enterprise Level ------------------------
    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_enterprise_custom_notification(self, rp_logger, resource, context):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EnterpriseCustomEmail" + str(random.randint(1, 35000))
        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource",
                                                                           kioskToken=None, token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource", None, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package placed in locker_ENT_CUSTOM":
            self.Failures.append("Did not get deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False, None,
                                                                          token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Picked-up_ENT_CUSTOM":
            self.Failures.append("Did not get pickup email, subject" + subject)

        # Check Department usecases
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'locker123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource", token)

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource", token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Placed in Department Locker_ENT_CUSTOM":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", True, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Removed from Locker_ENT_CUSTOM":
            self.Failures.append("Did not get stalemailpickup email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------- GMAIL Tests for Division Level ------------------------
    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_division_custom_notification(self, rp_logger, resource, context):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EnterpriseCustomEmail" + str(random.randint(1, 35000))
        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource",
                                                                           kioskToken=None, token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource", None, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package placed in locker_DIV_CUSTOM":
            self.Failures.append("Did not get deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False, None,
                                                                          token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Picked-up_DIV_CUSTOM":
            self.Failures.append("Did not get pickup email, subject" + subject)

        # Check Department usecases
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'locker123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource", token)

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource", token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Placed in Department Locker_DIV_CUSTOM":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", True, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Removed from Locker_DIV_CUSTOM":
            self.Failures.append("Did not get stalemailpickup email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ------------- GMAIL Tests for Location Level ------------------------

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_location_custom_notification(self, rp_logger, resource, context):
        """
        This test validates 2 emails for recipient (positive scenario)
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = "EnterpriseCustomEmail" + str(random.randint(1, 35000))
        user_cred = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'user_cred')
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        token = resource['login_api'].get_access_token_for_user_credentials(username=user_cred, password='Aqswde@123')

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource",
                                                                           kioskToken=None, token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource", None, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package placed in locker_LOC_CUSTOM":
            self.Failures.append("Did not get deposit email, subject" + subject)

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False, None,
                                                                          token=token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Picked-up_LOC_CUSTOM":
            self.Failures.append("Did not get pickup email, subject" + subject)

        # Check Department usecases
        departmentID = resource['data_reader'].pd_get_data(self.configparameter, test_name, "departmentID")
        departmentpickcode = 'locker123'
        departmentMail = True
        res, status_code = resource['dept_api'].verify_reserve_locker_dept_api(locker_bank, locker_size, TrkgID,
                                                                               departmentMail, departmentID, "valid",
                                                                               "validResource", token)

        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        context["manufacturerLockerID_dept"] = res['manufacturerLockerID']
        context["Res_trackID_dept"] = res['assetsReserved']['assets'][0]['primaryTrackingID']

        res, status_code = resource['dept_api'].verify_Deposit_locker_department_api(context, locker_bank, "valid",
                                                                                     "validResource", token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Placed in Department Locker_LOC_CUSTOM":
            self.Failures.append("Did not get department deposit email, subject" + subject)

        res, status_code = resource['dept_api'].verify_Pickup_locker_department_api(context, locker_bank,
                                                                                    departmentMail, departmentID,
                                                                                    departmentpickcode, "valid",
                                                                                    "validResource", True, token)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        time.sleep(10)
        subject = resource['gmailClient'].read_email_from_gmail(1, False)
        if subject != "Package Removed from Locker_LOC_CUSTOM":
            self.Failures.append("Did not get stalemailpickup email, subject" + subject)

        if len(self.Failures) > 0:  pytest.fail('\n'.join(map(str, self.Failures)))

    # ---------------- Notification Integration tests----------------------------

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_notification_uniqueID(self, rp_logger, resource, context):

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        TrkgID = test_name + str(random.randint(1, 35000))
        locker_bank = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'locker_bank')
        recipientID = resource['data_reader'].pd_get_data(self.configparameter, test_name, 'receiver')
        locker_size = resource['data_reader'].pd_get_data(self.configparameter, test_name, "locker_size")

        res, status_code = resource['lockerapi'].verify_reserve_locker_api(locker_bank=locker_bank, size=locker_size,
                                                                           accessible="", refrigeration="",
                                                                           climate_type="", TrkgID=TrkgID, EmailID="",
                                                                           recipientID=recipientID, token_type="valid",
                                                                           resource_type="validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        locker_unit = res['manufacturerLockerID']

        res, status_code = resource['lockerapi'].verify_deposit_locker_api(TrkgID, locker_unit, locker_bank,
                                                                           "valid", "validResource")
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True
        access_code = res['assetsDeposited']['accesscode']

        sample_string_bytes = TrkgID.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64TrkgID = base64_bytes.decode("ascii")

        uniqueID = '{tenant}_{mid}_{unit}_{base64}'.format(tenant=context['tenantID'], mid=locker_bank, unit=locker_unit, base64=base64TrkgID )

        res, status_code = resource['integration'].notification_uniqueID(uniqueID)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        res, status_code = resource['lockerapi'].verify_pickup_locker_api(access_code, locker_unit, locker_bank,
                                                                          "valid", "validResource", False)
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

    @pytest.mark.emailtest
    @pytest.mark.regressioncheck_lockers
    def test_compare_html_templates(self, rp_logger, resource, context):

        test_name = sys._getframe().f_code.co_name
        rp_logger.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        res, status_code = resource['integration'].get_locker_notifications(queryParam='belongings%20pi')
        assert self.validate_expected_and_actual_response_code_with_msg(200, status_code, res) is True

        html_body = res['NotificationConfigs']['notificationConfigDetail']['templateBody']
        self.log.info(html_body)