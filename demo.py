import os, json, time, requests, shutil, asyncio, threading, datetime, sqlite3, subprocess
from threading import Thread
from functools import partial
from datetime import datetime
import numpy as np
import pathlib
import shutil
import time
from datetime import datetime
import sympy
from py_essentials import simpleRandom as sr
import shutil
import base64
import re
import uiautomator2
import subprocess
from uiautomator2 import Device
import  os, json
from faker import Faker
import pyperclip
import requests
import sys
import random
from urllib.request import urlopen
CREATE_NO_WINDOW = 0x08000000


#SYSTEM VAR, PLEASE DONT CHANGE
debug_mode = False

#CONFIG VAR, CAN BE CHANGE
# max_thread  = 2 # <----- Số luồng tối đa chạy đồng thời



password = 'Stella1234'

email =''
code_mail=''
username=''
# TAO_ACC_XIT=''
# LOI_DANG_KI=''




list_key_tinsoft = ['TLBVlTKqeYzUdwuUeUdoKBDKbTtxbWfLx2p0lX']


proc = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
serviceList = proc.communicate()[0].decode('ascii').split('\n')
# print(proc)
print(serviceList)
list_serial = []

for i in range(1, len(serviceList) -2 ):
    try:
        device1 = serviceList[i].split('\t')[0]

        
        # if len(device1) < 20 :
        # print(len(device1))
        list_serial.append(device1)
        print(device1)
    except Exception as e:
        print(str(e))
        pass
print(list_serial) 
# time.sleep(1000)
if len(list_serial) < 1:
            print('Không tìm thấy thiết bị nào')
            sys.exit()
max_thread = len(list_serial)


async def chia_luong():
    global luot_dang_chay, current_index, luong_hien_tai
    so_lan_can_chay = 16
    current_index = 0
    luot_dang_chay = 0
    for luot_hien_tai in range(so_lan_can_chay):
        try:
            for luong_hien_tai in range(max_thread):

                while True:
                    if luot_dang_chay < max_thread:
                        # if luot_dang_chay < len(list_serial):
                        luot_dang_chay += 1
                        print(f'Lượt hiện tại: {luot_hien_tai} ---> luồng hiện tại:{luong_hien_tai} | index = {current_index} ---> số luồng đang chạy đồng thời : {luot_dang_chay}')
                    
                        x = threading.Thread(target = call_session_work, args = (current_index,))

                        x.start()
                        await asyncio.sleep(0.1)
                        break
                    else:
                        await asyncio.sleep(0.1)
                
                # if current_index < len(list_serial):
                current_index += 1

                #     os.system('pause')

        except Exception as e:
            if 'list index out of range' in str(e):
                # print("ĐÃ CHẠY HẾT SỐ LUỒNG CẦN CHẠY RỒI!")
                pass


def call_session_work(current_index): 
    try:   
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())   
        print('1')   
        asyncio.run(session_work(current_index,list_key_tinsoft))
        print('2')
    except Exception as e:
        print(f'Lỗi khi call_session_work {e}')


async def get_new_tinsoft(key_tinsoft,ten_thiet_bi, luong_hien_tai):
    global host, port, proxy


    print(key_tinsoft)
    # time.sleep(10000)
    a = f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={key_tinsoft}&location=0'
    # res = requests.get(a)
    res = urlopen(a)
    result = res.read()
    b = (json.loads(result))
    is_success = b['success']
    print(is_success)
    if is_success == True:
        proxy = (b['proxy'])
        print(proxy)
        doi_ip = f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy {proxy}'
        
        print(doi_ip)
        # os.system(doi_ip)
        # return proxy
        host, port = proxy.split(':')
        print(host,port)
        return proxy, host, port
    else:
        next_change = b['next_change']
        for nc in range(next_change+7):
            print(f'{key_tinsoft}\nWait {next_change+6-nc}s for next change', 1.5)
            # print(f'Wait {next_change+6-nc}s to get new proxy')
            time.sleep(1)
        a = f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={key_tinsoft}&location=0'
        # res = requests.get(a)
        res = urlopen(a)
        result = res.read()
        b = (json.loads(result))
        is_success = b['success']
        print(is_success)
        if is_success == True:
            proxy = (b['proxy'])
            print(proxy)
            host, port = proxy.split(':')
            print(host,port)
            
            doi_ip = f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy {proxy}'
            return proxy, host, port
            print(doi_ip)
            os.system(doi_ip)
        else:
            return False

