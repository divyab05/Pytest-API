from FrameworkUtilities import request_utils


class generate_hbc_token:

    def __init__(self, app_config):
        self.hbc_token_url = app_config.env_cfg['hbc_token_url']
        self.hbc_authorization_key = app_config.env_cfg['hbc_authorization_key']

    def generate_hbc_access_token(self):
        hbc_access_token = {}
        hbc_token_config = {
            'token_url': self.hbc_token_url,
            'authorization_header': self.hbc_authorization_key
        }

        response = request_utils.generate_token_for_hbc_flows(hbc_token_config)
        hbc_access_token['response_code'] = response['response_code']
        hbc_access_token['token'] = response['response_body']['access_token']
        return hbc_access_token
