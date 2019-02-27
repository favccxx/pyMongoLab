# mongodb database
from pymongo import MongoClient
from configUtil import DatabaseConfig


class Database(object):
    ''' 不使用配置文件
    def __init__(self, address, port, database, username, password):
        self.conn = MongoClient(host=address, port=port, username=username, password=password)
        self.db = self.conn[database]
    '''

    def __init__(self, database):
        print(DatabaseConfig)
        self.conn = MongoClient(host=DatabaseConfig.url, port=DatabaseConfig.port, username=DatabaseConfig.user, password=DatabaseConfig.password)
        self.db = self.conn[database]

    def get_state(self):
        return self.conn is not None and self.db is not None

    def insert_one(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def insert_many(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_many(data)
            return ret.inserted_id
        else:
            return ""

    def update_data(self, collection, condition, data):
        if self.get_state():
            return self.db[collection].update_many(condition, data, upsert=True)
        return 0

    def update(self, collection, data):
        # data format:
        # {key:[old_data,new_data]}
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        if self.get_state():
            return self.db[collection].update_many(data_filter, {"$setOnInsert": data_revised}).modified_count
        return 0

    def find(self, col, condition, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition)
            else:
                return self.db[col].find(condition, column)
        else:
            return None

    def delete(self, col, condition):
        if self.get_state():
            return self.db[col].delete_many(filter=condition).deleted_count
        return 0