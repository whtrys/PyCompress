# coding=utf-8
"""
Project:PyCompress
File:set.py
Author:whtry陈
Time:2021-08-21 11:15
程序的设置界面，本质是对setting.json的修改
"""
import json
import os
import tkinter.filedialog as tkfd
from tkinter import *

with open('setting.json', 'r', encoding='utf-8') as f:
    setting = json.load(f)
    f.close()

with open(setting["language"], 'r', encoding='utf-8') as f:
    language = json.load(f)
    f.close()


def restart_program():
    """
    重启程序
    :return: 无
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


def write_json(name, body):
    print(type(setting), name, body)
    setting[name] = body
    with open('{}\\setting.json'.format(os.getcwd()), 'w') as write_f:
        json.dump(setting, write_f, indent=4, ensure_ascii=False)


def choose_picture():
    global filepath
    filepath = tkfd.askopenfilename(filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('gif', '*.gif')])


def setting(bg):
    setting_window = Toplevel()
    setting_window.title(language["设置"])
    setting_window.geometry('880x500')
    Button(setting_window, text=language["主页背景图片 798x91\n点我更改"], command=choose_picture, height=4).grid(row=1, column=1)

    Label(setting_window, height=83, image=bg).grid(row=1, column=2)  # 背景图
