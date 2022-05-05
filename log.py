from datetime import datetime
import os
from pathlib import Path

PATH_LOG = (os.getcwd() + os.sep + 'log' + os.sep)


def writefile(data='', filename='log'):
    Path(PATH_LOG).mkdir(parents=True, exist_ok=True)
    with open(PATH_LOG + filename, 'a') as f:
        f.write(f'[{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}]: {data}\n')
