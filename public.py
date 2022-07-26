import os


def walk(path):
    lst = []
    if not os.path.exists(path):
        return -1
    for root, dirs, names in os.walk(path):
        for filename in names:
            lst.append(os.path.join(root, filename))
    return lst
