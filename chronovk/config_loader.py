"""
This module used to load credentials from config
"""
from configparser import ConfigParser
import os


class ConfigLoader():
    """Class that used for operating data with config"""

    def __init__(self):
        self.config = ConfigParser()
        if not os.path.isfile('config.ini'):
            self._create_config()

        self.config.read("config.ini")
        self.credentials = None
        try:
            self.credentials = self.config["CREDENTIALS"]
        except KeyError:
            self.credentials = self._create_config()

    def _create_config(self):
        """Creates config"""
        self.config.add_section('CREDENTIALS')
        with open('config.ini', 'w') as file:
            self.config.write(file)
        credentials = self.config["CREDENTIALS"]
        return credentials

    def _get_config_file(self):
        """Gets file associated with config"""
        file = open('config.ini', 'w+')
        return file

    def set_login(self):
        """Sets login to config"""
        login = input("Input login: ")
        self.config.set('CREDENTIALS', 'login', login)
        self.config.write(self._get_config_file())
        return login

    def set_password(self):
        """Sets password to config"""
        password = input("Input password: ")
        self.config.set('CREDENTIALS', 'password', password)
        self.config.write(self._get_config_file())
        return password

    def get_credentials(self):
        """Gets credentials from config"""
        password = self.credentials.get('password')
        login = self.credentials.get('login')
        return (login, password)
