#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as sct
import os

class zipper():
    def __init__(self):
        self.window = Tk()
        self.window.title("TkZip")
        self.window.geometry("764x320")
        self.canvas = Canvas(self.window)
        self.canvas.place(x=537,y=30)
        self.Filelist = []
        self.zip_content = []
   
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.filesBox = sct.ScrolledText(self.window,width=63,height=6)
        self.filesBox.place(x=10,y=31)
        self.entryDirs = Listbox(self.canvas,width=33,height=15)
        self.entryDirs.pack()
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.entryDirs.yview)
        self.btnSelect = Button(self.window,text="AGREGAR ARCHIVO",bg="orange",width=27,command=self.add_element)
        self.btnSelect.place(x=537,y=277)
        self.btnCreateZip = Button(self.window,text="CREAR ZIP",width=15,bg="light green",command=self.make_zip)
        self.btnCreateZip.place(x=217,y=170)
        
        self.file_list()

        self.window.mainloop()

    def file_list(self):
        for i in os.listdir():
            self.Filelist.append(i)
            self.entryDirs.insert(END,i)

    def add_element(self):
        element = self.Filelist[self.entryDirs.curselection()[0]]
        self.filesBox.insert(END,element+"\n")
        self.zip_content.append(element)

    def make_zip(self):
        try:
            with zipfile.ZipFile('carpeta_comprimida.zip','w') as archivo_zip:
                for i in self.zip_content:
                    archivo_zip.write(i)
            archivo_zip.close()
            messagebox.showinfo('TAREA COMPLETADA','Archivo .zip creado correctamente')
            self.zip_content = []
        except Exception as e:
            messagebox.showwarning('ERROR',str(e))

if __name__=="__main__":
    zipper()



