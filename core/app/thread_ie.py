from core.cnpj.cnpj_manager import CnpjManager
from core.proxys.proxy_manager import ProxyManager
from random import randint
from pathlib import Path
import threading
from core.utils import log, hutils, consts
import requests
import os
import time
from bs4 import BeautifulSoup
from core.cnpj.contribuinte import Contribuinte


class ThreadIE(threading.Thread):
    def __init__(self, aid=-1, auf='', alist=None, aid_reg_bd=-1, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super().__init__()
        self.id = aid
        self.__uf = auf
        self.ie_found = 0
        self.ie_not_found = 0
        self.cnpj_processed = 0
        self.__cnpj = CnpjManager('')
        self.__cnpj.id = aid
        self.__cnpj.list = alist
        self.__list_test = alist
        self.__payload = {
            '__VIEWSTATE': 'LTstk38s3a1n8ezhdLztWsPJkSXhkXEk0417MpRgtueDQHJrXF7jLZsLI0V+z5N6oHVGX4sJb9r3dMhaUY4IXm/kbhgRWbT8ngaMJJhEfd+PMoNKPiz0uyH8HVfUfesngZe3oknVzBd86kAXZZibMqPve3K/vyS1hy1Qz9AVJxJSyO7HPSnsi7+yM65rY9O0v4avOOxDchu/X1SCgofgGcjvBW5RtlMm0Ot9qO5b7dKk4gpzZU6iX+NWyil8LYCGBLpnLmk9plAzWsf7JXwEpmDGjnmbJ4qrF5PNj8cesue1m3gYeD2zFvSCDRPo/NUQAUYQNI1Nrn10unZW5FTM2XQFAFGQiXpr6eNw3yyO57dy7/UrIOjB/JrgwR11ErE6ouHos0OuCpGB9V0RIeIL3d1eMH6xH2XyOwW+cE/ElGzlCes3YRbEYISgUAs11/PxemBt+TG44QKGASGYBRDGy2UcPQF15GQZjqz1W67Y4Cndp6lIP5j3uSf8EzgmIfkO2IOI+DBfsbdkK0yB0KPhThJncNucbszqxCIJk7O1HVqgljVDqkaBDS4X0JLW3EDXgoNbCckAKbw+Apcr5wYp8SvTEHYcBrtCXF2SY48epszP2g3IUCIJdpc070bhLyrLZU738SBDJv5xouyRFhSqIMo4wDt4J57rbP5fdJfpK6VYhl3ps8tvT2TPlgmwfhY6kQXUl9nfYwSnBkAESuoblzMT0wSqx46aCFy0vfzLhb3krWxKNo7yNhAXf9v58cd43LuqUpzslWd3vEsIr0rBLwXSoiokizTKrv2yOJerBary+Wf+kLPB4WDHHPloUMpNhM7GoVrUf42WfLj3mByEdtHB/uxHdEEWroxpBIW9ro6reFyqcMsoCJaYhX+97kuiq1jeBxLKXZRYCng9/EIwm6X9h/4iAUYl8LtTcXhwAd+5XgBoSd0ciPl8Jw5TDy9r4qBqvlO0OtNC99m7aNLTknei1Yci7B86VCiskJUosiGA+viO8VXs6nv2qsEXsP717ZEhgbqCQJdVQj2PRO6KKDtEe/1ekHlAYMqUqmzlTZq225q7nUTMObgT3L+uAZCPTfMKeMzX1ldJayUflW+qcG8tzIy9WQDUAJ3q0QRBecFAKZBFtZ8EmZTBcYqUvJ1Gq1IhgDbLMURWQmtsHACVTUDPaoUqTlzaF3uj38yaVrd0Z0Sq/rLNdDBYM7dXRmVV6L2iVA8ehb7xCsViVtIP8/oZuT8T4yU7n++o1oKiJBFGhv+wk/mQsRtopifc6v05ayZZV6z8sz7s0kc4iIfpg6/81KYYBNlNMlKTQhGNSi5+nN8TiiAhqIR7Du5xKWXe0yd46KpLdb0n494pHkRVwwvwo/j4+UlshDqBxiFWSpnrckaMUqL+LtQdNlxXOGmR1AGJ8wy4YDSYN+qlvsHotjP5fLdE6y049Sxvqm5uU+sWkmos51S1HKQqmkVMN9kUG+TecKRSVtwAYUKxhy2ISy/K5zbrXfG3XhaTtO+U5QBkASaY5+jMpJeUIPPIMT6oOAeLzTJ+k0AlTITojy8PuUu6BbDJUivLGJaOgDEy2MJutnVMig101UHMpXwyBAN2zD/d3w==',
            '__VIEWSTATEGENERATOR': '0F85D1CD',
            '__VIEWSTATEENCRYPTED': '',
            '__EVENTVALIDATION': 'fB5rgUU/D6Hlfv7mom2Htj/ewh8gU3+SbzXP6aYamiFGHqu2LCIVCP9dWVxAT+uRnRAyIRUVnTQp012qA56tmltxJPQ6qTGZXvOufZB0mqIQMh+MlsSrdIdWgkXGOizmHRywC3xttYi8QPSDYEhc4gOS8HGQ2dkYh25/ilFAN7/8VZcZ9NLHiYSIQMUmNLLU22H6OPWzRXqGdRyy6Zz0idt90jWVg30YzlyhpyrkhA8PEjjuOGm1gH+RA7RUWnw9zuHcsoSQIVY6AA3brDH4+htz2kxulpx1X4HLONpNJWgV5FvLd1LOZFGKMBi+sCzEzGYoOshGjx78XMANDqSrOnlML6dAA19iz3z3GmGCTkHG3obX/z75UGvol9sZ+m4q+4Rt1QVA88nE56MPya073o7tGqPPEREF0NoTRiTwfKLiZwRSuVP6DIzPa3vGrUIOMZ5ubP0+LhyA+HGx+SS892TJxBufX6v6b9+4e2KOzk7cVyyxkRszfcXtrZEP/peiEFgJFhgRH6v/5cuHFsZ0hLZugZWXkEHIWGwnVA6wUr4WBI/cucGH+rPAzGT3cE2ARip+kd/kgjVLAmR3uERUFo2wo5ut4iDCZyZX90i9SDV+pZnCUbkxMkjPA6hif27xAKws5D3AgNXWWQ4oAH6mlC90bQPUCofhD+ZiUxSLbSsU9ZjuVVkniUdvM+1rxHumRSJMa6edlLI+Rdu8U0nzpY1yrCv2NVsJTThvR8oqGPhR7tTQBd05cx586HDHp4GoHs/qrvdR8bifQF63wSLwYZzJLXBJKtefmumC8eVyAfzbDgpGp8V9/uAoO1dl6EBWyV/PTX4fxVD49NFKgEUMYdzX6lOXGHlZYJTV1RSnJ95we0aFUVT6FS3Q5kutdTTb93va+fyBJlltJ/62xleVTjM7oTWSlUmTK4MS3Tcy5sWCk47NzJtVgZmaaai/yXISXeo1+II33CA53Y0mwBFRL/dYWTgABIiL1LsgOSOQA/qN+jvn27UafyUHI+ifMpIUvLq5QAuf/5ovajZO4e/omjuiV/E=',
            'txtie': '',
            'CmdUF': '',
            'CmdSituacao': '99',
            'AplicarFiltro': 'Aplicar+Filtro'
        }
        self.__PATH_NAME_LOG = f'extraction_{auf}_{aid_reg_bd}{os.sep}log{os.sep}'
        self.__PATH_NAME_EXTN = f'extraction_{auf}_{aid_reg_bd}{os.sep}dump{os.sep}'

    def run(self):
        self.request_ie()

    def request_ie(self):
        logFilename = f'{self.__PATH_NAME_LOG}log_thread_{str(self.id).zfill(3)}_{self.__uf}'
        outlog = f'[T{str(self.id).zfill(3)}|P{self.__cnpj.position}/S{len(self.__cnpj.list)}|{self.__payload.get("txtCNPJ")}]'
        try:
            vProxy = ProxyManager()
            vAddrs_prx = {'http': vProxy.next()}
            self.__payload.update({'txtCNPJ': self.__cnpj.next()})
            while not self.__cnpj.EOF:  # loop request
                try:
                    outlog = f'[T{str(self.id).zfill(3)}|P{self.__cnpj.position}/S{len(self.__cnpj.list)}|{self.__payload.get("txtCNPJ")}]'
                    headers = {'User-Agent': consts.userAgents[randint(0, 99)]}
                    r = requests.Response()
                    try:
                        r = requests.post(
                            'http://nfe.sefaz.ba.gov.br/servicos/nfenc/Modulos/Geral/NFENC_consulta_cadastro_ccc.aspx',
                            self.__payload,
                            headers=headers,
                            proxies=vAddrs_prx,
                            timeout=15,
                            allow_redirects=False)
                    except Exception as e:
                        log.writefile(f'{outlog}[REQUEST] Exception: {e}', logFilename)
                    log.writefile(f'{outlog}[REQUEST] Response: {r.status_code}', logFilename)
                    time.sleep(1)
                    if r.status_code == 200:
                        self.__parser(r.text, outlog, logFilename)
                    else:
                        if r.status_code in (403, 500, 502, 503, 504, None):
                            vAddrs_prx.update({'http': vProxy.next()})
                        log.writefile(f'{outlog}[REQUEST] Response: {r.status_code} BAD', logFilename)
                except Exception as e:
                    vAddrs_prx.update({'http': vProxy.next()})
                    log.writefile(f'{outlog}[MAIN_LOOP_EXCEPT] {e. __class__}\n {e}', logFilename)
                log.writefile(f'{outlog}[FOUND_NOT_FOUND] Found:{self.ie_found} Not found: {self.ie_not_found}', logFilename)
                self.cnpj_processed = self.__cnpj.position
        finally:
            log.writefile(f'{outlog}[MAIN_TRY_END] End CNPJs', logFilename)

    def __parser(self, text_html, outlog, logFilename):
        __FIELDS = ['cnpj', 'ie', 'razao_social', 'uf', 'situacao']
        list_ie = []
        soup = BeautifulSoup(text_html, "html.parser")
        if soup.find('span', {'id': 'lblConsultaVazia'}):
            self.ie_not_found += 1
            self.__payload.update({'txtCNPJ': self.__cnpj.next()})
        elif soup.find('table', {'id': 'Grid'}):
            table = soup.find('table', {'id': 'Grid'})
            rows = table.find_all('tr')[1::]
            for row in rows:
                cols = row.find_all('td')
                contrib = Contribuinte()
                for _index, _ele in enumerate(cols):
                    _s = _ele.text.strip()
                    log.writefile(f'{outlog}[OUT]: {_index}: {_s}', logFilename)
                    setattr(contrib, __FIELDS[_index], _s)
                list_ie.append(contrib)
            self.ie_found += len(list_ie)
            log.writefile(f'{outlog}[PARSER_DATA_IE] Found! {list_ie.__len__()}', logFilename)
            self.__saveIE(list_ie)
            self.__payload.update({'txtCNPJ': self.__cnpj.next()})
        else:
            log.writefile(f'{outlog}[PARSER_DATA_IE] Not found!', logFilename)
            self.ie_not_found += 1
            self.__payload.update({'txtCNPJ': self.__cnpj.next()})

    def __saveIE(self, aList_IE):
        import zlib
        v_dir = (os.getcwd() + os.sep + 'log' + os.sep)+self.__PATH_NAME_EXTN
        Path(v_dir).mkdir(parents=True, exist_ok=True)
        with open(f'{v_dir}extraction_thread_{str(self.id).zfill(3)}_{self.__uf}', 'a+b') as f:
            for c in aList_IE:
                _s = f'{c.cnpj}^|^{c.ie}^|^{c.razao_social}^|^{c.uf}^|^{c.cod_sit}^|^{c.situacao}'.encode('utf-8')
                _s = zlib.compress(_s)
                _size = len(_s).to_bytes(2, 'big')
                f.write(_size+_s)

