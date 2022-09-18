#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import os

#more code here
class zipper():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TkZip8")
        self.window.geometry("773x320")
        self.canvas = tk.Canvas(self.window)
        self.canvas.place(x=537,y=30)
        self.zip_content = []

        self.scrollbar = tk.Scrollbar(self.canvas,orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.Hscrollbar = tk.Scrollbar(self.canvas,orient=tk.HORIZONTAL)
        self.Hscrollbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.filesBox = sct.ScrolledText(self.window,width=63,height=11)
        self.filesBox.place(x=10,y=31)
        self.folderNme = tk.StringVar()
        self.folderNme.set(" ")###
        self.entryName = tk.Entry(self.window,width=38,textvariable=self.folderNme)
        self.entryName.place(x=100,y=216)
        self.labelName = tk.Label(self.window,text="ZIP FILE NAME:")
        self.labelName.place(x=10,y=216)
        self.btnClear = tk.Button(self.window,text="CLEAR ALL",bg="gray90")
        self.btnClear.place(x=450,y=212)
        self.entryDirs = tk.Listbox(self.canvas,width=34,height=14)
        self.entryDirs.pack()
        self.entryDirs.configure(selectmode='multiple')
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)
        self.entryDirs.config(xscrollcommand = self.Hscrollbar.set)
        self.scrollbar.config(command = self.entryDirs.yview)
        self.Hscrollbar.config(command = self.entryDirs.xview)
        self.btnSelect = tk.Button(self.window,text="ADD/REMOVE",width=15,bg="gray90")
        self.btnSelect.place(x=537,y=277)
        tk.Button(self.window,text="CLEAR SELECTION",width=14,bg="gray90").place(x=654,y=277)
        self.btnCreateZip = tk.Button(self.window,text="CREATE ZIP",width=73,bg="gray90")
        self.btnCreateZip.place(x=10,y=245)
        self.btnChangeDir = tk.Button(self.window,text="CHANGE DIR",width=73,bg="gray90")
        self.btnChangeDir.place(x=10,y=277)
        self.current_dir = tk.StringVar()
        self.currentDir = tk.Entry(self.window,width=128,textvariable=self.current_dir)
        self.currentDir.place(x=0,y=0)        

if __name__=="__main__":
    zipper()

