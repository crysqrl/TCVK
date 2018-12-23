"""
This is core module of chronovk.
"""
import random

import vk_api
from chronovk.exceptions import EmptyMessageException, WrongIdException
from chronovk.validators import id_validator
from chronovk.config_loader import ConfigLoader


class Vk():
    """Class that represents chronovk"""

    def __init__(self, login=None, password=None):
        # TOO DIFFICULT LOGIC
        # TODO: replace
        self.config = ConfigLoader()
        if login is None or password is None:
            login, password = self.config.get_credentials()

        if login is None:
            login = self.config.set_login()

        if password is None:
            password = self.config.set_password()

        self.vk_session = vk_api.VkApi(
            login=login,
            password=password,
            auth_handler=self._auth_handler,
            captcha_handler=self._captcha_handler
        )
        try:
            self.vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

    @property
    def api(self):
        """Property used for api methods calls"""

        return self.vk_session.get_api()

    def get_conversations(self, filter="all", fields=None, count=1):
        """Method that gets users conversations"""

        conversations = self.api.messages.getConversations(
            filter=filter, fields=fields, count=count
        )

        print(conversations)
        return conversations

    def get_messages(self, peer_id=None, count=1):
        """Method that gets messages from conversation"""

        if peer_id is None:
            raise WrongIdException

        id_validator(peer_id)

        messages = self.api.messages.getHistory(
            peer_id=peer_id,
            count=count
        )

        print(messages)
        return messages

    def send_message(self, peer_id=None, message=None):
        """Method to send messages"""

        if peer_id is None:
            raise WrongIdException

        id_validator(peer_id)
        if message is None:
            raise EmptyMessageException("Empty message")
        # random_id is a required parameter to avoid resending the message
        random_id = random.randint(10000, 16000)
        message_id = self.api.messages.send(
            peer_id=peer_id, random_id=random_id, message=message)

        print(message_id)
        return message_id

    @staticmethod
    def _captcha_handler(captcha):
        """Method to proccess captcha"""

        key = input("Enter captcha code {0}: ".format(
            captcha.get_url())).strip()
        return captcha.try_again(key)

    @staticmethod
    def _auth_handler():
        """Method to process 2FA"""

        key = input("Enter authentication code: ")
        remember = input("Remember me? y/n")
        if remember == "y":
            remember_device = True
        else:
            remember_device = False

        return key, remember_device
