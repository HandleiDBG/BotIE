from core.utils import banner, consts
from core.app.app import App
import colorama

colorama.init(autoreset=True)


def main():
    banner.banner()
    app = App()
    app.execute()


if __name__ == '__main__':
    main()









