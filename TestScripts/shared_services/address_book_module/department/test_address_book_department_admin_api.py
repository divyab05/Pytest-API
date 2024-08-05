""" This module contains all test cases."""
import inspect
import json
import logging
import random
import allure
import pytest
from hamcrest import assert_that, equal_to
from APIObjects.shared_services.addressbook_api import AddressbookAPI
from APIObjects.shared_services.client_management_api import ClientManagementAPI
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.execution_status_utility import ExecutionStatus
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.generic_utils import generate_random_string
from FrameworkUtilities.common_utils import common_utils

exe_status = ExecutionStatus()


@pytest.fixture()
def resource(app_config, generate_access_token, client_token):
    addressbook = {
        'app_config': app_config,
        'addressbook_api': AddressbookAPI(app_config, generate_access_token, client_token),
        'client_mgmt': ClientManagementAPI(app_config, generate_access_token, client_token),
        'data_reader': DataReader(app_config)}
    yield addressbook


@pytest.mark.usefixtures('initialize')
class TestAddrbookDept_Admin_API(common_utils):
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(scope='function')
    def initialize(self, resource):
        exe_status.__init__()

    @pytest.fixture(autouse=True)
    def class_level_setup(self, app_config, resource):
        """
        This method is used for one time setup of test execution process,
        which check for the test cases to run mentioned in the excel file.
        :return: it returns nothing
        """
        self.configparameter = "ADDRESSBOOK_MGMT"
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()

        self.Failures = []

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_01_verify_search_dept_in_sub_id_admin_api(self, resource):
        """
        This test validates that created departments can be fetched successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = resource['addressbook_api'].get_departments_api(sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(get_dept_resp, 200))

        departments = get_dept_resp.json()['departments']
        dept_id = departments[0]['departmentID']
        fetched_loc_id = departments[0]['locationID']
        assert_that(created_dept_id, equal_to(dept_id))
        assert_that(loc_id, equal_to(fetched_loc_id))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_02_verify_search_dept_by_location_id_admin_api(self, resource):
        """
        This test validates that departments' list can be fetched successfully as per the provided location ID(positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto Test Loc Dept {generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        search_dept_resp = resource['addressbook_api'].search_dept_with_query_api(sub_id=sub_id, query=name, is_admin=True)
        assert_that(self.validate_response_code(search_dept_resp, 200))

        departments = search_dept_resp.json()['departments']
        dept_id = departments[0]['departmentID']
        fetched_loc_id = departments[0]['locationID']
        assert_that(created_dept_id, equal_to(dept_id))
        assert_that(loc_id, equal_to(fetched_loc_id))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_03_verify_search_dept_by_invalid_location_id_admin_api(self, resource):
        """
        This test validates that error should be obtained when invalid location Id is provided (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']
        invalid_dept = f'invalid_dept_{created_dept_id}'
        invalid_loc = f'invalid_loc_{loc_id}'

        exp_dept_error_resp = (resource['addressbook_api'].build_exp_error_message_dept_loc_response(
            check_error_for='Department', searched_id=invalid_dept))
        get_invalid_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=invalid_dept, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_template(get_invalid_dept_resp, exp_dept_error_resp, 404))
        self.log.info(f'Error expected with 404 status, as searched with invalid dept {invalid_dept}')

        # exp_loc_error_resp = (resource['addressbook_api'].build_exp_error_message_dept_loc_response(
        #     check_error_for='Location', searched_id=invalid_loc))
        # get_invalid_loc_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
        #     sub_id=sub_id, dept_id=created_dept_id, loc_id=invalid_loc, is_admin=True))
        # assert_that(self.validate_response_template(get_invalid_loc_resp, exp_loc_error_resp, 404))
        # self.log.info(f'Error expected with 404 status, as searched with invalid loc {invalid_loc}')

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_04_verify_add_dept_with_loc_admin_api(self, resource):
        """
        This test validates that new departments can be created with location successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))

        del_dept_resp = (resource['addressbook_api'].delete_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(del_dept_resp, 200))

        exp_dept_error_resp = (resource['addressbook_api'].build_exp_error_message_dept_loc_response(
            check_error_for='Department', searched_id=created_dept_id))

        get_dept_after_del_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_template(get_dept_after_del_resp, exp_dept_error_resp, 404))
        self.log.info(f'Error expected with 404 status as the searched dept {created_dept_id} is deleted successfully!')

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_05_verify_add_dept_without_loc_admin_api(self, resource):
        """
        This test validates that new departments can be created without location successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))

        del_dept_resp = (resource['addressbook_api'].delete_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, is_admin=True))
        assert_that(self.validate_response_code(del_dept_resp, 200))

        exp_dept_error_resp = (resource['addressbook_api'].build_exp_error_message_dept_loc_response(
            check_error_for='Department', searched_id=created_dept_id))

        get_dept_after_del_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, is_admin=True))
        assert_that(self.validate_response_template(get_dept_after_del_resp, exp_dept_error_resp, 404))
        self.log.info(f'Error expected with 404 status as the searched dept {created_dept_id} is deleted successfully!')

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_06_verify_update_dept_admin_api(self, resource):
        """
        This test validates that departments can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        created_contacts = resource['addressbook_api'].create_n_contacts(sub_id=sub_id, no_of_contacts=2,
                                                                         del_existing_cont=True)
        contact1 = created_contacts[0]
        contact2 = created_contacts[1]

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))

        update_dept_resp = resource['addressbook_api'].update_dept_api(cont1=contact1, cont2=contact2, is_admin=True,
                                                                       sub_id=sub_id, dept_id=created_dept_id)
        assert_that(self.validate_response_code(update_dept_resp, 200))

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))
        contacts_list = []
        fetched_dept_id = get_dept_resp.json()['departmentID']
        fetched_contacts = get_dept_resp.json()['contacts']
        for contact in fetched_contacts:
            contacts_list.append(contact['contactId'])
        contacts_list.sort()
        assert_that(created_dept_id, equal_to(fetched_dept_id))
        assert_that(contact1, equal_to(contacts_list[0]))
        assert_that(contact2, equal_to(contacts_list[1]))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_07_verify_get_contact_details_admin_api(self, resource):
        """
        This test validates that contact details can be fetched from departments successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))
        fetched_dept_id = get_dept_resp.json()['departmentID']
        assert_that(created_dept_id, equal_to(fetched_dept_id))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_08_verify_search_dept_by_search_query_admin_api(self, resource):
        """
        This test validates that created departments can be fetched by search string successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto Test Loc Dept {generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        search_dept_resp = resource['addressbook_api'].search_dept_with_query_api(sub_id=sub_id, query=name,
                                                                                  is_admin=True)
        assert_that(self.validate_response_code(search_dept_resp, 200))

        departments = search_dept_resp.json()['departments']
        dept_id = departments[0]['departmentID']
        fetched_loc_id = departments[0]['locationID']
        assert_that(created_dept_id, equal_to(dept_id))
        assert_that(loc_id, equal_to(fetched_loc_id))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_09_verify_search_dept_by_non_existent_search_query_admin_api(self, resource):
        """
        This test validates that no departments should be fetched by invalid search string successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'no dept'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()

        search_dept_resp = resource['addressbook_api'].search_dept_with_query_api(sub_id=sub_id, query=name,
                                                                                  is_admin=True)
        assert_that(self.validate_response_code(search_dept_resp, 200))
        departments = search_dept_resp.json().get('departments')
        assert_that(departments, equal_to(None))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    @pytest.mark.skip(reason="patch api payload is changed!, need to determine and fix it")
    def test_10_verify_patch_update_admin_api(self, resource):
        """
        This test validates that departments can be updated successfully (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        name = f'Auto_Test_Loc_Dept_{generate_random_string()}'
        sub_id, ent_id, email, pwd = resource['addressbook_api'].get_sub_id_ent_id_user_cred_from_addressbook_file()
        loc_id = resource['client_mgmt'].get_loc_id_of_a_division_using_ent_id(ent_id=ent_id)

        created_contacts = resource['addressbook_api'].create_n_contacts(sub_id=sub_id, no_of_contacts=2,
                                                                         del_existing_cont=True)
        contact1 = created_contacts[0]
        contact2 = created_contacts[1]

        resource['addressbook_api'].delete_all_dept_by_dept_id_loc_id(sub_id=sub_id, is_admin=True)

        add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
        assert_that(self.validate_response_code(add_dept_resp, 201))
        created_dept_id = add_dept_resp.json()['departmentID']

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))

        # update_dept_resp = resource['addressbook_api'].update_dept_api(cont1=contact1, cont2=contact2, is_admin=True,
        #                                                                sub_id=sub_id, dept_id=created_dept_id)

        patch_update_dept_resp = (resource['addressbook_api']
                                  .patch_update_dept_api(operation_type='add', cont1=contact1, cont2=contact2, is_key_cont1=True,
                                                         is_admin=True, sub_id=sub_id, dept_id=created_dept_id))
        assert_that(self.validate_response_code(patch_update_dept_resp, 200))

        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
        assert_that(self.validate_response_code(get_dept_resp, 200))
        contacts_list = []
        fetched_dept_id = get_dept_resp.json()['departmentID']
        fetched_contacts = get_dept_resp.json()['contacts']
        for contact in fetched_contacts:
            contacts_list.append(contact['contactId'])
        contacts_list.sort()
        assert_that(created_dept_id, equal_to(fetched_dept_id))
        assert_that(contact1, equal_to(contacts_list[0]))
        assert_that(contact2, equal_to(contacts_list[1]))

    @pytest.mark.address_book_sp360commercial
    @pytest.mark.address_book_sp360commercial_reg
    def test_11_verify_import_contacts_in_dept_admin_api(self, resource):
        """
        This test validates that contacts can be imported in departments (positive scenario)
        :return: return test status
        """
        test_name = inspect.currentframe().f_code.co_name
        self.log.info(f'{test_name}')

        with allure.step(
                "Call Add new Departments API and validate that successful response is obtained: "):
            name = "AUTO_Test_Loc_Dept" + str(random.randint(1, 50000))
            get_row_data = resource['data_reader'].pd_get_row_data(self.configparameter, test_name)
            sub_id = str(get_row_data['subId'])
            loc_id = str(get_row_data['locationId'])
            contact1 = str(get_row_data['contact1'])
            contact2 = str(get_row_data['contact2'])

            add_dept_resp = resource['addressbook_api'].add_dept_api(name=name, loc_id=loc_id, sub_id=sub_id, is_admin=True)
            res = add_dept_resp.json()
            status_code = add_dept_resp.status_code

        with allure.step("Validate that Department with location is added successfully: "):
            if status_code != 201:
                err_desc = res['errors'][0]['errorDescription']
                self.Failures.append(
                    "There is a failure in adding new department : Expected:201 , Received : " + str(
                        status_code) + " , Obtained error message is: " + str(err_desc))

            else:
                created_dept_id = str(res['departmentID'])

                with allure.step("Fetch the created department: "):
                    get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
                        sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
                    res = get_dept_resp.json()
                    status_code = get_dept_resp.status_code
                    if status_code != 200:
                        err_desc = res['errors'][0]['errorDescription']
                        self.Failures.append(
                            "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                status_code) + " , Obtained error message is: " + str(err_desc))

                    else:
                        with allure.step("Import contacts in created department using PATCH API: "):
                            import_cont_dept_resp = resource['addressbook_api'].import_contacts_in_dept_api(sub_id=sub_id, dept_id=created_dept_id, is_admin=True)
                            res = import_cont_dept_resp.json()
                            status_code = import_cont_dept_resp.status_code
                            if status_code != 200:
                                err_desc = res['errors'][0]['errorDescription']
                                self.Failures.append(
                                    "There is a failure in importing contacts to the created depatment. Expected:200 , Received : " + str(
                                        status_code) + " , Obtained error message is: " + str(err_desc))

                            else:
                                with open(self.prop.get('ADDRESSBOOK_MGMT', 'import_dept_schema')) as schema:
                                    expected_schema = json.load(schema)

                                isValid = resource['addressbook_api'].verify_res_schema(res=res,
                                                                            expected_schema=expected_schema)

                                if len(isValid) > 0:
                                    self.Failures.append(
                                        "Response schema doesn't match with expected schema" + str(isValid))

                                else:
                                    with allure.step("Fetch the updated department: "):
                                        get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
                                            sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
                                        res = get_dept_resp.json()
                                        status_code = get_dept_resp.status_code

                                        if status_code != 200:
                                            err_desc = res['errors'][0]['errorDescription']
                                            self.Failures.append(
                                                "There is a failure in fetching the created depatment. Expected:200 , Received : " + str(
                                                    status_code) + " , Obtained error message is: " + str(err_desc))

                                        else:
                                            contacts_added = res['contacts']
                                            if len(contacts_added) == 0:
                                                self.Failures.append(
                                                    "Contacts are not imported to the department. Expected contacts > 0. ")

                with allure.step("Delete the created Department: "):
                    del_resp = resource['addressbook_api'].delete_dept_by_dept_id_loc_id_api(sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id,
                                                                      is_admin=True)
                    status_code = del_resp.status_code
                    if status_code != 200:
                        err_desc = res['errors'][0]['errorDescription']

                        self.Failures.append(
                            "There is a failure in deleting the department : Expected:200 , Received : " + str(
                                status_code) + " , Obtained error message is: " + str(err_desc))

                with allure.step("Fetch the deleted department: "):
                    get_dept_resp = (resource['addressbook_api'].get_dept_by_dept_id_loc_id_api(
                        sub_id=sub_id, dept_id=created_dept_id, loc_id=loc_id, is_admin=True))
                    res = get_dept_resp.json()
                    status_code = get_dept_resp.status_code
                    if status_code != 404:
                        self.Failures.append(
                            "Deleted department shouldn't be fetched.")
