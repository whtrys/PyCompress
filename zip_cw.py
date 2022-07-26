# coding=utf-8
"""
Project:PyCompress
File:zip_cw.py
Author:whtry陈
Time:2021-03-27 09:47
解压zip的带gui版本，使用tkinter库作为gui库
"""
import tkinter.messagebox as tkms
import zipfile
import os
import public


class Unzip:
    """
    解压zip
    """

    def __init__(self):
        self.zipFilePath = ''  # zip文件的位置
        self.savePath = ''  # zip文件释放的目录
        self.ConcludeFileNameList = []  # zip文件包含的所有文件/文件名
        self.zipMe = None  # zipfile模块中ZipFile对象的保存

    def recode(self, dir_names):
        """
        将乱码进行还原
        :param dir_names:解压保存的目录
        """
        os.chdir(dir_names)

        for temp_name in os.listdir('.'):
            try:
                new_name = temp_name.encode('cp437')
                new_name = new_name.decode("gbk")
                os.rename(temp_name, new_name)
                temp_name = new_name

                if os.path.isdir(temp_name):
                    # 对子文件夹进行递归调用
                    self.recode(temp_name)
                    os.chdir('..')

            except:
                pass

    def get_zip(self):
        """
        获取zip压缩包
        """
        self.zipMe = zipfile.ZipFile(self.zipFilePath, 'r')
        for name in self.zipMe.namelist():
            self.ConcludeFileNameList.append(name.encode('cp437').decode("gbk"))

    def save_zip(self):
        """
        释放压缩包
        """
        folderName = self.zipFilePath.replace('\\', '/').split("/")[-1].split(".")[0]
        save_dir = f'{self.savePath}/{folderName}'

        # 判断是否存在同名文件夹
        if os.path.exists(save_dir):
            result = tkms.askretrycancel("警告", "检测到与zip文件文件名重复的文件夹，是否覆盖？")
            if not result:
                save_dir = f'{save_dir}(2)'
                tkms.showinfo("提示", f"将会保存到 {save_dir} 文件夹")
                os.mkdir(save_dir)
            elif result:
                tkms.showinfo("提示", "将会覆盖")
        else:
            os.mkdir(save_dir)

        for file in self.zipMe.namelist():
            self.zipMe.extract(file, save_dir)

        self.recode(save_dir)


class Zip:
    def __init__(self):
        self.become_compress_dir = None
        self.save_dir = None

    def become_compress(self):
        """
        将文件夹压缩
        :return: 无
        """
        lst2 = []
        for i in public.walk(self.become_compress_dir):
            lst2.append(i.replace('\\', '/'))

            try:
                zip_name = self.become_compress_dir.split('/')[-1] + '.zip'
                print("不存在相同文件名的文件")
                z = zipfile.ZipFile(self.save_dir + '/' + zip_name, 'w', zipfile.ZIP_DEFLATED)
                for j in lst2:
                    z.write(filename=j)
                z.close()
                tkms.showinfo("提示", "压缩完成")
            except:
                tkms.showerror("zip压缩模块错误", "错位原因未知")
