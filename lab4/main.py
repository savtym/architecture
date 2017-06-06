from os import system
from view import Menu
from database import DataBase


DataBase.getInstance().loadDataBase()
while True:
    Menu.getInstance().out()
    command = Menu.getInstance().getCommand()
    getattr(command["controller"].getInstance(), command["action"])()
    system('clear')
