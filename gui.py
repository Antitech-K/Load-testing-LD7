#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from email import message
from tkinter import *
import os
import subprocess
from tkinter import messagebox




def start():
    status = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
    
    if status == "":
        messagebox.showinfo (message = "Не запущен тест-драйвер. Программа отменена.")
        pass
    elif status == '{"result":"READY"}' or status == '{"result":"ONLINE"}':
        subprocess.Popen([sys.executable, './main.py'])
        pass
    else:
        messagebox.showinfo (message = "Что-то не работает!")
        pass

def stop():
    os.system("curl --location --request GET http://localhost:3000/stop")
    pass


window = Tk()
window.title("Нагрузка на износ тонометр LD")
window.geometry ('640x350')
window.resizable (height=False, width=False)

frame = Frame(window)
frame.place(relheight=1, relwidth=1)

button1 = Button(frame, text='Запустить Кракена', bg = "green2", font= '16', command=start)
button2 = Button(frame, text='Выключить шарманку', bg = "red2", font= '16', command=stop)
button1.place(height=50, width=200, x= 80, y = 100)
button2.place(height=50, width=200, x= 350, y = 100)

window.mainloop()
