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
        self.window.geometry("773x320")
        self.window.config(bg="gainsboro")
        self.canvas = Canvas(self.window)
        self.canvas.place(x=537,y=30)
        #self.Filelist = []
        self.zip_content = []
   
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.Hscrollbar = Scrollbar(self.canvas,orient=HORIZONTAL)
        self.Hscrollbar.pack(side=BOTTOM,fill=X)
        self.filesBox = sct.ScrolledText(self.window,width=63,height=12)#height=6
        self.filesBox.place(x=10,y=31)
        self.entryDirs = Listbox(self.canvas,width=34,height=14)#height=15
        self.entryDirs.pack()
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)
        self.entryDirs.config(xscrollcommand = self.Hscrollbar.set)
        self.scrollbar.config(command = self.entryDirs.yview)
        self.Hscrollbar.config(command = self.entryDirs.xview)
        self.btnSelect = Button(self.window,text="AGREGAR/QUITAR ARCHIVO",bg="orange",width=28,command=self.add_element)
        self.btnSelect.place(x=537,y=277)
        self.btnCreateZip = Button(self.window,text="CREAR ZIP",width=73,bg="light green",command=self.make_zip)
        self.btnCreateZip.place(x=10,y=245)
        self.btnChangeDir = Button(self.window,text="CAMBIAR DIRECTORIO",width=73,bg="blue",fg="white",command=self.change_dir)
        self.btnChangeDir.place(x=10,y=277)
        self.current_dir = StringVar()
        self.currentDir = Entry(self.window,width=128,textvariable=self.current_dir)
        self.currentDir.place(x=0,y=0)
        
        
        self.file_list()

        self.window.mainloop()

    def file_list(self):
        self.Filelist = []
        for i in os.listdir():
            try:
                self.Filelist.append(i)
                self.entryDirs.insert(END,i)
                print(i)
            except:
                pass
        self.current_dir.set(os.getcwd())

    def add_element(self):
        try:
            element = self.Filelist[self.entryDirs.curselection()[0]]
            if element not in self.zip_content:
                self.filesBox.insert(END,element+"\n")
                self.zip_content.append(element)
            else:
                self.zip_content.remove(element)
                self.filesBox.delete('1.0',END)
                for i in self.zip_content:
                    self.filesBox.insert(END,i+"\n")
        except Exception as e:
            the_error = str(e)
            if the_error == "tuple index out of range":
                messagebox.showwarning("ERROR","No se seleccionó ningun elemento")
            else:
                messagebox.showwarning("ERROR",str(e))

    def folder_name(self):
        count=0
        for f in os.listdir():
            if 'carpeta_comprimida' in f:
                count+=1
        if count>0:
            return 'carpeta_comprimida '+str(count)+'.zip'
        else:
            return 'carpeta_comprimida.zip'

    def change_dir(self):
        new_dir = filedialog.askdirectory()
        if new_dir != "":
            self.entryDirs.delete(0,END)
            os.chdir(new_dir)
            self.filesBox.delete('1.0',END)
            self.zip_content=[]
            self.file_list()
            self.current_dir.set(os.getcwd())

    def make_zip(self):
        try:
            name = self.folder_name()
            with zipfile.ZipFile(name,'w') as archivo_zip:
                for i in self.zip_content:
                    archivo_zip.write(i)
            archivo_zip.close()
            messagebox.showinfo('TAREA COMPLETADA','Archivo .zip creado correctamente')
            self.zip_content = []
            self.filesBox.delete('1.0',END)
        except Exception as e:
            messagebox.showwarning('ERROR',str(e))

if __name__=="__main__":
    zipper()


