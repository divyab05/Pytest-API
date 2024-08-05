""" This module is used for developing/ accessing data reader utility. """

import os
import logging
import numpy
import pyexcel as exc
from FrameworkUtilities.config_utility import ConfigUtility
import FrameworkUtilities.logger_utility as log_utils
import pandas as pd


class DataReader:
    """
    This class includes basic reusable data helpers.
    """
    log = log_utils.custom_logger(logging.INFO)

    # config = ConfigUtility()

    def __init__(self, app_config):
        self.app_config = app_config
        self.config = ConfigUtility(app_config)
        # self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.cur_path = os.getcwd()

    def load_test_data(self, testfile):
        """
        This methods is used for loading excel file data for UI cases
        :return: it returns excel records
        """
        records = None

        # noinspection PyBroadException
        prop = self.config.load_properties_file()
        base_test_data = prop.get(testfile, 'base_test_data')
        if self.app_config.env_cfg['env'] == "DEV":
            ui_file_path = os.path.join(
                self.cur_path,
                r"TestData/" + self.app_config.env_cfg['Project'] + "/{arg1}".format(arg1=self.app_config.env_cfg['product_name'])+"/DEV/{}.xlsx".format(base_test_data))
        elif self.app_config.env_cfg['env'] == "QA":
            ui_file_path = os.path.join(
                self.cur_path,
                r"TestData/" + self.app_config.env_cfg['Project'] + "/{arg1}".format(arg1=self.app_config.env_cfg['product_name'])+ "/QA/{}.xlsx".format(base_test_data))
        elif self.app_config.env_cfg['env'] == "PPD":
            ui_file_path = os.path.join(
                self.cur_path,
                r"TestData/" + self.app_config.env_cfg['Project'] + "/{arg1}".format(arg1=self.app_config.env_cfg['product_name'])+ "/PPD/{}.xlsx".format(base_test_data))

        try:
            if ui_file_path is not None:
                records = exc.iget_records(file_name=ui_file_path)
        except Exception as ex:
            self.log.error(
                "Failed to load test data.\n{}".format(ex))

        return records

    def get_data(self, test_file, tc_name, column_name):
        """
        This method is used for returning column data specific to ui test case name
        :param tc_name: it takes test case name as input parameter
        :param column_name: it takes the name of the column for which value has to be returned
        :return:
        """
        value = None
        excel_records = self.load_test_data(test_file)

        # noinspection PyBroadException

        try:
            if excel_records is not None:
                for record in excel_records:
                    record_dict = dict(record)
                    if record_dict['TC_Name'] == tc_name:
                        value = record_dict[column_name]
                        break
                    else:
                        continue

        except Exception as ex:
            self.log.error(
                "Failed to get test data.\n{}".format(ex))

        return value

    def pd_load_test_data(self, testfile):
        """
        This method uses pandas library to load the given excel file and read the records.
        :return: it returns excel records
        """
        records = None

        prop = self.config.load_properties_file()
        base_test_data = prop.get(testfile, 'base_test_data')
        env = self.app_config.env_cfg['env']
        product_name = self.app_config.env_cfg['product_name']
        project = self.app_config.env_cfg['Project']

        ui_file_path = os.path.join(
            self.cur_path,
            r"TestData/{}/{}/{}/{}.xlsx".format(project, product_name, env, base_test_data)
        )

        try:
            records = pd.read_excel(ui_file_path)
        except Exception as ex:
            self.log.error("Failed to load test data.\n{}".format(ex))

        return records

    def pd_get_data(self, test_file, tc_name, column_name):
        """
        This method uses pandas library to fetch records from excel and return the column value
        associated with the given test case name.
        :param test_file: excel test data file
        :param tc_name: it takes test case name as input parameter
        :param column_name: it takes the name of the column for which value has to be returned
        :return: it returns the column_name value
        """

        excel_records = self.pd_load_test_data(test_file)

        try:
            if excel_records is None:
                raise ValueError("No data to process.")

            if 'TC_Name' not in excel_records:
                raise KeyError("Key 'TC_Name' not found in data.")

            tc_names = excel_records['TC_Name']
            if tc_name not in tc_names.values:
                raise ValueError("Value '{}' not found in 'TC_Name' column.".format(tc_name))

            index = tc_names[tc_names == tc_name].index[0]
            if column_name not in excel_records:
                raise KeyError("Key '{}' not found in data.".format(column_name))

            value = excel_records[column_name][index]

            if isinstance(value, numpy.float64):
                value = int(value)
                value = str(value)
            elif isinstance(value, numpy.int64):
                value = str(value)


        except (ValueError, KeyError) as ex:
            self.log.error("Failed to get test data.\n{}".format(ex))
            return None

        return value

    def pd_get_row_data(self, test_file, tc_name):
        """
        This method uses pandas library to fetch records from excel and return entire row
        associated with the given test case name.
        :param test_file: excel test data file
        :param tc_name: it takes test case name as input parameter
        :return: it returns the entire row data
        """

        excel_records = self.pd_load_test_data(test_file)
        df = pd.DataFrame(excel_records)
        try:
            if excel_records is None:
                raise ValueError("No data to process.")

            if 'TC_Name' not in excel_records:
                raise KeyError("Key 'TC_Name' not found in data.")

            tc_names = excel_records['TC_Name']
            if tc_name not in tc_names.values:
                raise ValueError("Value '{}' not found in 'TC_Name' column.".format(tc_name))

            index = df[df['TC_Name'] == tc_name].index[0]
            row = df.iloc[index]
            row_dict = row.to_dict()

            for key, value in row_dict.items():
                if isinstance(value, float) and not pd.isna(value):
                    row_dict[key] = int(value)
            row_data = {key: str(value) if isinstance(value, int) else value for key, value in row_dict.items()}

        except (ValueError, KeyError) as ex:
            self.log.error("Failed to get row data.\n{}".format(ex))
            return None

        return row_data

