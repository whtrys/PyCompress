import os
import tarfile
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import public


def become_compress(become_compress_dir):
    """
    将文件夹压缩
    :become_compress_dir: 压缩的路径
    :return: 无
    """
    if become_compress_dir is None:
        become_compress_dir = tkfd.askdirectory(title='选择要压缩的文件夹')
    if become_compress_dir == '':
        tkms.showerror("错误", "请选择保存的路径")
    else:
        lst2 = []
        for i in public.walk(become_compress_dir):
            lst2.append(i.replace('\\', '/'))

        save_dir = tkfd.askdirectory(title='选择保存的目录')
        if save_dir == '':
            tkms.showerror("错误", "请选择保存的路径")
        else:
            try:
                tar_filename = become_compress_dir.split('/')[-1]
                with tarfile.open(tar_filename, "w:gz") as tar:
                    tar.add(save_dir, arcname=os.path.basename(save_dir))
            except:
                tkms.showerror("tar压缩模块错误", "错位原因未知")


become_compress()
