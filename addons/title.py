import fade
from colorama import Fore, init

colors = {
    'DARK_GRAY': "\033[1;30m",
    'LIGHT_GRAY': "\033[0;37m"
}
init()
def blackwhite(text):
    faded = ""
    red = 0; green = 0; blue = 0
    for line in text.splitlines():
        faded += (f"\033[38;2;{blue};{green};{red}m{line}\033[0m\n")
        if not red == 255 and not green == 255 and not blue == 255:
            red += 20; green += 20; blue += 20
            if red > 255 and green > 255 and blue > 255:
                red = 255; green = 255; blue = 255
    return faded

class Logo:
    def __init__(self, creator):
        self.creator = creator

    def show(self):
        print(blackwhite(f"""
 ██▀███   ██▓ ██▓███   ██▓███   ██▓    ▓█████ 
▓██ ▒ ██▒▓██▒▓██░  ██▒▓██░  ██▒▓██▒    ▓█   ▀ 
▓██ ░▄█ ▒▒██▒▓██░ ██▓▒▓██░ ██▓▒▒██░    ▒███   
▒██▀▀█▄  ░██░▒██▄█▓▒ ▒▒██▄█▓▒ ▒▒██░    ▒▓█  ▄ 
░██▓ ▒██▒░██░▒██▒ ░  ░▒██▒ ░  ░░██████▒░▒████▒
░ ▒▓ ░▒▓░░▓  ▒▓▒░ ░  ░▒▓▒░ ░  ░░ ▒░▓  ░░░ ▒░ ░
  ░▒ ░ ▒░ ▒ ░░▒ ░     ░▒ ░     ░ ░ ▒  ░ ░ ░  ░
  ░░   ░  ▒ ░░░       ░░         ░ ░      ░   
   ░      ░                        ░  ░   ░  ░
                                {self.creator}"""))
    
    def __call__(self, txt):
        return f"{colors['DARK_GRAY']}[{colors['LIGHT_GRAY']}{txt}{colors['DARK_GRAY']}]{Fore.RESET} "