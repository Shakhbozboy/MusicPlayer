from tkinter import *
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import pygame
import os
from MusicPlayer import*








root = Tk()
player = MusicPlayer(root)
root.iconbitmap('C://Users//admin//PycharmProjects//musicProject//venv//resource//icon.ico')

root.mainloop()

