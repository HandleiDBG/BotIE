import os
from pathlib import Path

import time
import colorama
from colorama import Cursor
import sys
import requests
import ctypes





if __name__ == '__main__':
    colorama.init()
    active = [True] * 3

    while (True in active):
        for _index, item in enumerate(active):
            print(f'Antes: {active}')
            active[_index] = False
            print(f'Deposs: {active}')
            time.sleep(2)
    print(f'saiu: {active}')


    # out = [
    #         '|T:001|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:002|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:003|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:004|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:005|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:006|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|',
    #        '|T:007|P:000000/000000|Found:000000|NotFound:000000|PROCESSANDO|'
    # ]
    # arr = out
    # for _index, item in enumerate(out):
    #         arr[_index] = f'\033[{_index+2};{1}H\033[32m[*]|T:{str(_index).zfill(3)}|P:000000/000010|Found:000000|NotFound:000000|PROCESSAND| \033[0m'
    #
    # for _index, item in enumerate(out):
    #     for i in range(7):
    #         arr[_index] = f'\033[{_index+2};{1}H\033[32m[*]|T:{str(_index).zfill(3)}|P:{str(i).zfill(6)}/000010|Found:{str(i).zfill(6)}|NotFound:000000|PROCESSAND| \033[0m'
    #         print('\n'.join(arr))
    #         # print('\033[' + str(7 + 3) + 'A')
    #         time.sleep(0.1)
    #     print('\n'.join(arr))
    # print('\n'.join(arr))
    # sys.exit()
    # print('teste1')
    #
    # print('teste2')
