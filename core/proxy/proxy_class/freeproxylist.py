from bs4 import BeautifulSoup
from core.proxy.proxy_class.proxy_base import ProxyBase

# https://free-proxy-list.net/


class FreeProxyList(ProxyBase):
    def __init__(self):
        super().__init__()
        self.link_name = 'free-proxy-list.net'

    def _mount_list(self):
        urls = [
            'https://www.sslproxies.org/',
            'https://www.socks-proxy.net/',
            'https://free-proxy-list.net/'
        ]
        for url in urls:
            r = self._get(url)

            soup = BeautifulSoup(r, "html.parser")
            table = soup.find('table', {'class': 'table table-striped table-bordered'})

            if table:
                rows = table.find_all('tr')
                row_header = rows[:1][0].find_all('th')
                rows = rows[1::]

                __FIELDS = [s.text.strip() for s in row_header]

                idx_ip = __FIELDS.index('IP Address')
                idx_port = __FIELDS.index('Port')
                idx_prot = __FIELDS.index('Https')

                idx_version = __FIELDS.index('Version') if 'Version' in __FIELDS else None

                for row in rows:
                    cols = row.find_all('td')
                    ip = cols[idx_ip].text.strip()
                    port = cols[idx_port].text.strip()
                    if idx_version:
                        protocol = cols[idx_version].text.strip()
                    elif cols[idx_prot].text.strip() == 'yes':
                        protocol = 'HTTPS'
                    elif cols[idx_prot].text.strip() == 'no':
                        protocol = 'HTTP'
                    else:
                        protocol = ''

                    if all([ip, port, protocol]):
                        self._list.append(f'{protocol}://{ip}:{port}')