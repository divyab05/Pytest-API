import polling

from ConfigFiles.devicehub_services import device_hub_resource_path
from FrameworkUtilities import request_utils
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.generic_utils import generate_random_alphanumeric_string


class Get_HBC_Print_Job_Status:

    def __init__(self, general_config, app_config, custom_logger):
        self.general_config = general_config
        self.app_config = app_config
        self.custom_logger = custom_logger

    def send_get_print_job_status(self, token_type, token, invalid_resource_path, job_id):
        base_uri = ""
        headers = ""
        if token_type == "HBC":
            if type(invalid_resource_path) == str:
                base_uri = str(
                    self.app_config.env_cfg[
                        'hbc_shipping_api'] + device_hub_resource_path.get_Transaction_Status_By_JobID) + \
                           "/" + generate_random_alphanumeric_string()
            else:
                base_uri = str(
                    self.app_config.env_cfg['hbc_shipping_api'] +
                    device_hub_resource_path.get_Transaction_Status_By_JobID).replace("{jobid}", job_id)

            headers = {"Authorization": "{arg1}{arg2}".format(arg1="Bearer ", arg2=token)}
        elif token_type == "OKTA":
            if type(invalid_resource_path) == str:
                base_uri = str(
                    self.app_config.env_cfg[
                        'base_uri_devicehub'] + device_hub_resource_path.get_Transaction_v2_Status_By_JobID) + \
                           "/" + generate_random_alphanumeric_string()
            else:
                base_uri = str(
                    self.app_config.env_cfg['base_uri_devicehub'] +
                    device_hub_resource_path.get_Transaction_v2_Status_By_JobID).replace("{jobid}", job_id)

            headers = common_utils.set_devicehub_request_headers(self.app_config, True, token)

        if job_id == "invalid_job_id" or token == "invalid_token":
            result = request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                     invalid_resource_path)
        else:

            result = polling.poll(
                lambda: request_utils.send_request_based_on_http_method(base_uri, None, headers, None, "get",
                                                                        invalid_resource_path),
                step=3,
                timeout=30, check_success=self.check_job_completion)

        self.custom_logger.info("Response for get print job status api"
                                "is {arg1}".format(arg1=result))
        return result

    def check_job_completion(self, response):
        if response['response_body']['status'] == 'SUCCESS':
            return True
        else:
            return False
