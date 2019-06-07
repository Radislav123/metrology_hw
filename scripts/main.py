import os
from scripts.interface.interface import Window
# можете вставить здесь какой-нибудь код для инициализации переменных приложения
os.chdir("interface")
main_window = Window()
main_window.run()
