from cnpj_manager import CnpjManager
import os.path
import time
import threading
import sys
import queue
import os
import argparse
import colorama
import banner
import log
from thread_ie import ThreadIE
import ctypes


colorama.init()
q = queue.Queue()
keepRunning = True
threadCount = 0
listThreads = []

def animated_loading(aText):
    # chars = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    chars = '/—\|'
    for char in chars:
        sys.stdout.write('\r' + aText + char)
        time.sleep(.1)
        sys.stdout.flush()

def quickedit(enabled=1):
    # -10 is input handle => STD_INPUT_HANDLE (DWORD) -10 | https://docs.microsoft.com/en-us/windows/console/getstdhandle
    # default = (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x200)
    # 0x40 is quick edit, #0x20 is insert mode
    # 0x8 is disabled by default
    kernel32 = ctypes.windll.kernel32
    if enabled:
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x40 | 0x100))
    else:
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x00 | 0x100))

def outputTerm(aCountThreads):
    print('\033[1B')
    global listThreads
    active = [True] * aCountThreads
    quickedit()
    while (True in active):

        for _index, th in enumerate(listThreads):
            if not th.is_alive():
                vstatus = 'FINALIZADO'
                active[_index] = False
            else:
                vstatus = 'PROCESSANDO'
            print(f'\033[{_index+18};{1}H\033[32m[*]|T:{str(th.id + 1).zfill(3)}|P:{str(th.cnpj.position).zfill(6)}/{str(th.cnpj.size()).zfill(6)}|Found:{str(th.found).zfill(6)}|NotFound:{str(th.not_found).zfill(6)}|{vstatus}| \033[0m')
        time.sleep(2)
    quickedit(0)
    print(f'\033[{str(aCountThreads+20)};{1}H\r\033[32mFinalizado!\033[0m')
    sys.exit()

def init_threads(aCountThreads, aCnpj, aUF):
    global threadCount
    log.writefile('Iniciando threads')
    global listThreads
    listThreads = []
    for i in range(aCountThreads):
        threadCount += 1
        log.writefile(f'Iniciando thread: {threadCount}')
        vIni = ((aCnpj.size() // aCountThreads) * i)
        vEnd = aCnpj.size() if (i + 1 == aCountThreads) else ((aCnpj.size() // aCountThreads) * (i + 1))
        vList = aCnpj.list[vIni:vEnd]
        log.writefile(f'Thread: {threadCount} inicializada!')
        time.sleep(1)
        t = ThreadIE(i, aUF, vList)
        listThreads.append(t)

    for th in listThreads:
        th.start()
    log.writefile('Todas as threads iniciadas!')

def exec_thread(aCountThreads, aUF, aFilename):
    try:
        if not os.path.exists(os.getcwd() + "\\" + aFilename):
            return print('Filename does not exist or is invalid.')

        vCnpj = CnpjManager(aFilename)

        the_process = threading.Thread(name='process', target=vCnpj.load)
        the_process.start()
        while the_process.is_alive():
            animated_loading('\033[34m[*] Loading file... \033[0m')
        print(f'\r\033[32m[*] CNPJ file successfully loaded! Size:[{vCnpj.size()}]\033[0m')

        global threadCount

        the_process = threading.Thread(name='process', target=init_threads, args=(aCountThreads, vCnpj, aUF,))
        the_process.start()
        while the_process.is_alive():
            animated_loading('\033[34m[*] Starting threads [' + str(aCountThreads).zfill(3) + '/' + str(threadCount).zfill(3) + '] \033[0m')
        print(f'\r\033[32m[*]Threads started successfully!\033[0m')
        the_process = threading.Thread(name='process', target=outputTerm, args=(aCountThreads,))
        the_process.start()

    except Exception as e:
        print('Error thread: ' + str(e))
    finally:
       pass

def mySorted():
    if os.path.exists(os.getcwd() + '\SaidaTotal.txt'):
        vList = []
        with open('SaidaTotal.txt', 'r') as f:
            for line in f:
                temp = line.split()
                vList.append(line)
        f.close()
        vList = sorted(set(vList))
        with open('SaidaTotalSorted.txt', 'w') as f:
            for i in vList:
                f.writelines(i)
            f.close()

def main():
    banner.banner()
    parser = argparse.ArgumentParser(description='Usage python botie [options]')
    parser.add_argument('-t', '--threads', nargs=1, type=int, required=True, help='THREADS numbers')
    parser.add_argument('-uf', '--uf', nargs=1, required=True, help='State initials')
    parser.add_argument('-f', '--file', nargs=1, required=True, help='CNPJ list filename')
    args = parser.parse_args()
    exec_thread(args.threads[0], args.uf[0], args.file[0])

if __name__ == '__main__':
    main()
