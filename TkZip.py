#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import os

class zipper():
    def __init__(self):
        self.window = Tk()
        self.window.title("TkZip")
        self.window.geometry("764x316")
        self.canvas = Canvas(self.window)
        self.canvas.place(x=537,y=30)

        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.entryDirs = Listbox(self.canvas,width=33,height=15)
        self.entryDirs.pack()
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)

        

        self.window.mainloop()

if __name__=="__main__":
    zipper()
