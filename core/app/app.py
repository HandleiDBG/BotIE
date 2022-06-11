import time
import ctypes
from core.app.thread_ie import ThreadIE
from colorama import Fore
from core.db.monitor import MonitorDB


class App:
    def __init__(self):
        self.__thread_count = 0
        self.__list_threads = []
        self.__count_cnpj_ie = {'processed': 0, 'found': 0, 'n_found': 0}
        self.monitor = MonitorDB()
        self.__cnpj_list = []
        self.__uf = ''
        self.__num_threads = 0

    def execute(self):
        def __read_thread_props():
            self.__count_cnpj_ie = {'processed': 0, 'found': 0, 'n_found': 0}
            for _index, th in enumerate(self.__list_threads):
                self.__count_cnpj_ie['processed'] = self.__count_cnpj_ie['processed'] + th.found + th.not_found
                self.__count_cnpj_ie['found'] = self.__count_cnpj_ie['found'] + th.found
                self.__count_cnpj_ie['n_found'] = self.__count_cnpj_ie['n_found'] + th.not_found

        try:
            self.monitor.execute()
            while self.monitor.running:
                request = self.monitor.getRequest()
                if request:
                    if request.cnpj_list:
                        self.__cnpj_list = request.cnpj_list
                        self.__num_threads = 10 # Implementar um padrão pra quandidade de threads.
                        self.__uf = request.uf
                        print(f'Existe cnpj pra {self.__uf} {len(self.__cnpj_list)}')

                        self.__prepare_thread()
                        self.__start_threads()
                        while self.__list_threads:
                            __read_thread_props()

                            print(f'\r{Fore.GREEN}[*] Active threads:{str(len(self.__list_threads)).zfill(3)}/{str(self.__num_threads).zfill(3)}'
                                f'{Fore.GREEN} | CNPJ\'s processed:{str(self.__count_cnpj_ie["processed"]).zfill(5)}/{str(self.__cnpj_list.__len__())}'
                                f'{Fore.GREEN} | Found/NotFound:{str(self.__count_cnpj_ie["found"]).zfill(5)}/{str(self.__count_cnpj_ie["n_found"]).zfill(5)}',
                                end='',
                                flush=False)
                            if not [t for t in self.__list_threads if t.is_alive()]:
                                self.__list_threads = []
                                print(f'\n{Fore.GREEN}[*] All threads terminated!')
                                break
                            time.sleep(2)
                        print(f'\n{Fore.GREEN}[*] Extraction completed!')


                else:
                    print('sem dados')
                time.sleep(10)
        except Exception as e:
            print(f'\n{Fore.RED}[CRITICAL] Error execute APP!')
            print(f'{Fore.RED}[ERROR] {str(e)}')
            raise SystemExit(1)

    def __start_threads(self):
        try:
            for i, th in enumerate(self.__list_threads):
                th.start()
                print(f'\r{Fore.BLUE}[*] Starting threads [{str(i+1).zfill(3)}/{str(self.__num_threads).zfill(3)}]', end='', flush=False)
                time.sleep(1)
            print(f'\n{Fore.GREEN}[*] All threads started!')
        except Exception as e:
            print(f'\n{Fore.RED}[CRITICAL] Error while starting threads!')
            print(f'\r{Fore.RED}[ERROR] {str(e)}')
            raise SystemExit(1)

    def __prepare_thread(self):
        try:
            for i in range(self.__num_threads):
                print(f'\r{Fore.BLUE}[*] Preparing threads [{str(i+1).zfill(3)}/{str(self.__num_threads).zfill(3)}]', end='', flush=False)
                vIni = ((self.__cnpj_list.__len__() // self.__num_threads) * i)
                vEnd = self.__cnpj_list.__len__() if (i + 1 == self.__num_threads) else ((self.__cnpj_list.__len__() // self.__num_threads) * (i + 1))
                vList = self.__cnpj_list[vIni:vEnd]
                time.sleep(1)
                t = ThreadIE(i, self.__uf, vList)
                self.__list_threads.append(t)
            print(f'\n{Fore.GREEN}[*] All threads ready!')
        except Exception as e:
            print(f'\n{Fore.RED}[CRITICAL] Error while preparing threads!')
            print(f'\r{Fore.RED}[ERROR] {str(e)}')
            raise SystemExit(1)

    def __quickedit(self, enabled=1):
        # -10 is input handle => STD_INPUT_HANDLE (DWORD) -10 | https://docs.microsoft.com/en-us/windows/console/getstdhandle
        # default = (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x200)
        # 0x40 is quick edit, #0x20 is insert mode
        # 0x8 is disabled by default
        kernel32 = ctypes.windll.kernel32
        if enabled:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x40 | 0x100))
        else:
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x00 | 0x100))
