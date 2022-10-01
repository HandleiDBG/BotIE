import time
import os
from datetime import datetime
import ctypes
from core.app.thread_ie import ThreadIE
from colorama import Fore
from core.db.monitor import MonitorDB
from core.utils.hexcept import HExcept
import zlib
from core.proxy.proxys import Proxys


class App:
    def __init__(self):
        self.__thread_count = 0
        self.__list_threads = []
        self.__count_cnpj_ie = {'processed': 0, 'found': 0, 'n_found': 0}
        self.__monitor = MonitorDB()
        self.__cnpj_list = []
        self.__uf = ''
        self.__num_threads = 0
        self.datetime_formated = f'[{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}]'
        self.time_formated = f'[{datetime.today().strftime("%H:%M:%S")}]'
        self.__request_id = -1
        self.__proxy = None

    def __loadProxyList(self):
        self.__proxy = Proxys()


    def execute(self):
        def __read_thread_props():
            self.__count_cnpj_ie = {'processed': 0, 'found': 0, 'n_found': 0}
            for _index, th in enumerate(self.__list_threads):
                self.__count_cnpj_ie['processed'] = self.__count_cnpj_ie['processed'] + th.cnpj_processed
                self.__count_cnpj_ie['found'] = self.__count_cnpj_ie['found'] + th.ie_found
                self.__count_cnpj_ie['n_found'] = self.__count_cnpj_ie['n_found'] + th.ie_not_found

        try:
            self.__monitor.execute()
            while self.__monitor.running:
                print(f'Checking for a request...')
                request = self.__monitor.getRequest()
                if request.exist:
                    self.__uf = request.data.uf
                    self.__cnpj_list = request.data.cnpj_list
                    self.__num_threads = 20 if request.data.num_thread is None else request.data.num_thread
                    print(f'Extract request found: UF:{self.__uf} Amount:{len(self.__cnpj_list)}')
                    print('Loading proxy...')
                    self.__loadProxyList()
                    print(f'Proxy loaded! {self.__proxy.listSize}')
                    self.__request_id = request.data.id
                    self.__prepare_thread()
                    self.__start_threads()
                    qZero = len(str(self.__cnpj_list.__len__()))+1
                    while self.__list_threads:
                        __read_thread_props()
                        print(
                            f'\r{Fore.GREEN}[*] Active threads:{str(len(self.__list_threads)).zfill(3)}/{str(self.__num_threads).zfill(3)}'
                            f'{Fore.GREEN} | CNPJ\'s processed:{str(self.__count_cnpj_ie["processed"]).zfill(qZero)}/{str(self.__cnpj_list.__len__())}'
                            f'{Fore.GREEN} | Found/NotFound/Total:{str(self.__count_cnpj_ie["found"]).zfill(qZero)}/{str(self.__count_cnpj_ie["n_found"]).zfill(qZero)}/{str(self.__count_cnpj_ie["found"] + self.__count_cnpj_ie["n_found"]).zfill(qZero)}|{self.__proxy.listPosition}/{self.__proxy.listSize}/{self.__proxy.refreshCount}',
                            end='',
                            flush=False)
                        if not [t for t in self.__list_threads if t.is_alive()]:
                            self.__list_threads = []
                            print(f'\n{Fore.GREEN}[*] All threads terminated!')
                            break
                        time.sleep(2)
                    print(f'{Fore.GREEN}[*] Extraction completed!')
                    if self.__count_cnpj_ie['found'] > 0:
                        self.__process_file_ie()
                    # self.__process_file_ie()
                    if self.__monitor.finalize_request(id=self.__request_id,
                                                       num_cnpj_bd=len(self.__cnpj_list),
                                                       num_cnpj_processed=self.__count_cnpj_ie["processed"],
                                                       num_ie_found=self.__count_cnpj_ie["found"],
                                                       num_ie_not_found=self.__count_cnpj_ie["n_found"]
                                                       ):
                        print(f'{Fore.GREEN}[*] Completed request! ID: {self.__request_id}')
                    else:
                        HExcept.print_exit('Error updating request.')
                else:
                    print(f'{Fore.YELLOW}{self.time_formated}[INFO]{request.info}')
                time.sleep(60*10)  # The polling interval will be implemented soon...
        except Exception as e:
            HExcept.print_exit('Error execute APP!', e)
            raise

    def __start_threads(self):
        try:
            for i, th in enumerate(self.__list_threads):
                th.start()
                print(f'\r{Fore.BLUE}[*] Starting threads [{str(i + 1).zfill(3)}/{str(self.__num_threads).zfill(3)}]',
                      end='', flush=False)
                time.sleep(0.2)
            print(f'\n{Fore.GREEN}[*] All threads started!')
        except Exception as e:
            HExcept.print_exit('Error while starting threads!', e)

    def __prepare_thread(self):
        try:
            for i in range(self.__num_threads):
                print(f'\r{Fore.BLUE}[*] Preparing threads [{str(i + 1).zfill(3)}/{str(self.__num_threads).zfill(3)}]',
                      end='', flush=False)
                vIni = ((self.__cnpj_list.__len__() // self.__num_threads) * i)
                vEnd = self.__cnpj_list.__len__() if (i + 1 == self.__num_threads) else (
                            (self.__cnpj_list.__len__() // self.__num_threads) * (i + 1))
                vList = self.__cnpj_list[vIni:vEnd]
                time.sleep(0.5)
                t = ThreadIE(aid=i, auf=self.__uf, alist=vList, aid_reg_bd=self.__request_id, proxyObj=self.__proxy)
                self.__list_threads.append(t)
            print(f'\n{Fore.GREEN}[*] All threads ready!')
        except Exception as e:
            HExcept.print_exit('Error while preparing threads!', e)

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

    def __process_file_ie(self):
        vdir = (os.getcwd() + os.sep + 'log' + os.sep) + f'extraction_{self.__uf}_{self.__request_id}{os.sep}dump{os.sep}'
        list_files = list(filter(lambda x: x.startswith('extraction_thread_'), os.listdir(vdir)))
        insert = 'INSERT INTO ie (cnpj, ie, razao_social, uf, cod_sit, situacao, record_dt_hr) VALUES'
        records = []
        print(f'{Fore.BLUE}[*] Saving data in the database...')
        dt_hr = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        count_rec_tot = 0
        rec_saved = 0
        for _indexFile, file in enumerate(list_files):
            with open(vdir + file, 'rb') as f:
                while _size := f.read(2):
                    size = int.from_bytes(_size, 'big')
                    s = zlib.decompress(f.read(size)).decode('utf-8')
                    s = s.split('^|^')
                    values = '( '
                    for _index, ss in enumerate(s):
                        if _index == len(s) - 1:
                            values = values + f'"{ss}", "{dt_hr}")'
                        else:
                            values = values + f'"{ss}",'
                    records.append(values)
                count_rec_tot += len(records)

                if records:
                    quant_block = 1000
                    while records:
                        size_insert = records[:quant_block]
                        rec = insert + ','.join(records[:quant_block])
                        if self.__monitor.execute_script(rec):
                            rec_saved += len(size_insert)
                            print(f'\r{Fore.BLUE}[*] File:{_indexFile+1}|{len(list_files)} records:{str(rec_saved)}|{count_rec_tot}', end='', flush=False)
                            del records[:quant_block]
                        else:
                            HExcept.print_exit('Error in execute script!')

        print(f'\n{Fore.GREEN}[*] All data successfully saved in the database')
        # print(f'{Fore.GREEN}[*] Finished')

