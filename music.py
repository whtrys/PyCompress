# coding=utf-8
"""
Project:PyCompress
File:music.py
Author:whtry陈
Time:2021-03-27 09:47
"""
import winsound
import json

with open('setting.json', 'r', encoding='utf-8') as f:
    music = json.load(f)

music_path = music["music"]


def about_me_music():
    return winsound.PlaySound(music_path, winsound.SND_FILENAME | winsound.SND_ASYNC)


def stop_play_music(item):
    winsound.PlaySound(item, winsound.SND_PURGE)
