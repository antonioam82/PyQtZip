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
        self.special_chars = False

        self.scrollbar = tk.Scrollbar(self.canvas,orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.Hscrollbar = tk.Scrollbar(self.canvas,orient=tk.HORIZONTAL)
        self.Hscrollbar.pack(side=tk.BOTTOM,fill=tk.X)
        self.filesBox = sct.ScrolledText(self.window,width=63,height=11)
        self.filesBox.place(x=10,y=31)
        self.folderNme = tk.StringVar()
        self.folderNme.set(self.folder_name())###
        self.entryName = tk.Entry(self.window,width=38,textvariable=self.folderNme)
        self.entryName.place(x=100,y=216)
        self.labelName = tk.Label(self.window,text="ZIP FILE NAME:")
        self.labelName.place(x=10,y=216)
        self.btnClear = tk.Button(self.window,text="CLEAR ALL",bg="gray89",command=self.clear_all)
        self.btnClear.place(x=450,y=212)
        self.entryDirs = tk.Listbox(self.canvas,width=34,height=14)
        self.entryDirs.pack()
        self.entryDirs.configure(selectmode='multiple')
        self.entryDirs.config(yscrollcommand = self.scrollbar.set)
        self.entryDirs.config(xscrollcommand = self.Hscrollbar.set)
        self.scrollbar.config(command = self.entryDirs.yview)
        self.Hscrollbar.config(command = self.entryDirs.xview)
        self.btnSelect = tk.Button(self.window,text="ADD",width=7,bg="gray89",command=self.add_element)
        self.btnSelect.place(x=537,y=277)
        self.btnRemove = tk.Button(self.window,text="REMOVE",width=7,bg="gray89",command=self.remove_element)
        self.btnRemove.place(x=597,y=277)
        tk.Button(self.window,text="CLEAR SELECTION",width=14,bg="gray89",command=self.clear_selection).place(x=657,y=277)
        self.btnCreateZip = tk.Button(self.window,text="CREATE ZIP",width=73,bg="gray89",command=self.make_zip)
        self.btnCreateZip.place(x=10,y=245)
        self.btnChangeDir = tk.Button(self.window,text="CHANGE DIR",width=73,bg="gray89",command=self.change_dir)
        self.btnChangeDir.place(x=10,y=277)
        self.current_dir = tk.StringVar()
        self.currentDir = tk.Entry(self.window,width=128,textvariable=self.current_dir)
        self.currentDir.place(x=0,y=0)

        self.file_list()
 
        self.window.mainloop()

    def BMP(self,s):
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

    def add_element(self):
        for i in self.entryDirs.curselection():
            element = self.BMP(self.Filelist[i])
            print(element)
            if element not in self.zip_content:
                self.filesBox.insert(tk.END,element+"\n")
                self.zip_content.append(element)

    def remove_element(self):
        for i in self.entryDirs.curselection():
            element = self.BMP(self.Filelist[i])
            if element in self.zip_content:
                self.zip_content.remove(element)
                self.filesBox.delete('1.0',tk.END)
                for i in self.zip_content:
                    self.filesBox.insert(tk.END,i+"\n")

    def change_dir(self):
        new_dir = filedialog.askdirectory()
        if new_dir != "":
            self.entryDirs.delete(0,tk.END)
            os.chdir(new_dir)
            self.filesBox.delete('1.0',tk.END)
            self.zip_content=[]
            self.file_list()
            self.current_dir.set(os.getcwd())
            self.folderNme.set(self.folder_name())
            self.folder_name()

    def check_ext(self,text):
        if not text.endswith(".zip"):
            namef = text+".zip"
        else:
            namef = text
        return namef

    def folder_name(self):
        count=0
        for f in os.listdir():
            if 'carpeta_comprimida' in f:
                count+=1
        if count>0:
            return 'carpeta_comprimida '+str(count)+'.zip'
        else:
            return 'carpeta_comprimida.zip'


    def zip_info(self):
        name = self.check_ext(self.folderNme.get())
        with zipfile.ZipFile(name,'w') as archivo_zip:
            for i in self.zip_content:
                archivo_zip.write(i)
            #archivo_zip.close()
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

    def clear_selection(self):
        for i in self.entryDirs.curselection():
            self.entryDirs.selection_clear(i)
        #self.zip_content = []

    def clear_all(self):
        self.zip_content = []
        self.filesBox.delete('1.0',tk.END)

    def file_list(self):
        counter = 0
        self.Filelist = []
        for i in os.listdir():
            try:
                if os.path.isfile(i):
                    self.entryDirs.insert(tk.END,self.BMP(i))
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

if __name__=="__main__":
    zipper()


