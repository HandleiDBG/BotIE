from datetime import datetime
import os
from pathlib import Path

PATH_LOG = (os.getcwd() + os.sep + 'log' + os.sep)


def writefile(data='', filename=None):
    filename_path = ''
    if filename is not None:
        i = filename.rfind(os.sep)
        if i > -1:
            filename_path = filename[:i + 1]
            filename = filename[i + 1::]
    Path(PATH_LOG + filename_path).mkdir(parents=True, exist_ok=True)
    with open(PATH_LOG + filename_path + filename, 'a') as f:
        f.write(f'[{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}]: {data}\n')
