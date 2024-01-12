import requests
from core.consts import consts
import random
import re


class ProxyBase:
    def __init__(self):
        self._list = []

    def _listAppend(self, item):
        if self.__validate_proxy(item):
            if item.lower().startswith(('http', 'https')):
                self._list.append(item)

    def get_list(self):
        self._mount_list()
        return self._list

    def _get(self, url):
        headers = {'user-agent': consts.userAgents[random.randint(0, len(consts.userAgents) - 1)]}
        r = requests.get(url, headers=headers)
        return r.text

    def _mount_list(self):
        pass

    def __validate_proxy(self, proxy_string):
        proxy_regex = re.compile(r'^(https?|socks[45]):\/\/\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$', re.IGNORECASE)
        match = proxy_regex.match(proxy_string)
        return bool(match)

