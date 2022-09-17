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

if __name__=="__main__":
    zipper()
