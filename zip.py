import os
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkms
import zipfile


class Zip(object):
    def __init__(self, path):
        self.path = path

