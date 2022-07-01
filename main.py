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
os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 128")

a = 0 
while a != 20000:
    status = ''
    while status != '{"result":"READY"}':
        time.sleep (1)
        status = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
        if status =="":
            os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0") 
            print ("Не запущен тест-драйвер. Программа отменена.")
            exit()
    print("Запуск измерений.")
 
    try:
        url = 'http://localhost:3000/measure'
        body = {}
        headers = {'content-type': 'application/json'}
        try:
            requests.post(url, data=json.dumps(body), headers=headers, timeout=1)
            
        except requests.exceptions.ReadTimeout: 
            pass  
      
        status_working = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read() 
        if status_working != '{"result":"WORKING"}':
            print ("Бля...опять сломал. Давай с начала!", status_working )
            exit ()
        else:
            print("В работе", status_working)
            while status_working == '{"result":"WORKING"}':
                time.sleep (1) 
                status_working = os.popen("curl -s --location --request GET http://localhost:3000/status 2>&1").read()
                if status_working == "":
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
        print ("Жестко ты со мной.")    
        exit()

time.sleep(3)
os.system("/opt/RODOS4/RODOS4 --id 4798 --c10 0")
time.sleep(1)
print (shutdown_rodos())   

