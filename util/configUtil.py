import os
import configparser


class DatabaseConfig(object):
    url = '172.17.1.111'
    port = 27017
    user = 'mongouser'
    password = 'mongopwd'