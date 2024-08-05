"""
This module contains api utility functions.
"""

import logging
import requests
import math
import jsonschema
import json

from traceback import print_stack
from requests.exceptions import HTTPError
from jsonschema import Draft7Validator
import FrameworkUtilities.logger_utility as log_utils

class APIUtilily:
    """
    This class includes basic reusable api utility helpers.
    """
    def __init__(self):

        self.header_form = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'UTF-8'}
        self.header_json = {'Content-Type': 'application/json', 'charset': 'UTF-8',"Host":"submgmt-dev.fedramp.pitneycloud.com"}

    log = log_utils.custom_logger(logging.INFO)

    def get_api_response(self, endpoint, headers=""):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        response = None

        try:
            if headers == "":
                response = requests.get(endpoint)
            else:
                response = requests.get(endpoint, headers=headers)
            response.raise_for_status()


        except HTTPError as http_err:
            self.log.error(f'HTTP Error occurred.\n{http_err}')

        except Exception as ex:
            self.log.error(f'Failed to get the response, other error occurred.\n{ex}')

        return response

    def post_api_response(self, endpoint, headers, body='', files=''):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        response = None

        try:
            if (files==''):
                response = requests.post(endpoint,data=body,headers=headers)
                #response.raise_for_status()
                #if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
                #    res = response
                #else:
                #    res = None
            else:
                response= requests.post(endpoint, files=files, headers=headers)

        except HTTPError as http_err:

            self.log.error(f'HTTP Error occurred.\n{http_err}')
            #print_stack()

        except Exception as ex:
            self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
            #print_stack()

        return response

    def put_api_response(self, endpoint, headers, body=''):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        response = None

        try:
            if body=='':
                response = requests.put(endpoint, headers=headers)
                # response.raise_for_status()
                # if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
                #    res = response
                # else:
                #    res = None
            else:
                response = requests.put(endpoint, data=body, headers=headers)


        except HTTPError as http_err:

            self.log.error(f'HTTP Error occurred.\n{http_err}')
            #print_stack()

        return response

    def delete_api_response(self, endpoint, headers, body='', files=''):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        response = None

        try:
            if (files == ''):
                response = requests.delete(endpoint, data=body, headers=headers)
                # response.raise_for_status()
                # if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
                #    res = response
                # else:
                #    res = None
            else:
                response = requests.delete(endpoint, files=files, headers=headers)

        except HTTPError as http_err:

            self.log.error(f'HTTP Error occurred.\n{http_err}')
            #print_stack()

        except Exception as ex:
            self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
            #print_stack()

        return response

    def patch_api_response(self, endpoint, headers, body='', files=''):
        """
        This method is used to return the api response
        :return: This method return the api response
        """

        response = None

        try:
            if (files==''):
                response = requests.patch(endpoint,data=body,headers=headers)
                #response.raise_for_status()
                #if response.status_code == 200 or response.status_code == 201 or response.status_code == 400:
                #    res = response
                #else:
                #    res = None
            else:
                response= requests.patch(endpoint, files=files, headers=headers)

        except HTTPError as http_err:

            self.log.error(f'HTTP Error occurred.\n{http_err}')
            #print_stack()

        except Exception as ex:
            self.log.error(f'Failed to get the response, other error occurred.\n{ex}')
            #print_stack()

        return response


    def sort_list_util(self, endpoint='', sort_col='', headers=''):

        flag = True
        
        #Case 1: Verify records can be sorted in ascending order:
        param_val = "&sort=" + sort_col + ",asc"
        asc_endpoint = endpoint + param_val
        res = self.get_api_response(endpoint=asc_endpoint, headers=headers)

        if res.status_code != 200:
            self.log.error("There is an error in get API response. Expected: 200. Received " + str(
                res.status_code))
            flag = False
            return flag

        else:
            if res is not None:
                res = res.json()

            #total_count = res['pageInfo']['totalCount']
            limit = res['pageInfo']['limit']

            if limit != 0:
                #total_accounts = res['pageInfo']['limit']

                rec_list = []
                for i in range(limit):
                    rec_list.append(res['accounts'][i][sort_col])

                sorted_res_list = rec_list[:]

                sorted_res_list.sort(reverse=False)

                if (sorted_res_list != rec_list):
                    flag = False
                    self.log.error("List is not sorted correctly in ascending order")
                    return flag

        #Case 2: Verify records can be sorted in descending order:
        param_val = "?sort=" + sort_col + ",desc"
        desc_endpoint = endpoint + param_val
        res = self.get_api_response(endpoint=desc_endpoint, headers=headers)

        if res.status_code != 200:
            self.log.error("There is an error in get API response. Expected: 200. Received " + str(
                res.status_code))
            flag = False
            return flag

        else:
            if res is not None:
                res = res.json()

            #total_count = res['pageInfo']['totalCount']
            limit = res['pageInfo']['limit']

            if limit != 0:
                #total_accounts = res['pageInfo']['limit']

                rec_list = []
                for i in range(limit):
                    rec_list.append(res['accounts'][i][sort_col])

                sorted_res_list = rec_list[:]

                sorted_res_list.sort(reverse=True)

                if (sorted_res_list != rec_list):
                    flag = False
                    self.log.error("List is not sorted correctly in descending order")
                    return flag

        return flag


    def pagination_util(self, endpoint, headers=''):
        """
        This method returns the status of pagination in API
        :return: This method returns status of pagination
        """

        flag = True
        res = self.get_api_response(endpoint=endpoint, headers=headers)

        if res.status_code !=200:
            self.log.error("There is an error in get API response. Expected: 200. Received " + str(
                                res.status_code))
            flag = False
            return flag

        else:
            if res is not None:
                res = res.json()
                total_rec = int(res['pageInfo']['totalCount'])

                if total_rec == 0:
                    self.log.error(
                        "No data is available to verify pagination.")
                    flag = False

                else:

                    rec_limit = math.floor(total_rec * 0.25)  # taking limit as 25% of the total records

                    total_pages = int(total_rec/rec_limit)

                    rec_left_for_last_page = int(total_rec%total_pages)

                    if (rec_left_for_last_page) ==0:
                        total_pages = total_pages

                    else:
                        total_pages = total_pages+1

                    for i in range(total_pages - 1):

                        param_val = "&skip=" + str(i) + "&limit=" + str(
                            rec_limit)  # update the parameter value to skip one page in every iteration

                        paginated_service_url = endpoint + param_val

                        page_response = self.get_api_response(endpoint=paginated_service_url, headers=headers)

                        if page_response.status_code != 200:
                            self.log.error(
                                "There is an error in get API response. Expected: 200. Received " + str(
                                    page_response.status_code))
                            flag = False

                        else:
                            page_res = page_response.json()

                            key_val = list(page_res.keys())[1]  # fetch the key of paginated object

                            # Case2: Verify that records on all the pages are as per the provided limit
                            paginated_rec = len(page_res[key_val])

                            if str(paginated_rec) != str(rec_limit):
                                self.log.error(
                                    "Obtained records on page do not match with provided limit. Expected records: " + str(
                                        rec_limit) + " Received records " + str(paginated_rec))
                                flag = False
                                break

                    #Case 3: Verify records for last page

                    param_val = "&skip=" + str(total_pages - 1) + "&limit=" + str(
                        rec_limit)

                    paginated_service_url = endpoint + param_val

                    page_response = self.get_api_response(endpoint=paginated_service_url, headers=headers)

                    if page_response.status_code != 200:
                        self.log.error(
                            "There is an error in get API response. Expected: 200. Received " + str(
                                page_response.status_code))
                        flag = False

                    else:
                        page_res = page_response.json()

                        key_val = list(page_res.keys())[1]  # fetch the key of paginated object

                        # Case3: Verify that records on the last page are fetched correctly
                        paginated_rec = len(page_res[key_val])

                        if rec_left_for_last_page != 0:
                            if str(paginated_rec) != str(rec_left_for_last_page):
                                self.log.error(
                                    "Records on last page do not match with the expected remaining records. Expected records: " + str(
                                        rec_left_for_last_page) + " Received records " + str(paginated_rec))
                                flag = False

                    #Case4: Verify that records on max page+1 are 0

                    param_val = "&skip=" + str(total_pages) + "&limit=" + str(rec_limit)

                    paginated_service_url = endpoint + param_val

                    page_response = self.get_api_response(paginated_service_url, headers=headers)

                    if page_response.status_code != 200:
                        self.log.error(
                            "There is an error in get API response. Expected: 200. Received " + str(
                                page_response.status_code))
                        flag = False

                    else:
                        if page_response is not None:
                            page_res = page_response.json()
                            rec_count = page_res['pageInfo']['totalCount']

                            if int(rec_count) > 0:
                                self.log.error(
                                    "Total count of records after the last page should be 0")
                                flag = False
            return flag


    def schema_validation(self, response_schema, expected_schema):
        """
        This method returns the status of schema matching
        :return: This method returns status of schema validation
        """
        validator = Draft7Validator(expected_schema)
        schema_errors= list(validator.iter_errors(response_schema))
        return schema_errors