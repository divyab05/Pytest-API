from ConfigFiles.products_config import products_config


class Config:
    """This class is used intialize the config of different product
     and projects based on below parameter
     env:This is the environment getting from commandline
     project_name:This is the project_name getting from commandline
     product_name:This is the product_name getting from commandline
     """
    def __init__(self, env, project_name, product_name):

        if product_name == 'sp360commercial':
            self.env_cfg = products_config.sp360commercial[env][project_name]
            self.logIn_cfg = products_config.sp360commercial[env]['login_config']
        elif product_name == 'sp360global':
            self.env_cfg = products_config.sp360global[env][project_name]
            self.logIn_cfg = products_config.sp360global[env]['login_config']
        elif product_name == 'sp360canada':
            self.env_cfg = products_config.sp360canada[env][project_name]
            self.logIn_cfg = products_config.sp360canada[env]['login_config']
        elif product_name == 'fedramp':
            self.env_cfg = products_config.fedramp[env][project_name]
            self.logIn_cfg = products_config.fedramp[env]['login_config']
        elif product_name == 'sp360uk':
            self.env_cfg = products_config.sp360uk[env][project_name]
            self.logIn_cfg = products_config.sp360uk[env]['login_config']
        elif product_name == 'sp360au':
            self.env_cfg = products_config.sp360au[env][project_name]
            self.logIn_cfg = products_config.sp360au[env]['login_config']
        elif product_name == 'govcloud':
            self.env_cfg = products_config.govcloud[env][project_name]
            self.logIn_cfg = products_config.govcloud[env]['login_config']
