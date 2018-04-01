#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.3.9
"""
import os

import re

from DataBase import insert_email

def get_fname():
    current_dir = (os.getcwd() + '\email_number')
    print(current_dir)
    fb_list = os.listdir(current_dir)
    print(fb_list)
    file_list = []

    for name in fb_list:
        if os.path.splitext(name)[1] == '.txt' or \
            os.path.splitext(name)[1] == '.xls' or \
            os.path.splitext (name)[1] == '.xlsX':
            file_list.append(name)

    return file_list



def open_file():
    file_list = get_fname()
    for file in file_list:
        print(file)
        with open('.\\email_number\\' + file, 'r+',  encoding='gbk',) as fb:
            try:
                lines = fb.readlines()
                for line in lines:
                    print(line)
                    line = line.replace(' ', '')
                    if '@' in line:
                        insert_email(re.search(r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)', line).string)
                    else:
                        insert_email(re.search(r'[1-9][0-9]{4,}', line).string + '@qq.com')

            except Exception as e:
                print("Error {}".format(e))

if __name__ == '__main__':
    open_file()