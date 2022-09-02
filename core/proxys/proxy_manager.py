# Will be implemented soon...
import requests


class ProxyManager:
    def __init__(self):
        self.position = -1
        self.list = []

    def load(self):
        try:
            self.position = -1
            rHttp = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=no&anonymity=all&simplified=true', timeout=30)
            rSock4 = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1000&country=all', timeout=30)
            rSock5 = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1000&country=all', timeout=30)
            vList = []

            if rHttp.status_code == 200:
                for item in rHttp.text.split("\r\n"):
                    vList.append('HTTP://'+item)
            if rSock4.status_code == 200:
                for item in rSock4.text.split("\r\n"):
                    vList.append('SOCKS4://'+item)
            if rSock5.status_code == 200:
                for item in rSock5.text.split("\r\n"):
                    vList.append('SOCKS5://'+item)

            r = requests.get('https://www.proxyscan.io/api/proxy?last_check=9800&ping=300&limit=100&type=socks4,socks5,http,https', timeout=30)
            if r.status_code == 200 and r.json():
                for item in r.json():
                    self.list.append(item['Type'][0] + '://' + item['Ip'] + ':' + str(item['Port']))

            r = requests.get('https://proxylist.geonode.com/api/proxy-list?limit=500&sort_by=speed&sort_type=asc', timeout=30)

            if r.status_code == 200 and r.json():
                for data in r.json()['data']:
                    for protocol in data['protocols']:
                        self.list.append(f'{protocol.upper()}://{data["ip"]}:{data["port"]}')
            self.list = vList
            return True
        except:
            pass

    def next(self):
        try:
            if self.list and (self.position < len(self.list)):
                self.position = self.position + 1
                item = self.list[self.position]
                return item
            else:
                self.load()
                self.next()
        except:
            pass
