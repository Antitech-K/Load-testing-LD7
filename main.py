#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import os   
import requests
import json
import time
import logging                                                           



def shutdown_rodos():
    for x in range(16):
        a = "/opt/RODOS4/RODOS4 --id 4798 --c" +str(x) + " 0"
        os.system(a)
    return "Усё"   

start = os.system("curl --location --request GET http://localhost:3000/start")
down_rele = os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
time.sleep(0.5)
os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 128")


a = 0 
while a != 20000:
    status = ''
    while status != '{"result":"READY"}':
        time.sleep (1)
        status = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
        if status =="":
            down_rele
            print ("Не запущен тест-драйвер. Программа отменена.")
            exit()
        elif status == '{"result":"ONLINE"}':
            down_rele
            time.sleep(1)
            shutdown_rodos()
            print ("Выключаю шарманку")
            exit(0)
    print("Запуск измерений.")
    os.popen("./request_post.py")
    time.sleep(2)
    
    status_working = requests.get("http://localhost:3000/status")
    if status_working.text != '{"result":"WORKING"}':
        down_rele
        print ("Бля...опять что-то с измерениями. Давай с начала! Программа отменена.")
        exit()
    else:
        #print (status_working.text, type(status_working.text))
      
        while status_working.text == '{"result":"WORKING"}':
            status_working = requests.get("http://localhost:3000/status")
            time.sleep(1)
            #status_working = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
            #print (status_working.text)
            if status_working.text == "" or status_working == '{"result":"READY"}':
                os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
                print ("Хюстон, у нас проблемы. Программа отменена.")
                exit()
        #print ('Точка 1')
        if  status_working.text == '{"result":"RECOVERING"}' :
            file = open ('./clipboard.txt', 'r')
            resault_measure = file.read()
            file.close()
            #print (resault_measure.find('sys"'))
            if resault_measure.find('sys"') != 21:
                print("Прибор не выдал требуемые результаты.")
            elif resault_measure.find('sys"') == 21:
                file = open ('./result.txt', 'r')
                number = file.read()
                file.close()
                file = open ('./result.txt', 'w')
                number = int (number) + 1
                file.write(str (number))
                file.close()
                print("Кол-во измерений =", number)
        a += 1
        time.sleep(3)
        

'''     
        if measure.text.find('sys"') != 21:
            down_rele
            print ("Бля...опять что-то с измерениями. Давай с начала!")
            exit ()
        else:
            print("В работе", status_working)
            while status_working == '{"result":"WORKING"}':
                time.sleep (1) 
                status_working = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
                if status_working == "" or status_working == '{"result":"ONLINE"}':
                    os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
                    print ("Хюстон, у нас проблемы. Программа отменена.")
                    exit()
            
            if  status_working == '{"result":"RECOVERING"}' : 
                file = open ('./result.txt', 'r')
                number = file.read()
                file.close()
                file = open ('./result.txt', 'w')
                number = int (number) + 1
                file.write(str (number))
                file.close()
                print("Кол-во измерений =", number)
                a += 1
                time.sleep(3)
    except KeyboardInterrupt:
        os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
        os.system("curl --location --request GET http://localhost:3000/stop")
        shutdown_rodos()
        print ("Жестко ты со мной.")    
        exit()
'''
time.sleep(3)
os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
time.sleep(1)
print (shutdown_rodos())   

