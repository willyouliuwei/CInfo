# -*- coding: utf-8 -*-
# @time :
# @author : willyou
# @email : 867607248@qq.com
# @file : .py
# @software: pycharm
import logging
import telnetlib
import time
import datetime
import os





# Telnet登录方法，并返回结果成功或者失败
def login_telnet_func(tn, switch_host, switch_username, switch_password):
    tn.read_until(b'login:', timeout=10)
    tn.write(switch_username.encode('utf-8') + b'\r')
    tn.read_until(b'Password', timeout=10)
    tn.write(switch_password.encode('utf-8') + b'\r')
    time.sleep(1)
    switch_info = tn.read_very_eager().decode('utf-8')
    if '#' in switch_info:
        print(f'telnet {switch_host} successful!\n' + f'{switch_info}')
        return True
    else:
        print(f'telnet{switch_host} failed!\n'+f'{switch_info}' )
        return False


# 发送和处理接收到的信息并返回处理结果
def collect_info(tn, show_command):
    tn.write(b'terminal length 0\r') # 修改输出窗口，防止--More--
    switch_info = tn.read_until(b'#', timeout=10)
    comeleteInfo = switch_info.replace(b'\r\n', b'\r')
    print(f'{switch_info.decode("utf-8")}\n已修改输出窗口')
    time.sleep(2)
    for i in show_command:
        tn.write(f'{i}\r'.encode('utf-8'))
        switch_info = tn.read_until(b'#', timeout=10)
        if b'\r\r\n' in switch_info:
            switch_info = switch_info.replace(b'\r\r\n', b'\r\n')
            print(switch_info.decode('utf-8'))
            switch_info = switch_info.replace(b'\r\n', b'\r')
            comeleteInfo = comeleteInfo + switch_info
        else:
            switch_info = switch_info.decode('utf-8').splitlines()
            # switch_info = [i for i in switch_info if i != '']#删除多余空行
            for line in switch_info:
                comeleteInfo = comeleteInfo + f"{line}\r".encode('utf-8')
                print(line)
    tn.write(b'terminal length 25\r') # 输出窗口改回成默认大小
    print(tn.read_until(b'#', timeout=10).decode('utf-8'))
    return comeleteInfo


# 将输出信息保存到TXT文本，保存到指定目录下或默认桌面
def output_info(infoFileAddress, switchHost, message):
    nowTime = datetime.datetime.now()
    if os.path.exists(infoFileAddress):
        path = fr'{infoFileAddress}' + r'/配置信息收集' + fr'{nowTime.strftime("%Y-%m-%d")}'
        os.makedirs(fr'{path}', exist_ok=True)
        fileName = fr'{switchHost}' + fr'{nowTime.strftime("%Y-%m-%d %H-%M-%S")}' + r'.txt'
        file = open(fr'{path}' + fr'\{fileName}', 'w+', encoding='utf-8')
        file.write(message.decode('utf-8'))
        file.close()
    else:
        print('当前路径不存在，已保存配置到桌面')
        deskTopPath = os.path.join(os.path.expanduser("~"), 'Desktop')
        path = fr'{deskTopPath}' + r'/配置信息收集 ' + fr'{nowTime.strftime("%Y-%m-%d")}'
        fileName = fr'{switchHost} ' + fr'{nowTime.strftime("%Y-%m-%d %H时%M分%S秒")}' + r'.txt'
        os.makedirs(fr'{path}', exist_ok=True)
        file = open(fr'{path}' + fr'\{fileName}', 'w+', encoding='utf-8')
        file.write(message.decode('utf-8'))
        file.close()



if __name__ == '__main__':
    show_command = ['show version', 'show vendor', 'show running-config',
                    'show logging buffer level warning']
    host = ['192.168.2.100', '192.168.2.101', '192.168.2.102']
    username = 'admin'
    password = 'password'
    for i in host:
        tn1 = telnetlib.Telnet(i, timeout=10)
        if login_telnet_func(tn1, i, username, password):
            info = collect_info(tn1, show_command)
            output_info(r'C:\Users\willyou\Deskto', i, info)
        else:
            print('登录失败')
