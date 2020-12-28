import os, fnmatch
from tkinter import *


def find(pattern="*.mp3", path="E://2"):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result



