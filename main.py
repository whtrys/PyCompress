# coding=utf-8
"""
Project:PyCompress
File:main.py
Author:whtry陈
Time:2021-03-27 09:47
"""
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import os
import music
import zip_cw
import sys
import json

with open('setting.json', 'r', encoding='utf-8') as f:
    setting = json.load(f)

b_compress_item = setting["auto_save_item"]
support_file = [('zip文件', '*.zip'), ('rar文件', '*.rar')]  # ,('tar文件','*.tar'),('rar文件','*.rar')]
compress_item = ''
compress_files = ''
file_path_name = ''

with open(setting["language"], 'r', encoding='utf-8') as f:
    language = json.load(f)


def about_us():
    """
    关于我们
    :return: 无
    """
    # 背景音乐
    pm = music.about_me_music()
    # 主界面
    au = tk.Toplevel()
    au.geometry('480x270')
    au.resizable(0, 0)
    au.title(language['about_us'])
    tk.Label(au, text="PyCompress\n"
                      "一个简洁的解压&压缩软件\n"
                      "目前支持：zip\n\n"
                      "联系方式：\n"
                      "bilibili：whtry陈\n"
                      "邮件：whtrys@whtrys.space\n"
                      "博客：https://blog.whtrys.space\n(一定要用https！)\n\n"
                      "copyright  whtrys(whtry陈)\n",
             font=('微软雅黑', 13)).pack()

    def on_closing():
        music.stop_play_music(pm)
        au.destroy()

    au.protocol("WM_DELETE_WINDOW", on_closing)


def restart_program():
    """
    重启程序
    :return:
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


def decided(bt):
    """
    打开并判断打开的文件类型
    :param bt: 保存按键
    :return:
    """
    global compress_files
    global file_path_name
    global compress_item

    # 重启程序以清空缓存的文件
    if compress_item != '':
        restart_program()

    file_list.delete(0, tk.END)
    file_name = tkfd.askopenfilename(filetypes=support_file)

    file_name_sp = file_name.split('/')
    file_name_sp = file_name_sp[-1]
    choice = file_name_sp.split('.')
    file_path_name = choice[0]
    choice = choice[-1]
    compress_item = choice

    if choice == '':
        pass
    elif choice == 'zip':
        bt['state'] = 'normal'
        compress_files = zip_cw.get_zip(file_name, file_list)


def save_compress():
    if compress_item == 'zip':
        zip_cw.save_zip(save_zip_bt, compress_files, file_path_name)
        tkms.showinfo(language['tip'], "已解压")


def become_compress():
    if b_compress_item == 'zip':
        zip_cw.become_compress()
    elif b_compress_item == 'rar':
        pass


# ——————————————————————GUI——————————————————————
home = tk.Tk()
home.geometry('800x600')
home.resizable(0, 0)
home.title(language["home_title"])
ico_path = '{}\\img\\ico.ico'.format(os.getcwd())
home.iconbitmap(ico_path)

# 页头
# 图
# 创建一个图片管理类
bg_path = '{}\\img\\bg.jpg'.format(os.getcwd())
bg = ImageTk.PhotoImage(image=Image.open(bg_path))  # file：t图片路径
# 按钮
tk.Label(home, height=83, image=bg).pack(side='top', fill='x')  # 背景图

save_zip_bt = tk.Button(home, text="选择解压\n保存\n的位置", font=('微软雅黑', 8),
                        height=4, width=10, command=save_compress, state='disabled')
save_zip_bt.place(x=182, y=6)

tk.Button(home, text="打开\n压缩包", font=('微软雅黑', 8), height=4,
          width=10, command=lambda: decided(save_zip_bt)).place(x=2, y=6)
tk.Button(home, text="压缩\n文件夹", font=('微软雅黑', 8),
          height=4, width=10, command=become_compress).place(x=92, y=6)

tk.Button(home, text="关于\n我们", font=('微软雅黑', 8),
          height=4, width=10, command=about_us).place(x=717, y=6)

# 中间
tk.Label(home, text=language['file']).pack(anchor='w', pady=2)
file_list = tk.Listbox(home, font=("微软雅黑", 11))
file_list.pack(fill='both', expand='yes', anchor='center')

# 页脚 tip-小贴士
tk.Label(home, text=language["under_tip"], font=('微软雅黑', 10),
         bg='white').pack(side='bottom', fill='x')

tk.mainloop()
