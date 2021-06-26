# coding=utf-8
"""
Project:PyCompress
File:rar_cw.py
Author:whtry陈
Time:2021-03-27 09:47
解压rar，
注意：因为rar压缩算法不公开，所以使用了原生包，根目录下的UnRar.exe请勿删除
"""
import rarfile
import tkinter.messagebox as tkms
import tkinter.filedialog as tkfd
import os


def get_rar(filepath):
    """
    获取rar压缩包
    :param filepath: 打开的压缩包路径
    :return:
    """
    question = tkms.askyesno("提示", "rar不支持查看压缩文件内容，仅支持直接解压，是否继续")
    if question:
        rf = rarfile.RarFile(filepath)
        save_dir = tkfd.askdirectory()
        if save_dir == '':
            tkms.showerror("错误", "请选择保存的路径")
        else:
            file_name = filepath.split("\\")[-1].split(".")[0]
            save_dir = '{}/{}'.format(save_dir, file_name)
            # 判断是否存在同名文件夹
            if os.path.exists(save_dir):
                tkms.showerror("错误", "存在与该压缩包重名的文件夹")
                return
            else:
                os.mkdir(save_dir)
            try:
                rf.extractall(save_dir)
            except:
                tkms.showerror("错误","解压行为被打断\n压缩包中中可能存在不安全文件\n请确保安全软件没有拦截")
            else:
                tkms.showinfo("提示", "解压成功")
    else:
        tkms.showinfo("提示", "已取消")
