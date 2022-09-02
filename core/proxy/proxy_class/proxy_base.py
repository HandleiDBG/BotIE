import requests
from core.consts import consts
import random


class ProxyBase:
    def __init__(self):
        self._list = []

    def get_list(self):
        self._mount_list()
        return self._list

    def _get(self, url):
        headers = {'user-agent': consts.userAgents[random.randint(0, len(consts.userAgents) - 1)]}
        r = requests.get(url, headers=headers)
        return r.text

    def _mount_list(self):
        pass
