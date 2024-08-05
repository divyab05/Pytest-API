from FrameworkUtilities import request_utils


class generate_kiosk_token:

    def __init__(self, app_config):
        self.url = app_config.env_cfg['oauth_2.0']
        self.body = app_config.env_cfg['json_body']
        self.ILP_clientID = app_config.env_cfg['ILP_clientID']
        self.ILP_secret = app_config.env_cfg['ILP_secret']
        self.INT_clientID = app_config.env_cfg['INT_clientID']
        self.INT_secret = app_config.env_cfg['INT_secret']

        self.kioskRequest = {"url": self.url,
                             "body": self.body,
                             "clientID": self.ILP_clientID,
                             "clientSecret": self.ILP_secret}

        self.IntegratorRequest = {"url": self.url,
                                  "body": self.body,
                                  "clientID": self.INT_clientID,
                                  "clientSecret": self.INT_secret}

        self.response = request_utils.device_token_generation(self.kioskRequest)
        if self.response['response_code'] == 200:
            self.json_data = self.response['response_body']
            self.kiosk_token = "Bearer " + self.json_data['access_token']

        self.response = request_utils.device_token_generation(self.IntegratorRequest)
        if self.response['response_code'] == 200:
            self.json_data = self.response['response_body']
            self.integrator_token = "Bearer " + self.json_data['access_token']