async def open_proxy (proxy, device, host, port):
    try:
        LOI_DANG_KI = False
        device.app_stop_all()
        device.app_clear('com.twitter.android')
        device.app_clear('com.scheler.superproxy')
        
        device.app_start('com.scheler.superproxy', use_monkey= True)
        device.xpath ('//android.widget.Button[@index = "2"]').click_exists(timeout =5)
        device.xpath ('//android.widget.Button[@index = "2"]').click_exists(timeout =1)

        device.xpath ('//android.widget.EditText[@index = "1"]').click_exists(timeout =2)
        device.send_keys(host)
        device.xpath ('//android.widget.EditText[@index = "2"]').click_exists(timeout =2)
        device.send_keys(port)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.Button[@index = "1"]').click_exists(timeout =2)   
        device.xpath ('//android.widget.Button[@content-desc = "Start"]').click_exists(timeout =2)  
        device.xpath ('//android.widget.Button[@content-desc = "Start"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        if device.xpath("//android.widget.Button[contains(@content-desc, 'Stop')]").exists:
            print('Da doi proxy')
        else:
            LOI_DANG_KI = True
            return LOI_DANG_KI
    except Exception as e:
        print(str(e))
        pass





async def change_device(device):
    try:
        device.app_stop_all()
        device.app_start('com.device.emulator.pro', use_monkey= True)

        device.xpath ('//android.widget.TextView[@content-desc = "Random all"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.TextView[@content-desc = "Random all"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.TextView[@content-desc = "Random all"]').click_exists(timeout =1)
    except:
        pass



async def delete_acc (ten_thiet_bi, device):
    global LOI_DANG_KI
    LOI_DANG_KI = False
    

    try:

            # print(str(e))
        
        await asyncio.sleep(1)

        # print('533')

        try:
            os.system(f'adb -s "{ten_thiet_bi}" shell am start -a android.settings.SYNC_SETTINGS')
        except Exception as e:
            print(str(e))
            pass 
        # await os.system(f'adb -s "{ten_thiet_bi}" shell am start -a android.settings.SYNC_SETTINGS')
        # if device(text="Twitter").wait(timeout = 5) != True:
        try:
            device.xpath ('//android.widget.TextView[@text= "Twitter"]').click(timeout =3)
        except:
            # LOI_DANG_KI = True
            return
        # if device.xpath("//android.widget.TextView[contains(@text, 'Twitter')]").exists(timeout = 3):
        #     return 
        # device.xpath ('//android.widget.LinearLayout[@text = "com.android.settings:id/icon_frame"]').click_exists(timeout =2)
        device.xpath ('//android.widget.TextView[@text = "Twitter"]').click_exists(timeout =2)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.TextView[@text = "Twitter"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.Button[@text = "Xóa tài khoản"]').click_exists(timeout =2)
        await asyncio.sleep(1)
        device.xpath ('//android.widget.Button[@text = "Xóa tài khoản"]').click_exists(timeout =1)
        await asyncio.sleep(1)
        try:
            device.xpath ('//android.widget.Button[@resource-id= "android:id/button1"]').click(timeout =3)
        except:
            LOI_DANG_KI = True
            return
        await asyncio.sleep(1)
        # device.xpath ('//android.widget.Button[@resource-id= "android:id/button1"]').click_exists(timeout =1)
    except Exception as e:
        # print('loi...')
        print(str(e))
        pass

    
async def create_acc (device): 
    global TAO_ACC_XIT
    LOI_DANG_KI = False
    TAO_ACC_XIT = False
    try:
        # print('555')
        # device.app_stop_all()
        device.app_clear('com.twitter.android')
        device.app_start('com.twitter.android', use_monkey= True)
        await asyncio.sleep(2)      
        #check xem co bang dieu huong ko
        if device.xpath("//android.widget.Button[contains(@text, 'Tạo tài khoản')]").wait(timeout = 3) or device.xpath("//android.widget.Button[contains(@text, 'TẠO TÀI KHOẢN')]").wait(timeout = 3):
            
            print('1111')

        # if device(text="TẠO TÀI KHOẢN" or "Tạo tài khoản").wait(timeout = 5) == True:
            # device(text="Tạo tài khoản").click(timeout =5, offset = (random.random(), random.random() ))
            device(textMatches="TẠO TÀI KHOẢN").click(timeout =5, offset = (random.random(), random.random() ))
        else:
            # print('2222')
            try:
                await asyncio.sleep(1)
                device(text = "Tôi sẽ tham gia sau").click(timeout =3, offset = (random.random(), random.random() ))
            except:
                pass
            device.xpath ('//*[@content-desc = "Hiển thị bảng điều hướng"]').click(timeout =10)
            device(text="Tạo tài khoản").click(timeout =2, offset = (random.random(), random.random() ))
            device(text="Tạo tài khoản").click(timeout =3, offset = (random.random(), random.random() ))
        device(text="Bỏ qua bây giờ").click(timeout =2, offset = (random.random(), random.random() ))
        await asyncio.sleep(1)
        fake = Faker()
        Ten_nguoi_dung = fake.name()
        device.send_keys(Ten_nguoi_dung)
        device(text="Số điện thoại hoặc địa chỉ email").click(timeout =2, offset = (random.random(), random.random() ))
        try:
            device(text="Sử dụng email").click(timeout =2, offset = (random.random(), random.random()))
        except:
            LOI_DANG_KI = True
            TAO_ACC_XIT  = True
            return LOI_DANG_KI, TAO_ACC_XIT

    except Exception as e:
        print(str(e))
    
        pass


async def get_mail (link_creat,device ):   
    try:
        global email
        get_mail = requests.get(link_creat)
        json_getmail = json.loads(get_mail.text)
        email = json_getmail['mail_get_mail']
        device.send_keys(email)
        print(email)
        return email
    except:
        pass


async def create_acc_2(email, ten_thiet_bi, device): 
    global TAO_ACC_XIT
    try:
        print(ten_thiet_bi)
        
        TAO_ACC_XIT = False      
        LOI_DANG_KI = False
        device(text="Ngày sinh").click(timeout =2, offset = (random.random(), random.random() ))
        #chọn ngày sinh
        os.system(f'adb -s "{ten_thiet_bi}" shell "input touchscreen swipe 288 1818 288 {random.randint(1900, 2400)}"')
        await asyncio.sleep(1)
        #chọn tháng sinh
        os.system(f'adb -s "{ten_thiet_bi}" shell "input touchscreen swipe 528 1818 528 {random.randint(1900, 2500)}"')
        await asyncio.sleep(1)
        #chọn năm sinh
        os.system(f'adb -s "{ten_thiet_bi}" shell "input touchscreen swipe 768 1818 768 {random.randint(6000, 10000)}"')
        await asyncio.sleep(1)
        device(text="Tiếp theo").click( offset = (random.random(), random.random() ))

        #Hoàn tất đăng kí
        check_1 = device(text="Tùy chỉnh trải nghiệm của bạn").wait(timeout=3.0)

        if check_1 == True:
            device(text="Tiếp theo").click( offset = (random.random(), random.random() ))
        else:
            print('Error')

        check_2 = device(text="Tạo tài khoản của bạn").wait(timeout=3.0)
        if check_2 == True:
            device.swipe_ext("up")
            await asyncio.sleep(1)
            device(text="Đăng ký").click( offset = (random.random(), random.random() ))
            # if device(text ="Không thể hoàn tất đăng ký của bạn ngay bây giờ.").wait(timeout=2) or device(text="Chúng tôi cần chắc chắn rằng bạn là người thật.").wait(timeout = 7) == True:
            #     LOI_DANG_KI = True
            #     TAO_ACC_XIT = True
            #     print('xit 11')
            #     return TAO_ACC_XIT
            # else:
                # if device(text="Chúng tôi cần chắc chắn rằng bạn là người thật.").wait(timeout = 5) == True:
                #     print('xịt 1')
                #     TAO_ACC_XIT = True
                #     return TAO_ACC_XIT
                # else:
                #     pass

    
        else:
            print('lỗi 2')
    except Exception as e:
        print(str(e))
        pass



async def get_code (link_creat, device):
    global TAO_ACC_XIT
    TAO_ACC_XIT = False
    
    # print('1212')
    try:
        for i in range(15):
            get_code_mail = requests.get(link_creat)
            json_get_code_1=json.loads(get_code_mail.text)
            json_get_code_2 = json_get_code_1['mail_list'][0]
            code_mail = json_get_code_2['subject'].split(' ')[0]
            if code_mail.isdecimal() == True:
                device.send_keys(code_mail)
                break
            await asyncio.sleep(1)
        # print(code_mail)
        if code_mail.isdecimal() != True:
            # print('ewtga')
            TAO_ACC_XIT = True
            return TAO_ACC_XIT

        return code_mail
    except Exception as e:
        print(str(e))
        pass

    
async def create_acc_3(password, device):
    try:
        TAO_ACC_XIT = False 
        # print('1313')
        device(text="Tiếp theo").click(offset = (random.random(), random.random() ))
        device(text="Mật khẩu").click( offset = (random.random(), random.random() ))
        device.send_keys(password)
        await asyncio.sleep(2)
        device(text="Tiếp theo").click(offset = (random.random(), random.random() ))
        device(text="Bắt đầu").click( offset = (random.random(), random.random() ))
    except:
        pass


    #Check xem bi captcha khong
async def check_bi_khoa(device):
    global TAO_ACC_XIT
    TAO_ACC_XIT = False
    # print('1414')

    if device(text="Chúng tôi cần chắc chắn rằng bạn là người thật.").wait(timeout = 5) == True:
        print('xịt')
        TAO_ACC_XIT = True
        return TAO_ACC_XIT
    #Neu tai khoan bi khoa



async def creat_acc_4(device) :  
    global username
    try:
        device(text="Tiếp tục đến Twitter").click(offset = (random.random(), random.random() ))
        #Up avatar hoac khong
        device(text="Bỏ qua bây giờ").click(offset = (random.random(), random.random() ))
        #bo qua up bio
        try:
            device(text="Bỏ qua bây giờ").click( offset = (random.random(), random.random() ))
        except:
            pass
        # Lay username
        json_username = device.xpath('//android.widget.EditText[@resource-id="com.twitter.android:id/ocf_text_input_edit"]').info
        username = json_username['text']
        # print (username)
        # device.xpath('//android.widget.TextView[@text="Tiếp theo"]').click_exists(timeout =2, offset = (random.random, random.random ))
        # device.xpath('//android.widget.TextView[@text="Tiếp tục"]').click_exists(timeout =2, offset = (random.random, random.random ))
        # device.xpath('//android.widget.Button[@text="Cho phép"]').click_exists(timeout =2, offset = (random.random, random.random ))
        # #Theo doi 1 nguoi hoan tat dang ki
        # device.xpath('//android.widget.Button[@text="THEO DÕI"]').click_exists(timeout =5, offset = (random.random, random.random ))
        # device.xpath('//android.widget.TextView[@text="Kế tiếp"]').click_exists(timeout =5, offset = (random.random, random.random ))
        return username
    except:
        pass


async def Luu_acc (email, password, username):
    with open('acc twitter.txt', 'a+') as f:
        f.write(f'{email}|{password}|{username}\n')

# client = AdbClient(host="127.0.0.1", port=5037)
# devices = client.devices()
# for device in devices:
#     print(device.serial)






async def set_IP(proxy, ten_thiet_bi):
    # print(f'day la{proxy}')

    # adb shell settings put global http_proxy <ip>:<port>
    doi_ip = f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy {proxy}'
    # print(doi_ip)
    os.system(doi_ip)

    print(proxy)




async def session_work(current_index, list_key_tinsoft):
    global  list_used ,list_wallet, device1, list_serial, TAO_ACC_XIT, LOI_DANG_KI
    try:

        ten_thiet_bi = list_serial[luong_hien_tai-1]

        device =  Device(ten_thiet_bi)

        # device.app_install('https://d-14.winudf.com/b/APK/Y29tLnNjaGVsZXIuc3VwZXJwcm94eV81MDlfYzA1YjBhMzI?_fn=U3VwZXIgUHJveHlfMi4wLjdfQXBrcHVyZS5hcGs&_p=Y29tLnNjaGVsZXIuc3VwZXJwcm94eQ%3D%3D&download_id=otr_1224504042154037&is_hot=false&k=9a15f4f08b46aafc12d5f5bd139b2c6e648952bd')
        # os.system(f'adb -s "{ten_thiet_bi}" shell settings put global http_proxy :0')

        key_tinsoft = ''
        key_tinsoft = list_key_tinsoft[luong_hien_tai-1]




        for i in range(1000000):
      
            TAO_ACC_XIT = False
            LOI_DANG_KI =False
           # session_id = random.randint(1000000000000,999999999999999)
            #link_creat=  f'https://10minutemail.net/address.api.php?sessionid={session_id}'
            # print('11')
           # await change_device(device)
            # time.sleep(1000)
            # await get_new_tinsoft(key_tinsoft, ten_thiet_bi, luong_hien_tai)

            # # global key_tinsoft
            # proxy = ''
            # host = '188.74.183.10'
            # port = '8279'
            await open_proxy(proxy, device, host, port)
            if LOI_DANG_KI == True:
                continue

            time.sleep(1)

            # await delete_acc (ten_thiet_bi, device)
            if LOI_DANG_KI == True:
                continue
            await create_acc (device)
            await get_mail (link_creat,device)
            await create_acc_2(email, ten_thiet_bi, device)
            # print(f'1{TAO_ACC_XIT}')
            if TAO_ACC_XIT == True:
                continue
            await get_code (link_creat, device)
            # print(f'2{TAO_ACC_XIT}')
            if TAO_ACC_XIT == True:
                continue
            await check_bi_khoa(device)
            # print(f'3{TAO_ACC_XIT}')
            if TAO_ACC_XIT == True:
                continue
            await create_acc_3 (password, device)
            
            await check_bi_khoa(device)
            if TAO_ACC_XIT == True:
                continue
            
            await Luu_acc (email, password, username)
            await creat_acc_4(device)
    except Exception as e:
        print(e)
    print('1')









asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  
asyncio.run(chia_luong()) 