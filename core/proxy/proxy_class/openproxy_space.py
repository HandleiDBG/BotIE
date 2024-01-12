from bs4 import BeautifulSoup
from core.proxy.proxy_class.proxy_base import ProxyBase
import re

# https://openproxy.space/


class OpenProxySpace(ProxyBase):
    def __init__(self):
        super().__init__()
        self.link_name = 'openproxy.space'

    def _mount_list(self):
        protocol = ['http', 'socks4', 'socks5']
        for p in protocol:
            url = f'https://openproxy.space/list/{p}'
            r = self._get(url)

            soup = BeautifulSoup(r, "html.parser")
            data = soup.find_all('script')
            for s in data:
                s = s.text.strip()
                if 'return {layout:"main",data:[{protocols:' in s:
                    x = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}\b', s)
                    for i in list(map(lambda ss:  f'{p.upper()}://{ss}', x)):
                    # self._list.extend(list(map(lambda ss:  f'{p.upper()}://{ss}', x)))
                        self._listAppend(i)
