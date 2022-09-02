from bs4 import BeautifulSoup
from core.proxy.proxy_class.proxy_base import ProxyBase
import re


# https://pt.proxyservers.pro/


class PtProxyServersPro(ProxyBase):
    def __init__(self):
        super().__init__()
        self.link_name = 'pt.proxyservers.pro'

    def __get_pages(self, response):
        soup = BeautifulSoup(response, "html.parser")
        count_pages = 0
        pages = soup.find('ul', {'class': 'pagination justify-content-end'})
        pages = pages.find_all('a', {'class': 'page-link'})
        for p in pages:
            p = p.text.strip()
            if p.isdecimal():
                count_pages = p if int(p) > int(count_pages) else count_pages
        return int(count_pages)

    def _mount_list(self):
        def __decode(aHash: str, aHex: str):
            _ar = []
            for _index, n in enumerate(range(0, len(aHex), 2)):
                _ar.append(chr(int(aHex[n:n + 2], 16) ^ int(ord(aHash[_index % len(aHash)]))))
            return ''.join(_ar)

        current_page = 1
        url = 'https://pt.proxyservers.pro/proxy/list/speed/2/order/speed/order_dir/asc/page/'
        r = self._get(url + str(current_page))
        count_pages = self.__get_pages(r)

        while True:
            try:
                soup = BeautifulSoup(r, "html.parser")
                table = soup.find('table', {'class': 'table table-hover'})
                cHash = soup.find('div', {'class': 'card card-spec listdata-data'})
                cHash = cHash.find('script', string=re.compile('var chash')).text.strip()
                cHash = cHash[cHash.find("'")+1:cHash.find("';")]
                if table:
                    rows = table.find_all('tr')
                    row_header = rows[:1][0].find_all('th')
                    rows = rows[1::]
                    __FIELDS = [s.text.strip() for s in row_header]
                    idx_ip = __FIELDS.index('Endereço de IP')
                    idx_port = __FIELDS.index('Porto')
                    idx_prot = __FIELDS.index('Protocolo')
                    for row in rows:
                        cols = row.find_all('td')
                        if cols[0].has_attr('colspan'):
                            continue
                        ip = cols[idx_ip].text.strip()
                        port = __decode(cHash, cols[idx_port].find('span', {'class': 'port'})['data-port'])
                        protocol = 'SOCKS4' if cols[idx_prot].text.strip() == 'SOCKS4/5' else cols[idx_prot].text.strip()

                        if all([ip, port, protocol]):
                            self._list.append(f'{protocol}://{ip}:{port}')
                if current_page < count_pages:
                    current_page += 1
                    r = self._get(url + str(current_page))
                else:
                    self.__list = list
                    return False
            except:
                self.__list = list
                return False
