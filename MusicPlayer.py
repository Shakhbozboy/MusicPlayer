from tkinter import Tk, Listbox, MULTIPLE, END, Button
from tkinter import *
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
import pygame
import os
from State import *
from tkinter.filedialog import askdirectory
#from tkinter.ttk import *


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("MusicPlayer")
        # Window Geometry
        self.root.geometry("1000x700+200+200")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        self.status.set("not started")
        self.i = 0
        self.filePath = 'E://2'
        self.scale_var = IntVar()
        self.scale_var.set(60)
        self.current = 0
        self.colled = True

        my_menu = Menu(root)
        root.config(menu=my_menu)
        add_song = Menu(my_menu, font=("times new roman", 15, "bold"), bg="grey",
                                 fg="white", bd=5, relief=GROOVE)
        my_menu.add_cascade(label="Add song", menu=add_song)
        add_song.add_command(label="Select file", command=self.findPath)


        trackframe = LabelFrame(self.root, text="Song Track", font=("times new roman", 15, "bold"), bg="Navyblue",
                                fg="white", bd=5, relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=600)
        # Inserting Song Track Label
        songtrack = Label(trackframe, textvariable=self.track, width=20, font=("times new roman", 24, "bold"),
                          bg="Orange", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Status Label
        trackstatus = Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="orange",
                            fg="gold").grid(row=0, column=1, padx=10, pady=5)

        self.timeVar = StringVar()
        self.timeVar.set("0:0")
        self.timeLabel = Label(root, textvariable=self.timeVar).place(x=10, y=480)
        #self.progress = Scale(root, command=self.move, orient=HORIZONTAL, activebackground="blue", bd=10, fg="navyblue", bg="pink").place(x=10, y=500, width=580, height=10)
        self.slider_value = DoubleVar()
        self.slider_value.set(0)
        self.slider = Scale(root, orient=HORIZONTAL, length=500, sliderlength=10, label=self.timeLabel, showvalue=0, resolution=1, variable=self.slider_value,
                       ).place(x=0, y=500, width=600, height=40)








        # Creating Button Frame
        buttonframe = LabelFrame(self.root, bg="grey", fg="white", relief=GROOVE)
        buttonframe.place(x=0, y=550, width=600, height=50)
        self.voice_scale = Scale(buttonframe, orient=HORIZONTAL,sliderlength=10, variable=self.scale_var,command=self.updateValue,
activebackground="blue", bd=0, font=("times new roman", 16, "bold"), fg="navyblue", bg="pink").grid(row=0, column=0)


        prevbtn = Button(buttonframe, text="<-", command=self.playPrev, width=10, height=1,
                         font=("times new roman", 16, "bold"), fg="navyblue", bg="pink").grid(row=0, column=1, padx=10,
                                                                                              pady=5)

        # Inserting Play Button
        playbtn = Button(buttonframe, command=self.playsong,width=10, height=1,
                         font=("times new roman", 16, "bold"), fg="navyblue", bg="pink").grid(row=0, column=2, padx=10,pady=5)

        nextbtn = Button(buttonframe, text="->", command=self.playNext, width=10, height=1,
                         font=("times new roman", 16, "bold"), fg="navyblue", bg="pink").grid(row=0, column=3, padx=10,
                                                                                              pady=5)


        # Creating Playlist Frame
        songsframe = LabelFrame(self.root, text="Song Playlist", font=("times new roman", 15, "bold"), bg="grey",
                                fg="white", bd=5, relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=600)
        # Inserting scrollbar
        self.scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        # Inserting Playlist listbox
        self.mylist = Listbox(songsframe, yscrollcommand=self.scrol_y.set, selectmode=SINGLE, height=500,
                                font=("times new roman", 14, "bold"), bg="silver", fg="navyblue")

        selectButton = Button(root, text='',  underline=0, command=self.select)
        root.bind('<Double-1>', lambda x: selectButton.invoke())


        # Applying Scrollbar to listbox
        self.scrol_y.pack(side=RIGHT, fill=Y)
        self.scrol_y.config(command=self.mylist.yview)
        self.mylist.pack(fill=BOTH)
        self.playlist = []
        self.setPlaylist()







    # set slider to mp3 file position
    def ProgressBar(self, *value):
        for i in value:
            self.slider_value.set(int(i))
            pygame.mixer.music.set_pos(int(i))
        self.current = getdouble(value[-1])
        self.timeVar.set(f"{int(self.current//60)}:{int(self.current%60)}")


    def TrackPlay(self):
        if self.status.get() == "playing":
            self.current = pygame.mixer.music.get_pos()/1000  # .get_pos() returns integer in milliseconds
            #self.current += 1
            self.slider_value.set(self.current)  # .set_pos() works in seconds
            self.timeVar.set(f"{int(self.current//60)}:{int(self.current%60)}")
            self.root.after(1000, lambda: self.TrackPlay())


    def move(self, *args):
        for i in args:
            pygame.mixer.music.set_pos(getdouble(i))


    def updateValue(self, *arg):
        for i in arg:
            pygame.mixer.music.set_volume((int(i) /100))


    def setPlaylist(self):
        songtracks = find(path=self.filePath)
        for track in songtracks:
            self.playlist.append(track)
            self.mylist.insert(END, track)

    def playsong(self):
        if self.status.get() == 'not started' and len(self.playlist):
            # Displaying Selected Song title
            self.track.set(self.playlist[self.i])
            # Displaying Status
            self.status.set("playing")
            self.current = 0
            # Loading Selected Song
            pygame.mixer.music.load(self.playlist[self.i])
            # Playing Selected Song
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.60)
            self.TrackPlay()
        elif self.status.get() == "playing":
            # Displaying Status
            self.status.set("paused")
            # Paused Song
            pygame.mixer.music.pause()

        elif self.status.get() == "paused":
            # It will Display the  Status
            self.status.set("playing")
            # Playing back Song
            pygame.mixer.music.unpause()
            self.TrackPlay()



    def findPath(self):
        self.filePath = askdirectory()
        find(path=self.filePath)
        self.setPlaylist()

    def chooseSong(self):
        if len(self.playlist):
            self.status.set('not started')
            self.playsong()



    def playNext(self):
        if len(self.playlist):
            self.i = (self.i+1) % len(self.playlist)
            self.mylist.activate(self.i)
            self.chooseSong()


    def select(self):
        if len(self.playlist):
            name = self.mylist.get(ACTIVE)
            for i in range(len(self.playlist)):
                if self.playlist[i] == name:
                    self.i = i
            self.chooseSong()


    def playPrev(self):
        if len(self.playlist):
            if self.i == 0:
                self.i = len(self.playlist)-1
            else:
                self.i -= 1
            self.mylist.activate(self.i)
            self.chooseSong()



