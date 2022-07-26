# coding=utf-8
"""
Project:PyCompress
File:gui.py
Author:whtry陈
Time:2021-03-27 09:48
程序的GUI文件，方便适配
"""
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import os
import music
import zip_cw
import json
from windnd import hook_dropfiles
import rar_cw
import set

with open('setting.json', 'r', encoding='utf-8') as f:
    setting = json.load(f)
    f.close()

defaultCompress = setting["auto_save_item"]
support_file = [('zip文件', '*.zip'), ('rar文件', '*.rar')]  # ,('tar文件','*.tar')]
support_file_pure = ['zip', 'rar']

with open(setting["language"], 'r', encoding='utf-8') as f:
    language = json.load(f)
    f.close()


def about_us():
    """
    关于我们
    :return: 无
    """
    # 背景音乐
    if setting["music_run"] == "Yes":
        pm = music.about_me_music()
    # 主界面
    au = tk.Toplevel()
    au.geometry('480x270')
    au.resizable(None, None)
    au.title(language['关于我们'])
    tk.Label(au, text=language["关于我们_全"], font=('微软雅黑', 13)).pack()

    # 一旦关闭窗口，就关闭音乐
    def on_closing():
        music.stop_play_music(pm)
        au.destroy()

    if setting["music_run"] == "Yes":
        au.protocol("WM_DELETE_WINDOW", on_closing)


def dnd(file):
    """
    文件拖拽支持
    :param file: 拖进来的文件或文件夹
    """
    files = b'114514\n'.join(file).decode("gbk")

    file_list = files.split("114514\n")
    if len(file_list) > 1:
        tkms.showerror(language["错误"], language["请一次性拖拽一个文件"])
    else:
        for i in file_list:
            if not os.path.isfile(i):
                usr.zipDir = i.replace('\\', '/')
                usr.become_zip()  # 替换路径中的反斜杠（win这反人类的路径符号。。。）
            elif i.split(".")[-1] not in support_file_pure:
                tkms.showerror(language["错误"], language["错误！我们不支持这些格式！"])
            else:
                usr.decide(save_compress_bt, i)


class CompressFunctions:
    def __init__(self):
        self.zipFunction = None
        self.zipFilePath = None
        self.compressItem = None
        self.zipDir = None

    def decide(self, filepath=None):
        """
        打开并判断打开的文件类型
        :param filepath: 文件路径
        :return:
        """
        print("decide")
        file_list.delete(0, tk.END)

        if filepath is None:
            self.zipFilePath = tkfd.askopenfilename(filetypes=support_file)
            if self.zipFilePath == '':
                return
        else:
            self.zipFilePath = filepath

        file_name_sp = self.zipFilePath.split('\\')[-1]
        choice = file_name_sp.split('.')
        choice = choice[-1]

        if choice == 'zip':
            save_compress_bt.config(state=tk.NORMAL)
            self.compressItem = "zip"
            self.zipFunction = zip_cw.Unzip()
            self.zipFunction.zipFilePath = self.zipFilePath
            self.zipFunction.get_zip()
            for i in self.zipFunction.ConcludeFileNameList:
                file_list.insert(0, i)

        elif choice == 'rar':
            save_compress_bt.config(state=tk.NORMAL)
            compress_files = rar_cw.get_rar(filepath)

    def save_zip(self):
        """
        保存解压后的压缩文件
        """
        if self.compressItem == 'zip':
            save_compress_bt.config(state=tk.DISABLED)
            self.zipFunction.save_zip()

        tkms.showinfo(language['提示'], "已解压")

    def become_zip(self):
        """
        压缩文件夹
        """
        if self.zipDir is None:
            self.zipDir = tkfd.askdirectory(title='选择要压缩的文件夹')
        saveDir = tkfd.askdirectory(title='选择压缩文件保存的路径')

        if self.zipDir == '' or saveDir == '':
            return
        else:
            if defaultCompress == 'zip':
                self.zipFunction = zip_cw.Zip()
                self.zipFunction.become_compress()


usr = CompressFunctions()

# ——————————————————————GUI——————————————————————
home = tk.Tk()
home.geometry('800x600')
home.resizable(None, None)
home.title(language["主页标题"])
ico_path = '{}\\img\\ico.ico'.format(os.getcwd())
home.iconbitmap(ico_path)

# 检测拖拽
hook_dropfiles(home, func=dnd)

# 页头
# 图
# 创建一个图片管理类
bg_path = '{}\\img\\bg.jpg'.format(os.getcwd())
bg = ImageTk.PhotoImage(image=Image.open(bg_path))
# 按钮
tk.Label(home, height=83, image=bg).pack(side='top', fill='x')  # 背景图

save_compress_bt = tk.Button(home, text=language["选择解压\n保存\n的位置"], font=('微软雅黑', 8),
                             height=4, width=10, command=usr.save_zip, state=tk.DISABLED)
save_compress_bt.place(x=182, y=6)

tk.Button(home, text=language["打开\n压缩包"], font=('微软雅黑', 8), height=4,
          width=10, command=usr.decide).place(x=2, y=6)
tk.Button(home, text=language["压缩\n文件夹"], font=('微软雅黑', 8),
          height=4, width=10, command=usr.become_zip).place(x=92, y=6)

tk.Button(home, text=language["设置"], font=('微软雅黑', 8),
          height=4, width=10, command=lambda: set.setting(bg)).place(x=182, y=6)

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
