import argparse
from dotenv import dotenv_values


class EnvParser:
    def __init__(self):
        # Initialize command arguments
        p = argparse.ArgumentParser()
        # TODO: change default filepath with cmake integration
        p.add_argument('-f', default='../etc/.env', type=str, dest='config_file',
                       help='file of configuration', required=False)

        # Parse command arguments
        args = p.parse_args()

        # Read file of configuration
        config = dotenv_values(args.config_file)
        self._logging_level = config['logging_level']
        self._imap_server = config['imap_server']
        self._imap_username = config['imap_username']
        self._imap_password = config['imap_password']
        self._last_messages_count = int(config['last_messages_count'])
        self._api_token = config['api_token']
        self._proxy_url = config['proxy_url']
        self._proxy_username = config['proxy_username']
        self._proxy_password = config['proxy_password']
        self._changing_configuration = False

    @property
    def changing_configuration(self):
        return self._changing_configuration

    @changing_configuration.setter
    def changing_configuration(self, value: bool):
        self._changing_configuration = value

    @property
    def logging_level(self):
        return self._logging_level

    @logging_level.setter
    def logging_level(self, value):
        self._logging_level = value

    @property
    def imap_server(self):
        return self._imap_server

    @imap_server.setter
    def imap_server(self, value):
        self._imap_server = value

    @property
    def imap_username(self):
        return self._imap_username

    @imap_username.setter
    def imap_username(self, value):
        self._imap_username = value

    @property
    def imap_password(self):
        return self._imap_password

    @imap_password.setter
    def imap_password(self, value):
        self._imap_password = value

    @property
    def last_messages_count(self):
        return self._last_messages_count

    @last_messages_count.setter
    def last_messages_count(self, value):
        self._last_messages_count = value

    @property
    def api_token(self):
        return self._api_token

    @property
    def proxy_url(self):
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, value):
        self._proxy_url = value

    @property
    def proxy_username(self):
        return self._proxy_username

    @proxy_username.setter
    def proxy_username(self, value):
        self._proxy_username = value

    @property
    def proxy_password(self):
        return self._proxy_password

    @proxy_password.setter
    def proxy_password(self, value):
        self._proxy_password = value
