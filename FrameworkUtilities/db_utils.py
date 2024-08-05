import certifi
import pymongo
import logging
import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities import Crypt
from FrameworkUtilities.config_utility import ConfigUtility


class DbUtility:
    def __init__(self, app_config, db_name):
        self.app_config = app_config
        self.log = log_utils.custom_logger(logging.INFO)
        self.config = ConfigUtility(app_config)
        self.prop = self.config.load_properties_file()
        self.client = self.db_connect()
        self.db = self.client[db_name]

    def __enter__(self):
        self.log.info("Initializing MongoDB...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.info("Closing MongoDB Client!")
        self.client.close()

    def get_connection_url(self):
        username = self.app_config.env_cfg['db_username']
        password = Crypt.decode(key='DBENCRYPTIONKEY', enc=self.app_config.env_cfg['db_password'])
        connection_url = self.app_config.env_cfg['db_connection']\
            .replace('db_usr', username).replace('db_pwd', password)
        return connection_url

    def db_connect(self):
        self.log.info("Connect to MongoDB...")
        client = pymongo.MongoClient(self.get_connection_url(), tls=True, tlsCAFile=certifi.where())
        return client

    def db_disconnect(self, client=None):
        self.log.info("Disconnecting MongoDB!")
        if client:
            client.close()
        else:
            self.client.close()

    def get_one(self, table_name, conditions={}):
        single_doc = self.db[table_name].find_one(conditions)
        return single_doc

    def get_all(self, table_name, conditions={}, sort_index='_id', limit=100):
        all_doc = self.db[table_name].find(conditions).sort(sort_index, pymongo.DESCENDING).limit(limit)
        return all_doc

    def insert_one(self, table_name, value):
        self.db[table_name].insert(value)

    def update_push(self, table_name, where, what):
        self.db[table_name].update(where, {"$push": what}, upsert=False)

    def update_set(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what}, upsert=False)

    def update_multi(self, table_name, where, what):
        self.db[table_name].update_many(where, {"$set": what}, upsert=False, multi=True)

    def update_upsert(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what}, upsert=True)

    def del_one(self, table_name, conditions={}):
        result = self.db[table_name].delete_one(conditions)
        self.log.info(str(result.deleted_count) + " document deleted!")

    def del_many(self, table_name, conditions={}):
        result = self.db[table_name].delete_many(conditions)
        self.log.info(str(result.deleted_count) + " document(s) deleted!")

    def get_one_del_one(self, table_name, conditions={}):
        self.db[table_name].find_one_and_delete(conditions)

    def get_one_update_one(self, table_name, where, what, conditions={}):
        self.db[table_name].find_one_and_update(conditions, where, {"$set": what}, upsert=False)

    def group(self, table_name, key, condition, initial, reducer):
        all_doc = self.db[table_name].group(key=key, condition=condition, initial=initial, reduce=reducer)
        return all_doc
