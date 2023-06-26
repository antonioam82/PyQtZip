#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QProgressDialog
from PyQt5.QtCore import QModelIndex
import zipfile

class FileSystemView(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        # TITULO Y DIMENSIONES DE LA VENTANA.
        self.setWindowTitle('ZIP File Creator')
        self.setGeometry(300, 300, 800, 300)

        # DEFINIR DIRECTORIO.
        self.model = QFileSystemModel()
        self.model.setRootPath(dir_path)

        # RUTA DEL DIRECTORIO ACTUAL
        self.currentDirLabel = QLabel()
        self.currentDirLabel.setText(f"Directorio actual: {dir_path}")

        # GENERAR VISTA DE ARCHIVOS Y CARPETAS.
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(dir_path))
        self.tree.setColumnWidth(200, 250)
        self.tree.setAlternatingRowColors(True)

        # BOTÓN PARA CAMBIAR EL DIRECTORIO.
        self.changeDirButton = QPushButton("Cambiar Directorio")
        self.changeDirButton.clicked.connect(self.changeDirectory)

        # BOTÓN PARA CREAR ARCHIVO ZIP
        self.createZipButton = QPushButton("Crear ZIP")
        self.createZipButton.clicked.connect(self.createZip)

        # BOTÓN PARA EXTRAER ARCHIVO ZIP
        self.extractZipButton = QPushButton("Extraer ZIP")
        self.extractZipButton.clicked.connect(self.extractZip)

        # LAYOUT DE BOTONES
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.createZipButton)
        buttonsLayout.addWidget(self.extractZipButton)

        # LAYOUT PRINCIPAL
        layout = QVBoxLayout()
        layout.addWidget(self.currentDirLabel)
        layout.addWidget(self.tree)
        layout.addWidget(self.changeDirButton)
        layout.addLayout(buttonsLayout)

        self.setLayout(layout)

    # FUNCIÓN PARA CAMBIAR DIRECTORIO
    def changeDirectory(self):
        dirPath = QFileDialog.getExistingDirectory(self, "Seleccionar directorio", os.getcwd())
        if dirPath:
            self.tree.setRootIndex(self.model.index(dirPath))
            self.currentDirLabel.setText(f"Directorio actual: {dirPath}")

    # FUNCIÓN PARA CREACIÓN DE ARCHIVO "ZIP".
    def createZip(self):
        try:
            selected_index = self.tree.currentIndex()
            selected_path = self.model.filePath(selected_index)
            selected_folder_name = os.path.basename(selected_path)

            if selected_folder_name != ".txt" and os.path.isdir(selected_path):
                saveDirPath = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino", os.getcwd())
                if saveDirPath:
                    zip_filename = os.path.join(saveDirPath, selected_folder_name + ".zip")

                    # BARRA DE PROGRESO EMERGENTE
                    self.init_progress_bar("Creando archivo zip...")

                    with zipfile.ZipFile(zip_filename, "w") as zipf:
                        for i, (root, dirs, files) in enumerate(os.walk(selected_path)):
                            for j, file in enumerate(files):
                                file_path = os.path.join(root, file)
                                zipf.write(file_path, os.path.relpath(file_path, selected_path))

                                progress = (i * len(files) + j + 1) / (len(dirs) * len(files) + len(files)) * 100
                                progressDialog.setValue(progress)
                                if progressDialog.wasCanceled():
                                    progressDialog.close()
                                    return

                    progressDialog.close()
                    QMessageBox.information(self, "Archivo ZIP creado", f"Archivo ZIP '{selected_folder_name}.zip' creado correctamente.")
            else:
                QMessageBox.information(self, "Carpeta no seleccionada", "Seleccione una carpeta para comprimir.")
        except Exception as e:
            QMessageBox.information(self, "ERROR INESPERADO", str(e))

    def init_progress_bar(self, texto):
        global progressDialog
        progressDialog = QProgressDialog(texto, "Cancelar", 0, 100, self)
        progressDialog.setWindowTitle("Proceso")
        progressDialog.setAutoClose(True)
        progressDialog.setWindowModality(2)
        progressDialog.show()

    # FUNCIÓN PARA EXTRAER ARCHIVO ZIP.
    def extractZip(self):
        try:
            selected_index = self.tree.currentIndex()
            selected_path = self.model.filePath(selected_index)
            container_folder = os.path.splitext(os.path.basename(selected_path))[0]

            if selected_path.endswith(".zip"):
                saveDirPath = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino", os.getcwd())
                if saveDirPath:
                    new_dir = os.path.join(saveDirPath,container_folder)
                    os.mkdir(new_dir)

                    # BARRA DE PROGRESO EMERGENTE
                    self.init_progress_bar("Extrayendo archivo zip...")

                    with zipfile.ZipFile(selected_path, "r") as zip_ref:
                        file_count = len(zip_ref.infolist())
                        for index, file in enumerate(zip_ref.infolist()):
                            zip_ref.extract(file, new_dir)
                            progress = (index + 1) / file_count * 100
                            progressDialog.setValue(progress)
                            if progressDialog.wasCanceled():
                                progressDialog.close()
                                return

                    progressDialog.close()
                    QMessageBox.information(self, "Archivo ZIP extraído", "Archivo ZIP extraído correctamente.")
            else:
                QMessageBox.information(self, "Archivo no seleccionado", "Seleccione un archivo ZIP para extraer.")
        except Exception as e:
            QMessageBox.information(self, "ERROR INESPERADO", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # DIRECTORIO BASE.
    dirPath = os.getcwd()

    demo = FileSystemView(dirPath)
    demo.show()
    sys.exit(app.exec_())
