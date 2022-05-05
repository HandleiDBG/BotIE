import requests

class ProxyManager:
    def __init__(self):
        self.position = -1
        self.list = []

    def load(self):
        try:
            rHttp = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=no&anonymity=all&simplified=true')
            rSock4 = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=1000&country=all')
            rSock5 = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=1000&country=all')
            vList = []

            for item in rHttp.text.split("\r\n"):
                vList.append('HTTP://'+item)
            for item in rSock4.text.split("\r\n"):
                vList.append('SOCKS4://'+item)
            for item in rSock5.text.split("\r\n"):
                vList.append('SOCKS5://'+item)

            self.list = vList

            # r = requests.get(
            #     'https://www.proxyscan.io/api/proxy?last_check=9800&ping=300&limit=100&type=socks4,socks5,http,https')
            # if not r.json():
            #     return False
            #
            # for item in r.json():
            #     self.list.append(item['Type'][0] + '://' + item['Ip'] + ':' + str(item['Port']))
            #
            # self.position = 0

            return True
        except:
            pass
            # print('Error: Load Proxy!')

    # def load(self):
    #     r = requests.get('https://www.proxyscan.io/api/proxy?last_check=9800&uptime=50&ping=300&limit=100&type=socks4,socks5,http,https')
    #     vList = []
    #     if not r.json():
    #         return False
    #
    #     for item in r.json():
    #         vList.append(item['Type'][0] + '://' + item['Ip'] + ':' + str(item['Port']))
    #
    #     self.list = vList
    #     self.position = 0
    #     return True

    def next(self):
        try:
            if not self.list or not self.position <= len(self.list):
                self.load()
                self.position = -1
            if self.list:
                self.position = self.position + 1
                item = self.list[self.position]
                # self.list.remove(item)
                return item
        except:
            print('ProxyManager: Index out of range')
