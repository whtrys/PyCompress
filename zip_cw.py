# coding=utf-8
"""
Project:PyCompress
File:zip_cw.py
Author:whtry陈
Time:2021-03-27 09:47
解压zip
"""
from random import randint
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import zipfile
import os


def recode(dir_names):
    """
    将乱码进行还原
    :param dir_names:解压保存的目录
    """
    os.chdir(dir_names)

    for temp_name in os.listdir('.'):
        try:
            # 使用cp437对文件名进行解码还原
            new_name = temp_name.encode('cp437')
            # win下一般使用的是gbk编码
            new_name = new_name.decode("gbk")
            # 对乱码的文件名及文件夹名进行重命名
            os.rename(temp_name, new_name)
            # 传回重新编码的文件名给原文件名
            temp_name = new_name
        except:
            pass

    if os.path.isdir(temp_name):
        # 对子文件夹进行递归调用
        recode(temp_name)
        # 记得返回上级目录
        os.chdir('..')


def get_zip(filename, file_list):
    """
    获取zip压缩包
    :param filename: 打开的压缩包路径
    :param file_list: list窗口
    :return: zip库的zipfile
    """
    print("zip类型")
    zip_files = zipfile.ZipFile(filename, 'r')
    for i in zip_files.namelist():
        file_list.insert(0, i.encode('cp437').decode("gbk"))

    return zip_files


def save_zip(save_zip_bt, zip_files, just_file_name):
    """
    保存压缩包
    :param save_zip_bt:保存按键
    :param zip_files: list窗口
    :param just_file_name: 单纯的文件夹名
    :return:
    """
    if zip_files == '':
        save_zip_bt['state'] = 'disabled'
        tkms.showerror('错误', '请选择要解压的压缩包')
    else:
        save_dir = tkfd.askdirectory()
        if save_dir == '':
            pass
        else:
            save_dir = '{}\\{}'.format(save_dir, just_file_name)
            # 判断是否存在同名文件夹
            if os.path.exists(save_dir):
                tkms.showerror("错误", "存在与该压缩包重名的文件夹")
                return
            else:
                os.mkdir(save_dir)

            for file in zip_files.namelist():
                zip_files.extract(file, save_dir)
            recode(save_dir)


def become_compress(become_compress_dir):
    """
    将文件夹压缩
    :return: 无
    """
    if become_compress_dir is None:
        become_compress_dir = tkfd.askdirectory(title='选择要压缩的文件夹')
    if become_compress_dir == '':
        tkms.showerror("错误", "请选择保存的路径")
    else:
        def walk(path):
            lst = []
            if not os.path.exists(path):
                return -1
            for root, dirs, names in os.walk(path):
                for filename in names:
                    lst.append(os.path.join(root, filename))
            return lst

        lst2 = []
        for i in walk(become_compress_dir):
            lst2.append(i.replace('\\', '/'))

        save_dir = tkfd.askdirectory(title='选择保存的目录')
        if save_dir == '':
            tkms.showerror("错误", "请选择保存的路径")
        else:
            try:
                zip_name = become_compress_dir.split('/')[-1] + '.zip'
                print("不存在相同文件名的文件")
                z = zipfile.ZipFile(save_dir + '/' + zip_name, 'w', zipfile.ZIP_DEFLATED)
                for i in lst2:
                    z.write(filename=i)
                z.close()
                tkms.showinfo("提示", "压缩完成")
            except:
                tkms.showerror("zip压缩模块错误", "错位原因未知")
