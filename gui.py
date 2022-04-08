# coding=utf-8
"""
Project:PyCompress
File:gui.py
Author:whtry陈
Time:2021-03-27 09:48
程序的GUI文件，方便适配
"""
import json
import os
import sys
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms

from PIL import Image, ImageTk

import zip_cw

with open('setting.json', 'r', encoding='utf-8') as f:
    setting = json.load(f)
    f.close()

b_compress_item = setting["auto_save_item"]
support_file = [('zip文件', '*.zip')]
support_file_pure = ['zip', 'rar']
compress_item = ''
compress_files = ''
file_path_name = ''

with open(setting["language"], 'r', encoding='utf-8') as f:
    language = json.load(f)
    f.close()


def about_us():
    """
    关于我们
    :return: 无
    """
    # 主界面
    au = tk.Toplevel()
    au.geometry('480x270')
    au.resizable(None, None)
    au.title(language['关于我们'])
    tk.Label(au, text=language["关于我们_全"], font=('微软雅黑', 13)).pack()


def restart_program():
    """
    重启程序
    :return: 无
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


def decided(bt, filepath):
    """
    打开并判断打开的文件类型
    :param bt: 保存按键
    :param filepath: 文件路径
    :return:
    """
    global compress_files
    global file_path_name
    global compress_item

    # 重启程序以清空缓存的文件
    if compress_item != '':
        restart_program()

    file_list.delete(0, tk.END)
    if filepath == "None":
        filepath = tkfd.askopenfilename(filetypes=support_file)

    file_name_sp = filepath.split('\\')
    file_name_sp = file_name_sp[-1]
    choice = file_name_sp.split('.')
    file_path_name = choice[0]
    choice = choice[-1]
    compress_item = choice

    # TODO : 还有一堆别的格式要接入。。。啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊！
    if choice == '':
        pass
    elif choice == 'zip':
        bt['state'] = 'normal'
        compress_files = zip_cw.get_zip(filepath, file_list)


def save_compress():
    """
    保存解压后的压缩文件
    """
    if compress_item == 'zip':
        zip_cw.save_zip(save_compress_bt, compress_files, file_path_name)
    tkms.showinfo(language['提示'], "已解压")


def become_compress(file=None):
    """
    压缩文件夹
    """

    if b_compress_item == 'zip':
        zip_cw.become_compress(file)


# ——————————————————————GUI——————————————————————
home = tk.Tk()
home.geometry('800x600')
home.resizable(None, None)
home.title(language["主页标题"])
# 页头
# 图
# 创建一个图片管理类
bg_path = './img/bg.jpg'
bg = ImageTk.PhotoImage(image=Image.open(bg_path))
# 按钮
tk.Label(home, height=83, image=bg).pack(side='top', fill='x')  # 背景图

save_compress_bt = tk.Button(home, text=language["选择解压\n保存\n的位置"], font=('微软雅黑', 8),
                             height=4, width=10, command=save_compress, state='disabled')
save_compress_bt.place(x=182, y=6)

tk.Button(home, text=language["打开\n压缩包"], font=('微软雅黑', 8), height=4,
          width=10, command=lambda: decided(save_compress_bt, "None")).place(x=2, y=6)
tk.Button(home, text=language["压缩\n文件夹"], font=('微软雅黑', 8),
          height=4, width=10, command=become_compress).place(x=92, y=6)

tk.Button(home, text=language["关于我们"], font=('微软雅黑', 8),
          height=4, width=10, command=about_us).place(x=717, y=6)

# 中间
tk.Label(home, text=language['文件：']).pack(anchor='w', pady=2)
file_list = tk.Listbox(home, font=("微软雅黑", 11))
file_list.pack(fill='both', expand=1, anchor='center')

# 页脚 tip-小贴士
tk.Label(home, text=language["底部提示"], font=('微软雅黑', 10),
         bg='white').pack(side='bottom', fill='x')

tk.mainloop()
