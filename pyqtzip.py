import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import QModelIndex
import zipfile

class FileSystemView(QWidget):
    def __init__(self, dir_path):
        super().__init__()

        # TITULO Y DIMENSIONES DE LA VENTANA.
        self.setWindowTitle('File System Viewer')
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

        # MOSTRAR VENTANA CON LA VISTA, LA RUTA ACTUAL Y LOS BOTONES.
        layout = QVBoxLayout()
        layout.addWidget(self.currentDirLabel)
        layout.addWidget(self.tree)
        layout.addWidget(self.changeDirButton)
        layout.addWidget(self.createZipButton)

        self.setLayout(layout)

    def changeDirectory(self):
        dirPath = QFileDialog.getExistingDirectory(self, "Seleccionar directorio", os.getcwd())
        if dirPath:
            self.tree.setRootIndex(self.model.index(dirPath))
            self.currentDirLabel.setText(f"Directorio actual: {dirPath}")

    def createZip(self):
        selected_index = self.tree.currentIndex()
        selected_path = self.model.filePath(selected_index)
        selected_folder_name = os.path.basename(selected_path)

        zip_filename = selected_folder_name + ".zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, dirs, files in os.walk(selected_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, selected_path))

        print("Archivo ZIP creado:", zip_filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # DIRECTORIO BASE.
    dirPath = os.getcwd()

    demo = FileSystemView(dirPath)
    demo.show()
    sys.exit(app.exec_())
