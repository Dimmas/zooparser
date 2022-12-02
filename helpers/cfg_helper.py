import json
from pathlib import Path

myself = Path(__file__).resolve()


class CFG_helper(object):  # Singleton pattern
    __settings__ = None
    __settings_file__ = str(myself.parents[1] / 'settings.json')

    def __new__(cls, settings_file=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CFG_helper, cls).__new__(cls)
        return cls.instance

    def __init__(self, settings_file=None):
        if not settings_file:
            settings_file = self.__settings_file__
        if not self.__settings__:
            with open(settings_file, 'r', encoding='utf-8') as f:
                self.__settings__ = json.load(f)

    def get_categories(self):
        if self.__settings__:
            if self.__settings__['categories'] == 0:
                return None
            return self.__settings__['categories']

    def get_output_directory(self):
        if self.__settings__:
            return self.__settings__['output_directory']

    def get_delay_range_s(self):
        if self.__settings__:
            return self.__settings__['delay_range_s']

    def get_max_retries(self):
        if self.__settings__:
            return self.__settings__['max_retries']

    def get_headers(self):
        if self.__settings__:
            return self.__settings__['headers']

    def get_logs(self):
        if self.__settings__:
            return self.__settings__['logs']

    def get_restart(self):
        if self.__settings__:
            return self.__settings__['restart']
