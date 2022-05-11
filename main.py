# -*- coding: utf-8 -*-
# @time :
# @author : willyou
# @email : 867607248@qq.com
# @file : .py
# @software: pycharm

import telnetlib
import time

host = '192.168.2.100'
username = 'admin'
password = 'password'


def login_telnet_func(tn, switch_host, switch_username, switch_password):
    tn.read_until(b'login:', timeout=10)
    tn.write(switch_username.encode('utf-8') + b'\n')
    tn.read_until(b'Password', timeout=10)
    tn.write(switch_password.encode('utf-8') + b'\n')
    time.sleep(1)
    switch_info = tn.read_very_eager().decode('utf-8')
    print(switch_info)
    if '#' in switch_info:
        print(f'{switch_info}\n' + f'telnet {switch_host} successful!\n')
        return True
    else:
        return False

def collect_info(tn, show_command):
    tn.write(b'')
    tn.write(f'{show_command}\n'.encode('utf-8'))
    time.sleep(1)
    switch_info = tn.read_very_eager().decode('utf-8')

    print(switch_info)


if __name__ == '__main__':
    tn1 = telnetlib.Telnet(host, timeout=10)
    if login_telnet_func(tn1, host, username, password):
        collect_info(tn1, 'show version')
    else:
        print('登录失败')
