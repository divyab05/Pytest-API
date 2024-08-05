import logging
import json
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.api_utils import APIUtilily
from FrameworkUtilities.common_utils import common_utils
from FrameworkUtilities.config_utility import ConfigUtility


class EnrichTokenAPI:
    """This class defines the method and element identifications for main page."""

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, app_config):
        self.json_data = None
        self.app_config = app_config
        self.api = APIUtilily()
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.common = common_utils()
        self.env = str(self.app_config.env_cfg['env']).lower()
        self.endpoint = str(self.app_config.env_cfg['enrich_api'])
        self.headers = {"Host": self.endpoint[8:]}

    def get_user_details_from_file(self, user_type='client'):
        with open(self.prop.get('ENRICH_API', 'sample_enrich_user_data')) as file:
            self.json_data = json.load(file)

        prod_name = self.app_config.env_cfg['product_name']

        email = self.json_data[prod_name][self.env][user_type]['email']
        password = self.json_data[prod_name][self.env][user_type]['password']
        user_id = self.json_data[prod_name][self.env][user_type]['user_id']
        return email, password, user_id

    def get_enrich_user_details_by_user_id_api(self, user_id='', scope='adm,spa,anx'):
        query_param = '?scope=' + scope
        enrich_user_details_endpoint = self.endpoint + '/api/v1/enrich/users/' + user_id \
            + '/products/SPA/token' + query_param

        client_id = str(self.app_config.env_cfg['enrich_cli_id'])
        client_secret = str(self.app_config.env_cfg['enrich_cli_secret'])
        basic_auth = self.common.get_basic_auth(client_id=client_id, client_secret=client_secret)

        self.headers = {"Authorization": basic_auth}

        response = self.api.get_api_response(enrich_user_details_endpoint, self.headers)
        return response
