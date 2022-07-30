import os
import zipfile


class Compress:
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
                # 传回重新编码的文件名给原文件名
                temp_name = new_name

                if os.path.isdir(temp_name):
                    # 对子文件夹进行递归调用
                    self.recode(temp_name)
                    # 记得返回上级目录
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
        print(save_dir)

        # 判断是否存在同名文件夹
        if os.path.exists(save_dir):
            if input("-->检测到与zip文件文件名重复的文件夹，是否覆盖？(Y/N)") == "N":
                save_dir = f'{save_dir}(2)'
                os.mkdir(save_dir)
            else:
                print("-->将会覆盖")
        else:
            os.mkdir(save_dir)

        for file in self.zipMe.namelist():
            self.zipMe.extract(file, save_dir)

        self.recode(save_dir)


print("zip解压乱码替代解压工具 命令行版本 v0.0.1")
print("author:whtrys github:https://github.com/whtrys/PyCompress")


def checkPath(path, types):
    """
    判断释放路径是否存在
    """
    if types == 0:
        if not os.path.isfile(path):
            userIn = input("Error:该文件不存在，请重新输入：")
            user.zipFilePath = userIn
            checkPath(userIn, 0)

    elif types == 1:
        if not os.path.exists(path):
            userIn = input("Error:该路径不存在，请重新输入：")
            user.savePath = userIn
            checkPath(userIn, 1)


while True:
    user = Compress()

    user.zipFilePath = input("-->请输入zip文件路径（请不要添加双引号）：")
    checkPath(user.zipFilePath, 0)
    user.savePath = input("-->请输入zip文件释放路径（请不要添加双引号）：")
    checkPath(user.savePath, 1)

    try:
        user.get_zip()

    except Exception as err:
        print("Error:源zip文件损坏！无法解压缩。")

    else:
        print("-->包含以下文件/文件夹\n")
        for i in user.ConcludeFileNameList:
            print(i)

        choose = input("\n-->请问是否解压？(Y/N)")
        if choose == "Y":
            user.save_zip()
            print("-->解压完成！")
        else:
            print("-->已取消")
