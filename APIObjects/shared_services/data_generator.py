import csv
import logging
import random
import re
from faker import Faker
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility
from FrameworkUtilities.generic_utils import generate_random_string

fake = Faker(locale='en_US')


class DataGenerator:
    """
    This class defines the methods and setters to create test data.

    Attributes:
        log (Logger): The logger instance for logging information.
    """

    account_names = set()
    account_codes = set()
    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        """
        Initializes a new instance of the DataGenerator class.

        :param app_config: The application configuration.
        """
        self.api = APIUtilily()
        self.json_data = None
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.common = common_utils()

    @staticmethod
    def user_data_setter():
        name = fake.name()
        name_data = name.split(' ', )
        first_name = name_data[0]
        last_name = name_data[1]
        email = fake.email()
        role = random.choice(['ADMIN', 'USER'])
        division = random.choice(['Default'])
        bpn = random.choice(['0010084011'])
        location = random.choice(['Default Location'])
        company = random.choice(['Pitney Bowes', 'PB', 'SPSS'])
        # Address line 1:
        address = fake.address()
        address_data = address.split('\n', )
        address_line1 = address_data[0]

        city = fake.city()
        state = fake.state_abbr()
        country = fake.current_country_code()
        postal = fake.postalcode()

        # Phone number:
        number = fake.phone_number()
        phone = str(re.sub('[^0-9]+', '', number))[0:10]

        cost_account = ''

        return [first_name, last_name, email, role, division, bpn, location, company, address_line1, city, state,
                country, postal, phone, cost_account]

    @staticmethod
    def alm_cost_account_data_setter():
        name = fake.name()
        code = str(name.replace(' ', '')).lower()
        desc = fake.text()[0:25]
        pwd_enabled = random.choice(['TRUE', 'FALSE'])
        pwd_code = ''
        if pwd_enabled == 'TRUE':
            pwd_code = 'test'
        status = 'TRUE'
        parent_name = ''
        next_parent_name = ''
        billable = random.choice(['TRUE', 'FALSE'])

        return [name, code, desc, pwd_enabled, pwd_code, status, parent_name, next_parent_name, billable]

    @staticmethod
    def remove_special_characters(input_string):
        # Remove all special characters and keep only alphanumeric characters
        return re.sub(r'[^a-zA-Z0-9]', '', input_string)

    @staticmethod
    def cost_account_data_setter():
        name = fake.name().replace(' ', '').lower()
        name = DataGenerator.remove_special_characters(name)

        code = name.strip()

        desc = fake.text(max_nb_chars=25)
        desc = DataGenerator.remove_special_characters(desc)

        pwd_enabled = random.choice([True, False])
        pwd_code = 'test' if pwd_enabled else ''

        status = True
        parent_name = ''
        next_parent_name = ''
        billable = random.choice([True, False])

        return [name, code, desc, pwd_enabled, pwd_code, status, parent_name, next_parent_name, billable]

    @staticmethod
    def auto_import_cost_account_data_setter(access_level='', access_lvl_value='', div_name=''):
        name = fake.name()
        code = str(name.replace(' ', '')).lower()
        desc = fake.text()[0:25]
        pwd_enabled = random.choice(['TRUE', 'FALSE'])
        pwd_code = 'test' if pwd_enabled else ''
        status = 'TRUE'
        parent_name = ''
        next_parent_name = ''
        billable = random.choice(['TRUE', 'FALSE'])

        if not access_level:
            access_level = random.choice(['E', 'D', 'L'])

        if access_level == 'E' or access_level == 'D':
            access_lvl_value = ''
            div_name = ''

        if access_level == 'L':
            access_lvl_value = 'Default'
            div_name = 'Default'

        return [name, code, desc, pwd_enabled, pwd_code, status, parent_name, next_parent_name, billable, access_level,
                access_lvl_value, div_name]

    @staticmethod
    def notification_data_setter():
        templateName = fake.text()[0:25]
        templateBody = fake.text()[0:100]
        templateSubject = fake.text()[0:30]

        return [templateName, templateBody, templateSubject]

    @staticmethod
    def address_book_data_setter():
        """
        Generates and returns a list of test data for an address book entry.

        :return:The list of test data for an address book entry.
        """
        name = fake.name()
        full_company = fake.company()
        company = full_company.split(",")[0].strip()
        email = fake.email()
        number = fake.phone_number()
        phone = re.sub('[^0-9]+', '', number)[:10]
        address = fake.address()
        city = fake.city()
        state = fake.state()
        postal = fake.postalcode()
        country = fake.current_country_code()
        internal_delivery = False
        personal_id = generate_random_string(char_count=10)
        dept_name = f'Dept {fake.word()}'
        accessibility = random.choice([True, False])
        notification_all = random.choice([True, False])
        primary_location = random.choice(['OFFICE', 'MAILSTOP'])
        additional_email_ids = fake.email()
        office_location = random.randint(1, 9)
        mail_stop_id = random.randint(1, 99)

        def get_address_data(address):
            address_lines = address.split('\n')
            addr1 = address_lines[0]
            addr2 = address_lines[1] if len(address_lines) > 1 else ''
            addr3 = address_lines[2] if len(address_lines) > 2 else ''
            return addr1, addr2, addr3

        addr1, addr2, addr3 = get_address_data(address)
        return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery,
                personal_id, dept_name, office_location, mail_stop_id, accessibility, notification_all,
                primary_location, additional_email_ids]

    @staticmethod
    def dynamic_template_address_book_data_setter(plan_case=None):
        """
        Generates and returns a list of test data for an address book entry required in the dynamic template.

        :param plan_case: The plan case for generating the address book data.
        :return: The list of test data for an address book entry.
        """

        name = fake.name()
        full_company = fake.company()
        company = full_company.split(",")[0].strip()
        email = fake.email()
        number = fake.phone_number()
        phone = re.sub('[^0-9]+', '', number)[:10]
        address = fake.address()
        city = fake.city()
        state = fake.state()
        postal = fake.postalcode()
        country = fake.current_country_code()
        internal_delivery = False
        personal_id = generate_random_string(char_count=10)
        dept_name = f'Dept {fake.word()}'
        accessibility = random.choice([True, False])
        notification_all = random.choice([True, False])
        primary_location = random.choice(['OFFICE', 'MAILSTOP'])
        additional_email_ids = fake.email()
        office_location = random.randint(1, 9)
        mail_stop_id = random.randint(1, 99)

        def get_address_data(address):
            address_lines = address.split('\n')
            addr1 = address_lines[0]
            addr2 = address_lines[1] if len(address_lines) > 1 else ''
            addr3 = address_lines[2] if len(address_lines) > 2 else ''
            return addr1, addr2, addr3

        def generate_office_location():
            return f'Site {fake.city()}', f'Building {fake.word()}', f'Floor {fake.random_int(min=1, max=50)}', \
                f'Office {fake.color_name()} {fake.word()}'

        def generate_mailstop():
            return f'Mailstop Site {fake.city()}', f'Mailstop Building {fake.word()}', \
                f'Mailstop Floor {fake.random_int(min=1, max=50)}', f'Mailstop Office {fake.color_name()} {fake.word()}'

        if plan_case == 'case1' or plan_case == 'case2':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery,
                    personal_id, dept_name, generate_office_location(), generate_mailstop(), accessibility,
                    notification_all, primary_location, additional_email_ids]
        elif plan_case == 'case3' or plan_case == 'case6' or plan_case == 'case7' or plan_case == 'case9':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery,
                    personal_id, dept_name, office_location, mail_stop_id, accessibility, notification_all,
                    primary_location, additional_email_ids]
        elif plan_case == 'case4':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery,
                    personal_id, dept_name, generate_office_location(), generate_mailstop(), accessibility,
                    notification_all, primary_location, additional_email_ids, random.choice([True, False])]
        elif plan_case == 'case5':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, internal_delivery,
                    personal_id, dept_name, generate_office_location(), generate_mailstop(), accessibility,
                    notification_all, primary_location, additional_email_ids]
        elif plan_case == 'case8':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, personal_id,
                    dept_name, accessibility, notification_all, additional_email_ids]
        elif plan_case == 'case10':
            addr1, addr2, addr3 = get_address_data(address)
            return [name, company, email, phone, addr1, addr2, addr3, city, state, postal, country, personal_id,
                    dept_name, accessibility, notification_all, additional_email_ids]
        else:
            raise ValueError(f'Given plan case {plan_case} is invalid!')

    def create_addressbook_import_file(self, no_of_records=2, filepath=None):
        """
        Creates an import file with the generated contacts/addressbook test data for the specified number of records.

        :param no_of_records: The number of records to generate in the import file. Defaults to 2.
        :param filepath: The path to the import file to be created.

        :return: None
        """

        if filepath:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'Company', 'Email', 'Phone', 'AddressLine1', 'AddressLine2', 'AddressLine3',
                                 'CityTown', 'StateProvince', 'PostalCode', 'CountryCode', 'InternalDelivery',
                                 'PersonnelID', 'Department Name', 'OfficeLocation', 'MailStopID', 'Accessibility',
                                 'NotificationAll', 'PrimaryLocation', 'AdditionalEmailIds'])
                for _ in range(no_of_records):
                    writer.writerow(self.address_book_data_setter())
            self.log.info(f'Generated data updated in the address book import file: {filepath}')
        else:
            raise ValueError(f'create_addressbook_import_file: csv filepath is None!')

    def create_addressbook_dynamic_template_import_file(self, no_of_records=2, filepath=None, plan_case=None,
                                                        plan_headers=None):
        """
        Creates a dynamic template import file with the generated contacts/addressbook test data
        for the specified number of records.

        :param no_of_records: The number of records to generate in the import file. Defaults to 2.
        :param filepath: The path to the import file to be created.
        :param plan_case: The plan case for generating the address book data.
        :param plan_headers: The comma-separated string of headers for the import file.

        :return: None
        """

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if not plan_headers:
                raise ValueError(f'csv_headers are not provided!')

            writer.writerow([header.strip('"') for header in plan_headers.split(",")])
            for _ in range(no_of_records):
                writer.writerow(self.dynamic_template_address_book_data_setter(plan_case=plan_case))
        self.log.info(f'Generated data updated in the address book import file: {filepath}')

    def download_export_file_into_csv(self, filepath=None, encoded_link=None):
        """
        Downloads an export file and saves its content as a CSV file.

        :param filepath: The path to save the CSV file.
        :param encoded_link: The encoded link to download the export file.

        :return: None
        """

        if encoded_link:
            decoded_file_link = self.common.decode_base_64(encoded_link)
            self.log.info('download_file_link: \n' + decoded_file_link)

            download_file_resp = self.api.get_api_response(endpoint=decoded_file_link)
            self.common.validate_response_code(download_file_resp, 200)

            file_data = download_file_resp.text
            lines = file_data.strip().split('\n')  # Split the file data into individual lines

            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for line in lines:
                    writer.writerow(line.split(','))  # Split each line by comma and write as a row
            self.log.info(f'Export contacts data is placed in: {filepath}')
