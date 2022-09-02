import os
import sqlite3
from sqlite3 import Error
from types import SimpleNamespace
import core.consts.consts as consts
from core.utils.hexcept import HExcept
from core.db import schemas
from datetime import datetime

PATH_BASE = (consts.PATH_CURRENT_APP + 'base' + os.sep)
PATH_BASE_FILENAME = (PATH_BASE + 'botie.db')


class MonitorDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.running = False

    def execute(self):
        self.__execute()

    def __execute(self):
        self.__create_connection()

    def __create_base_structure(self):
        try:
            self.cursor.execute(schemas.CREATE_TABLE_COMPANY)
            self.cursor.execute(schemas.CREATE_TABLE_REQUEST_STACK)
            self.cursor.execute(schemas.CREATE_TABLE_IE)
            self.connection.commit()
        except Error as e:
            HExcept.print_exit('Error execute crete_structure!', e)

    def __create_connection(self):
        base_exist = os.path.exists(PATH_BASE_FILENAME)
        self.connection = sqlite3.connect(PATH_BASE_FILENAME)
        try:
            if not base_exist:
                self.__create_base_structure()
            self.connection.row_factory = self.__dict_factory
            self.cursor = self.connection.cursor()
            # PRAGMA soon...
            # self.cursor.execute('PRAGMA journal_mode = OFF')
            # self.cursor.execute('PRAGMA synchronous = 0')
            # self.cursor.execute('PRAGMA cache_size = 1000000')
            # self.cursor.execute('PRAGMA locking_mode = EXCLUSIVE')
            # self.cursor.execute('PRAGMA temp_store = MEMORY')
            self.running = True
        except Exception as e:
            HExcept.print_exit('Error execute crete_connection!', e)

    def __dict_factory(self, cursor, row):
        class __Row(object):
            def __init__(self, _dict):
                self.__dict__.update(_dict)

        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return __Row(d)

    def __searchCNPJ(self, _packet):
        self.cursor.execute(' SELECT cnpj FROM company WHERE uf = ? ORDER BY 1', (_packet.data.uf,))
        fatch = self.cursor.fetchall()
        if fatch:
            vList = list(map(lambda s: s.cnpj, fatch))
            setattr(_packet.data, "cnpj_list", vList)
            _packet.exist = True
            _packet.info = f'Requests found: {_packet.data.uf}'
            return _packet
        else:
            _packet.exist = False
            _packet.info = f'Request found. But there is no data for UF: {_packet.data.uf}'
            return _packet

    def getRequest(self):
        _packet = SimpleNamespace(data=None, exist=False, info='')
        self.cursor.execute(' SELECT * FROM request_stack WHERE status = "pending" ORDER BY id ASC LIMIT 1')
        _packet.data = self.cursor.fetchone()
        if _packet.data is not None:
            return self.__searchCNPJ(_packet)
        else:
            _packet.exist = False
            _packet.info = 'No requests found.'
            return _packet

    def execute_script(self, script):
        try:
            self.connection.executescript(script)
            return True
        except Exception as e:
            print(script)
            HExcept.print_exit('Error execute execute_script!', e)
            return False

    def finalize_request(self, id: int, num_cnpj_bd: int, num_cnpj_processed: int, num_ie_found: int, num_ie_not_found: int):
        update = (
                'UPDATE request_stack ' +
                f'SET status = "success", ' +
                f'dt_hr_end = "{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}", ' +
                f'num_cnpj_bd = {num_cnpj_bd}, ' +
                f'num_cnpj_processed = {num_cnpj_processed}, ' +
                f'num_ie_found = {num_ie_found}, ' +
                f'num_ie_not_found = {num_ie_not_found} ' +
                f'WHERE id = {id};'
        )
        try:
            self.cursor.execute(update)
            self.connection.commit()
            return True
        except Exception as e:
            HExcept.print_exit('Error execute finalize_request!', e)
            return False

