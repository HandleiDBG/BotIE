from colorama import Fore


class HExcept:

    @staticmethod
    def print_exit(custom_msg='', msg_except=''):
        print(f'\n{Fore.RED}[CRITICAL] {custom_msg}')
        print(f'{Fore.RED}[ERROR] {str(msg_except)}')
        raise SystemExit(1)

