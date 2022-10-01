from core.proxy.proxy_class import freeproxylist, proxylistdownload, openproxy_space, ptproxyserverspro


class Proxys:
    def __init__(self):
        self.__listProxyPosition = 0
        self.__count_refresh = 0
        self.__listObj = None
        self.__listProxy = None
        self.__itProxy = None
        self.__mount()

    def __mount(self):
        self.__count_refresh += 1
        self.__listProxyPosition = 0
        self.__mountListObj()
        if self.__listObj:
            self.__mountListProxy()

    def __mountListProxy(self):
        try:
            _list = []
            for obj in self.__listObj:
                _list.extend(obj.get_list())
            self.__listProxy = _list
            self.__itProxy = iter(_list)
        except:
            self.__listProxy = None
            raise

    def __mountListObj(self):
        try:
            self.__listObj = [
                freeproxylist.FreeProxyList(),
                proxylistdownload.ProxyListDownload(),
                openproxy_space.OpenProxySpace()
                # ptproxyserverspro.PtProxyServersPro()
            ]
        except:
            self.__listObj = None
            raise

    def getNext(self):
        try:
            _p = next(self.__itProxy)
            self.__listProxyPosition += 1
            return _p
        except:
            self.__mount()
            _p = next(self.__itProxy)
            self.__listProxyPosition += 1
            return _p

    @property
    def listSize(self):
        return len(self.__listProxy) if self.__listProxy else -1

    @property
    def listPosition(self):
        return self.__listProxyPosition

    @property
    def refreshCount(self):
        return self.__count_refresh

