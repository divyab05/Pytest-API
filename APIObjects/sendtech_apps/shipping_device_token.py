import contextvars
import re
import jwt
import requests
from urllib3.exceptions import InsecureRequestWarning




class generate_shipping_app_token:

    def __init__(self, app_config):
         self.oktaHost = app_config.env_cfg['cseries_okta_preview_host']
         self.id = app_config.env_cfg['cseries_id']
         self.clientID = app_config.env_cfg['cseries_client_id']
         self.scope = app_config.env_cfg['cseries_scope']
         self.responseType = app_config.env_cfg['cseries_response_type']
         self.redirectURI = app_config.env_cfg['cseries_redirect_uri']
         self.nonce = app_config.env_cfg['cseries_nonce']
         self.state = app_config.env_cfg['cseries_state']
         self.oktaLoginAuthUrl=app_config.env_cfg['cseries_okta_log_in_auth_url']
         self.responseMode = app_config.env_cfg['cseries_response_mode']
         self.prompt = app_config.env_cfg['cseries_prompt']
         self.sessionToken = app_config.env_cfg['cseries_sessionToken']
         self.app_config=app_config
         self.username=self.app_config.env_cfg['username']
         self.password=self.app_config.env_cfg['enc_pwd']








    def generate_session_token(self, data):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        resp = requests.post(self.oktaLoginAuthUrl, data,
                             headers={"Content-Type": "application/json"}, verify=False)
        json_data = resp.json()
        session_Token = json_data['sessionToken']
        return session_Token


    def cseries_authorize_user(self, session_token):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        headr = {"Authorization": "okta_client_credential"}
        updated_url = self.oktaHost
        cseries_id = self.id
        auth_url = updated_url + '/oauth2/' + str(cseries_id) + '/v1/authorize'
        params = {'client_id': self.clientID,
                  'scope': self.scope,
                  'response_type': self.responseType,
                  'redirect_uri': self.redirectURI,
                  'nonce': self.nonce,
                  'state': self.state,
                  'response_mode': self.responseMode,
                  'prompt': self.prompt,
                  'sessionToken': self.sessionToken.replace('[tok]', str(session_token))}
        response = requests.get(auth_url, headers=headr, params=params, verify=False)
        return response.content


    def generate_cseries_access_token(self,get_env, get_username, get_password,custom_logger):
        if get_username == 'default':
            username = self.username
            password = self.password
            data = '{"username":"' + username + '","password":"' + password + '"}'
            custom_logger.info("Generating cseries access token with user - {arg1}, based on environment {arg2}"
                               .format(arg1=username, arg2=get_env))
        else:
            data = '{"username":"' + get_username + '","password":"' + get_password + '"}'
            custom_logger.info("Generating cseries access token with user - {arg1}, based on environment {arg2}"
                               .format(arg1=get_username, arg2=get_env))

        session_token = self.generate_session_token(data)
        # print("session token is ",session_token)
        html_data = self.cseries_authorize_user( session_token)
        # print("html data output from token api",html_data)

        okta_token = re.findall('name="access_token" value="([a-zA-Z0-9._-]*)"', str(html_data))[0]

        print("access token",okta_token)
        # okta_token=contextvars.ContextVar(okta_token)
        return okta_token






