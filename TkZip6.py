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
        self.zip_content = []
        self.special_chars = False
 
 
        self.scrollbar = Scrollbar(self.canvas,orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.Hscrollbar = Scrollbar(self.canvas,orient=HORIZONTAL)
        self.Hscrollbar.pack(side=BOTTOM,fill=X)
        self.filesBox = sct.ScrolledText(self.window,width=63,height=11)
        self.filesBox.place(x=10,y=31)
        self.folderNme = StringVar()
        self.folderNme.set(self.folder_name())
        self.entryName = Entry(self.window,width=38,textvariable=self.folderNme)
        self.entryName.place(x=187,y=216)
        self.labelName = Label(self.window,text="NOMB CARPETA COMPRIMIDA:",bg="gainsboro")
        self.labelName.place(x=10,y=216)
        self.btnClear = Button(self.window,text="BORRAR TODO",command=self.clear_all)
        self.btnClear.place(x=439,y=212)
        self.entryDirs = Listbox(self.canvas,width=34,height=14)
        self.entryDirs.pack()
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)
        self.entryDirs.config(xscrollcommand = self.Hscrollbar.set)
        self.scrollbar.config(command = self.entryDirs.yview)
        self.Hscrollbar.config(command = self.entryDirs.xview)
        self.btnSelect = Button(self.window,text="AÑADIR/QUITAR",bg="orange",width=31,command=self.add_element)
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
        counter = 0
        self.Filelist = []
        for i in os.listdir():
            try:
                self.entryDirs.insert(END,self.BMP(i))
                counter+=1
                self.Filelist.append(i)
            except:
                self.special_chars = True
                pass
        self.current_dir.set(os.getcwd())
 
        if self.special_chars == True:
            messagebox.showinfo("ARCHIVOS EXCLUIDOS",'''Se ha detectado uno o más archivos que
por contener caracteres especiales no son
suceptibles de ser comprimidos en un ZIP.
Cambie el nombre de dichos archivos para
su posible inclusión.''')
        print(counter)
        self.special_chars = False
 
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
                messagebox.showwarning("ERROR","No se seleccionó ningun elemento.")
            else:
                messagebox.showwarning("ERROR",str(e))
 
    def check_ext(self,text):
        if not text.endswith(".zip"):
            namef = text+".zip"
        else:
            namef = text
        return namef
 
    def clear_all(self):
        self.zip_content = []
        self.filesBox.delete('1.0',END)

    def BMP(self,s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))
 
    def folder_name(self):
        if self.folderNme.get() == "":
            count=0
            for f in os.listdir():
                if 'carpeta_comprimida' in f:
                    count+=1
            if count>0:
                return 'carpeta_comprimida '+str(count)+'.zip'
            else:
                return 'carpeta_comprimida.zip'
        else:
            return self.folderNme.get()
 
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
            self.folderNme.set(self.folder_name())
 
    def zip_info(self):
        name = self.check_ext(self.folderNme.get())
        with zipfile.ZipFile(name,'w') as archivo_zip:
            for i in self.zip_content:
                archivo_zip.write(i)
            archivo_zip.close()
            messagebox.showinfo('TAREA COMPLETADA','Archivo \'{}\' creado correctamente.'.format(name))
            self.folderNme.set(self.folder_name())
 
    def make_zip(self):
        try:
            if len(self.zip_content) > 0:
                self.zip_info()
            else:
                message = messagebox.askquestion("CARPETA ZIP VACÍA",'¿Crear carpeta zip vacía?')
                if message == "yes":
                    self.zip_info()
        except Exception as e:
            messagebox.showwarning('ERROR',str(e))
 
if __name__=="__main__":
    zipper()
