from pyfiglet import Figlet


def banner():
    print('\033[2J')
    custom_fig = Figlet(font='larry3d')
    print('\033[31m' + custom_fig.renderText('BOTIE') + '\033[0m')
    print('[!] BOTIE is a script to capture state registrations using cnpj.\n\n')