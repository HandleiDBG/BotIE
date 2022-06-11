import sqlite3
from sqlite3 import Error
import os
import core.utils.consts as consts

PATH_BASE = (consts.PATH_CURRENT_APP + 'base' + os.sep)
PATH_BASE_FILENAME = (PATH_BASE + 'botie.db')


class MonitorDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.running = False

    def __create_base_structure(self):
        try:
            self.cursor.execute(
                'CREATE TABLE company ( cnpj TEXT NOT NULL, uf TEXT NOT NULL, import_date TEXT NOT NULL );')
            self.cursor.execute('CREATE TABLE request_stack (' +
                                'id INTEGER PRIMARY KEY NOT NULL,' +
                                'uf CHAR(2) NOT NULL,' +
                                'num_thread INT NOT NULL DEFAULT ( -1),' +
                                'dt_hr_scheduled DATETIME NOT NULL DEFAULT (datetime() ),' +
                                'dt_hr_inclusion DATETIME NOT NULL DEFAULT (datetime() ),' +
                                'dt_hr_end DATETIME,' +
                                'status TEXT DEFAULT pendente NOT NULL,' +
                                'num_cnpj_bd        BIGINT,' +
                                'num_cnpj_processed BIGINT,' +
                                'num_ie_found       BIGINT,' +
                                'num_ie_not_found   BIGINT );'
                                )
            self.connection.commit()
        except Error as e:
            print(e)

    def __create_connection(self):
        base_exist = os.path.exists(PATH_BASE_FILENAME)
        try:
            self.connection = sqlite3.connect(PATH_BASE_FILENAME)
            if not base_exist:
                self.__create_base_structure()
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            self.connection.row_factory = self.__dict_factory
            self.cursor = self.connection.cursor()
            self.running = True

    def __dict_factory(self, cursor, row):
        class __Row(object):
            def __init__(self, _dict):
                self.__dict__.update(_dict)

        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return __Row(d)

    def __searchCNPJ(self, request):
        self.cursor.execute(' SELECT cnpj FROM company WHERE uf = ? ORDER BY 1 ASC LIMIT 100', (request.uf,))
        vList = list(map(lambda s: s.cnpj, self.cursor.fetchall()))
        setattr(request, "cnpj_list", vList)
        return request

    def getRequest(self):
        self.cursor.execute(' SELECT * FROM request_stack WHERE status = "pendente" ORDER BY id ASC LIMIT 1')
        request = self.cursor.fetchone()
        if request is not None:
            return self.__searchCNPJ(request)

    def __execute(self):
        self.__create_connection()

    def execute(self):
        self.__execute()
